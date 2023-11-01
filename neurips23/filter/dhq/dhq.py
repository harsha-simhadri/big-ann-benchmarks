import pdb
import pickle
import random

import numpy as np
import os

from multiprocessing.pool import ThreadPool
from threading import current_thread
from functools import partial
import struct
import faiss
import DHQ
from tqdm import tqdm, trange
from multiprocessing.pool import ThreadPool

from faiss.contrib.inspect_tools import get_invlist
from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
from math import log10, pow


def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]

def find_invlists(index):
    try:
        inverted_lists = index.invlists
    except:
        base_index = faiss.downcast_index(index.base_index)
        inverted_lists = base_index.invlists
    return inverted_lists



def metric_mapping(_metric: str):
    _metric_type = {"angular": "IP", "euclidean": "L2"}.get(_metric, None)
    if _metric_type is None:
        raise Exception(f"[DHQ] Not support metric type: {_metric}!!!")
    return _metric_type


def process_one_data(k, docs_per_word, xb):

    if not os.path.exists("data/base.fvecs_" + str(k) +"_doc"):
        with open("data/base.fvecs_" + str(k) +"_doc", "wb") as fp:
            docs = csr_get_row_indices(docs_per_word, k)
            for y in docs:
                d = struct.pack("I", int(y))
                fp.write(d)
    if not os.path.exists("data/base.fvecs_" + str(k)):
        with open("data/base.fvecs_" + str(k), "wb") as fp:
            docs = csr_get_row_indices(docs_per_word, k)
            for y in xb[docs]:
                d = struct.pack("I", y.size)
                fp.write(d)
                for x in y:
                    if type(x).__name__ == "float32":
                        a = struct.pack("B", int(x) % 255)
                        fp.write(a)
                    else:
                        a = struct.pack("B", x)
                        fp.write(a)


def process_data_all(xb):
    if not os.path.exists("data/base.fvecs_all" + "_doc"):
        with open("data/base.fvecs_all" + "_doc", "wb") as fp:
            for y in range(xb.shape[0]):
                d = struct.pack("I", int(y))
                fp.write(d)
    if not os.path.exists("data/base.fvecs_all"):
        with open("data/base.fvecs_all", "wb") as fp:
            for y in xb:
                d = struct.pack("I", y.size)
                fp.write(d)
                for x in y:
                    if type(x).__name__ == "float32":
                        a = struct.pack("B", int(x) % 255)
                        fp.write(a)
                    else:
                        a = struct.pack("B", x)
                        fp.write(a)
