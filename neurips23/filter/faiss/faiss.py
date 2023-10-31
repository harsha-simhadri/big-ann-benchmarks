import pdb
import pickle
import numpy as np
import os

from multiprocessing.pool import ThreadPool

import faiss

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated

import bow_id_selector

def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]

def make_bow_id_selector(mat, id_mask=0):
    sp = faiss.swig_ptr
    if id_mask == 0:
        return bow_id_selector.IDSelectorBOW(mat.shape[0], sp(mat.indptr), sp(mat.indices))
    else:
        return bow_id_selector.IDSelectorBOWBin(
            mat.shape[0], sp(mat.indptr), sp(mat.indices), id_mask
        )

def set_invlist_ids(invlists, l, ids):
    n, = ids.shape
    ids = np.ascontiguousarray(ids, dtype='int64')
    assert invlists.list_size(l) == n
    faiss.memcpy(
        invlists.get_ids(l),
        faiss.swig_ptr(ids), n * 8
    )



def csr_to_bitcodes(matrix, bitsig):
    """ Compute binary codes for the rows of the matrix: each binary code is
    the OR of bitsig for non-0 entries of the row.
    """
    indptr = matrix.indptr
    indices = matrix.indices
    n = matrix.shape[0]
    bit_codes = np.zeros(n, dtype='int64')
    for i in range(n):
        # print(bitsig[indices[indptr[i]:indptr[i + 1]]])
        bit_codes[i] = np.bitwise_or.reduce(bitsig[indices[indptr[i]:indptr[i + 1]]])
    return bit_codes


class BinarySignatures:
    """ binary signatures that encode vectors """

    def __init__(self, meta_b, proba_1):
        nvec, nword = meta_b.shape
        # number of bits reserved for the vector ids
        self.id_bits = int(np.ceil(np.log2(nvec)))
        # number of bits for the binary signature
        self.sig_bits = nbits = 63 - self.id_bits

        # select binary signatures for the vocabulary
        rs = np.random.RandomState(123)    # we rely on this to be reproducible!
        bitsig = np.packbits(rs.rand(nword, nbits) < proba_1, axis=1)
        bitsig = np.pad(bitsig, ((0, 0), (0, 8 - bitsig.shape[1]))).view("int64").ravel()
        self.bitsig = bitsig

        # signatures for all the metadata matrix
        self.db_sig = csr_to_bitcodes(meta_b, bitsig) << self.id_bits

        # mask to keep only the ids
        self.id_mask = (1 << self.id_bits) - 1

    def query_signature(self, w1, w2):
        """ compute the query signature for 1 or 2 words """
        sig = self.bitsig[w1]
        if w2 != -1:
            sig |= self.bitsig[w2]
        return int(sig << self.id_bits)

