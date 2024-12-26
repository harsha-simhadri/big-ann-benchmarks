import PyCANDYAlgo

import numpy as np

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
import os

class faiss_HNSW(BaseOODANN):
    def __init__(self, metric, index_params):
        self.indexkey="HNSW32"
        self.name = "faiss_HNSW"
        self.ef=16

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        d = ds.d
        index = PyCANDYAlgo.index_factory_ip(d, self.indexkey)

        xb = ds.get_dataset()

        index.add(xb.shape[0], xb.flatten())
        index.verbose = True
        self.index = index
        self.nb = ds.nb
        self.xb = xb

        return


    def query(self, X, k):


        querySize = X.shape[0]
        print(f"Searching with ef={self.ef}")
        results = self.index.search(querySize, X.flatten(), k, self.ef)
        res = np.array(results).reshape(X.shape[0], k)


        self.res = res

    def set_query_arguments(self, query_args):
        if "ef" in query_args:
            self.ef = query_args['ef']
        else:
            self.ef = 16

    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.faissindex"