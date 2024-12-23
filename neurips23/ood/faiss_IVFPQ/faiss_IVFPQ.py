import PyCANDYAlgo

import numpy as np

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
import os

class faiss_IVFPQ(BaseOODANN):
    def __init__(self, metric, index_params):
        self.indexkey="IVF1024,SQ8"
        self.name = "faiss_HNSW"
        self.nprobe=1

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        d = ds.d
        index = PyCANDYAlgo.index_factory_l2(d, self.indexkey)
        self.vecDim =  d

        xb = ds.get_dataset()
        print("train")
        index.train(xb.shape[0], xb.flatten())
        index.add(xb.shape[0], xb.flatten())
        self.index = index
        self.nb = ds.nb
        self.xb = xb

        return


    def query(self, X, k):
        querySize = X.shape[0]
        print(f"Searching with ef={self.nprobe}")
        results = self.index.search(querySize, X.flatten(), k, self.nprobe)
        res = np.array(results).reshape(X.shape[0], k)


        self.res = res

    def set_query_arguments(self, query_args):
        if "nprobe" in query_args:
            self.nprobe = query_args['nprobe']
        else:
            self.nprobe = 1

    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.faissindex"