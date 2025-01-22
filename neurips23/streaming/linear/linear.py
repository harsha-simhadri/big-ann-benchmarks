import PyCANDYAlgo

import numpy as np
from numpy import typing as npt

from neurips23.streaming.base import BaseStreamingANN
import torch
import traceback

class linear(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.indexkey= index_params['indexkey']
        self.metric = metric
        self.name = "linear"
        self.trained = False

    def setup(self, dtype, max_pts, ndim):
        index = None
        if self.metric == 'euclidean':
            index = PyCANDYAlgo.index_factory_l2(ndim, self.indexkey)
        else:
            index = PyCANDYAlgo.index_factory_ip(ndim, self.indexkey)

        self.my_index = -1 * np.ones(max_pts, dtype=int)
        # Mapping from global id to faiss index id
        self.my_inverse_index = -1*np.ones(max_pts, dtype=int)

        self.index = index
        self.ntotal = 0

    def insert(self, X,ids):
        mask = self.my_inverse_index[ids]==-1
        new_ids = ids[mask]

        new_data = X[mask]
        if(new_data.shape[0]!=0):
            if(self.trained):
                #self.index.add(X.shape[0],X.flatten())
                self.index.add(new_data.shape[0], new_data.flatten())

            else:

                #self.index.train(X.shape[0],X.flatten())
                self.index.train(new_data.shape[0], new_data.flatten())
                #self.index.add(X.shape[0], X.flatten())
                self.index.add(new_data.shape[0], new_data.flatten())
                self.trained=True
            indices = np.arange(self.ntotal, self.ntotal + new_data.shape[0])
            self.my_index[indices] = new_ids
            print(f"Faiss indices {indices[0]} : {indices[-1]} to Global {new_ids[0]}:{new_ids[-1]}")
            self.my_inverse_index[new_ids] = indices
            self.ntotal += new_data.shape[0]
        else:
            print("Not Inserting Same Data!")


    def delete(self, ids):
        return


    def query(self, X, k):


        querySize = X.shape[0]

        results = np.array(self.index.search(querySize, X.flatten(), k, self.ef))
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