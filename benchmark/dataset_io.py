"""
I/O functions for the fileformats used in the competition.
"""

import numpy as np
import os
import time

from urllib.request import urlopen
from scipy.sparse import csr_matrix





def download(src, dst=None, max_size=None):
    """ download an URL, possibly cropped """
    if os.path.exists(dst):
        print("Already exists")
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

def xbin_write(x, fname):
    f = open(fname, "wb")
    n, d = x.shape
    np.array([n, d], dtype='uint32').tofile(f)
    x.tofile(f)

def u8bin_write(x, fname):
    assert x.dtype == "uint8"
    xbin_write(x, fname)

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
    """ make the simplest possible array of the input"""
    return np.ascontiguousarray(x)

def usbin_write(ids, dist, fname):
    ids = np.ascontiguousarray(ids, dtype="int32")
    dist = np.ascontiguousarray(dist, dtype="float32")
    assert ids.shape == dist.shape
    f = open(fname, "wb")
    n, d = dist.shape
    np.array([n, d], dtype='uint32').tofile(f)
    ids.tofile(f)
    dist.tofile(f)

#########################################################
# Sparse I/O routines
#########################################################

def write_sparse_matrix(mat, fname):
    """ write a CSR matrix in the spmat format """
    with open(fname, "wb") as f:
        sizes = np.array([mat.shape[0], mat.shape[1], mat.nnz], dtype='int64')
        sizes.tofile(f)
        indptr = mat.indptr.astype('int64')
        indptr.tofile(f)
        mat.indices.astype('int32').tofile(f)
        mat.data.astype('float32').tofile(f)

def read_sparse_matrix_fields(fname):
    """ read the fields of a CSR matrix without instanciating it """
    with open(fname, "rb") as f:
        sizes = np.fromfile(f, dtype='int64', count=3)
        nrow, ncol, nnz = sizes
        indptr = np.fromfile(f, dtype='int64', count=nrow + 1)
        assert nnz == indptr[-1]
        indices = np.fromfile(f, dtype='int32', count=nnz)
        assert np.all(indices >= 0) and np.all(indices < ncol)
        data = np.fromfile(f, dtype='float32', count=nnz)
        return data, indices, indptr, ncol

def mmap_sparse_matrix_fields(fname):
    """ mmap the fields of a CSR matrix without instanciating it """
    with open(fname, "rb") as f:
        sizes = np.fromfile(f, dtype='int64', count=3)
        nrow, ncol, nnz = sizes
    ofs = sizes.nbytes
    indptr = np.memmap(fname, dtype='int64', mode='r', offset=ofs, shape=nrow + 1)
    ofs += indptr.nbytes
    indices = np.memmap(fname, dtype='int32', mode='r', offset=ofs, shape=nnz)
    ofs += indices.nbytes
    data = np.memmap(fname, dtype='float32', mode='r', offset=ofs, shape=nnz)
    return data, indices, indptr, ncol

def read_sparse_matrix(fname, do_mmap=False):
    """ read a CSR matrix in spmat format, optionally mmapping it instead """
    if not do_mmap:
        data, indices, indptr, ncol = read_sparse_matrix_fields(fname)
    else:
        data, indices, indptr, ncol = mmap_sparse_matrix_fields(fname)

    return csr_matrix((data, indices, indptr), shape=(len(indptr) - 1, ncol))
