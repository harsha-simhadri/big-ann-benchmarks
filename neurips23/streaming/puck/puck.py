# !/usr/bin/env python3
#-*- coding:utf-8 -*-
################################################################################
#
# Copyright (c) 2021 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
@file: puck_inmem.py
@author: yinjie06(yinjie06@baidu.com)
@date: 2021-10-06 13:44
@brief: 
"""
import ctypes

from neurips23.streaming.base import BaseStreamingANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
from PyCANDYAlgo import puck
import gflags
import multiprocessing.pool
import multiprocessing
import gc
import os
import numpy as np
import time
import math
import struct
import sys
print(sys.version)
CPU_LIMIT = multiprocessing.cpu_count()
class Puck(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self._index_params = index_params
        self._metric = metric
        self.indexkey = index_params.get("indexkey", "NA")

        self.index = puck.PuckSearcher()
        self.topk = 10
        self.n = 0
        self.build_memory_usage = -1

    def track(self):
        #T1 means in memory
        return "T1 for 10M & 100M"


    def init_indexkey(self):
        #一级聚类中心
        if "C" in self._index_params:
            puck.update_gflag('coarse_cluster_count', "%d"%(self._index_params['C']))
            self.indexkey = "C%s"%(self._index_params['C'])
        #二级聚类中心
        if "F" in self._index_params:
            puck.update_gflag('fine_cluster_count', "%d"%(self._index_params['F']))
            self.indexkey += "_F%s"%(self._index_params['F'])
        #filter
        if "FN" in self._index_params:
            puck.update_gflag('filter_nsq', "%d"%(self._index_params['FN']))
            self.indexkey += "_FN%s"%(self._index_params['FN'])
        #量化
        if "N" in self._index_params:
            if int(self._index_params['N']) > 1:
                puck.update_gflag('whether_pq', 'true')
                puck.update_gflag('nsq', "%d"%(self._index_params['N']))
                self.indexkey += "_N%s"%(self._index_params['N'])
            else:
                puck.update_gflag('whether_pq', 'false')
                self.indexkey += "_Flat"
        
        if "tinker_neighborhood" in self._index_params:
            puck.update_gflag('tinker_neighborhood', "%d"%(self._index_params['tinker_neighborhood']))
            self.indexkey += "_Neighborhood%s"%(self._index_params['tinker_neighborhood'])
        if "tinker_construction" in self._index_params:
            puck.update_gflag('tinker_construction', "%d"%(self._index_params['tinker_construction']))
            self.indexkey += "_Construction%s"%(self._index_params['tinker_construction'])
        if "index_type" in self._index_params:
            puck.update_gflag('index_type', "%d"%(self._index_params['index_type']))
        if "radius_rate" in self._index_params:
            puck.update_gflag('radius_rate', "%f"%(self._index_params['radius_rate']))
            self.indexkey += "_RadiusRate%s"%(self._index_params['radius_rate'])
        if "filter_topk" in self._index_params:
            puck.update_gflag('filter_topk', "%d"%(self._index_params['filter_topk']))
            self.indexkey += "_filter_topk%s"%(self._index_params['filter_topk'])


    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.puckindex"

    def index_tag_name(self, name):
        return f"{name}.{self.indexkey}.puckindex"

    def setup(self, dtype, max_pts, ndim):
        print("setup")
        puck.update_gflag('max_point_stored', '%d'%(max_pts))
        puck.update_gflag('whether_norm', 'false')
        puck.update_gflag('max_point_stored', "%d"%(max_pts))
        puck.update_gflag('feature_dim', "%d"%(ndim))
        self.init_indexkey()
        #索引存储目录
        dataset = "streaming"
        puck.update_gflag('kmeans_iterations_count',"1")
        puck.update_gflag('threads_count', "%d"%(CPU_LIMIT))
        puck.update_gflag('context_initial_pool_size', "%d"%(2 * CPU_LIMIT))
        print(self.index_name(dataset))
        puck.update_gflag('index_path', self.index_name(dataset))

        if not os.path.exists(self.index_name(dataset)):
            index_dir = os.path.join(os.getcwd(), self.index_name(dataset))
            os.makedirs(index_dir, mode=0o777, exist_ok=True)
        
        #训练用目录         
        if not os.path.exists('mid-data'):
            os.mkdir('mid-data')

        print(1) 
        self.index.init()

    def set_query_arguments(self, query_args):
        for key, value in query_args.items():
            puck.update_gflag(key, "%s"%value)
        #query_args_list = query_args.strip().split(',')
        #self.index.update_params(int(self.topk), int(query_args_list[1]), int(query_args_list[2]),int(query_args_list[3]))
        puck.update_gflag('threads_count', "%d"%(CPU_LIMIT))
        self.index.init()
        #topk是作为检索参数传入puck
        self.qas = query_args
    def insert(self, X, ids):
        n, d = X.shape
        #self.index.batch_add(n, d, swig_ptr(X), swig_ptr(ids))
        self.index.batch_add(n, d, X.flatten(), ids.tolist())
    def delete(self, ids):
        n = len(ids)
        #self.index.batch_delete(n, swig_ptr(ids))
        self.index.batch_delete(n, ids.tolist())
    def query(self, X, topK):
        n, d = X.shape
        self.res = (np.empty((n, topK), dtype='float32'), np.empty((n, topK), dtype='uint32'))
        #self.index.search(n, swig_ptr(X), topK, swig_ptr(self.res[0]), swig_ptr(self.res[1]))
        self.index.search(n, X.flatten(), topK, self.res[0].flatten(), self.res[1].flatten())
        #print(self.res[0])
        #print(self.res[1])
    def get_results(self):
        return self.res[1]
    
    def __str__(self):
        return f'Puck{self.indexkey, self.qas}'
