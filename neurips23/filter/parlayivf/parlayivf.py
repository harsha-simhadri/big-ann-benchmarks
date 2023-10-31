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
        self._max_iter = int(index_params['max_iter'])

        self._weight_classes = tuple(index_params['weight_classes'])
        self._build_params = tuple([wp.BuildParams(int(d['max_degree']), int(d['limit']), float(d['alpha'])) for d in index_params['build_params']]) # tuple of BuildParams objects
        self._max_degree = tuple([int(d['max_degree']) for d in index_params['build_params']]) 

        if 'bitvector_cutoff' in index_params:
            self._bitvector_cutoff = index_params['bitvector_cutoff']
        else:
            self._bitvector_cutoff = self._cutoff

        if 'T' in index_params:
            os.environ['PARLAY_NUM_THREADS'] = str(min(int(index_params['T']), os.cpu_count()))

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
        return os.path.join(index_dir, self.index_name())
        # return os.path.join(index_dir, self.index_name())

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
            self.index.set_target_points(self._target_points)
        else:
            self._target_points = 5000

        if 'tiny_cutoff' in query_args:
            self._tiny_cutoff = query_args['tiny_cutoff']
            self.index.set_tiny_cutoff(self._tiny_cutoff)
        else:
            self._tiny_cutoff = 1000

        if 'sq_target_points' in query_args:
            self._sq_target_points = query_args['sq_target_points']
            self.index.set_sq_target_points(self._sq_target_points)
        else:
            self._sq_target_points = self._target_points

        if 'beam_widths' in query_args:
            self._beam_widths = query_args['beam_widths']
        else:
            self._beam_widths = [100, 100, 100]

        if 'search_limits' in query_args:
            self._search_limits = query_args['search_limit']
        else:
            self._search_limits = list(self._weight_classes) + [3_000_000]
            
        self.set_beamsearch_params()

    def set_beamsearch_params(self, k=10):
        for i in range(3):
            self.index.set_query_params(wp.QueryParams(k, self._beam_widths[i], 1.35, self._search_limits[i], self._max_degree[i]), i)
        
    
    def fit(self, dataset):
        start = time.time()
        ds = DATASETS[dataset]()
        self.dtype = ds.dtype

        if hasattr(self, 'index'):
            print("Index already exists, skipping fit")
            return

        self.index = wp.init_squared_ivf_index(self._metric, self.dtype)

        self.index.set_max_iter(self._max_iter)
        self.index.set_bitvector_cutoff(self._bitvector_cutoff)

        for i, bp in enumerate(self._build_params):
            self.index.set_build_params(bp, i)

        print("Index initialized")
        self.index.fit_from_filename(ds.get_dataset_fn(), os.path.join(ds.basedir, ds.ds_metadata_fn), self._cutoff, self._cluster_size, str(self.create_index_dir(ds)), self._weight_classes, False)
        # self.index.print_stats()
        print(f"Index fit in {time.time() - start} seconds")

    def load_index(self, dataset):
        """this should in theory work"""
        start = time.time()
        ds = DATASETS[dataset]()
        self.dtype = ds.dtype

        if hasattr(self, 'index'):
            print("Index already exists, skipping fit")
            return

        self.index = wp.init_squared_ivf_index(self._metric, self.dtype)

        self.index.set_max_iter(self._max_iter)
        self.index.set_bitvector_cutoff(self._bitvector_cutoff)

        for i, bp in enumerate(self._build_params):
            self.index.set_build_params(bp, i)

        print("Index initialized")
        self.index.fit_from_filename(ds.get_dataset_fn(), os.path.join(ds.basedir, ds.ds_metadata_fn), self._cutoff, self._cluster_size, str(self.create_index_dir(ds)), self._weight_classes, True)
        # self.index.print_stats()
        print(f"Index loaded in {time.time() - start} seconds")
        return True
    
    def filtered_query(self, X, filter, k):
        start = time.time()

        if k != 10:
            self.set_beamsearch_params(k)

        # there's almost certainly a way to do this in less than 0.1s, which costs us ~200 QPS
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
        self.index.print_stats() # should be commented out for production
        self.index.reset()

    def get_results(self):
        # print(self.res.shape)
        # print(self.query_dists.shape)
        # print(self.res[:10, :10])
        # print(self.query_dists[:10, :10])
        return self.res
    
    def __str__(self):
        return f"ParlayIVF(metric={self._metric}, dtype={self.dtype}, T={os.environ['PARLAY_NUM_THREADS']}, cluster_size={self._cluster_size:,}, cutoff={self._cutoff:,}, target_points={self._target_points:,}, tiny_cutoff={self._tiny_cutoff:,}, max_iter={self._max_iter:,}, weight_classes={self._weight_classes}, max_degrees={self._max_degree}, beam_widths={self._beam_widths}, search_limits={self._search_limits})"
    
    def index_name(self):
        return f"parlayivf_{self._metric}_{self.dtype}"