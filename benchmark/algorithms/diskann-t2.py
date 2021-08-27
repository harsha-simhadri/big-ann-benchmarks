from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import diskannpy

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

class Diskann(BaseANN):
    def __init__(self, metric, index_params):
        if (index_params.get("R")==None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L")==None):
            print("Error: missing parameter L")
            return
        if (index_params.get("B")==None):
            print("Error: missing parameter B")
            return
        if(index_params.get("M")==None):
            print("Error: missing parameter M")
            return

        self._index_params = index_params
        self._metric = metric

        self.R = index_params.get("R")
        self.L = index_params.get("L")
        self.B = index_params.get("B")
        self.M = index_params.get("M")

    def index_name(self):
        return f"R{self.R}_L{self.L}_B{self.B}_M{self.M}"

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, "T2")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.__str__())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        """

        ds = DATASETS[dataset]()
        d = ds.d

        buildthreads = self._index_params.get("buildthreads", -1)
        if buildthreads == -1:
            buildthreads = diskannpy.omp_get_max_threads()

        print("Set build-time number of threads:", buildthreads)
        diskannpy.omp_set_num_threads(buildthreads)

        index_dir = self.create_index_dir(ds)
        self.index_path = os.path.join(index_dir, self.index_name())

        if ds.distance() == "euclidean":
            metric = diskannpy.L2
        elif ds.distance() == "ip":
            metric = diskannpy.INNER_PRODUCT
        else:
            print("Unsuported distance function.")
            return False
        
        
        if not hasattr(self, 'index'):
            if ds.dtype == "float32":
                self.index = diskannpy.DiskANNFloatIndex(metric)
            elif ds.dtype == "int8":
                self.index = diskannpy.DiskANNInt8Index(metric)
            elif ds.dtype == "uint8":
                self.index = diskannpy.DiskANNUInt8Index(metric)
            else:
                print ("Unsupported data type.")
                return False

        start = time.time()
        self.index.build(ds.get_dataset_fn(), self.index_path, self.R, self.L, self.B, self.M, buildthreads)
        end = time.time()
        print("DiskANN index built in %.3f s" % (end - start))

        
        num_nodes_to_cache = int(ds.nb/1000) if ds.nb > 1000000 else int(ds.nb/100) 
        print(f"Loading index and caching {num_nodes_to_cache} nodes..")
        self.index.load_index(self.index_path, diskannpy.omp_get_max_threads(), num_nodes_to_cache)


    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        ds = DATASETS[dataset]()
        if ds.distance() == "euclidean":
            metric = diskannpy.L2
        elif ds.distance() == "ip":
            metric = diskannpy.INNER_PRODUCT
        else:
            print("Unsuported distance function.")
            return False
        
        if ds.dtype == "float32":
            self.index = diskannpy.DiskANNFloatIndex(metric)
        elif ds.dtype == "int8":
            self.index = diskannpy.DiskANNInt8Index(metric)
        elif ds.dtype == "uint8":
            self.index = diskannpy.DiskANNUInt8Index(metric)
        else:
            print ("Unsupported data type.")
            return False

        index_dir = self.create_index_dir(ds)        
        if not (os.path.exists(index_dir)) and 'url' not in self._index_params:
            return False

        index_path = os.path.join(index_dir, self.index_name())
        index_components = [
            'pq_pivots.bin', 'pq_pivots.bin_centroid.bin', 'pq_pivots.bin_chunk_offsets.bin',
            'pq_pivots.bin_rearrangement_perm.bin',  'sample_data.bin', 'sample_ids.bin',
            'pq_compressed.bin', 'disk.index'
            ]
        for component in index_components:
            index_file = index_path + '_' + component
            if not (os.path.exists(index_file)):
                if 'url' in self._index_params:
                    index_file_source = self._index_params['url'] + '/' + self.index_name() + '_' + component
                    print(f"Downloading index in background. This can take a while.")
                    download_accelerated(index_file_source, index_file, quiet=True)
                else:
                    return False

        print("Loading index")

        num_nodes_to_cache = int(ds.nb/1000) if ds.nb > 1000000 else int(ds.nb/100) 
        if (self.index.load_index(index_path, diskannpy.omp_get_max_threads(), num_nodes_to_cache) == 0):
            print ("Load index success.")
            return True
        else:
            return False

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        self.res, self.query_dists = self.index.batch_search_numpy_input(X, dim, nq, k, self.Ls, self.BW, self.threads)

    def range_query(self, X, radius):
        """
        Carry out a batch query for range search with
        radius.
        """
        pass

    def get_additional(self):
        """
        Allows to retrieve additional results.
        """
        return {}

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = self._query_args.get("Ls")
        self.BW = self._query_args.get("BW")
        self.threads = self._query_args.get("T")


    def __str__(self):
        return "DiskANN"
