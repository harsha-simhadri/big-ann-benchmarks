from __future__ import absolute_import
import numpy
import cupy

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS

import cuann
from cuann import libcuann
from cuann import ivfpq

mempool = cupy.cuda.MemoryPool(cupy.cuda.malloc_managed)
cupy.cuda.set_allocator(mempool.malloc)


def memmap_bin_file(bin_file, dtype, shape=None):
    if bin_file is None:
        return None
    a = numpy.memmap(bin_file, dtype='uint32', shape=(2,))
    if shape is None:
        shape = (a[0], a[1])
    elif len(shape) != 2 or shape[0] > a[0] or shape[1] != a[1]:
        raise RuntimeError('The specified shape is invalid (shape: {})'.format(shape))
    # print('# {}: shape: {}, dtype: {}'.format(bin_file, shape, dtype))
    return numpy.memmap(bin_file, dtype=dtype, offset=8, shape=shape)


class CuannsIvfpq(BaseANN):
    def __init__(self, metric, index_params):
        self._metric = metric
        self._index_params = index_params
        self._algo = ivfpq.CuannIvfPq()

        self._query_args = None
        self._dataset = None

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

    def _index_file_name(self, dataset):
        return 'data/indices/t3/CuannsIvfpq/{}.cluster_{}.pq_{}.{}_bit'.format(
            dataset,
            self._index_params['num_clusters'],
            self._index_params['dim_pq'],
            self._index_params['bit_pq'])

    def _setup_dataset(self, dataset):
        if self._dataset is None:
            self._dataset = dataset
            self._dsi = DATASETS[dataset]()
            self._ds = memmap_bin_file(
                self._dsi.get_dataset_fn(), self._dsi.dtype,
                (self._dsi.nb, self._dsi.d))
            print('# self._ds.shape: {}'.format(self._ds.shape))

    def _setup_trainset(self, rate=10):
        # Create trainset by picking-up vectors randomly from dataset
        num_ts = self._ds.shape[0] // rate
        indexes = numpy.arange(self._ds.shape[0])
        numpy.random.shuffle(indexes)
        self._ts = self._ds[numpy.sort(indexes[:num_ts])]
        print('# self._ts.shape: {}'.format(self._ts.shape))

    def track(self):
        return 'T3'

    def load_index(self, dataset):
        self._setup_dataset(dataset)

        index_fn = self._index_file_name(dataset)
        if self._algo.load_index(index_fn) is False:
            print('# Failed to load index ({})'.format(index_fn))
            return False

        assert(self._algo._index_params['numDataset'] <= self._dsi.nb)
        assert(self._algo._index_params['dimDataset'] == self._dsi.d)
        assert(self._algo._index_params['numClusters'] == self._index_params['num_clusters'])
        assert(self._algo._index_params['dimPq'] == self._index_params['dim_pq'])
        assert(self._algo._index_params['bitPq'] == self._index_params['bit_pq'])
        return True

    def fit(self, dataset):
        self._setup_dataset(dataset)
        self._setup_trainset()

        _distance = self._dsi.distance()
        if _distance is "euclidean":
            similarity=libcuann.CUANN_SIMILARITY_L2
        elif _distance is "ip":
            similarity=libcuann.CUANN_SIMILARITY_INNER
        else:
            raise RuntimeError('Unsupported distance ({})'.format(_distance))

        index_fn = self._index_file_name(dataset)
        # print('# index_fn: {}'.format(index_fn))
        self._algo.build_index(index_fn, self._ds, self._ts,
                               self._index_params['num_clusters'],
                               self._index_params['dim_pq'],
                               self._index_params['bit_pq'],
                               similarity=similarity,
                               randomRotation=1)

    def set_query_arguments(self, query_args):
        print('# query_args: {}'.format(query_args))
        self._query_args = query_args
        num_probes = self._query_args['num_probes']
        gpu_topk = int(self._query_args['topk'] * self._query_args['refine_rate'])
        gpu_topk = max(gpu_topk, self._query_args['topk'])
        max_batch_size = self._query_args['max_batch_size']
        self._algo.set_search_params(num_probes, gpu_topk, max_batch_size)
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
