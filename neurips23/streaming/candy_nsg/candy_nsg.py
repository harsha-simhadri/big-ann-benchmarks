import PyCANDYAlgo

import numpy as np
from numpy import typing as npt

from neurips23.streaming.base import BaseStreamingANN
import torch

class candy_nsg(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.indexkey="faiss"
        self.faissIndexTag = index_params['indexkey']
        self.metric = metric
        self.name = "candy_nsg"
        self.ef=16
        self.trained = False

    def setup(self, dtype, max_pts, ndim):
        index = PyCANDYAlgo.createIndex(self.indexkey, ndim)
        cm = PyCANDYAlgo.ConfigMap()
        if self.metric == 'euclidean':
            cm.edit("metricType", "L2")
        else:
            cm.edit("metricType", "IP")
        cm.edit("faissIndexTag", self.faissIndexTag)
        cm.edit("vecDim", ndim)
        index.setConfig(cm)
        self.index = index
        self.my_index = -1 * np.ones(max_pts, dtype=int)
        # Mapping from global id to faiss index id
        self.my_inverse_index = -1*np.ones(max_pts, dtype=int)
        self.ntotal = 0

        return

    def insert(self, X,ids):

        mask = self.my_inverse_index[ids] == -1
        new_ids = ids[mask]

        new_data = X[mask]
        if (new_data.shape[0] != 0):
            subA = torch.from_numpy(new_data.copy())
            if(self.trained):
                self.index.insertTensorWithIds(new_ids,subA)
            else:
                self.index.loadInitialTensorWithIds(new_ids,subA)
                self.trained = True
            indices = np.arange(self.ntotal, self.ntotal + new_data.shape[0])
            self.my_index[indices] = new_ids
            print(f"Indices {indices[0]} : {indices[-1]} to Global {new_ids[0]}:{new_ids[-1]}")
            self.my_inverse_index[new_ids] = indices
            self.ntotal += new_data.shape[0]
        else:
            print("Not Inserting Same Data!")


    def delete(self, ids):
        self.index.deleteIndex(ids)
        return

    def query(self, X, k):


        queryTensor = torch.from_numpy(X.copy())
        results = np.array(self.index.searchIndex(queryTensor, k))
        ids = self.my_index[results]
        res = ids.reshape(X.shape[0], k)
        self.res = res

    def set_query_arguments(self, query_args):
        if "ef" in query_args:
            self.ef = query_args['ef']
        else:
            self.ef = 16

    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.faissindex"