import os
import sparse_hnswlib
import numpy as np
from neurips23.sparse.base import BaseSparseANN
from benchmark.datasets import DATASETS, download_accelerated


class SparseHNSW(BaseSparseANN):
    def __init__(self, metric, method_param):
        assert metric == "ip"
        self.method_param = method_param
        self.name = "sparse_hnswlib"
        self.efC = self.method_param["efConstruction"]
        self.M = self.method_param["M"]
        self.nt = self.method_param["buildthreads"]

    def fit(self, dataset):
        print("begin fit")
        ds = DATASETS[dataset]()
        
        p = sparse_hnswlib.Index(space="ip", dim=8)
        p.init_index(
            max_elements=ds.nb,
            csr_path=ds.get_dataset_fn(),
            ef_construction=self.efC,
            M=self.M,
        )
        p.add_items(num_threads=self.nt)
        
        index_dir = os.path.join(os.getcwd(), "data", "indices", "sparse", "shnsw")
        index_path = os.path.join(index_dir, "shnsw-{}-{}-{}".format(dataset, self.efC, self.M)) 
        if not os.path.exists(index_dir):
            os.makedirs(index_dir, mode=0o777, exist_ok=True)
        p.save_index(index_path)
        self.p = p

    def load_index(self, dataset):
        print("begin load")
        index_dir = os.path.join(os.getcwd(), "data", "indices", "sparse", "shnsw")
        index_path = os.path.join(index_dir, "shnsw-{}-{}-{}".format(dataset, self.efC, self.M)) 
        if not os.path.exists(index_dir):
            return False
        if not os.path.exists(index_path):
            return False
        ds = DATASETS[dataset]()
        X = ds.get_dataset()
        self.p = sparse_hnswlib.Index(space="ip", dim=8)
        print("#########")
        self.p.load_index(index_path)
        print("!!!!!!!!")
        return True

    def set_query_arguments(self, parameters):
        print("开始 set")
        ef = parameters
        self.p.set_ef(ef)

    def query(self, X, topK):
        # N, _ = X.shape
        self.I, _ = self.p.knn_query(X.indptr, X.indices, X.data, k=topK, num_threads=self.nt)
        
    def get_results(self):
        return self.I