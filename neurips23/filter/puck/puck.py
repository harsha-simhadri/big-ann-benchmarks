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

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
from puck import py_puck_api
import multiprocessing.pool
from multiprocessing import Process
import os
import numpy as np
import time
import math
import struct

CPU_LIMIT = multiprocessing.cpu_count() 
swig_ptr = py_puck_api.swig_ptr

class Puck(BaseFilterANN):
    def __init__(self, metric, index_params):
        self._index_params = index_params
        self._metric = metric
        self.indexkey = index_params.get("indexkey", "NA")

        self.index = py_puck_api.PySearcher()
        self.topk = 10
        self.n = 0
        self.build_memory_usage = -1
        self.index_type = 1
        print("after init")

    def init_dataset_key(self, dataset):

        #更新gflags
        ds = DATASETS[dataset]()
        d = ds.d
        #特征纬度
        py_puck_api.update_gflag('feature_dim', "%d"%(d))

        #根据距离计算方式调整
        self.whether_norm = False
        py_puck_api.update_gflag('whether_norm', 'false')
        self.ip2cos = 0
        if ds.distance() == "angular":
            self.whether_norm = True
            py_puck_api.update_gflag('whether_norm', 'true')
        elif ds.distance() == "ip":
            self.ip2cos = 1
        py_puck_api.update_gflag('ip2cos', '%d'%(self.ip2cos))

        self.init_indexkey()
        #测试
        py_puck_api.update_gflag('kmeans_iterations_count',"1") 

    def check_feature(self, dataset):
        self.init_dataset_key(dataset)
        ds = DATASETS[dataset]()
        d = ds.d
        #索引存储目录
        py_puck_api.update_gflag('index_path', self.index_name(dataset))
        if not os.path.exists(self.index_name(dataset)):
            index_dir = os.path.join(os.getcwd(), self.index_name(dataset))
            os.makedirs(index_dir, mode=0o777, exist_ok=True)
        
        if if ds.search_type() != "knn_filtered":
            self.index_type = 1
            py_puck_api.update_gflag('index_type', "1")
        if self.index_type == 3:
            meta_indices_file_name = self.index_name(dataset) + "/indices.dat"
            meta_indices_file = open(meta_indices_file_name, 'wb')
            meta_indptr_file_name = self.index_name(dataset) + "/indptr.dat"
            meta_indptr_file = open(meta_indptr_file_name, 'wb')
            
            meta_to_write = ds.get_dataset_metadata()
            buf = struct.pack('i', len(meta_to_write.indices))
            meta_indices_file.write(buf)
            buf = struct.pack('i' * len(meta_to_write.indices), *(meta_to_write.indices))
            meta_indices_file.write(buf)
            meta_indices_file.close() 
            
            buf = struct.pack('i', len(meta_to_write.indptr))
            meta_indptr_file.write(buf)
            buf = struct.pack('i' * len(meta_to_write.indptr), *(meta_to_write.indptr))
            meta_indptr_file.write(buf)
            meta_indptr_file.close() 
        
        #训练用目录         
        if not os.path.exists('mid-data'):
            os.mkdir('mid-data')
        #格式化文件数据，将来可不要，后续可修改训练接口
        all_feature_file = open("%s/all_data.feat.bin"%(self.index_name(dataset)), 'wb')

        add_part=100000
        i0 = 0
        t0 = time.time()
        for xblock in ds.get_dataset_iterator(bs=add_part):
            i1 = i0 + len(xblock)
            i0 = i1
            for x in xblock:
                feat = x.astype(np.float32)
                if(self.whether_norm):
                    feat = feat / np.sqrt(np.dot(feat, feat))
                elif(self.ip2cos > 0):
                    norm = np.dot(feat, feat)
                    if norm > 1.0:
                        print("not support, please contact yinjie06")
                        return False
                    feat = np.append(feat, math.sqrt(1.0 - norm))

                buf = struct.pack('i', len(feat))
                all_feature_file.write(buf)
                buf = struct.pack('f' * len(feat), *feat)
                all_feature_file.write(buf)
            print("  adding %d:%d / %d [%.3f s] " % (i0, i1, ds.nb, time.time() - t0))
        all_feature_file.close()
    
    def fit(self, dataset):
        print("start fit")
        
        #self.check_feature(dataset)
        p = Process(target=self.check_feature, args=(dataset,))
        p.start()
        p.join()
        self.init_dataset_key(dataset)
        ds = DATASETS[dataset]()
        py_puck_api.update_gflag('index_path', self.index_name(dataset))
        #训练数据采样
        py_puck_api.update_gflag('train_points_count', "5000000")
        py_puck_api.update_gflag('pq_train_points_count', "500000")
        print(self.index_name(dataset)) 

        print("start to train")  
        self.index.build(ds.nb)
        self.load_index(dataset) 
    
    def init_indexkey(self):
        #一级聚类中心
        if "C" in self._index_params:
            py_puck_api.update_gflag('coarse_cluster_count', "%d"%(self._index_params['C']))
            self.indexkey = "C%s"%(self._index_params['C'])
        #二级聚类中心
        if "F" in self._index_params:
            py_puck_api.update_gflag('fine_cluster_count', "%d"%(self._index_params['F']))
            self.indexkey += "_F%s"%(self._index_params['F'])
        #filter
        if "FN" in self._index_params:
            py_puck_api.update_gflag('filter_nsq', "%d"%(self._index_params['FN']))
            self.indexkey += "_FN%s"%(self._index_params['FN'])
        #量化
        if "N" in self._index_params:
            if int(self._index_params['N']) > 1:
                py_puck_api.update_gflag('whether_pq', 'true')
                py_puck_api.update_gflag('nsq', "%d"%(self._index_params['N']))
                self.indexkey += "_N%s"%(self._index_params['N'])
            else:
                py_puck_api.update_gflag('whether_pq', 'false')
                self.indexkey += "_Flat"
        
        if "tinker_neighborhood" in self._index_params:
            py_puck_api.update_gflag('tinker_neighborhood', "%d"%(self._index_params['tinker_neighborhood']))
            self.indexkey += "_Neighborhood%s"%(self._index_params['tinker_neighborhood'])
        if "tinker_construction" in self._index_params:
            py_puck_api.update_gflag('tinker_construction', "%d"%(self._index_params['tinker_construction']))
            self.indexkey += "_Construction%s"%(self._index_params['tinker_construction'])
        if "index_type" in self._index_params:
            self.index_type = int(self._index_params['index_type'])
            py_puck_api.update_gflag('index_type', "%d"%(self._index_params['index_type']))

    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.puckindex"

    def index_tag_name(self, name):
        return f"{name}.{self.indexkey}.puckindex"

    def load_index(self, dataset):
        print("Loading index")
        self.init_indexkey()
        ds = DATASETS[dataset]()
        self.topk = ds.default_count()
        print("self.topk=%d"%self.topk)
        py_puck_api.update_gflag('topk', "%s"%(ds.default_count()))
        py_puck_api.update_gflag('index_path', self.index_name(dataset))
        py_puck_api.update_gflag('context_initial_pool_size', "%d"%(CPU_LIMIT))
        py_puck_api.update_gflag('threads_count', "%d"%(CPU_LIMIT))
        print(self.index_name(dataset))
        ret = self.index.init()
        print("ret = ",ret)
        if ret != 0:
            return False
        self.index.show()
        self.n = ds.nq
        return True
    
    def set_query_arguments(self, query_args):
        for key, value in query_args.items():
            py_puck_api.update_gflag(key, "%s"%value)
        #query_args_list = query_args.strip().split(',')
        #self.index.update_params(int(self.topk), int(query_args_list[1]), int(query_args_list[2]),int(query_args_list[3]))
        self.index.init()
        #topk是作为检索参数传入puck
        self.res = (np.empty((self.n, self.topk), dtype='float32'), np.empty((self.n, self.topk), dtype='uint32'))
        self.qas = query_args
    
    def query(self, X, topK):

        n, d = X.shape
        self.index.search(n, swig_ptr(X), topK, swig_ptr(self.res[0]), swig_ptr(self.res[1]))
        #print(self.res[0])
        print(self.res[1])
    def get_results(self):
        return self.res[1]
    def filtered_query(self, X, filter, k):
        n, d = X.shape
        x_float = X.astype(np.float32)
        meta_q = filter
        self.index.filter_search(n, swig_ptr(x_float), k, swig_ptr(self.res[0]), swig_ptr(self.res[1]), swig_ptr(filter.indptr), swig_ptr(filter.indices))
    
    def __str__(self):
        return f'Puck{self.indexkey, self.qas}'
