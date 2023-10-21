import numpy as np
import os
import time
import wrapper as wp

from collections import defaultdict

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated

class ParlayIVF(BaseFilterANN):

    def __init__(self, metric, index_params):
        self._index_params = index_params
        self._metric = self.translate_dist_fn(metric)
        print(index_params)

        self._cluster_size = int(index_params['cluster_size'])
        self._cutoff = int(index_params['cutoff'])

        if 'T' in index_params:
            os.environ['PARLAY_NUM_THREADS'] = str(index_params['T'])

        self.name = f'parlayivf_{self._metric}_{self._cluster_size}_{self._cutoff}'

    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return 'Euclidian'
        elif metric == 'ip':
            return 'mips'
        else:
            raise Exception('Invalid metric')

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "filter")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'parlayivf')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return os.path.join(index_dir, self.index_name())
        
    def index_name(self):
        return f'parlayivf_{self._metric}_{self._cluster_size}_{self._cutoff}_{self._target_points}'

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        # if 'n_lists' in query_args:
        #     self._lists = query_args['n_lists']
        # else:
            # self._lists = 500
        # if 'cutoff' in query_args:
        #     self._cutoff = query_args['cutoff']
        # else:
        #     self._cutoff = 20_000
        if 'target_points' in query_args:
            self._target_points = query_args['target_points']
        else:
            self._target_points = 5000
        
    
    def fit(self, dataset):
        start = time.time()
        ds = DATASETS[dataset]()
        self.dtype = ds.dtype

        if hasattr(self, 'index'):
            print("Index already exists, skipping fit")
            return

        self.index = wp.init_squared_ivf_index(self._metric, self.dtype)
        print("Index initialized")
        self.index.fit_from_filename(ds.get_dataset_fn(), os.path.join(ds.basedir, ds.ds_metadata_fn), self._cutoff, self._cluster_size)
        # self.index.print_stats()
        print(f"Index fit in {time.time() - start} seconds")

    def load_index(self, dataset):
        """need to implement serialization, but build is currently plenty fast enough"""
        return False
    
    def filtered_query(self, X, filter, k):
        start = time.time()

        # it's possible the below construction takes as long as 10 seconds, which is probably too long
        # filters = [wp.QueryFilter(*filter[i, :].nonzero()[1]) for i in range(filter.shape[0])]

        rows, cols = filter.nonzero()
        filter_dict = defaultdict(list)

        for row, col in zip(rows, cols):
            filter_dict[row].append(col)

        # filters = [wp.QueryFilter(*filters[i]) for i in filters.keys()]
        filters = [None] * len(filter_dict.keys())
        for i in filter_dict.keys():
            filters[i] = wp.QueryFilter(*filter_dict[i])

        print(f"Filter construction took {time.time() - start} seconds")
        search_start = time.time()
        nq = X.shape[0]
        self.res, self.query_dists = self.index.batch_filter_search(X, filters, nq, k)
        print(f"Search took {time.time() - search_start} seconds")

    def get_results(self):
        # print(self.res.shape)
        # print(self.query_dists.shape)
        # print(self.res[:10, :10])
        # print(self.query_dists[:10, :10])
        return self.res
    
    def __str__(self):
        return f"ParlayIVF(metric={self._metric}, cluster_size={self._cluster_size}, cutoff={self._cutoff}, target_points={self._target_points})"