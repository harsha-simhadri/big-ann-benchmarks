from __future__ import absolute_import
import psutil
import os
import time
import numpy as np

from PyCANDYAlgo import diskannpy

from neurips23.streaming.base import BaseStreamingANN


class diskann(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.name = "diskann"
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

    def index_name(self):
        return f"R{self.R}_L{self.L}"

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "streaming")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'diskann')
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
        if dtype == 'uint8':
            return np.uint8
        elif dtype == 'int8':
            return np.int8
        elif dtype == 'float32':
            return np.float32
        else:
            raise Exception('Invalid data type')

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
            algo_type=diskannpy.AlgoType.DISKANN,
            distance_metric=self.translate_dist_fn(self._metric),  # 确保返回的是 diskann::Metric 类型
            max_vectors=max_pts,  # 最大向量数
            dimensions=ndim,  # 向量维度
            graph_degree=self.R,  # 图的度数
            complexity=self.L,  # 算法复杂度
            num_threads=self.insert_threads,  # 插入时使用的线程数
            initial_search_complexity=100  # 初始搜索复杂度
        )
        self.max_pts = max_pts
        print('Index class constructed and ready for update/search')
        self.active_indices = set()
        self.num_unprocessed_deletes = 0

    def insert(self, X, ids):
        self.active_indices.update(ids + 1)
        print('#active pts', len(self.active_indices), '#unprocessed deletes', self.num_unprocessed_deletes)
        if len(self.active_indices) + self.num_unprocessed_deletes >= self.max_pts:
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
        self.res, self.query_dists = self.index.batch_search(
            X, nq, k, self.Ls, self.search_threads)
        self.res = self.res - 1

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") == None else query_args.get("Ls")
        self.search_threads = self._query_args.get("T")

    def __str__(self):
        return f'diskann({self.index_name(), self._query_args})'
