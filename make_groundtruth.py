import argparse
import logging
import time
import resource
import pdb

import numpy as np

import faiss

from faiss.contrib.exhaustive_search import range_search_gpu

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


def range_ground_truth(ds, radius, bs):
    """Computes the exact range search results for a dataset that possibly
    does not fit in RAM but for which we have an iterator that
    returns it block by block.
    """
    print("loading queries")
    xq = ds.get_queries()

    if ds.distance() == "angular":
        faiss.normalize_L2(xq)

    print("range_ground_truth queries size %s radius=%g" % (xq.shape, radius))

    t0 = time.time()
    nq, d = xq.shape

    metric_type = (
        faiss.METRIC_L2 if ds.distance() == "euclidean" else
        faiss.METRIC_INNER_PRODUCT if ds.distance() in ("ip", "angular") else
        1/0
    )

    index = faiss.IndexFlat(d, metric_type)

    if faiss.get_num_gpus():
        print('running on %d GPUs' % faiss.get_num_gpus())
        index_gpu = faiss.index_cpu_to_all_gpus(index)
    else:
        index_gpu = None

    results = []

    # compute ground-truth by blocks, and add to heaps
    i0 = 0
    tot_res = 0
    for xbi in ds.get_dataset_iterator(bs=bs):
        ni = xbi.shape[0]
        if ds.distance() == "angular":
            faiss.normalize_L2(xbi)

        index.add(xbi)
        if index_gpu is None:
            lims, D, I = index.range_search(xq, radius)
        else:
            index_gpu.add(xbi)
            lims, D, I = range_search_gpu(xq, radius, index_gpu, index)
            index_gpu.reset()
        index.reset()
        I = I.astype("int32")
        I += i0
        results.append((lims, D, I))
        i0 += ni
        tot_res += len(D)
        print(f"[{time.time() - t0:.2f} s] {i0} / {ds.nb} vectors, {tot_res} matches",
            end="\r", flush=True)
    print()
    print("merge into single table")
    # merge all results in a single table
    nres = np.zeros(nq, dtype="int32")
    D = []
    I = []
    for q in range(nq):
        nres_q = 0
        for lims_i, Di, Ii in results:
            l0, l1 = lims_i[q], lims_i[q + 1]
            if l1 > l0:
                nres_q += l1 - l0
                D.append(Di[l0:l1])
                I.append(Ii[l0:l1])
        nres[q] = nres_q

    D = np.hstack(D)
    I = np.hstack(I)
    assert len(D) == nres.sum() == len(I)
    print("GT time: %.3f s (%d vectors)" % (time.time() - t0, i0))
    return nres, D, I

def usbin_write(x, fname):
    assert x.dtype == 'int32'
    f = open(fname, "wb")
    n, d = x.shape
    np.array([n, d], dtype='uint32').tofile(f)
    x.tofile(f)

def range_result_write(nres, I, fname):
    """ write the range search file format:
    int32 n_queries
    int32 total_res
    int32[n_queries] nb_results_per_query
    int32[total_res] database_ids
    """
    nres = np.ascontiguousarray(nres, dtype="int32")
    I = np.ascontiguousarray(I, dtype="int32")
    total_res = nres.sum()
    nq = len(nres)
    assert I.shape == (total_res, )
    f = open(fname, "wb")
    np.array([nq, total_res], dtype='uint32').tofile(f)
    nres.tofile(f)
    I.tofile(f)



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
    aa('--radius', default=96237, type=float, help="range search radius")
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

    if ds.search_type() == "knn":
        D, I = knn_ground_truth(ds, k=args.k, bs=args.bs)
        print(f"writing index matrix of size {I.shape} to {args.o}")
        # write in the usbin format
        usbin_write(I.astype("int32"), args.o)
    elif ds.search_type() == "range":
        nres, D, I = range_ground_truth(ds, radius=args.radius, bs=args.bs)
        print(f"writing results {I.shape} to {args.o}")
        range_result_write(nres, I, args.o)


