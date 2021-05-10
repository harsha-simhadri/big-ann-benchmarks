import argparse
import logging
import time
import resource

import numpy as np

import faiss

from benchmark.datasets import DATASETS


def knn_ground_truth(ds, k, bs):
    """Computes the exact KNN search results for a dataset that possibly
    does not fit in RAM but for which we have an iterator that
    returns it block by block.
    """
    print("loading queries")
    xq = ds.get_queries()

    if ds.distance() == "angular":
        faiss.normalize_L2(xq)

    print("knn_ground_truth queries size %s k=%d" % (xq.shape, k))

    t0 = time.time()
    nq, d = xq.shape
    rh = faiss.ResultHeap(nq, k)

    metric_type = (
        faiss.METRIC_L2 if ds.distance() == "euclidean" else
        faiss.METRIC_INNER_PRODUCT if ds.distance() in ("ip", "angular") else
        1/0
    )

    index = faiss.IndexFlat(d, metric_type)

    if faiss.get_num_gpus():
        print('running on %d GPUs' % faiss.get_num_gpus())
        index = faiss.index_cpu_to_all_gpus(index)

    # compute ground-truth by blocks, and add to heaps
    i0 = 0
    for xbi in ds.get_dataset_iterator(bs=bs):
        ni = xbi.shape[0]
        if ds.distance() == "angular":
            faiss.normalize_L2(xbi)

        index.add(xbi)
        D, I = index.search(xq, k)
        I += i0
        rh.add_result(D, I)
        index.reset()
        i0 += ni
        print(f"[{time.time() - t0:.2f} s] {i0} / {ds.nb} vectors", end="\r", flush=True)

    rh.finalize()
    print()
    print("GT time: %.3f s (%d vectors)" % (time.time() - t0, i0))

    return rh.D, rh.I


def usbin_write(x, fname):
    assert x.dtype == 'int32'
    f = open(fname, "wb")
    n, d = x.shape
    np.array([n, d], dtype='uint32').tofile(f)
    x.tofile(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('dataset options')
    aa('--dataset', choices=DATASETS.keys(), required=True)

    group = parser.add_argument_group('computation options')
    # determined from ds
    # aa('--range_search', action="store_true", help="do range search instead of kNN search")
    aa('--k', default=100, type=int, help="number of nearest kNN neighbors to search")
    aa('--radius', default=1.5, type=float, help="range search radius")
    aa('--bs', default=100_000, type=int, help="batch size for database iterator")
    aa("--maxRAM", default=100, type=int, help="set max RSS in GB (avoid OOM crash)")

    group = parser.add_argument_group('output options')
    aa('--o', default="", help="output file name")

    args = parser.parse_args()

    if args.maxRAM > 0:
        print("setting max RSS to", args.maxRAM, "GiB")
        resource.setrlimit(
            resource.RLIMIT_DATA, (args.maxRAM * 1024 ** 3, resource.RLIM_INFINITY)
        )

    ds = DATASETS[args.dataset]

    print(ds)

    D, I = knn_ground_truth(ds, k=args.k, bs=args.bs)

    print(f"writing index matrix of size {I.shape} to {args.o}")
    # write in the usbin format
    usbin_write(I.astype("int32"), args.o)


