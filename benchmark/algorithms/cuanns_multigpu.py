from __future__ import absolute_import
import numpy
import os
import sys
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, sanitize

sys.path.append("/home/soft")
import pycuann


class CuannsMultiGPU(BaseANN):
    def __init__(self, metric, build_param):
        dim = build_param["dim"]
        dtype = build_param["dtype"]

        if "dev_list" in build_param:
            dev_list = build_param["dev_list"]
        else:
            dev_list = []

        if "graph_k" in build_param:
            graph_k = build_param["graph_k"]
        else:
            graph_k = 96

        if "nlist" in build_param:
            nlist = build_param["nlist"]
        else:
            nlist = 10000

        if "nprobe" in build_param:
            nprobe = build_param["nprobe"]
        else:
            nprobe = 16

        if "max_k" in build_param:
            max_k = build_param["max_k"]
        else:
            max_k = 10

        if "max_batch_size" in build_param:
            max_batch_size = build_param["max_batch_size"]
        else:
            max_batch_size = 10000

        self._algo = pycuann.PyCUANN(
            metric, dim, dtype, dev_list, graph_k, nlist, nprobe, max_k, max_batch_size
        )

    def __str__(self):
        return self.__class__.__name__

    def track(self):
        return "T3"

    def _index_file_name(self, dataset):
        return f"data/indices/t3/{self}/{dataset}"

    def _get_dataset(self, dataset):
        ds = DATASETS[dataset]()
        return next(ds.get_dataset_iterator(bs=ds.nb))

    def load_index(self, dataset):
        try:
            self._algo.load(self._index_file_name(dataset))
            ds = self._get_dataset(dataset)
            self._algo.set_search_dataset(ds)
            return True
        except Exception as e:
            print(e)
            return False

    def set_query_arguments(self, query_args):
        if "iteration_num" in query_args:
            iteration_num = query_args["iteration_num"]
        else:
            iteration_num = 5

        if "searcher_num" in query_args:
            searcher_num = query_args["searcher_num"]
        else:
            searcher_num = 16

        if "searcher_k" in query_args:
            searcher_k = query_args["searcher_k"]
        else:
            searcher_k = 32

        if "max_batch_buffer_size" in query_args:
            max_batch_buffer_size = query_args["max_batch_buffer_size"]
        else:
            max_batch_buffer_size = 10000

        self._algo.set_search_param(
            iteration_num, searcher_num, searcher_k, max_batch_buffer_size
        )

    def query(self, X, k):
        self.res = self._algo.search(X, k)

    def get_results(self):
        return self.res
