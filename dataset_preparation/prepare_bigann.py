
"""
Prepare the bigann dataset in the format expected for the 1B ANN competition

"""

import sys

from faiss.contrib import datasets as faiss_datasets
import numpy as np


ds = faiss_datasets.DatasetBigANN()

stage = int(sys.argv[1])

outdir = "/tmp/bigann_competiton_format/"

def u8bin_write(x, fname):
    assert x.dtype == 'uint8'
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
    u8bin_write(xt[selection], outdir + "query.private.10K.u8bin")

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





