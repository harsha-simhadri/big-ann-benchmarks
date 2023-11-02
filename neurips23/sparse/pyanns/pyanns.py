from __future__ import absolute_import

import gc
import os
import numpy as np

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS
import pyanns

class Pyanns(BaseANN):
    def __init__(self, metric, index_params):
        assert metric == "ip"
        self.name = "pyanns"

    def fit(self, dataset): # e.g. dataset = "sparse-small"

        self.ds = DATASETS[dataset]()
        assert self.ds.data_type() == "sparse"

        print("start add")
        path = 'hnsw_sparse.idx' 

        self.searcher = pyanns.SparseGrapSearcher(self.ds.get_dataset_fn(), path)
        print("done add")

    def load_index(self, dataset):
        return None

    def set_query_arguments(self, query_args):
        self._budget = query_args["budget"]
        self.ef = query_args["ef"]
        self.searcher.set_ef(self.ef)

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq = X.shape[0]
        self.res = self.searcher.search_batch(nq, X.indptr, X.indices, X.data, k, self._budget).reshape(-1, k)

    def get_results(self):
        return self.res

    def __str__(self):
        return f'pyanns_qdrop{self._budget}_ef{self.ef}'
