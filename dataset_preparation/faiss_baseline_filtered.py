import argparse
import time
import resource
import threading
import numpy as np
from multiprocessing.pool import ThreadPool

import faiss

import benchmark.datasets
from benchmark.dataset_io import usbin_write

from benchmark.datasets import DATASETS

def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]

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
    aa('--indexname', default="/tmp/filtered.faissindex", help="where to store the index")
    aa('--build', action="store_true", default=False)

    group = parser.add_argument_group('computation options')
    aa('--k', default=10, type=int, help="number of nearest kNN neighbors to search")
    aa("--maxRAM", default=100, type=int, help="set max RSS in GB (avoid OOM crash)")
    aa('--nt', default=32, type=int, help="nb processes in thread pool")
    aa('--nprobe', default=16, type=int, help="nb probes for IVF")

    group = parser.add_argument_group('output options')
    aa('--o', default="/tmp/search_results", help="output file name")

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
    D = np.zeros((ds.nq, k), dtype='float32')
    I = -np.ones((ds.nq, k), dtype='int32')

    print("load dataset vectors")
    xb = ds.get_dataset()
    print("  size", xb.shape)

    if args.build:
        print("instanciate", args.indexkey)
        index = faiss.index_factory(ds.d, args.indexkey)
        print("train")
        index.train(xb)
        print("populate")
        index.add(xb)
        print("store", args.indexname)
        faiss.write_index(index, args.indexname)
    else:
        print("read", args.indexname)
        index = faiss.read_index(args.indexname)

    print("load query vectors")
    xq = ds.get_queries()
    print("  size", xq.shape)
    nprobe = args.nprobe
    print("setting nprobe", nprobe)
    faiss.ParameterSpace().set_index_parameter(index, "nprobe", nprobe)

    print("preparing ground-truth")
    gt_I, _ = ds.get_groundtruth()

    if ds.search_type() == "knn":
        print("perform unfiltered search")
        bs = 1024
        tot_recall = 0
        ntot = 0
        faiss.omp_set_num_threads(args.nt)
        t0 = time.time()
        for i0 in range(0, ds.nq, bs):
            D[i0:i0+bs], I[i0:i0+bs] = index.search(xq[i0:i0+bs], k)
            # import pdb; pdb.set_trace()
            ntot += len(D[i0:i0+bs])
            print(f"{i0}/{ds.nq} inter={tot_recall/ntot:.4f}", end="\r", flush=True)
        t1 = time.time()
        print()

    else:
        print("load dataset + query metadata")
        meta_b = ds.get_dataset_metadata()
        meta_q = ds.get_queries_metadata()
        print("  sizes", meta_b.shape, meta_q.shape)
        print("transpose doc-word matrix to inverted file")
        docs_per_word = meta_b.T.tocsr()
        ndoc_per_word = docs_per_word.indptr[1:] - docs_per_word.indptr[:-1]
        freq_per_word = ndoc_per_word / ds.nb


        t0 = time.time()
        print("database size", xb.shape)
        totsz = [0, 0]
        lock = threading.Lock()
        last_t = [time.time()]
        reporting_id = threading.get_ident()

        def process_one_row(q):
            qwords = csr_get_row_indices(meta_q, q)
            assert qwords.size in (1, 2)
            w1 = qwords[0]
            freq = freq_per_word[w1]
            if qwords.size == 2:
                w2 = qwords[1]
                freq *= freq_per_word[w2]
            else:
                w2 = -1

            if freq < 1e-3:
                # lookup word first
                docs = csr_get_row_indices(docs_per_word, w1)
                if w2 == -1:
                    docs = np.intersect1d(
                        docs, csr_get_row_indices(docs_per_word, w2),
                        assume_unique=True)

                assert len(docs) >= k
                xb_subset = xb[docs]
                totsz[0] += docs.size
                totsz[1] += 1
                Di, Ii = faiss.knn(xq[q : q + 1], xb_subset, k=k)
                D[q, :] = Di.ravel()
                I[q, :] = docs[Ii.ravel()]
            else:
                def is_member(b):
                    terms = csr_get_row_indices(meta_b, b)
                    if w1 not in terms:
                        return False
                    if w2 != -1:
                        return w2 in terms

                params = faiss.SearchParametersIVF(
                    sel=faiss.PyCallbackIDSelector(is_member),
                    nprobe=nprobe
                )
                Di, Ii = index.search(
                    xq[q:q+1], k, params=params
                )
                D[q:q+1] = Di
                I[q:q+1] = Ii

        print("starting search with nt=", args.nt)
        if args.nt == 1:
            map(process_one_row, range(ds.nq))
        else:
            faiss.omp_set_num_threads(1)
            pool = ThreadPool(args.nt)
            list(pool.map(process_one_row, range(ds.nq)))
        t1 = time.time()

    print()
    if args.o:
        print("Writing result to", args.o)
        usbin_write(I, D, args.o)
    gt = ds.get_groundtruth()
    recall = faiss.eval_intersection(gt_I, I) / k / ds.nq
    print(f"time {t1 - t0:.3f} recall {recall:.4f}")



