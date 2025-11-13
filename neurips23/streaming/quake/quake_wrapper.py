from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import logging
import torch
import torch.nn as nn
import math

from quake import MaintenancePolicyParams, IndexBuildParams, SearchParams, IndexPartition, QuakeIndex
from neurips23.streaming.base import BaseStreamingANN

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
    
    def extract_build_args(self):
        # Get the operation related parameters
        batch_size = self.index_params_.get("batch_size", 10000)
        self.insert_chunk_size_ = batch_size
        self.delete_chunk_size_ = batch_size

        # Configure the index parameters
        IndexPartition.delete_resize_threshold = self.index_params_.get("delete_threshold", 0.7)
        IndexPartition.capacity_resize_threshold = self.index_params_.get("capacity_threshold", 1.15)

        # Create the build related parameters
        build_args = self.index_params_.get("build_args", {})
        base_level_params = IndexBuildParams()
        base_level_params.metric = self.metric_
        base_level_params.nlist = build_args.get("nlist", 1024)
        base_level_params.num_workers = build_args.get("search_workers", 8)
        base_level_params.niter = build_args.get("niter", 25)

        upper_level_params = IndexBuildParams()
        upper_level_params.nlist = 1
        upper_level_params.metric = self.metric_
        upper_level_params.num_workers = 0
        base_level_params.parent_params = upper_level_params
        self.build_params_ = base_level_params

        # Create the mainteance params
        mainteance_args = self.index_params_.get("mainteance_args", {})
        self.run_mainteance_ = mainteance_args.get("run_mainteance", True)

        mainteance_params = MaintenancePolicyParams()
        mainteance_params.window_size = mainteance_args.get("window_size", 5000)
        mainteance_params.split_threshold_ns = mainteance_args.get("split_threshold", 2100)
        mainteance_params.split_knn_iterations = mainteance_args.get("split_iterations", 10)
        mainteance_params.delete_threshold_ns = mainteance_args.get("delete_threshold", 2750)
        mainteance_params.partition_reduction_threshold = mainteance_args.get("reduction_threshold", 0.45)
        mainteance_params.refinement_radius = mainteance_args.get("refinment_radius", 0)
        mainteance_params.refinement_iterations = mainteance_args.get("refinement_iterations", 5)
        mainteance_params.min_partition_size = mainteance_args.get("min_partition_size", 1024)
        mainteance_params.enable_split_rejection = mainteance_args.get("enable_split_rejection", True)
        mainteance_params.enable_delete_rejection = mainteance_args.get("enable_delete_rejection", True)
        self.mainteance_params_ = mainteance_params
    
    def set_query_arguments(self, query_args):
        self.query_args_ = query_args

        # Extract the index build and search parameters at each level
        search_args = query_args.get("search_args", {})
        self.search_fraction_ = search_args.get("search_fraction", 0.1)

        search_params = SearchParams()
        search_params.recall_target = search_args.get("recall_target", -1.0)
        search_params.batched_scan = search_args.get("batched_scan", True)
        search_params.batch_size = search_args.get("batch_size", 500)
        search_params.track_hits = search_args.get("track_hits", True)
        self.search_params_ = search_params
    
    def setup(self, dtype, max_pts, ndim):
        # Verify that the data type is float32 because that is all that quake supports
        if dtype != 'float32':
            raise Exception(f"Quake doesn't support data type of {dtype}")

        self.max_pts_ = max_pts
        self.code_size_ = ndim
    
    def perform_mainteance(self):
        if self.run_mainteance_ and self.index_ is not None:
            mainteance_result = self.index_.maintenance()
        
    def insert(self, X, ids):            
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
        start_time = time.time()
        for chunk_idx in range(num_chunks):
            # Determine the vector and ids in this chunk
            start_idx = int(chunk_idx * self.insert_chunk_size_)
            if start_idx >= num_vectors:
                break
            end_idx = min(int((chunk_idx + 1) * self.insert_chunk_size_), num_vectors)

            # Add in the chunk into the index
            chunk_vectors = insert_vectors[start_idx : end_idx, : ]
            chunk_ids = insert_ids[start_idx : end_idx]
            self.index_.add(chunk_vectors, chunk_ids)

        end_time = time.time()
        
        self.perform_mainteance()
    
    def delete(self, ids):
        # Store the queries to run when the index is build
        if self.index_ is None:
            self.initial_delete_args_.append(ids)
            return 

        # Convert the input into a tensor
        num_ids = ids.shape[0]
        delete_ids = torch.from_numpy(ids).to(torch.int64)

        # Remove the ids from the index in chunks
        num_chunks = int(math.ceil(num_ids/self.delete_chunk_size_))
        start_time = time.time()
        for chunk_idx in range(num_chunks):
            # Determine the ids in this chunk
            start_idx = int(chunk_idx * self.delete_chunk_size_)
            if start_idx >= num_ids:
                break
            end_idx = min(int((chunk_idx + 1) * self.delete_chunk_size_), num_ids)

            # Remove the ids from the index
            chunk_ids = delete_ids[start_idx : end_idx]
            self.index_.remove(chunk_ids)

        end_time = time.time()
        self.perform_mainteance()
    
    def query(self, X, k):
        self.search_params_.k = k # Update k based on input argument

        if self.index_ is None: # Create the index if it doesn't exist
            if len(self.intial_insert_args_) == 0:
                raise Exception("Query called before any inserts")

            # Get the build vectors and ids
            combined_vectors_arr = np.concatenate([vectors for vectors, ids in self.intial_insert_args_])
            build_vectors = torch.from_numpy(combined_vectors_arr).to(torch.float32)
            combined_ids_arr = np.concatenate([ids for vectors, ids in self.intial_insert_args_])
            build_ids = torch.from_numpy(combined_ids_arr).to(torch.int64)
            self.intial_insert_args_.clear()

            # Now build the index
            self.index_ = QuakeIndex()
            self.index_.build(build_vectors, build_ids, self.build_params_)

            # TODO: Currently we are naively calling delete after building the index but later combine the inserts
            # and deletes before calling build
            if len(self.initial_delete_args_) > 0:
                delete_ids_arr = np.concatenate([ids for ids in self.initial_delete_args_])
                delete_ids = torch.from_numpy(delete_ids_arr)
                delete_tensor = self.index_.remove(delete_ids)
                self.initial_delete_args_.clear()

            # Also configure the mainteance parameters
            self.index_.initialize_maintenance_policy(self.mainteance_params_)
        
        # Configure the nprobe based on the index details
        self.search_params_.nprobe = int(self.search_fraction_ * self.index_.nlist())

        # Run the queries against the index
        num_queries = X.shape[0]
        queries = torch.from_numpy(X).to(torch.float32)
        search_result = self.index_.search(queries, self.search_params_)
        self.res = search_result.ids.numpy().astype(np.uint32)
        end_time = time.time()

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