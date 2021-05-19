
"""
Prepare the bigann dataset in the format expected for the 1B ANN competition

"""

import sys

from faiss.contrib import datasets as faiss_datasets
import numpy as np


# source data is in the native Faiss format
ds = faiss_datasets.DatasetBigANN()

stage = int(sys.argv[1])

outdir = "/scratch/matthijs/bigann_competiton_format/"

def u8bin_write(x, fname):
    assert x.dtype == 'uint8'
    f = open(fname, "wb")
    n, d = x.shape
    np.array([n, d], dtype='uint32').tofile(f)
    x.tofile(f)

def ibin_write(x, fname):
    assert x.dtype == 'int32'
    f = open(fname, "wb")
    n, d = x.shape
    np.array([n, d], dtype='uint32').tofile(f)
    x.tofile(f)


if stage == 1:  # convert query format
    # xq = ds.get_queries()
    xq = faiss_datasets.bvecs_mmap(ds.basedir + 'bigann_query.bvecs')
    xq = np.ascontiguousarray(xq)
    u8bin_write(xq, outdir + "query.public.10K.u8bin")

elif stage == 2:  # sample new queries from train set
    secretkey = int(sys.argv[2])
    rs = np.random.RandomState(secretkey)
    xt = faiss_datasets.bvecs_mmap(ds.basedir + 'bigann_learn.bvecs')
    print("size", xt.shape)
    selection = rs.choice(len(xt), 10000, replace=False)
    u8bin_write(xt[selection], outdir + f"query.private.{secretkey}.10K.u8bin")

elif stage == 3:  # convert 10M subset

    xb = faiss_datasets.bvecs_mmap(ds.basedir + 'bigann_base.bvecs')
    u8bin_write(xb[:10**7], outdir + "base.10M.u8bin")

elif stage == 4:  # write the 1B vectors...

    xb = faiss_datasets.bvecs_mmap(ds.basedir + 'bigann_base.bvecs')
    bs = 10**6
    f = open(outdir + "base.1B.u8bin", "wb")
    np.array(xb.shape, dtype='uint32').tofile(f)
    for i in range(1000):
        print(i, end="\r", flush=True)
        xb[i * bs : (i + 1) * bs].tofile(f)

elif stage == 5: # convert the training vectors

    xb = faiss_datasets.bvecs_mmap(ds.basedir + 'bigann_learn.bvecs')
    bs = 10**6
    f = open(outdir + "learn.100M.u8bin", "wb")
    np.array(xb.shape, dtype='uint32').tofile(f)
    for i in range(100):
        print(i, end="\r", flush=True)
        xb[i * bs : (i + 1) * bs].tofile(f)

elif stage == 6:
    # convert ground-truth files for public queries
    gt = ds.get_groundtruth()
    ibin_write(gt, outdir + "GT.public.1B.ibin")

    ds10M = faiss_datasets.DatasetBigANN(10)
    gt = ds.get_groundtruth()
    ibin_write(gt, outdir + "GT.public.10M.ibin")







