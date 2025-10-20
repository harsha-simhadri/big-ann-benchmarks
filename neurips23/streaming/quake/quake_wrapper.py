from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import logging
import torch
import torch.nn as nn
import math

from quake import MaintenancePolicyParams
from quake.index_wrappers.quake import QuakeWrapper

from neurips23.streaming.base import BaseStreamingANN

# Use to save tensor in a way that can be read by C++ code
class TensorWrapper(nn.Module):
    def __init__(self, tensor):
        super(TensorWrapper, self).__init__()
        self.register_buffer('tensor', tensor)

    def forward(self, x):
        return x

# The implementation of this class is based on the diskann implementation
class quake(BaseStreamingANN):

    def __init__(self, metric, index_params):
        # Validate the metric type
        if metric == "euclidean":
            self.metric_ = "l2"
        else:
            raise Exception(f"Invalid metric type of {metric}")

        self.name = "quake"
        self.index_params_ = index_params

        # Verify and extract the index params
        self.extract_build_args()

        self.intial_insert_args_ = [] # Store all of the inserts before the first build
        self.initial_delete_args_ = [] # Store all of the deletes before the first build
        self.index_ = None

        # Parameters related to saving the arguments
        self.save_args_ = False
        if self.save_args_:
            self.save_dir_ = "/home/app/data/MSTuring-30M-clustered/index_arguments"
            os.makedirs(self.save_dir_, exist_ok=True)
            self.step_num_ = 1
    
    def extract_build_args(self):
        # Get the index related arguments
        self.nc_ = self.index_params_.get("nc", 1024)
        self.insert_chunk_size_ = self.index_params_.get("insert_chunk_size", 500)
        self.delete_chunk_size_ = self.index_params_.get("delete_chunk_size", 500)
        self.query_chunk_size_ = self.index_params_.get("query_chunk_size", 500)

        # Create the mainteance params
        self.run_mainteance_ = str(self.index_params_.get("run_mainteance", "True")).lower() == "true"
        self.m_params = MaintenancePolicyParams()

        if "delete_threshold" in self.index_params_:
            self.m_params.delete_threshold_ns = self.index_params_["delete_threshold"]
        if "split_threshold" in self.index_params_:
            self.m_params.split_threshold_ns = self.index_params_["split_threshold"]
        if "refinement_radius" in self.index_params_:
            self.m_params.refinement_radius = self.index_params_["refinement_radius"]
        if "refinement_iterations" in self.index_params_:
            self.m_params.refinement_iterations = self.index_params_["refinement_iterations"]
        if "enable_split_rejection" in self.index_params_:
            self.m_params.enable_split_rejection = str(self.index_params_["enable_split_rejection"]).lower() == "true"
        if "enable_delete_rejection" in self.index_params_:
            self.m_params.enable_delete_rejection = str(self.index_params_["enable_delete_rejection"]).lower() == "true"
        if "window_size" in self.index_params_:
            self.m_params.window_size = self.index_params_["window_size"]
        if "min_partition_size" in self.index_params_:
            self.m_params.min_partition_size = self.index_params_["min_partition_size"]
        if "max_partition_size" in self.index_params_:
            self.m_params.max_partition_size = self.index_params_["max_partition_size"]
    
    def set_query_arguments(self, query_args):
        self.query_args_ = query_args

        # Extract the query args
        self.num_workers_ = self.query_args_.get("num_search_workers", 16)
        self.nprobe_ = self.query_args_.get("nprobe", 16)
        self.recall_target_ = self.query_args_.get("recall_target", 0.9)
        self.use_batch_scan_ = str(self.query_args_.get("use_batch_scan", "False")).lower() == "true"
        self.initial_search_fraction_ = self.query_args_.get("initial_search_threshold", 0.05)
        self.recompute_threshold_ = self.query_args_.get("recompute_threshold", 0.1)
        self.aps_flush_period_us_ = self.query_args_.get("flush_period_us", 50)
        self.num_job_distribute_workers_ = self.query_args_.get("num_job_distribute_workers", 1)
        self.num_merge_workers_ = self.query_args_.get("num_merge_workers", 1)
        self.use_numa_ = str(self.query_args_.get("use_numa", "True")).lower() == "true"
    
    def setup(self, dtype, max_pts, ndim):
        # Verify that the data type is float32 because that is all that quake supports
        if dtype != 'float32':
            raise Exception(f"Quake doesn't support data type of {dtype}")

        self.max_pts_ = max_pts
        self.code_size_ = ndim
    
    def perform_mainteance(self):
        if self.run_mainteance_ and self.index_ is not None:
            mainteance_result = self.index_.maintenance()
            print(f"Mainteance Result: Num Splits - {mainteance_result.n_splits}, Num Deletes - {mainteance_result.n_deletes}, Time us - {mainteance_result.total_time_us}")
    
    def save_buffer_to_disk(self, save_suffix, save_buffer):
        # Determine the save path
        save_name = f"step_{self.step_num_}_{save_suffix}.pth"
        save_path = os.path.join(self.save_dir_, save_name)

        # Serialize and save the tensors
        wrapper_module = TensorWrapper(save_buffer)
        scripted_module = torch.jit.script(wrapper_module)
        torch.jit.save(scripted_module, save_path)
        
    def insert(self, X, ids):
        # If save is enabled then save the arguments
        if self.save_args_:
            save_suffix = "insert"
            self.save_buffer_to_disk(save_suffix + "_vectors", torch.from_numpy(X).to(torch.float32))
            self.save_buffer_to_disk(save_suffix + "_ids", torch.from_numpy(ids).to(torch.int64))
            self.step_num_ += 1
            
        # Record these as the tensors to initialize the vector with
        if self.index_ is None:
            self.intial_insert_args_.append((X, ids))
            return
            
        # Convert the input into tensors
        num_vectors = ids.shape[0]
        insert_vectors = torch.from_numpy(X).to(torch.float32)
        insert_ids = torch.from_numpy(ids).to(torch.int64)
        
        # Insert in the vectors to the index in chunks
        num_chunks = int(math.ceil(num_vectors/self.insert_chunk_size_))
        for chunk_idx in range(num_chunks):
            # Determine the vector and ids in this chunk
            start_idx = int(chunk_idx * self.insert_chunk_size_)
            if start_idx >= num_vectors:
                break
            end_idx = min(int((chunk_idx + 1) * self.insert_chunk_size_), num_vectors)

            chunk_vectors = insert_vectors[start_idx : end_idx, : ]
            chunk_ids = insert_ids[start_idx : end_idx]

            # Add in the chunk into the index
            self.index_.add(chunk_vectors, chunk_ids)
        
        self.perform_mainteance()
    
    def delete(self, ids):
        # If save is enabled then save the arguments
        if self.save_args_:
            self.save_buffer_to_disk("delete_ids", torch.from_numpy(ids).to(torch.int64))
            self.step_num_ += 1

        # Store the queries to run when the index is build
        if self.index_ is None:
            self.initial_delete_args_.append(ids)
            return 

        # Convert the input into a tensor
        num_ids = ids.shape[0]
        delete_ids = torch.from_numpy(ids).to(torch.int64)

        # Remove the ids from the index in chunks
        num_chunks = int(math.ceil(num_ids/self.delete_chunk_size_))
        for chunk_idx in range(num_chunks):
            # Determine the ids in this chunk
            start_idx = int(chunk_idx * self.delete_chunk_size_)
            if start_idx >= num_ids:
                break
            end_idx = min(int((chunk_idx + 1) * self.delete_chunk_size_), num_ids)

            chunk_ids = delete_ids[start_idx : end_idx]
            
            # Remove the ids from the index
            self.index_.remove(chunk_ids)
        
        self.perform_mainteance()
    
    def query(self, X, k):
        if self.save_args_:
            self.save_buffer_to_disk("search_vectors", torch.from_numpy(X).to(torch.float32))
            self.step_num_ += 1

        if self.index_ is None:
            if len(self.intial_insert_args_) == 0:
                raise Exception("Query called before any inserts")

            # Get the build vectors and ids
            combined_vectors_arr = np.concatenate([vectors for vectors, ids in self.intial_insert_args_])
            build_vectors = torch.from_numpy(combined_vectors_arr).to(torch.float32)
            combined_ids_arr = np.concatenate([ids for vectors, ids in self.intial_insert_args_])
            build_ids = torch.from_numpy(combined_vectors_arr).to(torch.int64)

            # Now build the index
            print("Building initial quake index with", build_ids.shape[0], "vectors")
            self.index_ = QuakeWrapper()
            self.index_.build(
                build_vectors,
                self.nc_,
                metric=self.metric_,
                ids=build_ids,
                num_workers=self.num_workers_,
                code_size=self.code_size_,
                num_merge_workers=self.num_merge_workers_,
                use_numa=self.use_numa_
            )

            # TODO: Currently we are naively calling delete after building the index but later combine the inserts
            # and deletes before calling build
            if len(self.initial_delete_args_) > 0:
                delete_ids_arr = np.concatenate([ids for ids in self.initial_delete_args_])
                delete_ids = torch.from_numpy(delete_ids_arr)
                delete_tensor = self.index_.remove(delete_ids)

            # Also configure the mainteance parameters
            self.index_.index.initialize_maintenance_policy(self.m_params)
            
        # Convert the input into the right format
        num_queries = X.shape[0]
        queries = torch.from_numpy(X).to(torch.float32)

        # Run the queries against the index in chunks
        num_chunks = int(math.ceil(num_queries/self.query_chunk_size_))
        chunk_resuls = []
        for chunk_idx in range(num_chunks):
            # Determine the vector in this chunk
            start_idx = int(chunk_idx * self.query_chunk_size_)
            if start_idx >= num_queries:
                break
            end_idx = min(int((chunk_idx + 1) * self.query_chunk_size_), num_queries)

            chunk_vectors = queries[start_idx : end_idx, : ]

            # Run the query against the index and save the result
            search_result = self.index_.search(
                chunk_vectors,
                k=k,
                nprobe=self.nprobe_,
                batched_scan=self.use_batch_scan_,
                recall_target=self.recall_target_,
                initial_search_fraction=self.initial_search_fraction_,
                recompute_threshold=self.recompute_threshold_,
                aps_flush_period_us=self.aps_flush_period_us_,
                n_threads=self.num_job_distribute_workers_
            )
            chunk_resuls.append(search_result.ids)

        # Combine the chunk results
        combined_result = torch.cat(chunk_resuls, 0)
        self.res = combined_result.numpy().astype(np.uint32)
        self.perform_mainteance()
    
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "streaming")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.name)
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir
    
    def __str__(self):
        return f'{self.name}({self.index_params_}, {self.query_args_})'