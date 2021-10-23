from __future__ import absolute_import
import numpy as np
import os
import time
import subprocess
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

import ngtpy

class NGT(BaseANN):
    def __init__(self, metric, params):
        self._params = params
        self._metric = metric
        self._quantization = params.get("q", 1024)
        self._quantization_sample = params.get("s", 100)
        self._blob = params.get("b", 10000)
        self._num_of_r_samples = params.get("rs", 1000)
        self._num_of_r_iterations = params.get("ri", 10)
        self._r_step = params.get("rx", 2)
        #self._ngt_root = "data/ngt"  # debug
        self._ngt_root = "ngt"
        self._ngt_index_root = self._ngt_root + "/indexes/"
        self._is_open = False

    def setIndexPath(self, dataset):
        path = f"data/indices/trackT2/algo.NGT:q{self._quantization}-s{self._quantization_sample}-b{self._blob}-rs{self._num_of_r_samples}-ri{self._num_of_r_iterations}"
        os.makedirs(path, exist_ok=True)
        self._index_path = os.path.join(path, DATASETS[dataset]().short_name())
        
    def fit(self, dataset):
        index_params = self._params
        ds = DATASETS[dataset]()
        if ds.d <= 128:
            pseudo_dimension = 128
            subvector_dimension = 2
        elif ds.d <= 256:
            pseudo_dimension = 256
            subvector_dimension = 4
        self.setIndexPath(dataset)
        print("NGT dataset:", dataset)
        print("NGT dataset str:", ds.__str__())
        print("NGT distance:", ds.distance())
        print("NGT dimension:", ds.d)
        print("NGT type:", ds.dtype)
        print("NGT nb:", ds.nb)
        print("NGT nb_M:", ds.nb_M)
        print("NGT dataset file name:", ds.get_dataset_fn())
        print("NGT quantization (q):", self._quantization)
        print("NGT quantization sample (s):", self._quantization_sample)
        print("NGT blob (b):", self._blob)
        print("NGT # of r samples (rs):", self._num_of_r_samples)
        print("NGT # of r iterations (rs):", self._num_of_r_iterations)
        print("NGT ngt root:", self._ngt_root)
        print("NGT index path:", self._index_path)
        print("NGT build.sh:", self._ngt_root + '/build.sh')
        args = ['/bin/bash', self._ngt_root + '/build.sh',
                #'--search',
                '--root=' + self._ngt_root, 
                '--object=' + ds.get_dataset_fn(),
                '--benchmark=' + self._index_path, '-d=' + str(pseudo_dimension),
                '-D=' + str(subvector_dimension),
                '-f', '-m=KMEANS_QUANTIZATION', '-n=' + str(ds.nb),
                '-q=' + str(self._quantization), '-E=' + str(self._quantization_sample),
                '-b=' + str(self._blob),
                '-r=' + str(self._num_of_r_samples), '-R=' + str(self._num_of_r_iterations),
                '-X=' + str(self._r_step)]
        print(args)
        subprocess.call(args)

        if not self._is_open:
            print("NGT: opening the index...")
            self._index = ngtpy.QuantizedBlobIndex(self._index_path)
            self._is_open = True

    def load_index(self, dataset):
        self.setIndexPath(dataset)

        if not os.path.exists(self._index_path + "/grp"):
            return False

        if not self._is_open:
            print("NGT: opening the index...")
            self._index = ngtpy.QuantizedBlobIndex(self._index_path)
            self._is_open = True

    def set_query_arguments(self, query_args):
        self._epsilon = query_args.get("epsilon", 0.1)
        self._edge_size = query_args.get("edge", 0)
        self._exploration_size = query_args.get("blob", 120)
        # only this part is different from t1
        self._exact_result_expansion = query_args.get("expansion", 2.0)
        #self._exact_result_expansion = 0.0
        self._index.set(epsilon=self._epsilon, edge_size=self._edge_size,
                        exploration_size=self._exploration_size,
                        exact_result_expansion=self._exact_result_expansion)
        print(f"NGT: epsilon={self._epsilon} edge={self._edge_size} blob={self._exploration_size}")

    def query(self, X, n):
        self._results = ngtpy.BatchResults()
        self._index.batchSearch(X, self._results, n)

    def range_query(self, X, radius):
        print("NGT: range_query")

    def get_results(self):
        return self._results.getIDs()

    def get_range_results(self):
        return self._results.getIndex(), self._results.getIndexedIDs(), self._results.getIndexedDistances()

    def __str__(self):
        return f"NGT-T2:q{self._quantization}-b{self._blob}-rs{self._num_of_r_samples}-ri{self._num_of_r_iterations}-e{self._epsilon:.3f}-b{self._exploration_size}-x{self._exact_result_expansion}"