class FAISS(BaseFilterANN):

    def __init__(self,  metric, index_params):
        self._index_params = index_params
        self._metric = metric
        print(index_params)
        self.indexkey = index_params.get("indexkey", "IVF32768,SQ8")
        self.binarysig = index_params.get("binarysig", True)
        self.binarysig_proba1 = index_params.get("binarysig_proba1", 0.1)
        self.metadata_threshold = 1e-3
        self.nt = index_params.get("threads", 1)
    

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        if ds.search_type() == "knn_filtered" and self.binarysig:
            print("preparing binary signatures")
            meta_b = ds.get_dataset_metadata()
            self.binsig = BinarySignatures(meta_b, self.binarysig_proba1)
            print("writing to", self.binarysig_name(dataset))
            pickle.dump(self.binsig, open(self.binarysig_name(dataset), "wb"), -1)
        else:
            self.binsig = None

        if ds.search_type() == "knn_filtered":
            self.meta_b = ds.get_dataset_metadata()
            self.meta_b.sort_indices()

        index = faiss.index_factory(ds.d, self.indexkey)
        xb = ds.get_dataset()
        print("train")
        index.train(xb)
        print("populate")
        if self.binsig is None:
            index.add(xb)
        else:
            ids = np.arange(ds.nb) | self.binsig.db_sig
            index.add_with_ids(xb, ids)

        self.index = index
        self.nb = ds.nb
        self.xb = xb
        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.index)
        print("store", self.index_name(dataset))
        faiss.write_index(index, self.index_name(dataset))

    
    def index_name(self, name):
        return f"data/{name}.{self.indexkey}.faissindex"
    
    def binarysig_name(self, name):
        return f"data/{name}.{self.indexkey}.binarysig"


    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        if not os.path.exists(self.index_name(dataset)):
            if 'url' not in self._index_params:
                return False

            print('Downloading index in background. This can take a while.')
            download_accelerated(self._index_params['url'], self.index_name(dataset), quiet=True)

        print("Loading index")

        self.index = faiss.read_index(self.index_name(dataset))

        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.index)

        ds = DATASETS[dataset]()

        if ds.search_type() == "knn_filtered" and self.binarysig:
            if not os.path.exists(self.binarysig_name(dataset)):
                print("preparing binary signatures")
                meta_b = ds.get_dataset_metadata()
                self.binsig = BinarySignatures(meta_b, self.binarysig_proba1)
            else:
                print("loading binary signatures")
                self.binsig = pickle.load(open(self.binarysig_name(dataset), "rb"))
        else:
            self.binsig = None

        if ds.search_type() == "knn_filtered":
            self.meta_b = ds.get_dataset_metadata()
            self.meta_b.sort_indices()

        self.nb = ds.nb
        self.xb = ds.get_dataset()

        return True        

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
        for i0 in range(0, nq, bs):
            _, self.I[i0:i0+bs] = self.index.search(X[i0:i0+bs], k)

    
    def filtered_query(self, X, filter, k):
        print('running filtered query')
        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int32')
        meta_b = self.meta_b
        meta_q = filter
        docs_per_word = meta_b.T.tocsr()
        ndoc_per_word = docs_per_word.indptr[1:] - docs_per_word.indptr[:-1]
        freq_per_word = ndoc_per_word / self.nb
        
        def process_one_row(q):
            faiss.omp_set_num_threads(1)
            qwords = csr_get_row_indices(meta_q, q)
            assert qwords.size in (1, 2)
            w1 = qwords[0]
            freq = freq_per_word[w1]
            if qwords.size == 2:
                w2 = qwords[1]
                freq *= freq_per_word[w2]
            else:
                w2 = -1
            if freq < self.metadata_threshold:
                # metadata first
                docs = csr_get_row_indices(docs_per_word, w1)
                if w2 != -1:
                    docs = bow_id_selector.intersect_sorted(
                        docs, csr_get_row_indices(docs_per_word, w2))

                assert len(docs) >= k, pdb.set_trace()
                xb_subset = self.xb[docs]
                _, Ii = faiss.knn(X[q : q + 1], xb_subset, k=k)
 
                self.I[q, :] = docs[Ii.ravel()]
            else:
                # IVF first, filtered search
                sel = make_bow_id_selector(meta_b, self.binsig.id_mask if self.binsig else 0)
                if self.binsig is None:
                    sel.set_query_words(int(w1), int(w2))
                else:
                    sel.set_query_words_mask(
                        int(w1), int(w2), self.binsig.query_signature(w1, w2))

                params = faiss.SearchParametersIVF(sel=sel, nprobe=self.nprobe)

                _, Ii = self.index.search(
                    X[q:q+1], k, params=params
                )
                Ii = Ii.ravel()
                if self.binsig is None:
                    self.I[q] = Ii
                else:
                    # we'll just assume there are enough results
                    # valid = Ii != -1
                    # I[q, valid] = Ii[valid] & binsig.id_mask
                    self.I[q] = Ii & self.binsig.id_mask


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
        faiss.cvar.indexIVF_stats.reset()
        if "nprobe" in query_args:
            self.nprobe = query_args['nprobe']
            self.ps.set_index_parameters(self.index, f"nprobe={query_args['nprobe']}")
            self.qas = query_args
        else:
            self.nprobe = 1
        if "mt_threshold" in query_args:
            self.metadata_threshold = query_args['mt_threshold']
        else:
            self.metadata_threshold = 1e-3

    def __str__(self):
        return f'Faiss({self.indexkey, self.qas})'

   