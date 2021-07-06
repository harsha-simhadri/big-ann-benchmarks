from __future__ import absolute_import
#import sys
#sys.path.append("install/lib-faiss")  # noqa
import numpy
import sklearn.preprocessing
import ctypes
import faiss
import os
import subprocess
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS
from benchmark.sensors.power_capture import power_capture

class FaissGPU(BaseANN):
    def query(self, X, n):
        if self._metric == 'angular':
            X /= numpy.linalg.norm(X)
        if not power_capture.enabled():
            print("query size", X.size, X.shape) 
        self.res = self.gindex.search(X.astype(numpy.float32, copy=False), n)
        #GW self.res = self.gindex.search(X.view(numpy.float32), n)

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


class FaissIVFGPU(FaissGPU):
    def __init__(self, metric, n_list):
        self._n_list = n_list
        self._metric = metric
        self.index = None
        self.gindex = None
        self.quantizer = None
        self.res = None
        self.resource = None

    def done(self):
        if self.gindex:
            self.gindex.reset() # release GPU and memory?

    def index_name(self, name):
        return f"data/ivf_{name}_{self._n_list}_{self._metric}"

    def fit(self, dataset):
        X = DATASETS[dataset].get_dataset() 

        if self._metric == 'angular':
            X = sklearn.preprocessing.normalize(X, axis=1, norm='l2')

        if X.dtype != numpy.float32:
            raise Exception("Must be float32 mmap type")

        self.quantizer = faiss.IndexFlatL2(X.shape[1])
        self.index = faiss.IndexIVFFlat(
            self.quantizer, X.shape[1], self._n_list, faiss.METRIC_L2)

        if faiss.get_num_gpus():
            print('Running on %d GPUs' % faiss.get_num_gpus())
            self.resource = faiss.StandardGpuResources()
            self.resource.noTempMemory()
        else:
            raise Exception("GPUs not available.")

        self.index.train(X)
        self.index.add(X)
        faiss.write_index(self.index, self.index_name(dataset))
        self.gindex = faiss.index_cpu_to_gpu(self.resource, 0, self.index)

    def load_index(self, dataset):
        if not os.path.exists(self.index_name(dataset)):
            return False

        self.index = faiss.read_index(self.index_name(dataset))

        if faiss.get_num_gpus():
            print('Running on %d GPUs' % faiss.get_num_gpus())
            self.resource = faiss.StandardGpuResources()
            self.resource.noTempMemory()
        else:
            raise Exception("GPUs not available.")
            
        self.gindex = faiss.index_cpu_to_gpu(self.resource, 0, self.index)

        return True


    def set_query_arguments(self, n_probe):
        faiss.cvar.indexIVF_stats.reset()
        self._n_probe = n_probe
        self.index.nprobe = self._n_probe 
        self.gindex.nprobe = self._n_probe

    def get_additional(self):
        return {"dist_comps": faiss.cvar.indexIVF_stats.ndis +      # noqa
                faiss.cvar.indexIVF_stats.nq * self._n_list}

    def __str__(self):
        return 'FaissIVFGPU(n_list=%d, n_probe=%d)' % (self._n_list,
                                                    self._n_probe)
