import sys
import numpy
import os

from benchmark.datasets import DATASETS

#
# DEEP1B
#

# DEEP1M dataset 
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-1M.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-1M"]()
    ds.prepare(False)

    print("counting")
    count = 0
    for dt in ds.get_dataset_iterator():
        count += 1
    print("%d" % count, type(dt), dt.shape, dt.dtype)

    arr = numpy.empty( (0,96), dt.dtype )
    print("arr shape", dt.shape)

    print("appending")
    for dt in ds.get_dataset_iterator():
        arr = numpy.concatenate( (arr, dt), axis=0 )
        print(dt.shape, arr.shape)

    print("saving",fname)
    numpy.save( fname, arr )
    print("done")

# DEEP1B query set
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-queries.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-1M"]()
    ds.prepare(False)

    queries = ds.get_queries()
    print(queries.shape)

    print("saving",fname)
    numpy.save( fname, queries )
    print("done")

# DEEP1B query set - 1000
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-queries-1000.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-1M"]()
    ds.prepare(False)

    queries = ds.get_queries()
    print(queries.shape)
    queries = queries[:1000,:]
    print(queries.shape)

    print("saving",fname)
    numpy.save( fname, queries )
    print("done")

# DEEP1M of DEEP1B, gt set - 1000
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-1M-gt-1000.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-1M"]()
    ds.prepare(False)

    I, D = ds.get_groundtruth()
    print(I.shape)
    I = I[:1000,:]
    print(I.shape)

    print("saving",fname)
    numpy.save( fname, I )
    print("done")

# DEEP1B query set - 100
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-queries-100.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-1M"]()
    ds.prepare(False)

    queries = ds.get_queries()
    print(queries.shape)
    queries = queries[:100,:]
    print(queries.shape)

    print("saving",fname)
    numpy.save( fname, queries )
    print("done")

# DEEP1M of DEEP1B, gt set - 100
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-1M-gt-100.npy"
if not os.path.exists(fname):

    gt1000 = "/mnt/nas1/fvs_benchmark_datasets/deep-1M-gt-1000.npy"
    I = numpy.load(gt1000)
    print(I.shape)
    I = I[:100,:]
    print(I.shape)

    print("saving",fname)
    numpy.save( fname, I )
    print("done")

# DEEP1B query set - 10
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-queries-10.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-1M"]()
    ds.prepare(False)

    queries = ds.get_queries()
    print(queries.shape)
    queries = queries[:10,:]
    print(queries.shape)

    print("saving",fname)
    numpy.save( fname, queries )
    print("done")

# DEEP1M of DEEP1B, gt set - 10
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-1M-gt-10.npy"
if not os.path.exists(fname):

    gt1000 = "/mnt/nas1/fvs_benchmark_datasets/deep-1M-gt-1000.npy"
    I = numpy.load(gt1000)
    print(I.shape)
    I = I[:10,:]
    print(I.shape)

    print("saving",fname)
    numpy.save( fname, I )
    print("done")

# DEEP10M dataset 
fname = "/mnt/nas1/fvs_benchmark_datasets/deep-10M.npy"
if not os.path.exists(fname):
    ds = DATASETS["deep-10M"]()
    ds.prepare(False)

    print("counting")
    count = 0
    for dt in ds.get_dataset_iterator():
        count += 1
    print("%d" % count, type(dt), dt.shape, dt.dtype)

    arr = numpy.empty( (0,96), dt.dtype )
    print("arr shape", dt.shape)

    print("appending")
    for dt in ds.get_dataset_iterator():
        arr = numpy.concatenate( (arr, dt), axis=0 )
        print(dt.shape, arr.shape)

    print("saving",fname)
    numpy.save( fname, arr )
    print("done")

print("Done.")
