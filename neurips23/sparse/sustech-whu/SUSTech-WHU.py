from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import sys

sys.path.append("/home/app/SUSTech-WHU-Sparse")
import hnswsparse
from neurips23.sparse.base import BaseSparseANN
from benchmark.datasets import DATASETS, download_accelerated


class HnswSparse(BaseSparseANN):
    def __init__(self, metric, index_params):
        assert metric == "ip"
        self.name = "hnswsparse"
        self._index_params = index_params
        self._metric = metric
        self.M = index_params.get("M")
        self.ef = index_params.get("ef")
        self._index_n = f"M{self.M}_ef{self.ef}.hnsw"

    def index_name(self):
        return self._index_n

    def fit(self, dataset):  # e.g. dataset = "sparse-small"
        """
        Build the index for the data points given in dataset name.
        """
        ds = DATASETS[dataset]()
        index_dir = self.create_index_dir(dataset)
        if hasattr(self, "index"):
            print("Index object exists already")
            return
        assert ds.data_type() == "sparse"
        dataset_fn = ds.get_dataset_fn()
        index_fn = f"{dataset}_M{self.M}_ef{self.ef}.hnsw"
        index_fn = os.path.join(index_dir, index_fn)
        print("index name: " + index_fn)
        hnswsparse.build_index(index_fn, dataset_fn, self.M, self.ef)
        self.index = hnswsparse.HnswSparse(index_fn, dataset_fn)
        print("Index status: " + str(self.index))

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        m = self.M
        ef = self.ef
        ds = DATASETS[dataset]()
        index_dir = self.create_index_dir(dataset)
        if not (os.path.exists(index_dir)):
            return False
        index_fn = f"{dataset}_M{m}_ef{ef}.hnsw"
        index_fn = os.path.join(index_dir, index_fn)
        dataset_fn = ds.get_dataset_fn()
        if not os.path.exists(index_fn):
            return False
        print("loading index")
        self.index = hnswsparse.HnswSparse(index_fn, dataset_fn)
        print("loading index success")
        return True

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", dataset)
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        print(index_dir)
        return index_dir

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        indptr = X.indptr
        indices = X.indices
        data = X.data
        # ncol = X.shape[1]
        # nnz = X.nnz
        nrow = X.shape[0]
        # prepare the queries as a list of dicts
        res = self.index.search(nrow, indptr, indices, data, self.ef, k)
        self.I = np.array(res, dtype="int32")

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.ef = query_args.get("ef")

    def get_results(self):
        return self.I

    def __str__(self):
        return f"{self._query_args})"

    # def gen_probility_prune(filename):
    #     with open(filename, "r") as f:
    #         lines = f.readlines()
    #         sum_score = 0
    #         for line in lines:
    #             x, y = map(int, line.split())
    #             sum_score += y
    #         probility = []
    #         mean_score = sum_score / len(lines)
    #         sum_score = 0
    #         for line in lines:
    #             x, y = map(int, line.split())
    #             if y > mean_score:
    #                 sum_score += y
    #         for line in lines:
    #             x, y = map(int, line.split())
    #             if y > mean_score:
    #                 probility.append((x, y / sum_score))
    #     with open("probility.txt", "w") as f:
    #         for p in probility:
    #             f.write(str(p[0]) + " " + str(p[1]) + "\n")
    # print(len(probility))
    # return probility


# probility = gen_probility_prune("nonzero_and_gt.txt")
