from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import pyanns
import diskannpy
import gc

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS, download_accelerated


class Pyanns(BaseOODANN):
    def __init__(self, metric, index_params):
        self.name = "diskann+sq8"
        if (index_params.get("R") == None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L") == None):
            print("Error: missing parameter L")
            return
        self._index_params = index_params
        self._metric = metric

        self.R = index_params.get("R")
        self.L = index_params.get("L")

        self.dir = "indices"
        self.path = self.index_name()

    def index_name(self):
        return f"R{self.R}_L{self.L}"
            
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "ood")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'diskann')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir


    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return 'l2'
        elif metric == 'ip':
            return 'mips'
        else:
            raise Exception('Invalid metric')

    def translate_dist_fn_pyanns(self, metric):
        if metric == 'euclidean':
            return 'L2'
        elif metric == 'ip':
            return 'IP'
        else:
            raise Exception('Invalid metric')

    def translate_dtype(self, dtype: str):
        if dtype == 'uint8':
            return np.uint8
        elif dtype == 'int8':
            return np.int8
        elif dtype == 'float32':
            return np.float32
        else:
            raise Exception('Invalid data type')

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        """
        ds = DATASETS[dataset]()
        d = ds.d

        buildthreads = self._index_params.get("buildthreads", -1)
        print(buildthreads)
        if buildthreads == -1:
            buildthreads = 0

        index_dir = self.create_index_dir(ds)
        
        if  hasattr(self, 'index'):
            print('Index object exists already')
            return

        print(ds.get_dataset_fn())
        
        graph_path = f'{index_dir}/{self.index_name()}'
        
        if not os.path.exists(graph_path):
            start = time.time()
            diskannpy.build_memory_index(
                data = ds.get_dataset_fn(),
                distance_metric = self.translate_dist_fn(ds.distance()),
                vector_dtype = self.translate_dtype(ds.dtype),
                index_directory = index_dir,
                index_prefix = self.index_name(),
                complexity=self.L,
                graph_degree=self.R,
                num_threads = buildthreads,
                alpha=1.2,
                use_pq_build=False,
                num_pq_bytes=0, #irrelevant given use_pq_build=False
                use_opq=False
            )
            end = time.time()
            print("DiskANN index built in %.3f s" % (end - start))
        gc.collect()
        g = pyanns.Graph(graph_path, 'diskann')
        self.searcher = pyanns.Searcher(
            g, ds.get_dataset(), self.translate_dist_fn_pyanns(ds.distance()), "SQ8U")
        self.searcher.optimize()
        print('Index ready for search')

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        return False

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, _ = X.shape
        self.res = self.searcher.batch_search(X, k).reshape(nq, -1)

    def set_query_arguments(self, query_args):
        self.ef = query_args.get("ef")
        self.searcher.set_ef(self.ef)

    def __str__(self):
        return f'pyanns({self.index_name()})_ef{self.ef}'
