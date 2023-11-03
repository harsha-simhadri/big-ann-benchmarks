
import numpy as np
import os
import faiss
from multiprocessing.pool import ThreadPool
import psutil
import os
import copy
from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
import bow_id_selector
import bow_id_selector as bis

class hwtl_sdu_anns_filter(BaseFilterANN):

    def __init__(self, metric, method_param):
        self.meta_b = None
        self.name = 'gffc'
        self.dir = 'gffc_indices'
        self.path = f'gffc_indices.gffc'
        self.nt = method_param.get("threads", 16)

    def fit(self, dataset):
        res = os.popen('cp bow_id_selector.py results')
        res = os.popen('cp _bow_id_selector.so results')
        global list
        print(u'in fit：%.4f GB' % (psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024 / 1024))
        ds = DATASETS[dataset]()
        xb = ds.get_dataset()
        meta_b = ds.get_dataset_metadata()
        self.meta_b = meta_b
        self.xb = xb
        if ds.search_type() == "knn_filtered":

            print("preparing DataSet")

            rows = []
            print(xb.shape)
            sp = faiss.swig_ptr
            docs_per_word = meta_b.T.tocsr()
            self.docs_per_word = docs_per_word
            n_tags = len(docs_per_word.indptr) - 1
            print(xb.dtype)
            print(len(self.meta_b.indptr), len(self.meta_b.indices), len(self.docs_per_word.indptr), len(self.docs_per_word.indices), (self.xb).shape)
            if self.xb.dtype != 'uint8':
                self.xb = self.xb.astype('uint8')
            self.gff = bow_id_selector.GFF(xb.shape[0], xb.shape[1], n_tags, sp(self.meta_b.indptr), sp(self.meta_b.indices), sp(self.docs_per_word.indptr), sp(self.docs_per_word.indices), sp(self.xb))
            self.gff.set_parallel(self.nt)
            self.gff.build()

    def index_name(self, name):
        return f"data/{name}.{self.path}.gffc"

    def binarysig_name(self, name):
        return f"data/{name}.{self.path}.binarysig"

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """

        return False

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
        raise NotImplementedError()

    def query(self, X, k):
        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int32')
        bs = 1024
        raise NotImplementedError()
        # for i0 in range(0, nq, bs):
        #     _, self.I[i0:i0 + bs] = self.index.search(X[i0:i0 + bs], k)

    def filtered_query(self, X, filter, k):
        print('running filtered query')
        sp = faiss.swig_ptr
        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int64')
        meta_q = filter
        qw = -np.ones(nq * 2, dtype='int32')
        qD = np.empty(nq * k, dtype='float32')
        for i in range(nq) :
            qw[i * 2] = meta_q.indices[meta_q.indptr[i]]
            if meta_q.indptr[i] == meta_q.indptr[i + 1] - 2 :
                qw[i * 2 + 1] = meta_q.indices[meta_q.indptr[i] + 1]
        self.gff.set_parallel(self.nt)
        if X.dtype != 'uint8':
                X = X.astype('uint8')
        self.gff.search(nq, sp(X), k, sp(qw), sp(qD), sp(self.I), float(self.nprobe), float(self.expansion), int(self.threshold))

    def get_results(self):
        return self.I

    def set_query_arguments(self, query_args):
        faiss.cvar.indexIVF_stats.reset()
        print(query_args)
        if "nprobe" in query_args:
            self.nprobe = query_args['nprobe']
            self.expansion = query_args['expansion']
            self.threshold = query_args['threshold']

    def __str__(self):
        return f'HWTL_SDU-ANNS-filter({self.name}, {self.nprobe}, {self.expansion}, {self.threshold})'



