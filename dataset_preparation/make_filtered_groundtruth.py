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

    group = parser.add_argument_group('computation options')
    aa('--k', default=100, type=int, help="number of nearest kNN neighbors to search")
    aa("--maxRAM", default=100, type=int, help="set max RSS in GB (avoid OOM crash)")
    aa('--nt', default=32, type=int, help="nb processes in thread pool")

    group = parser.add_argument_group('output options')
    aa('--o', default="/tmp/filtered_res", help="output file name")

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

    assert ds.search_type() == "knn_filtered"
    k = ds.default_count()
    D = np.zeros((ds.nq, k), dtype='float32')
    I = -np.ones((ds.nq, k), dtype='int32')

    print("load dataset vectors")
    xb = ds.get_dataset()
    print("  size", xb.shape)
    print("load query vectors")
    xq = ds.get_dataset()
    print("  size", xq.shape)

    print("load dataset + query metadata")
    meta_b = ds.get_dataset_metadata()
    meta_q = ds.get_queries_metadata()
    print("  sizes", meta_b.shape, meta_q.shape)
    print("transpose doc-word matrix to inverted file")
    docs_per_word = meta_b.T.tocsr()

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
        docs = csr_get_row_indices(docs_per_word, w1)
        if qwords.size == 2:
            w2 = qwords[1]
            docs = np.intersect1d(docs, csr_get_row_indices(docs_per_word, w2))
        xb_subset = xb[docs]
        totsz[0] += docs.size
        totsz[1] += 1
        Di, Ii = faiss.knn(xq[q : q + 1], xb_subset, k=k)
        D[q, :] = Di.ravel()
        I[q, :] = docs[Ii.ravel()]
        with lock:
            if time.time() - last_t[0] > 1:
                print(
                    f"[{time.time() - t0:.3f} s] {totsz[1]}/{ds.nq} ndis={totsz[0]}",
                    end="\r", flush=True
                )
                last_t[0] = time.time()

    if args.nt == 1:
        map(process_one_row, range(ds.nq))
    else:
        faiss.omp_set_num_threads(1)
        pool = ThreadPool(args.nt)
        list(pool.map(process_one_row, range(ds.nq)))

    print("Writing result to", args.o)
    usbin_write(I, D, args.o)


