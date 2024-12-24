import PyCANDYAlgo

import numpy as np

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
import os
import torch

class candy_hnsw(BaseOODANN):
    def __init__(self, metric, index_params):
        self.indexkey="HNSWNaive"
        self.name = "candy_HNSW"
        self.ef=16

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        d = ds.d
        index = PyCANDYAlgo.createIndex(self.indexkey, d)

        xb = ds.get_dataset()
        subA = torch.from_numpy(xb.copy())
        index.loadInitialTensor(subA)
        self.index = index
        self.nb = ds.nb
        self.xb = xb

        return


    def query(self, X, k):


        queryTensor = torch.from_numpy(X.copy())
        results = self.index.searchIndex(queryTensor, k)
        res = np.array(results).reshape(X.shape[0], k)

        self.res = res

    def set_query_arguments(self, query_args):
        if "ef" in query_args:
            self.ef = query_args['ef']
        else:
            self.ef = 16

    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.faissindex"