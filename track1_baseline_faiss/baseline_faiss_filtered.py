import argparse
import time
import resource
import threading
import pdb
import pickle
import numpy as np

from multiprocessing.pool import ThreadPool

import faiss
from faiss.contrib.inspect_tools import get_invlist

import benchmark.datasets
from benchmark.dataset_io import usbin_write
from benchmark.datasets import DATASETS

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



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('dataset options')
    aa('--dataset', choices=DATASETS.keys(), required=True)
    aa('--prepare', default=False, action="store_true",
        help="call prepare() to download the dataset before computing")
    aa('--basedir', help="override basedir for dataset")
    aa('--private', default=False, action="store_true",
        help="handle private queries")

    group = parser.add_argument_group('building options')
    aa("--indexkey", default="IVF32768,SQ8", help="Set the index type")
    aa('--indexname', default="/tmp/filtered.faissindex",
        help="where to store the index")
    aa('--build', action="store_true", default=False)

    group = parser.add_argument_group('binary signatures options')
    aa('--binarysig', action="store_true", default=False,
        help="add binary signatures to ids to improve filtering")
    aa('--binarysig_proba1', default=0.1, type=float,
        help="probabilty of having a 1 in the binary signatures")
    aa('--binarysig_file', default="/tmp/binarysigs.pickle",
        help="where to store the binary signatures table")
    aa('--binarysig_strip', action="store_true", default=False,
       help="Strip binary signatures after loading (for debugging)")

    group = parser.add_argument_group('computation options')
    aa('--k', default=10, type=int, help="number of nearest kNN neighbors to search")
    aa("--maxRAM", default=100, type=int, help="set max RSS in GB (avoid OOM crash)")
    aa('--nt', default=32, type=int, help="nb processes in thread pool")
    aa('--nprobe', default=16, type=int, help="nb probes for IVF")
    aa('--nq', default=-1, type=int, help="limit number of queries")
    aa('--metadata_threshold', default=1e-3, type=float,
        help="threshold on predicted proba below which we use a metadata invfile")

    group = parser.add_argument_group('output options')
    aa('--o', default="", help="output file name")

    args = parser.parse_args()

    print("args:", args)

    if args.basedir:
        print("setting datasets basedir to", args.basedir)
        benchmark.datasets.BASEDIR
        benchmark.datasets.BASEDIR = args.basedir

    if args.maxRAM > 0:
        print("setting max RSS to", args.maxRAM, "GiB")
        resource.setrlimit(
            resource.RLIMIT_DATA, (args.maxRAM * 1024 ** 3, resource.RLIM_INFINITY)
        )

    ds = DATASETS[args.dataset]()

    print(ds)

    if args.prepare:
        print("downloading dataset...")
        ds.prepare()
        print("dataset ready")


    assert ds.search_type() in ("knn_filtered", "knn")

    k = ds.default_count()

    print("load dataset vectors")
    xb = ds.get_dataset()
    print("  size", xb.shape)

    if args.binarysig:
        print("preparing binary signatures")
        if args.build:
            meta_b = ds.get_dataset_metadata()
            binsig = BinarySignatures(meta_b, args.binarysig_proba1)
            print("writing to", args.binarysig_file)
            pickle.dump(binsig, open(args.binarysig_file, "wb"), -1)
        else:
            print("reading from", args.binarysig_file)
            binsig = pickle.load(open(args.binarysig_file, "rb"))
    else:
        binsig = None

    if args.build:
        print("instanciate", args.indexkey)
        index = faiss.index_factory(ds.d, args.indexkey)
        print("train")
        index.train(xb)
        print("populate")
        if binsig is None:
            index.add(xb)
        else:
            ids = np.arange(ds.nb) | binsig.db_sig
            index.add_with_ids(xb, ids)
        print("store", args.indexname)
        faiss.write_index(index, args.indexname)
    else:
        print("read", args.indexname)
        index = faiss.read_index(args.indexname)

    if args.binarysig_strip and binsig:
        print("stripping binary signatures from index")
        index_ivf = faiss.extract_index_ivf(index)
        invlists = index_ivf.invlists
        for i in range(index_ivf.nlist):
            ids, _ = get_invlist(invlists, i)
            ids &= binsig.id_mask
            set_invlist_ids(invlists, i, ids)
        binsig = None

    print("load query vectors")
    xq = ds.get_queries()
    print("  size", xq.shape)

    print("preparing ground-truth")
    gt_I, _ = ds.get_groundtruth()

    if args.nq >= 0:
        print("cropping nb of queries to", args.nq)
        ds.nq = args.nq
        xq = xq[:args.nq]
        gt_I = gt_I[:args.nq]

    D = np.zeros((ds.nq, k), dtype='float32')
    I = -np.ones((ds.nq, k), dtype='int32')

    nprobe = args.nprobe
    print("setting nprobe", nprobe)
    faiss.ParameterSpace().set_index_parameter(index, "nprobe", nprobe)


    if ds.search_type() == "knn":
        print("perform unfiltered search")
        bs = 1024
        tot_recall = 0
        ntot = 0
        faiss.omp_set_num_threads(args.nt)
        t0 = time.time()
        for i0 in range(0, ds.nq, bs):
            D[i0:i0+bs], I[i0:i0+bs] = index.search(xq[i0:i0+bs], k)
            ntot += len(D[i0:i0+bs])
            print(f"{i0}/{ds.nq} inter={tot_recall/ntot:.4f}", end="\r", flush=True)
        t1 = time.time()
        print()

    else:
        print("load dataset + query metadata")
        meta_b = ds.get_dataset_metadata()
        meta_b.sort_indices()

        meta_q = ds.get_queries_metadata()
        if args.nq >= 0:
            meta_q = meta_q[:args.nq]
        print("  sizes", meta_b.shape, meta_q.shape)
        print("transpose doc-word matrix to inverted file")
        docs_per_word = meta_b.T.tocsr()
        ndoc_per_word = docs_per_word.indptr[1:] - docs_per_word.indptr[:-1]
        freq_per_word = ndoc_per_word / ds.nb

        t0 = time.time()
        print("database size", xb.shape)
        cum_t = [0, 0]
        cum_n = [0, 0]
        reporting_id = threading.get_ident()

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
            t0 = time.time()
            if freq < args.metadata_threshold:
                # metadata first
                docs = csr_get_row_indices(docs_per_word, w1)
                if w2 != -1:
                    if False:
                        docs = np.intersect1d(
                            docs, csr_get_row_indices(docs_per_word, w2),
                            assume_unique=True)
                    else:
                        docs = bow_id_selector.intersect_sorted(
                            docs, csr_get_row_indices(docs_per_word, w2))

                assert len(docs) >= k, pdb.set_trace()
                if True:
                    xb_subset = xb[docs]
                    Di, Ii = faiss.knn(xq[q : q + 1], xb_subset, k=k)
                else:
                    dis = np.empty(len(docs), dtype="float32")
                    docs_i64 = docs.astype('int64')
                    faiss.fvec_L2sqr_by_idx(
                        faiss.swig_ptr(dis),
                        faiss.swig_ptr(xq[q]),
                        faiss.swig_ptr(xb),
                        faiss.swig_ptr(docs_i64),
                        ds.d, 1, len(docs)
                    )
                    o = dis.argsort()
                    Ii = o[:k]
                    Di = dis[o[:k]]
                D[q, :] = Di.ravel()
                I[q, :] = docs[Ii.ravel()]
                ii = 0
            else:
                # IVF first, filtered search
                sel = make_bow_id_selector(meta_b, binsig.id_mask if binsig else 0)
                if binsig is None:
                    sel.set_query_words(int(w1), int(w2))
                else:
                    sel.set_query_words_mask(
                        int(w1), int(w2), binsig.query_signature(w1, w2))

                params = faiss.SearchParametersIVF(sel=sel, nprobe=nprobe)

                Di, Ii = index.search(
                    xq[q:q+1], k, params=params
                )
                D[q] = Di.ravel()
                Ii = Ii.ravel()
                if binsig is None:
                    I[q] = Ii
                else:
                    # we'll just assume there are enough resutls
                    # valid = Ii != -1
                    # I[q, valid] = Ii[valid] & binsig.id_mask
                    I[q] = Ii & binsig.id_mask
                ii = 1
            t1 = time.time()
            cum_t[ii] += t1 - t0
            cum_n[ii] += 1

        print("starting search with nt=", args.nt)
        if args.nt <= 1:
            for q in range(ds.nq):
                process_one_row(q)
        else:
            faiss.omp_set_num_threads(1)
            pool = ThreadPool(args.nt)
            list(pool.map(process_one_row, range(ds.nq)))
        t1 = time.time()
        print()
        print(f"metadata first search: {cum_n[0]}, {cum_t[0]:.3f} s, {cum_t[0]/cum_n[0] * 1000:.3f} ms / q")
        print(f"IVF first search: {cum_n[1]}, {cum_t[1]:.3f} s, {cum_t[1]/cum_n[1] * 1000:.3f} ms / q")

    if args.o:
        print("Writing result to", args.o)
        usbin_write(I, D, args.o)

    recall = faiss.eval_intersection(gt_I, I) / k / ds.nq
    print(f"time {t1 - t0:.3f} recall {recall:.4f}")




