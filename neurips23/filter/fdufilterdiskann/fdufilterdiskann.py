from __future__ import absolute_import
import os
import time
import numpy as np

# import diskannpy
import filterdiskann

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS, download_accelerated
from multiprocessing.pool import ThreadPool


def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]


class fdufilterdiskann(BaseFilterANN):
    def __init__(self, metric, index_params):
        self.name = "fdufilterdiskann"
        if index_params.get("R") == None:
            print("Error: missing parameter R")
            return
        self._index_params = index_params
        self._metric = metric

        self.R = index_params.get("R")
        self.L = index_params.get("L")
        self.nt = index_params.get("buildthreads", 1)
        

    def index_name(self):
        return f"R{self.R}_L{self.L}"

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "filter")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, "fdufilterdiskann")
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
        
    def translate_dtype(self, dtype:str):
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

        buildthreads = self._index_params.get("buildthreads", 1)
        self.nt = buildthreads
        self.meta_b = ds.get_dataset_metadata()
        self.meta_b.sort_indices() # 对每行的列排序
        index_dir = self.create_index_dir(ds)

        if hasattr(self, "index"):
            print("Index object exists already")
            return

        print(ds.get_dataset_fn())

        start = time.time()
        
        print(ds.ds_metadata_fn)
        
        print("building index")
        alpha = self._index_params.get("alpha", 1.2)
        filterdiskann.build(ds.get_dataset_fn(), index_dir + '/' + self.index_name(), os.path.join(ds.basedir, ds.ds_metadata_fn),
                            buildthreads, self.R, self.L, alpha)
        
        end = time.time()
        print("DiskANN index built in %.3f s" % (end - start))


        print('Loading index..')
        search_threads, search_L = self._index_params.get("T", 16), self._index_params.get("Ls", 20)
        print('search threads:', search_threads, 'search L:', search_L)
        self.index = filterdiskann.FilterDiskANN(filterdiskann.Metric.L2, index_dir + '/' + self.index_name(), ds.nb,
                                                 ds.d, search_threads, search_L)
        print('Index ready for search')

    def get_index_components(self, dataset):
        index_components = ['_pts_to_hash.txt', '_new_to_raw.txt', '_labels_to_medoids.txt', '_labels_to_hash.txt', '_label.bin', '_csr_offset.bin', '_csr_data.bin', '.data']
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

        search_threads, search_L = self._index_params.get("T", 16), self._index_params.get("Ls", 20)

        print('search threads:', search_threads, 'search L:', search_L)
        self.index = filterdiskann.FilterDiskANN(filterdiskann.Metric.L2, index_dir + '/' + self.index_name(), ds.nb,
                                                 ds.d, search_threads, search_L)
        print ("Load index success.")
        return True
        

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") == None else query_args.get("Ls")
        self.search_threads = self._query_args.get("T")

    def filtered_query(self, X, filter, k):
        print('running filtered query diskann')
        nq = X.shape[0]
        self.I = np.zeros((nq, k), dtype='uint32', order='C')  # result IDs
        # # meta_b = self.meta_b  # data_metadata
        meta_q = filter # query_metadata
        threshold_1 = self._query_args.get("threshold_1")
        threshold_2 = self._query_args.get("threshold_2")

        print("runing in ", self.search_threads, '    nq:', nq)

        self.index.search(X, meta_q.indptr, meta_q.indices, nq, k, self.Ls, self.search_threads, threshold_1, threshold_2, self.I)
            

    def get_results(self):
        return self.I

    def __str__(self):
        return f"diskann({self.index_name(), self._query_args})"

if __name__ == "__main__":
    print(1)