class DHQINDEX(BaseFilterANN):

    def __init__(self,  metric, index_params):
        self.build_label = None
        self._index_params = index_params
        self._metric = metric

        self.train_size = index_params.get('train_size', 2000000)
        self.indexkey = index_params.get("indexkey", "IVF1024,SQ8")
        self.nt = index_params.get("threads", 8)
        self.DHQ = None
        self.metric = metric_mapping(metric)
        self.R = index_params['R']
        self.L = index_params['L']
        self.level = index_params['level']
        self.name = 'DHQ(%s)' % index_params
        self.path = f'dim_{192}_R_{self.R}_L_{self.L}.DHQ'
        self.nt = index_params.get("threads", 8)
        self.skip_label_list_less = []
        self.skip_label_list_large = []
        self.ndoc_per_word = None


    def fit(self, dataset):
        faiss.omp_set_num_threads(self.nt)
        ds = DATASETS[dataset]()
        xb = ds.get_dataset()
        if not os.path.exists(self.index_name(dataset)):
            faiss_index = faiss.index_factory(ds.d, self.indexkey)
            print("faiss train")
            print('train_size', self.train_size)
            if self.train_size is not None:
                x_train = xb[:self.train_size]
            else:
                x_train = xb
            faiss_index.train(x_train)
            bs = 1024
            print("faiss add")
            for i0 in range(0, ds.nb, bs):
                faiss_index.add(xb[i0: i0 + bs])
            self.faiss_index = faiss_index
            faiss.write_index(faiss_index, self.index_name(dataset))
        else:
            self.faiss_index = faiss.read_index(self.index_name(dataset))
        self.nb = ds.nb
        self.xb = xb
        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.faiss_index)

        build_label_str = ""
        if ds.search_type() == "knn_filtered":
            meta_b = ds.get_dataset_metadata()
            meta_b.sort_indices()
            self.docs_per_word = meta_b.T.tocsr()
            self.docs_per_word.sort_indices()
            self.ndoc_per_word = self.docs_per_word.indptr[1:] - self.docs_per_word.indptr[:-1]
            self.freq_per_word = self.ndoc_per_word / self.nb
            del meta_b

            print('begin align')
            inverted_lists = find_invlists(self.faiss_index)
            align_id_map = dict()
            align_pos = dict()
            for i in range(inverted_lists.nlist):
                list_ids, _ = get_invlist(inverted_lists, i)
                for pos, id in enumerate(list_ids):
                    # print('list: ', i, "id: ", id, "pos: ",pos)
                    align_id_map[id] = i
                    align_pos[id] = pos

            print('done align')

            #GRAPH

            one_freq_sort_index = sorted(range(len(self.freq_per_word)), key=lambda k: self.freq_per_word[k], reverse=True)

            build_label = []
            for k in one_freq_sort_index:
                if self.ndoc_per_word[k] > 1000000:
                    build_label_str = build_label_str + str(k) + ","
                    build_label.append(k)

            self.build_label = set(build_label)

            print("Data Cut Begin")
            process_data_all(xb)
            for k in build_label:
                process_one_data(k, self.docs_per_word, xb)
            print("Data Cut Done")
            os.system("ls -ll")
            if not os.path.exists("data/label_base.txt"):
                with open("data/label_base.txt", "w", encoding='utf-8') as f:
                    meta_b = ds.get_dataset_metadata()
                    for row in range(ds.nb):
                        list = csr_get_row_indices(meta_b, row)
                        row_str = ','.join(str(i) for i in list)
                        if len(list) == 0:
                            row_str = str(-1)
                        f.write(row_str)
                        if row < (ds.nb - 1):
                            f.write("\n")
                    del meta_b

            print("label_base Done")
            print('graph begin')
            dim = xb.shape[1]
            self.DHQ = DHQ.FilterIndex("HNSW", dim=dim,
                                                  metric=self.metric, input_data_path="data/base.fvecs",
                                                  label_data_path="data/label_base.txt", final_index_path_prefix=self.path,
                                                  level=self.level, R=self.R, L=self.L)

            indices = np.array(self.docs_per_word.indices)
            indptr = self.docs_per_word.indptr

            self.align_indices, self.align_num, self.align_id, self.align_id_num, self.align_po_id = self.DHQ.filter_wise(
                align_id_map, align_pos, indices, indptr, self.docs_per_word.shape[0])

            self.align_indices = np.array(self.align_indices)
            self.align_id = np.array(self.align_id, dtype=np.int16)
            self.align_num = np.array(self.align_num, dtype=np.int32)
            self.align_id_num = np.array(self.align_id_num, dtype=np.int32)
            self.align_po_id = np.array(self.align_po_id, dtype=np.int32)

            self.max_range = -1
            for i in range(len(self.align_num) - 1):
                delta = self.align_num[i + 1] - self.align_num[i]
                if delta > self.max_range:
                    self.max_range = delta

            self.DHQ.filter_build(build_label_str[:len(build_label_str) - 1], 0)
            print('graph end')

    def index_name(self, name):
        return f"data/{name}.{self.path}.DHQ"

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
        try:
            self.faiss_index.k_factor = 0.1
        except Exception as e:
            print(e)
            pass
        for i0 in range(0, nq, bs):
            _, self.I[i0:i0+bs] = self.faiss_index.search(X[i0:i0+bs], k)



    def filtered_query(self, X, filter, k):

        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int32')
        meta_q = filter
        selector_by_thread = dict()
        def process_one_row(q):
            faiss.omp_set_num_threads(1)
            thread = current_thread()

            qwords = csr_get_row_indices(meta_q, q)
            w1 = qwords[0]
            if qwords.size == 1 and w1 in self.build_label:
                #tmp = self.DHQ.search(X[q: q + 1], k, 0, str(w1)).ravel()
                tmp = self.DHQ.search_with_random(X[q: q + 1], k, 0, str(w1), self.random).ravel()
                self.I[q] = tmp
            else:
                if qwords.size == 2:
                    w2 = qwords[1]
                else:
                    w2 = -1
                if thread not in selector_by_thread:
                    sp = faiss.swig_ptr
                    sel = faiss.IDSelectorFilterWise(sp(self.align_po_id), sp(self.align_num),
                                                                          sp(self.align_id), sp(self.align_id_num),
                                                                          int(self.max_range))
                    selector_by_thread[thread] = sel
                else:
                    sel = selector_by_thread.get(thread)
                sel.set_words(int(w1), int(w2))
                params = faiss.SearchParametersIVF(sel=sel, nprobe=self.nprobe, max_codes=self.num, selector_probe_limit=self.align_prob)
                _, Ii = self.faiss_index.search(X[q:q+1], k, params=params)
                Ii = Ii.ravel()
                self.I[q] = Ii

        if self.nt <= 1:
            for q in range(nq):
                process_one_row(q)
        else:
            faiss.omp_set_num_threads(self.nt)
            pool = ThreadPool(self.nt)
            list(pool.map(process_one_row, range(nq)))

    def get_results(self):
        return self.I

    def set_query_arguments(self, query_args):
        #faiss.cvar.indexIVF_stats.reset()
        #faiss.cvar.IDSelectorMy_Stats.reset()
        self.qas = query_args
        if "ef" in query_args:
            self.ef = query_args['ef']
            self.DHQ.set_query_ef(self.ef)
        if "nprobe" in query_args:
            self.nprobe = query_args['nprobe']
            self.ps.set_index_parameters(self.faiss_index, f"nprobe={query_args['nprobe']}")
            self.align_prob = query_args['nprobe']
            self.ps.set_index_parameters(self.faiss_index, f"selector_probe_limit={query_args['nprobe']}")
        else:
            self.nprobe = 1
            self.align_prob = 0
        if "random" in query_args:
            self.random = query_args['random']
        else:
            self.random = 50
        if "num" in query_args:
            self.num = query_args["num"]
            self.ps.set_index_parameters(self.faiss_index, f"max_codes={query_args['num']}")
        else:
            self.num = -1



    def __str__(self):
        return f'DHQ({self.name, self.qas})'
