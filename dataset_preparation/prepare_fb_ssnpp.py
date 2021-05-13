
"""
Prepare the FB SSN++ dataset in the format expected for the 1B ANN competition

The datafiles have already been produced on the prod side:

- FB_ssnpp_database.u8bin: the 1B database vectors, deduplicated, already
  in correct format

- 1M_queries_no_bursts_compressed.npy: a little less than 1M query vectors,
   selected not to be bursty

"""
import sys
import numpy as np

secret_suffix = sys.argv[1]

basedir = "/checkpoint/matthijs/billion-scale-ann-benchmarks/FB_ssnpp/"

def u8bin_write(x, fname):
    assert x.dtype == 'uint8'
    f = open(fname, "wb")
    n, d = x.shape
    np.array([n, d], dtype='uint32').tofile(f)
    x.tofile(f)

xqall_fp32 = np.load(basedir + "1M_queries_no_bursts_compressed.npy")
xqall = xqall_fp32.astype('uint8')
assert np.all(xqall == xqall_fp32)
u8bin_write(
    xqall[:10**5],
    basedir + "FB_ssnpp_public_queries.u8bin"
)
u8bin_write(
    xqall[10**5: 2 * 10**5],
    basedir + "FB_ssnpp_heldout_queries_" + secret_suffix + ".u8bin"
)

