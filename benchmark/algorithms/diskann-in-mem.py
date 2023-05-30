from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import diskannpy

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

class DiskANNInMem(BaseANN):
    def __init__(self, metric, index_params):
        self.name = "DiskANNInMem"
        if (index_params.get("R")==None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L")==None):
            print("Error: missing parameter L")
            return

        self._index_params = index_params
        self._metric = metric

        self.R = index_params.get("R")
        self.L = index_params.get("L")

    def track(self):
        return "T2"

    def index_name(self):
        return f"R{self.R}_L{self.L}"
        
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.__str__())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir

    def translate_dist_fn(metric):
        if metric == "euclidean":
            return "l2"
        elif metric == "ip":
            return "mips"
        else:
            raise Exception('Invalid metric')

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        """

        ds = DATASETS[dataset]()
        d = ds.d

        buildthreads = self._index_params.get("buildthreads", -1)
        if buildthreads == -1:
            buildthreads = 0

        metric = translate_dist_fn(ds.distance())
        index_dir = self.create_index_dir(ds)
        
        if  hasattr(self, 'index'):
            print('Index object exists already')
            return

        start = time.time()
        diskannpy.build_memory_index(
            data = ds.get_dataset_fn(),
            metric = metric,
            vector_dtype = ds.dtype,
            index_directory = index_dir,
            index_prefix = self.index_name(),
            complexity=L,
            graph_degree=R,
            num_thread = buildthreads,
            alpha=1.2,
            use_pq_build=False,
            num_pq_bytes=0, #irrelevant given use_pq_build=False
            use_opq=False
        )
        end = time.time()
        print("DiskANN index built in %.3f s" % (end - start))

        
        print('Loading index..')
        self..load_index(self.index_path, diskannpy.omp_get_max_threads(), num_nodes_to_cache, self.cache_mechanism)
        self.index = diskannpy.StaticMemoryIndex(
            metric = metric,
            vector_dtype = ds.dtype,
            index_directory = index_dir,
            index_prefix = self.index_name(),
            num_threads = 64, #to allocate scratch space for up to 64 search threads
            initial_search_complexity = 100
        )
        print(Index ready for search')

    def get_index_components(self, dataset):
        index_components = ['', '.data']
        ds = DATASETS[dataset]()
        if ds.distance() == "ip":
            index_components = index_components + []
        return index_components

    def index_files_to_store(self, dataset):
        return [self.create_index_dir(DATASETS[dataset]()), self.index_name(), self.get_index_components(dataset)]

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        ds = DATASETS[dataset]()
        metric = translate_dist_fn(ds.distance())        

        index_dir = self.create_index_dir(ds)        
        if not (os.path.exists(index_dir)) and 'url' not in self._index_params:
            return False

        index_path = os.path.join(index_dir, self.index_name())
        index_components = self.get_index_components(dataset)

        for component in index_components:
            index_file = index_path + component
            if not (os.path.exists(index_file)):
                if 'url' in self._index_params:
                    index_file_source = self._index_params['url'] + '/' + self.index_name() + component
                    print(f"Downloading index in background. This can take a while.")
                    download_accelerated(index_file_source, index_file, quiet=True)
                else:
                    return False

        print("Loading index")

        self.index = diskannpy.StaticMemoryIndex(
            metric = metric,
            vector_dtype = ds.dtype,
            index_directory = index_dir,
            index_prefix = self.index_name(),
            num_threads = 64, #to allocate scratch space for up to 64 search threads
            initial_search_complexity = 100
        )
        print ("Load index success.")
        return True
        
    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        self.res, self.query_dists = self.index.batch_search(
            X, k, self.Ls, self.threads)
     

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") == None else query_args.get("Ls")        
        self.Lmin = 0 if query_args.get("Lmin") == None else query_args.get("Lmin")        
        self.Lmax = 0 if query_args.get("Lmax") == None else query_args.get("Lmax")                        
        self.threads = self._query_args.get("T")
