from __future__ import absolute_import
import psutil
import os
import time
import numpy as np

import hnswlib

from neurips23.streaming.base import BaseStreamingANN

class hnsw(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.name = "hnsw"
        if (index_params.get("M")==None):
            print("Error: missing parameter M")
            return
        if (index_params.get("ef_construction")==None):
            print("Error: missing parameter ef_construction")
            return
        self._index_params = index_params
        self._metric = self.translate_dist_fn(metric)
        self.consolidate_threshold = index_params.get("consolidate_threshold", .2)
        if (self.consolidate_threshold < 0) or (self.consolidate_threshold > 1):
            print("Invalid consolidation threshold specified, defaulting to 20%")
            self.consolidate_threshold = .2
        self.M = index_params.get("M")
        self.ef_construction = index_params.get("ef_construction")
        self.threads = index_params.get("threads")
        self.stats = {"search_time": 0.0, "search_times":[], "insert_time":0.0, "delete_time":0.0}

    def index_name(self): 
        return f"M{self.M}_ef_construction{self.ef_construction}"
        
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "streaming")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'hnsw')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir

    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return 'l2'
        elif metric == 'ip':
            return 'ip'
        elif metric == 'cosine':
            return 'cosine'
        else:
            raise Exception('Invalid metric')
        
    def translate_dtype(self, dtype:str):
        if dtype == 'uint8':
            return np.uint8
        elif dtype == 'int8':
            return np.int8
        elif dtype == 'float32':
            return np.float32
        else:
            raise Exception('Invalid data type')

    def setup(self, dtype, max_pts, ndim):
        self.index = hnswlib.Index(self._metric, ndim)
        self.max_points = int(max_pts*(1+self.consolidate_threshold))
        self.index.init_index(max_elements=self.max_points, ef_construction=self.ef_construction, M=self.M, allow_replace_deleted=True)
        self.index.set_num_threads(self.threads)
        print('Index constructed with max_points', self.max_points, 'ef_construction', self.ef_construction, 'M', self.M,'threads', self.threads)
        self.active_indices = set()
        self.num_unprocessed_deletes = 0
    
    def insert(self, X, ids):
        self.active_indices.update(ids)
        do_replace = self.check_for_replace()
        start = time.perf_counter()
        self.index.add_items(X, ids, replace_deleted = do_replace)
        end = time.perf_counter()
        self.stats["insert_time"] += end-start
        if do_replace:
            print("Inserted with replacement")
            self.num_unprocessed_deletes = max(0, self.num_unprocessed_deletes-len(ids))

    # return true if either max_pts would be exceeded or
    # the fraction of deleted points in the index is too high
    def check_for_replace(self):
        print('#active pts', len(self.active_indices), '#unprocessed deletes', self.num_unprocessed_deletes)
        delete_condition1 = (len(self.active_indices) + self.num_unprocessed_deletes >= self.max_points)
        if self.consolidate_threshold == 0:
            delete_condition2 = False
        else:
            delete_condition2 = (self.num_unprocessed_deletes > len(self.active_indices)*self.consolidate_threshold) 
        return (delete_condition1 or delete_condition2)

    def delete(self, ids):
        for id in ids:
            self.index.mark_deleted(id)
        self.active_indices.difference_update(ids)
        self.num_unprocessed_deletes += len(ids)

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        start = time.perf_counter()
        self.res, self.query_dists = self.index.knn_query(X, k=k)
        end = time.perf_counter()
        self.stats["search_time"] += end-start
        self.stats["search_times"].append(end-start)

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.ef_search = 0 if query_args.get("ef_search") == None else query_args.get("ef_search")                             
        self.index.set_ef(self.ef_search)

    def __str__(self):
        return f'hnsw({self.index_name(), self._query_args})'

    def get_additional(self):
        return self.stats
