from __future__ import absolute_import
#import sys
#sys.path.append("install/lib-faiss")  # noqa
import numpy
import sklearn.preprocessing
import ctypes
import faiss
import os
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS


class Faiss(BaseANN):
    def query(self, X, n):
        if self._metric == 'angular':
            X /= numpy.linalg.norm(X)
        self.res = self.index.search(X.astype(numpy.float32), n)

    def get_results(self):
        D, I = self.res
        return I
#        res = []
#        for i in range(len(D)):
#            r = []
#            for l, d in zip(L[i], D[i]):
#                if l != -1:
#                    r.append(l)
#            res.append(r)
#        return res


class FaissIVF(Faiss):
    def __init__(self, metric, n_list):
        self._n_list = n_list
        self._metric = metric

    def index_name(self, name):
        return f"data/ivf_{name}_{self._n_list}_{self._metric}"

    def fit(self, dataset):
        X = DATASETS[dataset].get_dataset() # assumes it fits into memory

        if self._metric == 'angular':
            X = sklearn.preprocessing.normalize(X, axis=1, norm='l2')

        if X.dtype != numpy.float32:
            X = X.astype(numpy.float32)

        self.quantizer = faiss.IndexFlatL2(X.shape[1])
        index = faiss.IndexIVFFlat(
            self.quantizer, X.shape[1], self._n_list, faiss.METRIC_L2)
        index.train(X)
        index.add(X)
        faiss.write_index(index, self.index_name(dataset))
        self.index = index

    def load_index(self, dataset):
        if not os.path.exists(self.index_name(dataset)):
            return False

        self.index = faiss.read_index(self.index_name(dataset))
        return True

    def set_query_arguments(self, n_probe):
        faiss.cvar.indexIVF_stats.reset()
        self._n_probe = n_probe
        self.index.nprobe = self._n_probe

    def get_additional(self):
        return {"dist_comps": faiss.cvar.indexIVF_stats.ndis +      # noqa
                faiss.cvar.indexIVF_stats.nq * self._n_list}

    def __str__(self):
        return 'FaissIVF(n_list=%d, n_probe=%d)' % (self._n_list,
                                                    self._n_probe)
