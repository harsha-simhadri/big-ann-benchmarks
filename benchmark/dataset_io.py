"""
I/O functions for the fileformats used in the competition.
"""

import os
import time
from urllib.request import urlopen
import numpy as np






def download(src, dst=None, max_size=None):
    """ download an URL, possibly cropped """
    if os.path.exists(dst):
        return
    print('downloading %s -> %s...' % (src, dst))
    if max_size is not None:
        print("   stopping at %d bytes" % max_size)
    t0 = time.time()
    outf = open(dst, "wb")
    inf = urlopen(src)
    info = dict(inf.info())
    content_size = int(info['Content-Length'])
    bs = 1 << 20
    totsz = 0
    while True:
        block = inf.read(bs)
        elapsed = time.time() - t0
        print(
            "  [%.2f s] downloaded %.2f MiB / %.2f MiB at %.2f MiB/s   " % (
                elapsed,
                totsz / 2**20, content_size / 2**20,
                totsz / 2**20 / elapsed),
            flush=True, end="\r"
        )
        if not block:
            break
        if max_size is not None and totsz + len(block) >= max_size:
            block = block[:max_size - totsz]
            outf.write(block)
            totsz += len(block)
            break
        outf.write(block)
        totsz += len(block)
    print()
    print("download finished in %.2f s, total size %d bytes" % (
        time.time() - t0, totsz
    ))


def download_accelerated(src, dst, quiet=False, sas_string=""):
    """ dowload using an accelerator. Make sure the executable is in the path """
    print('downloading %s -> %s...' % (src, dst))
    if "windows.net" in src:
        if sas_string == "":
            cmd = f"azcopy copy {src} {dst}"
        else:
            cmd = f"azcopy copy '{src}?{sas_string}' '{dst}'"
    else:
        cmd = f"axel --alternate -n 10 {src} -o {dst}"
        if quiet:
            cmd += " -q"

    print("running", cmd)
    ret = os.system(cmd)
    assert ret == 0

def upload_accelerated(local_dir, blob_prefix, component, sas_string, quiet=False):
    """ Upload index component to Azure blob using SAS string"""
    src = os.path.join(local_dir, component)
    dst = blob_prefix + '/' + component + '?' + sas_string
    print('Uploading %s -> %s...' % (src, dst))

    cmd = f"azcopy copy '{src}' '{dst}'"
    print("running", cmd)
    ret = os.system(cmd)
    assert ret == 0


def bvecs_mmap(fname):
    x = np.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def ivecs_read(fname):
    a = np.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()

def xbin_mmap(fname, dtype, maxn=-1):
    """ mmap the competition file format for a given type of items """
    n, d = map(int, np.fromfile(fname, dtype="uint32", count=2))

    # HACK - to handle improper header in file for private deep-1B
    # if override_d and override_d != d:
    #    print("Warning: xbin_mmap map returned d=%s, but overridig with %d" % (d, override_d))
    #    d = override_d
    # HACK

    assert os.stat(fname).st_size == 8 + n * d * np.dtype(dtype).itemsize
    if maxn > 0:
        n = min(n, maxn)
    return np.memmap(fname, dtype=dtype, mode="r", offset=8, shape=(n, d))

def range_result_read(fname):
    """ read the range search result file format """
    f = open(fname, "rb")
    nq, total_res = np.fromfile(f, count=2, dtype="int32")
    nres = np.fromfile(f, count=nq, dtype="int32")
    assert nres.sum() == total_res
    I = np.fromfile(f, count=total_res, dtype="int32")
    D = np.fromfile(f, count=total_res, dtype="float32")
    return nres, I, D

def knn_result_read(fname):
    n, d = map(int, np.fromfile(fname, dtype="uint32", count=2))
    assert os.stat(fname).st_size == 8 + n * d * (4 + 4)
    f = open(fname, "rb")
    f.seek(4+4)
    I = np.fromfile(f, dtype="int32", count=n * d).reshape(n, d)
    D = np.fromfile(f, dtype="float32", count=n * d).reshape(n, d)
    return I, D

def read_fbin(filename, start_idx=0, chunk_size=None):
    """ Read *.fbin file that contains float32 vectors
    Args:
        :param filename (str): path to *.fbin file
        :param start_idx (int): start reading vectors from this index
        :param chunk_size (int): number of vectors to read.
                                 If None, read all vectors
    Returns:
        Array of float32 vectors (numpy.ndarray)
    """
    with open(filename, "rb") as f:
        nvecs, dim = np.fromfile(f, count=2, dtype=np.int32)
        nvecs = (nvecs - start_idx) if chunk_size is None else chunk_size
        arr = np.fromfile(f, count=nvecs * dim, dtype=np.float32,
                          offset=start_idx * 4 * dim)
    return arr.reshape(nvecs, dim)


def read_ibin(filename, start_idx=0, chunk_size=None):
    """ Read *.ibin file that contains int32 vectors
    Args:
        :param filename (str): path to *.ibin file
        :param start_idx (int): start reading vectors from this index
        :param chunk_size (int): number of vectors to read.
                                 If None, read all vectors
    Returns:
        Array of int32 vectors (numpy.ndarray)
    """
    with open(filename, "rb") as f:
        nvecs, dim = np.fromfile(f, count=2, dtype=np.int32)
        nvecs = (nvecs - start_idx) if chunk_size is None else chunk_size
        arr = np.fromfile(f, count=nvecs * dim, dtype=np.int32,
                          offset=start_idx * 4 * dim)
    return arr.reshape(nvecs, dim)


def sanitize(x):
    return np.ascontiguousarray(x, dtype='float32')

