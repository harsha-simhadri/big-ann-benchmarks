from __future__ import absolute_import
import psutil
import os
import time
import numpy as np

from PyCANDYAlgo import diskannpy

from neurips23.streaming.base import BaseStreamingANN


class Pyanns(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.name = "pyanns"
        if (index_params.get("R") == None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L") == None):
            print("Error: missing parameter L")
            return
        self._index_params = index_params
        self._metric = metric

        self.R = index_params.get("R")
        self.L = index_params.get("L")
        self.insert_threads = index_params.get("insert_threads")
        self.consolidate_threads = index_params.get("consolidate_threads")
        self.mx = None
        self.mi = None

    def index_name(self):
        return f"R{self.R}_L{self.L}"

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "streaming")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'pyanns')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir

    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return diskannpy.Metric.L2
        elif metric == 'ip':
            return diskannpy.Metric.L2
        elif metric == 'angular':
            return diskannpy.Metric.COSINE
        else:
            raise Exception('Invalid metric')

    def translate_dtype(self, dtype: str):
        return np.uint8

    def setup(self, dtype, max_pts, ndim):
        if dtype == 'uint8':
            index_class = diskannpy.DynamicMemoryUInt8Index
        elif dtype == 'int8':
            index_class = diskannpy.DynamicMemoryInt8Index
        elif dtype == 'float32':
            index_class = diskannpy.DynamicMemoryFloatIndex
        else:
            raise Exception('Invalid dtype for index creation')
        self.index = index_class(
            algo_type=diskannpy.AlgoType.PYANNS,
            distance_metric=self.translate_dist_fn(self._metric),
            # vector_dtype = self.translate_dtype(dtype),
            max_vectors=max_pts,
            dimensions=ndim,
            graph_degree=self.R,
            complexity=self.L,
            num_threads=self.insert_threads,  # to allocate scratch space for up to 64 search threads
            initial_search_complexity=100
        )
        self.max_pts = max_pts
        print('Index class constructed and ready for update/search')
        self.active_indices = set()
        self.num_unprocessed_deletes = 0

    def quant(self, X, mi, mx):
        return np.clip((X - mi) / (mx - mi) * 255.0, 0.0, 255.0).astype('uint8')

    def insert(self, X, ids):
        if self.mi is None:
            self.mi = X.min()
            self.mx = X.max()
        X = self.quant(X, self.mi, self.mx)
        self.active_indices.update(ids + 1)
        print('#active pts', len(self.active_indices), '#unprocessed deletes', self.num_unprocessed_deletes)
        if len(self.active_indices) + self.num_unprocessed_deletes >= self.max_pts:
            print("try to delete")
            self.index.consolidate_delete()
            self.num_unprocessed_deletes = 0
        retvals = self.index.batch_insert(X, ids + 1, len(ids), self.insert_threads)
        if -1 in retvals:
            print('insertion failed')
            print('insertion return values', retvals)


    def delete(self, ids):
        for id in ids:
            self.index.mark_deleted(id + 1)
        self.active_indices.difference_update(ids + 1)
        self.num_unprocessed_deletes += len(ids)

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        X = self.quant(X, self.mi, self.mx)
        self.res, self.query_dists = self.index.batch_search(
            X, nq, k, self.Ls, self.search_threads)
        self.res = self.res - 1

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") == None else query_args.get("Ls")
        self.search_threads = self._query_args.get("T")

    def __str__(self):
        return f'pyanns({self.index_name(), self._query_args})'
