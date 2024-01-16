import pdb
import pickle
import numpy as np
import os
import diskannpy
import filter_searcher
from multiprocessing.pool import ThreadPool

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated

def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]


class Zilliz(BaseFilterANN):

    def __init__(self,  metric, index_params):
        self._index_params = index_params
        self._metric = metric
        print(index_params)
        
        self.R = index_params['R']
        self.L = index_params['L']
        self.threshold = index_params['threshold']
        self.threshold2 = index_params['threshold2']

    def index_name(self): 
        return f"R{self.R}_L{self.L}"
    
    def index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "filter")
        index_dir = os.path.join(index_dir, 'diskann3')
        index_dir = os.path.join(index_dir, dataset.short_name())
        index_dir = os.path.join(index_dir, self.index_name())
        return index_dir

    def is_existed(self, dataset, i):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "filter")
        index_dir = os.path.join(index_dir, 'diskann3')
        index_dir = os.path.join(index_dir, dataset.short_name())
        index_dir = os.path.join(index_dir, self.index_name())
        index_dir = os.path.join(index_dir, f'_{i}')
        return os.path.exists(index_dir) 
        
    def create_index_dir(self, dataset, i):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "filter")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'diskann3')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, f'_{i}')
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
        ds = DATASETS[dataset]()
        meta_b = ds.get_dataset_metadata()
        meta_b.sort_indices()
        meta_T = meta_b.transpose().tocsr()
        n, m = meta_b.shape
        
        def build(i, l):
            if self.is_existed(ds, i):
                return
            index_dir = self.create_index_dir(ds, i)
            diskannpy.build_memory_index(
                data = ds.get_dataset()[l],
                distance_metric = self.translate_dist_fn(ds.distance()),
                vector_dtype = self.translate_dtype(ds.dtype),
                index_directory = index_dir,
                index_prefix = self.index_name(),
                complexity=self.L,
                graph_degree=self.R,
                num_threads = 8,
                alpha=1.2,
                use_pq_build=False,
                num_pq_bytes=0, #irrelevant given use_pq_build=False
                use_opq=False
            )
            
        
        big_idx = []
        for i in range(m):
            ids = csr_get_row_indices(meta_T, i)
            x = len(ids)
            if x > self.threshold:
                build(i, ids)
            if x > self.threshold2:
                big_idx.append(i)
    
        for i in range(len(big_idx)):
            for j in range(i + 1, len(big_idx)):
                ids = filter_searcher.intersect_sorted(csr_get_row_indices(meta_T, big_idx[i]), csr_get_row_indices(meta_T, big_idx[j]))
                x = len(ids)
                if x > self.threshold2:
                    cur_id = big_idx[i] * m + big_idx[j] + m
                    build(cur_id, ids)
        del meta_b, meta_T 
        self.searcher = filter_searcher.Searcher()
        self.searcher.load(os.path.join(ds.basedir, ds.ds_metadata_fn), self.index_dir(ds), ds.get_dataset_fn(), self.R, self.L)

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        print("start load")
        ds = DATASETS[dataset]()
        if not os.path.exists(self.index_dir(ds)):
            return False
        self.searcher = filter_searcher.Searcher()
        self.searcher.load(os.path.join(ds.basedir, ds.ds_metadata_fn), self.index_dir(ds), ds.get_dataset_fn(), self.R, self.L)

        print("done load")
        return True

    def filtered_query(self, X, filter, k):
        ef = self.ef
        nq, d = X.shape
        self.I = self.searcher.search_batch(X, k, ef, filter.indptr, filter.indices).reshape(nq, k)

    def get_results(self):
        return self.I

    def set_query_arguments(self, query_args):
        self.ef = query_args['ef']
        return

    def __str__(self):
        return f'filter_searcher_{self.index_name()}_ef{self.ef}'
