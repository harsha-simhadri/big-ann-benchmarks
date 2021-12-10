#-*- coding:utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
@file: puck_t1.py
@author: yinjie06(yinjie06@baidu.com)
@date: 2021-10-06 13:44
@brief: 
"""
from benchmark.algorithms.base import BaseANN
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated
from puck import py_puck_api
import os
import numpy as np
import time

swig_ptr = py_puck_api.swig_ptr
class Puck(BaseANN):
    def __init__(self, metric, index_params):
        self._index_params = index_params
        self._metric = metric
        self._query_bs = -1
        self.indexkey = index_params.get("indexkey", "NA")

        if 'query_bs' in index_params:
            self._query_bs = index_params['query_bs']
        self.index = py_puck_api.PySearcher()
        self.topk = 10
        self.n = 0
        
    def track(self):
        return "T1"

    def fit(self, dataset):
        print("Puck provide the index-data and the Docker image for search. We will open Puck to open source community at the end of this year.")

    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.puckindex"

    def index_tag_name(self, name):
        return f"{name}.{self.indexkey}.puckindex"

    def load_index(self, dataset):
        index_components = ["filer_data.dat","GNOIMI_coarse.dat","GNOIMI_fine.dat","index.dat","learn_assign.dat"]
        ############ download index && update links
        print(self.index_name(dataset))
        if not os.path.exists(self.index_name(dataset)):
            if 'url' not in self._index_params:
                return False
            #5 index files will be downloaded in this lib 
            index_dir = os.path.join(os.getcwd(), self.index_name(dataset))
            print(index_dir)
            os.makedirs(index_dir, mode=0o777, exist_ok=True)
            print('Downloading index in background. This can take a while.')
            for component in index_components:
                download_accelerated(self._index_params['url']+"_"+component, self.index_name(dataset)+"/"+component, quiet=True)
                time.sleep(60)
        print("Loading index")
        index_tag = self.index_tag_name(dataset)
        cmd = " ln -s %s ./puck_index"%(self.index_name(dataset))
        print(cmd)     
        os.system(cmd)
        cmd = " ls -al puck_index/"
        os.system(cmd)
        self.index.init()
        self.index.show()
        ds = DATASETS[dataset]()
        self.n = ds.nq
        return True
    
    def set_query_arguments(self, query_args):
        query_args_list = query_args.strip().split(',')
        self.index.update_params(int(query_args_list[0]), int(query_args_list[1]), int(query_args_list[2]),int(query_args_list[3]))
        self.topk = int(query_args_list[0])
        self.res = (np.empty((self.n, self.topk), dtype='float32'), np.empty((self.n, self.topk), dtype='uint32'))
        self.qas = query_args
        print(type(self.res[0]), len(self.res[0]))
    
    def query(self, X, topK):
        n, d = X.shape
        self.index.search(n, swig_ptr(X), swig_ptr(self.res[0]), swig_ptr(self.res[1]))
    
    def get_results(self):
        return self.res[1]
    
    def __str__(self):
        return f'Puck({self.qas})'

