from __future__ import absolute_import
import numpy
import cupy

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS

import cuann
from cuann import libcuann
from cuann import ivfpq
from cuann import utils

mempool = cupy.cuda.MemoryPool(cupy.cuda.malloc_managed)
cupy.cuda.set_allocator(mempool.malloc)


class CuannsIvfpq(BaseANN):
    def __init__(self, metric, index_params):
        self._metric = metric
        self._index_params = index_params
        self._algo = ivfpq.CuannIvfPq()

        self._query_args = None
        self._dsi = None

    def __str__(self):
        if self._query_args is not None:
            name = '{}(refine_rate={},num_probes={})'.format(
                self.__class__.__name__,
                self._query_args['refine_rate'],
                self._query_args['num_probes']
            )
        else:
            name = self.__class__.__name__
        return name

    def track(self):
        return 'T3'

    def _index_file_name(self, dataset):
        return 'data/indices/t3/CuannsIvfpq/{}.cluster_{}.pq_{}.{}_bit'.format(
            dataset,
            self._index_params['num_clusters'],
            self._index_params['dim_pq'],
            self._index_params['bit_pq'])

    def load_index(self, dataset):
        self._dataset = dataset
        self._dsi = DATASETS[dataset]()

        # Original dataset is needed for refinement
        self._ds = utils.memmap_bin_file(self._dsi.get_dataset_fn(), self._dsi.dtype)

        index_fn = self._index_file_name(dataset)
        if self._algo.load_index(index_fn) is False:
            raise RuntimeError('Failed to load index ({})'.format(index_fn))

        assert(self._algo._index_params['numDataset'] <= self._dsi.nb)
        assert(self._algo._index_params['dimDataset'] == self._dsi.d)
        assert(self._algo._index_params['numClusters'] == self._index_params['num_clusters'])
        assert(self._algo._index_params['dimPq'] == self._index_params['dim_pq'])
        assert(self._algo._index_params['bitPq'] == self._index_params['bit_pq'])
        return True

    def set_query_arguments(self, query_args):
        print('# query_args: {}'.format(query_args))
        self._query_args = query_args
        num_probes = self._query_args['num_probes']
        gpu_topk = self._query_args['topk'] * self._query_args['refine_rate']
        batch_size = self._query_args['batch_size']
        self._algo.set_search_params(num_probes, gpu_topk, batch_size)
        mempool.free_all_blocks()

    def query(self, X, k):
        assert(X.shape[1] == self._algo._index_params['dimDataset'])
        assert(k == self._query_args['topk'])
        X = X.astype(self._dsi.dtype)
        I, D = self._algo.search(X)
        if self._query_args['refine_rate'] > 1:
            I, D = self._algo.refine(self._ds, X, cupy.asnumpy(I), k)
        self._res = (I, D)

    def get_results(self):
        I, D = self._res
        if isinstance(I, cupy.ndarray):
            return cupy.asnumpy(I)
        else:
            return I
