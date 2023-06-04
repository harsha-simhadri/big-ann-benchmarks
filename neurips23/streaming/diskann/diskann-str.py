from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import diskannpy

from neurips23.streaming.base import BaseStreamingANN

class diskann(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.name = "diskann"
        if (index_params.get("R")==None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L")==None):
            print("Error: missing parameter L")
            return
        self._index_params = index_params
        self._metric = metric

        self.R = index_params.get("R")
        self.L = index_params.get("L")
        self.Ls = index_params.get("Ls")
        self.insert_threads = index_params.get("insert_threads")
        self.consolidate_threads = index_params.get("consolidate_threads")
        self.search_threads = index_params.get("search_threads")

    def index_name(self):
        return f"R{self.R}_L{self.L}"
        
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.__str__())
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
            return 'mips'
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
        self.index = diskannpy.DynamicMemoryIndex(
            distance_metric = self.translate_dist_fn(self._metric),
            vector_dtype = self.translate_dtype(dtype),
            index_prefix = self.index_name(),
            graph_degree = self.R,
            complexity=self.L,
            num_threads = self.insert_threads, #to allocate scratch space for up to 64 search threads
            initial_search_complexity = self.Ls
        )
        print('Index class constructed and ready for update/search')
    
    def insert(self, X, ids):
        self.index.batch_insert(X, ids)

    def delete(self, ids):
        self.index.batch_delete(ids)

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        self.res, self.query_dists = self.index.batch_search(
            X, k, self.Ls, self.search_threads)

    def set_query_arguments(self, query_args):
        raise NotImplementedError
