import os
import time
import numpy as np
import psutil
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

import bbannpy


class BbANN(BaseANN):
    def __init__(self, metric, index_params):
        self.name = "BBANN"
        self.metric = metric
        self.index_params = index_params
        self.identifier = index_params.get("identifier")
        self.para = bbannpy.BBAnnParameters()
        print("init BbAnn with the following parameters")
        for key in index_params:
            print(key, index_params[key])
            if hasattr(self.para, key):
                setattr(self.para, key, index_params[key])

    def set_query_arguments(self, query_args):
        print("query BbAnn with the following parameters")
        for key in query_args:
            print(key, query_args[key])
            if hasattr(self.para, key):
                setattr(self.para, key, query_args[key])
        pass

    def done(self):
        pass

    def track(self):
        return "T2"

    def index_name(self):
        """
        File name for the index.
        """
        return f"{self.identifier}_index"

    def create_index_dir(self, dataset):
        """
        Return a folder name, in which we would store the index.
        """
        print("trying to create index dir:", self.index_params)
        if "overrideIndexPath" in self.index_params:
            print("Override index path:", self.index_params["overrideIndexPath"])
            return self.index_params["overrideIndexPath"]
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
        print(index_dir)
        return index_dir

    def get_index_dir(self, dataset):
        if "overrideIndexPath" in self.index_params:
            print("Override index path:", self.index_params["overrideIndexPath"])
            return self.index_params["overrideIndexPath"]
        index_dir = os.path.join(os.getcwd(), "data", "indices")
        index_dir = os.path.join(index_dir, "T2")
        index_dir = os.path.join(index_dir, self.__str__())
        index_dir = os.path.join(index_dir, dataset.short_name())
        index_dir = os.path.join(index_dir, self.index_name())
        return index_dir

    def get_index_components(self, dataset):
        index_components = [
            'bucket-centroids.bin', 'hnsw-index.bin', 'cluster-combine_ids.bin'
        ]

        K1 = self.index_params.get("K1")
        for i in range(K1):
            raw_data = 'cluster-' + str(i) + '-global_ids.bin'
            global_ids = 'cluster-' + str(i) + '-raw_data.bin'
            index_components = index_components + [raw_data, global_ids]

        ds = DATASETS[dataset]()
        if 'vector_use_sq' in self.index_params and self.index_params['vector_use_sq']:
            index_components = index_components + ['meta']

        if 'use_hnsw_sq' in self.index_params and self.index_params['use_hnsw_sq']:
            index_components = index_components + ['hnsw-index.bin.codes']

        return index_components

    def index_files_to_store(self, dataset):
        """
        Specify a triplet with the local directory path of index files,
        the common prefix name of index component(s) and a list of
        index components that need to be uploaded to (after build)
        or downloaded from (for search) cloud storage.
        For local directory path under docker environment, please use
        a directory under
        data/indices/track(T1 or T2)/algo.__str__()/DATASETS[dataset]().short_name()
        """

        return [self.create_index_dir(DATASETS[dataset]()) # local_dir
                , ""                                       # index_prefix
                , self.get_index_components(dataset)       # components
                ]

    def set_index_type(self, ds_distance, ds_dtype):
        if ds_distance == "euclidean":
            self.para.metric = bbannpy.L2
        elif ds_distance == "ip":
            self.para.metric = bbannpy.INNER_PRODUCT
        else:
            print("Unsuported distance function.")
            return False

        if not hasattr(self, 'index'):
            if ds_dtype == "float32":
                self.index = bbannpy.FloatIndex(self.para.metric)
            elif ds_dtype == "int8":
                self.index = bbannpy.Int8Index(self.para.metric)
            elif ds_dtype == "uint8":
                self.index = bbannpy.UInt8Index(self.para.metric)
            else:
                print("Unsupported data type.")
                return False
        return True

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        Assumes that after fitting index is loaded in memory.
        """
        ds = DATASETS[dataset]()
        d = ds.d
        index_dir = self.create_index_dir(ds)
        if not self.set_index_type(ds.distance(), ds.dtype):
            return False

        self.para.dataFilePath = ds.get_dataset_fn()
        self.para.indexPrefixPath = index_dir+"/"

        start = time.time()
        self.index.build(self.para)
        end = time.time()
        print("bbAnn index built in %.3f s" % (end - start))
        print(f"Loading index from {self.para.indexPrefixPath}")
        self.index.load_index(self.para.indexPrefixPath, self.para)

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        ds = DATASETS[dataset]()
        index_dir = self.get_index_dir(ds)
        if not (os.path.exists(index_dir)) and 'url' not in self.index_params:
            return False
        if not self.set_index_type(ds.distance(), ds.dtype):
            return False
        self.para.indexPrefixPath = index_dir + "/"

        index_components = self.get_index_components(dataset)
        for component in index_components:
            index_file = self.para.indexPrefixPath + component
            if not (os.path.exists(index_file)):
                if 'url' in self.index_params:
                    index_file_source = self.index_params['url'] + '/' + component
                    print(f"Downloading index in background. This can take a while.")
                    download_accelerated(index_file_source, index_file, quiet=True)
                else:
                    return False

        print(f"Loading index from {self.para.indexPrefixPath}")
        self.index.load_index(self.para.indexPrefixPath, self.para)
        return True

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq, dim = (np.shape(X))
        self.res, self.query_dists = self.index.batch_search(
            X, dim, nq, k, self.para)
        # print(self.res)

    def range_query(self, X, radius):
        """
        Carry out a batch query for range search with
        radius.
        """
        nq, dim = (np.shape(X))
        # print(f"Query index with para {self.para}")
        self.rangeres_lim, (self.rangeres_ids, self.rangeres_dists) = self.index.range_search(
            X, dim, nq, radius, self.para)

    def get_results(self):
        """
        Helper method to convert query results of k-NN search.
        If there are nq queries, returns a (nq, k) array of integers
        representing the indices of the k-NN for each query.
        """
        return self.res

    def get_range_results(self):
        """
        Helper method to convert query results of range search.
        If there are nq queries, returns a triple lims, I, D.
        lims is a (nq) array, such that

            I[lims[q]:lims[q + 1]] in int

        are the indiices of the indices of the range results of query q, and

            D[lims[q]:lims[q + 1]] in float

        are the distances. 
        --------------------------
        NEED TO CHECK THE ORDER of I and D in plot.py/ utils.py.
        
        --------------------------

        """
        return (self.rangeres_lim, self.rangeres_dists, self.rangeres_ids)

    def get_additional(self):
        """
        Allows to retrieve additional results.
        """
        return {}

    def __str__(self):
        return self.name

    def get_memory_usage(self):
        """Return the current memory usage of this algorithm instance
        (in kilobytes), or None if this information is not available."""
        # return in kB for backwards compatibility
        return psutil.Process().memory_info().rss / 1024
