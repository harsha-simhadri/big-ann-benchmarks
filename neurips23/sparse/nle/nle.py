from __future__ import absolute_import

import numpy as np

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS

import os
import argparse
import pandas as pd
import json
from tqdm import tqdm
from .interface import PisaIndex
import shutil

# Build parameters: none
# Query parameters: budget (in ms) for computing all the scores
class NLE(BaseANN):
    def __init__(self, metric, index_params):    
        index_path = "./results/indexes/"
        index_path_full = "./results/indexes/"
        self.index_base = PisaIndex(index_path,overwrite=True)
        self.index_full = PisaIndex(index_path_full,overwrite=True)
        self.name = "pisa"
        self.t1 = index_params["t1"]
        self.t2 = index_params["t2"]
        self.k = 100

    def fit(self, dataset):
        self.index_base.path += dataset+"-"+str(self.t1)
        self.index_full.path += dataset+"-"+str(self.t2)
        if not os.path.exists(os.path.join(self.index_base.path,"quantized.q0.bmw.64.block_simdbp")):
            if os.path.exists(self.index_base.path) and os.path.isdir(self.index_base.path):
                shutil.rmtree(self.index_base.path)
            os.makedirs(self.index_base.path,exist_ok=True)
            self.ds = DATASETS[dataset]()
            assert self.ds.data_type() == "sparse"

            N_VEC_LIMIT = 10000 # batch size
            it = self.ds.get_dataset_iterator(N_VEC_LIMIT)
            self.index_base.index(it,self.t1)

        if not os.path.exists(os.path.join(self.index_full.path,"quantized.q0.bmw.64.block_simdbp")):
            if os.path.exists(self.index_full.path) and os.path.isdir(self.index_full.path):
                shutil.rmtree(self.index_full.path)
        
            os.makedirs(self.index_full.path,exist_ok=True)
            self.ds = DATASETS[dataset]()
            assert self.ds.data_type() == "sparse"

            N_VEC_LIMIT = 10000 # batch size
            it = self.ds.get_dataset_iterator(N_VEC_LIMIT)
            self.index_full.index(it,self.t2)
        if not os.path.exists(os.path.join(self.index_full.path,"inv.fwd")):
            self.index_full.generate_forward()
        self.index_base.load_inv(self.index_full,k=10,k1=-1,k2=-1,k3=100)
        self.index_full.load_forward()

    def load_index(self, dataset):
        # if dataset not in self.index_base.path:
        #     self.index_base.path += dataset+"-"+str(self.t1)
        # if dataset not in self.index_full.path:
        #     self.index_full.path += dataset+"-"+str(self.t2)

        # self.index_base.load_inv(self.index_full,k=10,k1=-1,k2=-1,k3=100)
        # self.index_full.load_forward()
        return None

    def set_query_arguments(self, query_args):
        self.k1 = query_args["k1"]
        self.k2 = query_args["k2"]
        try:
            self.k3 = query_args["k3"]
        except:
            self.k3 = 100

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        res = self.index_base.retrieve(self.index_full, X, k,k1=self.k1, k2=self.k2, bm25_k1=self.k3)
        self.I = res

    def get_results(self):
        return self.I
