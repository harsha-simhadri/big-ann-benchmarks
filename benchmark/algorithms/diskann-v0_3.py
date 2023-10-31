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
        self.name = "DiskANN-v0.3"
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
        self.PQ = 0 if index_params.get("PQ") == None else index_params.get("PQ")
        self.C = -1 if index_params.get("C") == None else index_params.get("C")
        self.cache_mechanism = 1 if index_params.get("CM") == None else index_params.get("CM")
        if self.C == 0:
            self.cache_mechanism = 0
        print(self.PQ)

    def track(self):
        return "T2"

    def index_name(self):
        if self.PQ == 0:
            return f"R{self.R}_L{self.L}_B{self.B}_M{self.M}"
        else:
            return f"R{self.R}_L{self.L}_B{self.B}_M{self.M}_PQ{self.PQ}"

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
        if self.PQ > 0:
            self.index.build(ds.get_dataset_fn(), self.index_path, self.R, self.L, self.B, self.M, buildthreads, self.PQ)
        else:
            self.index.build(ds.get_dataset_fn(), self.index_path, self.R, self.L, self.B, self.M, buildthreads)
        end = time.time()
        print("DiskANN index built in %.3f s" % (end - start))

        
        if self.C > 0:
            num_nodes_to_cache = self.C
        else:
            num_nodes_to_cache = int(ds.nb/1000) if ds.nb > 1000000 else int(ds.nb/100) 
        print(f"Loading index and caching {num_nodes_to_cache} nodes..")
        self.index.load_index(self.index_path, diskannpy.omp_get_max_threads(), num_nodes_to_cache, self.cache_mechanism)

    def get_index_components(self, dataset):
        index_components = [
                '_pq_pivots.bin', '_pq_pivots.bin_centroid.bin', '_pq_pivots.bin_chunk_offsets.bin',
                '_pq_pivots.bin_rearrangement_perm.bin',  '_sample_data.bin', '_sample_ids.bin',
                '_pq_compressed.bin', '_disk.index', '_disk.index_medoids.bin'
                ]
        ds = DATASETS[dataset]()
        if ds.distance() == "ip":
            index_components = index_components + [
                    '_disk.index_centroids.bin', '_disk.index_max_base_norm.bin', '_disk.index_medoids.bin'
                    ]
        if self.PQ > 0:
            index_components = index_components + [
                    '_disk.index_pq_pivots.bin', '_disk.index_pq_pivots.bin_centroid.bin',
                    '_disk.index_pq_pivots.bin_chunk_offsets.bin', '_disk.index_pq_pivots.bin_rearrangement_perm.bin'
                    ]
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

        if self.C > 0:
            num_nodes_to_cache = self.C
        else:
            num_nodes_to_cache = int(ds.nb/1000) if ds.nb > 1000000 else int(ds.nb/100) 
        if (self.index.load_index(index_path, diskannpy.omp_get_max_threads(), num_nodes_to_cache, self.cache_mechanism) == 0):
            print ("Load index success.")
            return True
        else:
            return False

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        [self.res, self.query_dists], self.stats = self.index.batch_search_numpy_input(X, dim, nq, k, self.Ls, self.BW, self.threads)
        self.stats["dist_comps"] = self.stats["mean_dist_comps"] * nq

    def range_query(self, X, radius):
        """
        Carry out a batch query for range search with
        radius.
        """
        nq, dim = np.shape(X)
        [self.rangeres_lim, [self.rangeres_ids, self.rangeres_dists]], self.stats = self.index.batch_range_search_numpy_input(
                X, dim, nq, radius, self.Lmin, self.Lmax, self.BW, self.threads)
        self.stats["dist_comps"] = self.stats["mean_dist_comps"] * nq
        
    def get_range_results(self):
        return (self.rangeres_lim, self.rangeres_dists, self.rangeres_ids)

    def get_additional(self):
        return self.stats

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") == None else query_args.get("Ls")        
        self.Lmin = 0 if query_args.get("Lmin") == None else query_args.get("Lmin")        
        self.Lmax = 0 if query_args.get("Lmax") == None else query_args.get("Lmax")                        
        self.BW = self._query_args.get("BW")
        self.threads = self._query_args.get("T")
