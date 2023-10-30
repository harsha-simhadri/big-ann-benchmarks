from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import sys
sys.path.append("/home/app/SUSTech-OOD")
import graphood

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS, download_accelerated

class IndexGraphOOD(BaseOODANN):
    def __init__(self, metric, index_params):
        self.name = "graphood"
        self._index_params = index_params
        self._metric = metric

        self.M = index_params.get("M")
        self.ef = index_params.get("ef")
        self.cluster_num = index_params.get("cluster_num")
        self.hnsw_n = f'M{self.M}_ef{self.ef}.hnsw'
        self.ivf_n = f'{self.cluster_num}.ivf'
        self.sq_n = f"sq"

    def index_name(self):
        return f"M{self.M}_ef{self.ef}_c{self.cluster_num}"

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "ood")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'final')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        print(index_dir)
        return index_dir

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        """

        ds = DATASETS[dataset]()
        d = ds.d

        index_dir = self.create_index_dir(ds)
        self.hnsw_fn = os.path.join(index_dir, self.hnsw_n)
        self.ivf_fn = os.path.join(index_dir, self.ivf_n)
        self.sq_fn = os.path.join(index_dir, self.sq_n)

        if  hasattr(self, 'index'):
            print('Index object exists already')
            return

        start = time.time()
        graphood.build_index(ds.get_dataset_fn(), self.hnsw_fn, self.ivf_fn, self.sq_fn, self.M, self.ef, self.cluster_num)
        end = time.time()
        print("index built in %.3f s" % (end - start))
        
        print('Loading index..')
        self.index = graphood.IndexGraphOOD(d, ds.nb, self.hnsw_fn, self.ivf_fn, self.sq_fn)
        print('Index ready for search')

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        ds = DATASETS[dataset]()
        d = ds.d

        index_dir = self.create_index_dir(ds)        
        if not (os.path.exists(index_dir)) and 'url' not in self._index_params:
            return False
        
        self.hnsw_fn = os.path.join(index_dir, self.hnsw_n)
        self.ivf_fn = os.path.join(index_dir, self.ivf_n)
        self.sq_fn = os.path.join(index_dir, self.sq_n)
        
        for component in [self.hnsw_fn, self.ivf_fn, self.sq_fn]:
            if not (os.path.exists(component)):
                if 'url' in self._index_params:
                    index_file_source = self._index_params['url'] + '/' + self.index_name() + component
                    print(f"Downloading index in background. This can take a while.")
                    download_accelerated(index_file_source, component, quiet=True)
                else:
                    return False

        print("Loading index")

        self.index = graphood.IndexGraphOOD(d, ds.nb, self.hnsw_fn, self.ivf_fn, self.sq_fn)
        print ("Load index success.")
        print(sys.getsizeof(self.index))
        return True
        
    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        self.res = self.index.batch_search(nq, X, k, self.ef, self.nprobe)
    

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.ef = query_args.get("ef")                             
        self.nprobe = query_args.get("nprobe")

    def __str__(self):
        return f'{self._query_args})'