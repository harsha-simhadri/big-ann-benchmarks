import math
import numpy
import os
import random
import sys
import struct
import time

import numpy as np

from urllib.request import urlopen
from urllib.request import urlretrieve

BASEDIR = "data/"

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


def download_accelerated(src, dst, quiet=False):
    """ dowload using an accelerator. Make sure the executable is in the path """
    print('downloading %s -> %s...' % (src, dst))
    if "windows.net" in src:
        cmd = f"azcopy copy {src} {dst}"
    else:
        cmd = f"axel --alternate -n 10 {src} -o {dst}"
        if quiet:
            cmd += " -q"

    print("running", cmd)
    ret = os.system(cmd)
    assert ret == 0


def bvecs_mmap(fname):
    x = numpy.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def ivecs_read(fname):
    a = numpy.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()

def xbin_mmap(fname, dtype, maxn=-1):
    """ mmap the competition file format for a given type of items """
    n, d = map(int, np.fromfile(fname, dtype="uint32", count=2))
    assert os.stat(fname).st_size == 8 + n * d * np.dtype(dtype).itemsize
    if maxn > 0:
        n = min(n, maxn)
    return np.memmap(fname, dtype=dtype, mode="r", offset=8, shape=(n, d))

#GW - I may eventually remove these
def xbin_mmap_floatarray(fname, shape):
    x = np.memmap(fname, dtype=numpy.float32, mode="r", offset=0, shape=shape)
    return x

def xbin_mmap_with_cast(fname, r_dtype, w_dtype, maxn=-1):
    """ mmap the competition file format for a given type of items """
    n, d = map(int, np.fromfile(fname, dtype="uint32", count=2))
    assert os.stat(fname).st_size == 8 + n * d * np.dtype(r_dtype).itemsize
    n = max(n, maxn)
    x = np.memmap(fname, dtype=r_dtype, mode="r", offset=8, shape=(n, d))
    x = x.astype( w_dtype )
    return x
#GW

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
    return numpy.ascontiguousarray(x, dtype='float32')


class Dataset():
    def prepare(self):
        """
        Download and prepare dataset, queries, groundtruth.
        """
        pass
    def get_dataset_fn(self):
        """
        Return filename of dataset file.
        """
        pass
    def get_dataset(self):
        """
        Return memmapped version of the dataset.
        """
        pass
    def get_dataset_iterator(self, bs=512, split=(1, 0)):
        """
        Return iterator over blocks of dataset of size at most 512.
        The split argument takes a pair of integers (n, p) where p = 0..n-1
        The dataset is split in n shards, and the iterator returns only shard #p
        This makes it possible to process the dataset independently from several
        processes / threads.
        """
        pass
    def get_queries(self):
        """
        Return (nq, d) array containing the nq queries.
        """
        pass
    def get_groundtruth(self, k=None):
        """
        Return (nq, k) array containing groundtruth indices
        for each query."""
        pass

    def search_type(self):
        """
        "knn" or "range"
        """
        pass

    def distance(self):
        """
        "euclidean" or "ip" or "angular"
        """
        pass

    def default_count(self):
        return 10


    def __str__(self):
        return (
            f"Dataset {self.__class__.__name__} in dimension {self.d}, with distance {self.distance()}, "
            f"search_type {self.search_type()}, size: Q {self.nq} B {self.nb}")


#############################################################################
# Datasets for the competition
##############################################################################



class DatasetCompetitionFormat(Dataset):
    """
    Dataset in the native competition format, that is able to read the
    files in the https://big-ann-benchmarks.com/ page.
    The constructor should set all fields. The functions below are generic.

    For the 10M versions of the dataset, the database files are downloaded in
    part and stored with a specific suffix. This is to avoid having to maintain
    two versions of the file.
    """

    def prepare(self, skip_data=False):
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        # start with the small ones...
        for fn in [self.qs_fn, self.gt_fn]:
            if fn is None:
                continue
            if fn.startswith("https://"):
                sourceurl = fn
                outfile = os.path.join(self.basedir, fn.split("/")[-1])
            else:
                sourceurl = os.path.join(self.base_url, fn)
                outfile = os.path.join(self.basedir, fn)
            if os.path.exists(outfile):
                print("file %s already exists" % outfile)
                continue
            download(sourceurl, outfile)

        if skip_data:
            return

        fn = self.ds_fn
        sourceurl = os.path.join(self.base_url, fn)
        outfile = os.path.join(self.basedir, fn)
        if os.path.exists(outfile):
            print("file %s already exists" % outfile)
            return
        if self.nb == 10**9:
            download_accelerated(sourceurl, outfile)
        else:
            # download cropped version of file
            file_size = 8 + self.d * self.nb * np.dtype(self.dtype).itemsize
            outfile = outfile + '.crop_nb_%d' % self.nb
            if os.path.exists(outfile):
                print("file %s already exists" % outfile)
                return
            download(sourceurl, outfile, max_size=file_size)
            # then overwrite the header...
            header = np.memmap(outfile, shape=2, dtype='uint32', mode="r+")
            assert header[0] == 10**9
            assert header[1] == self.d
            header[0] = self.nb

    def get_dataset_fn(self):
        fn = os.path.join(self.basedir, self.ds_fn)
        if os.path.exists(fn):
            return fn
        if self.nb != 10**9:
            fn += '.crop_nb_%d' % self.nb
            return fn
        else:
            raise RuntimeError("file not found")

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        nsplit, rank = split
        i0, i1 = self.nb * rank // nsplit, self.nb * (rank + 1) // nsplit
        filename = self.get_dataset_fn()
        x = xbin_mmap(filename, dtype=self.dtype, maxn=self.nb)
        assert x.shape == (self.nb, self.d)
        for j0 in range(i0, i1, bs):
            j1 = min(j0 + bs, i1)
            yield sanitize(x[j0:j1])

    def search_type(self):
        return "knn"

    def get_groundtruth(self, k=None):
        assert self.gt_fn is not None
        fn = self.gt_fn.split("/")[-1]   # in case it's a URL
        assert self.search_type() == "knn"

        I, D = knn_result_read(os.path.join(self.basedir, fn))
        assert I.shape[0] == self.nq
        if k is not None:
            assert k <= 100
            I = I[:, :k]
            D = D[:, :k]
        return I, D

    def get_dataset(self):
        assert self.nb <= 10**7, "dataset too large, use iterator"
        return sanitize(next(self.get_dataset_iterator(bs=self.nb)))

    def get_queries(self):
        filename = os.path.join(self.basedir, self.qs_fn)
        x = xbin_mmap(filename, dtype=self.dtype)
        assert x.shape == (self.nq, self.d)
        return sanitize(x)

subset_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/"

class SSNPPDataset(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        # assert nb_M in (10, 1000)
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 256
        self.nq = 100000
        self.dtype = "uint8"
        self.ds_fn = "FB_ssnpp_database.u8bin"
        self.qs_fn = "FB_ssnpp_public_queries.u8bin"

        self.gt_fn = (
            "FB_ssnpp_public_queries_1B_GT.rangeres" if self.nb_M == 1000 else
            subset_url + "GT_100M/ssnpp-100M" if self.nb_M == 100 else
            subset_url + "GT_10M/ssnpp-10M" if self.nb_M == 10 else
            None
        )

        self.base_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/"
        self.basedir = os.path.join(BASEDIR, "FB_ssnpp")

    def search_type(self):
        return "range"

    def default_count(self):
        return 60000

    def distance(self):
        return "euclidean"

    def get_groundtruth(self, k=None):
        """ override the ground-truth function as this is the only range search dataset """
        assert self.gt_fn is not None
        fn = self.gt_fn.split("/")[-1]   # in case it's a URL
        return range_result_read(os.path.join(self.basedir, fn))

class BigANNDataset(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 128
        self.nq = 10000
        self.dtype = "uint8"
        self.ds_fn = "base.1B.u8bin"
        self.qs_fn = "query.public.10K.u8bin"
        self.gt_fn = (
            "GT.public.1B.ibin" if self.nb_M == 1000 else
            subset_url + "GT_100M/bigann-100M" if self.nb_M == 100 else
            subset_url + "GT_10M/bigann-10M" if self.nb_M == 10 else
            None
        )
        # self.gt_fn = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/bigann/public_query_gt100.bin" if self.nb == 10**9 else None
        self.base_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/bigann/"
        self.basedir = os.path.join(BASEDIR, "bigann")

    def distance(self):
        return "euclidean"

class BigANNDatasetT3(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 128
        self.nq = 10000
        self.dtype = "uint8"
        self.ds_fn = "base.1B.u8bin"
        self.qs_fn = "query.public.10K.u8bin"
        self.gt_fn = "GT.public.1B.ibin" if self.nb == 10**9 else None
        self.base_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/bigann/"
        self.basedir = os.path.join(BASEDIR, "bigann")

    def get_dataset_fn(self):
        ds_fn = super().get_dataset_fn()
        ds_fn_fp = ds_fn + ".float32"
        if os.path.exists( ds_fn_fp ):
            return ds_fn_fp
        else:
            return ds_fn

    def get_dataset(self):
        ds_fn = super().get_dataset_fn()
        ds_fn_fp = ds_fn + ".float32"
        if os.path.exists( ds_fn_fp ):
            return xbin_mmap_floatarray( ds_fn_fp, ( self.nb, self.d ) )
        else:
            return super().get_dataset()

    def get_groundtruth(self,k=None):
        if self.gt_fn:
            return super().get_groundtruth(k)
        else: # assume its a crop
            gt_crop = os.path.join( self.basedir, "gt.ibin.crop_nb_%d" % self.nb )
            if os.path.exists(gt_crop):
                gt = xbin_mmap(os.path.join( gt_crop), dtype=np.int32)
                if k is not None:
                    assert k <= 100
                    gt = gt[:, :k]
                return gt
            else:
                raise Exception("No ground truth file.")

    def get_queries(self):
        ds_fn = super().get_dataset_fn()
        ds_fn_fp = ds_fn + ".float32"
        if os.path.exists( ds_fn_fp ):
            filename = os.path.join(self.basedir, self.qs_fn)
            return xbin_mmap_with_cast( filename, np.uint8, np.float32 )
        else:
            return super().get_queries()

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        ds_fn = super().get_dataset_fn()
        ds_fn_fp = ds_fn + ".float32"
        if os.path.exists( ds_fn_fp ):
            nsplit, rank = split
            i0, i1 = self.nb * rank // nsplit, self.nb * (rank + 1) // nsplit
            filename = self.get_dataset_fn()
            x = xbin_mmap_floatarray(filename, (self.nb, 128))
            assert x.shape == (self.nb, self.d)
            for j0 in range(i0, i1, bs):
                j1 = min(j0 + bs, i1)
                yield sanitize(x[j0:j1])
        else:
            return super().get_dataset_iterator(bs, split)

    def distance(self):
        return "euclidean"

class Deep1BDataset(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 96
        self.nq = 10000
        self.dtype = "float32"
        self.ds_fn = "base.1B.fbin"
        self.qs_fn = "query.public.10K.fbin"
        self.gt_fn = (
            "https://storage.yandexcloud.net/yandex-research/ann-datasets/deep_new_groundtruth.public.10K.bin" if self.nb_M == 1000 else
            subset_url + "GT_100M/deep-100M" if self.nb_M == 100 else
            subset_url + "GT_10M/deep-10M" if self.nb_M == 10 else
            None
        )
        self.base_url = "https://storage.yandexcloud.net/yandex-research/ann-datasets/DEEP/"
        self.basedir = os.path.join(BASEDIR, "deep1b")

    def distance(self):
        return "euclidean"




class Text2Image1B(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 200
        self.nq = 100000
        self.dtype = "float32"
        self.ds_fn = "base.1B.fbin"
        self.qs_fn = "query.public.100K.fbin"
        self.gt_fn = (
            "https://storage.yandexcloud.net/yandex-research/ann-datasets/t2i_new_groundtruth.public.100K.bin" if self.nb_M == 1000 else
            subset_url + "GT_100M/text2image-100M" if self.nb_M == 100 else
            subset_url + "GT_10M/text2image-10M" if self.nb_M == 10 else
            None
        )
        self.base_url = "https://storage.yandexcloud.net/yandex-research/ann-datasets/T2I/"
        self.basedir = os.path.join(BASEDIR, "text2image1B")

    def distance(self):
        return "ip"

class MSTuringANNS(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 100
        self.nq = 100000
        self.dtype = "float32"
        self.ds_fn = "base1b.fbin"
        self.qs_fn = "query100K.fbin"
        self.gt_fn = (
            "query_gt100.bin" if self.nb_M == 1000 else
            subset_url + "GT_100M/msturing-100M" if self.nb_M == 100 else
            subset_url + "GT_10M/msturing-10M" if self.nb_M == 10 else
            None
        )
        self.base_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/MSFT-TURING-ANNS/"
        self.basedir = os.path.join(BASEDIR, "MSTuringANNS")

    def distance(self):
        return "euclidean"


class MSSPACEV1B(DatasetCompetitionFormat):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 100
        self.nq = 29316
        self.dtype = "int8"
        self.ds_fn = "spacev1b_base.i8bin"
        self.qs_fn = "query.i8bin"
        self.gt_fn = (
            "public_query_gt100.bin" if self.nb_M == 1000 else
            subset_url + "GT_100M/msspacev-100M" if self.nb_M == 100 else
            subset_url + "GT_10M/msspacev-10M" if self.nb_M == 10 else
            None
        )
        self.base_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/spacev1b/"
        self.basedir = os.path.join(BASEDIR, "MSSPACEV1B")

    def distance(self):
        return "euclidean"

class RandomRangeDS(DatasetCompetitionFormat):
    def __init__(self, nb, nq, d):
        self.nb = nb
        self.nq = nq
        self.d = d
        self.dtype = 'float32'
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, f"random{self.nb}")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        import sklearn.datasets
        import sklearn.model_selection
        from sklearn.neighbors import NearestNeighbors

        print(f"Preparing datasets with {self.nb} random points and {self.nq} queries.")


        X, _ = sklearn.datasets.make_blobs(
            n_samples=self.nb + self.nq, n_features=self.d,
            centers=self.nq, random_state=1)

        data, queries = sklearn.model_selection.train_test_split(
            X, test_size=self.nq, random_state=1)


        with open(os.path.join(self.basedir, self.ds_fn), "wb") as f:
            np.array([self.nb, self.d], dtype='uint32').tofile(f)
            data.astype('float32').tofile(f)
        with open(os.path.join(self.basedir, self.qs_fn), "wb") as f:
            np.array([self.nq, self.d], dtype='uint32').tofile(f)
            queries.astype('float32').tofile(f)

        print("Computing groundtruth")

        nbrs = NearestNeighbors(n_neighbors=100, metric="euclidean", algorithm='brute').fit(data)
        D, I = nbrs.kneighbors(queries)

        nres = np.count_nonzero((D < math.sqrt(self.default_count())) == True, axis=1)
        DD = np.zeros(nres.sum())
        II = np.zeros(nres.sum(), dtype='int32')

        s = 0
        for i, l in enumerate(nres):
            DD[s : s + l] = D[i, 0 : l]
            II[s : s + l] = I[i, 0 : l]
            s += l

        with open(os.path.join(self.basedir, self.gt_fn), "wb") as f:
            np.array([self.nq, nres.sum()], dtype='uint32').tofile(f)
            nres.astype('int32').tofile(f)
            II.astype('int32').tofile(f)
            DD.astype('float32').tofile(f)

    def get_groundtruth(self, k=None):
        """ override the ground-truth function as this is the only range search dataset """
        assert self.gt_fn is not None
        fn = self.gt_fn.split("/")[-1]   # in case it's a URL
        return range_result_read(os.path.join(self.basedir, fn))

    def search_type(self):
        return "range"

    def default_count(self):
        return 49

    def distance(self):
        return "euclidean"

    def __str__(self):
        return f"RandomRange({self.nb})"

class RandomDS(DatasetCompetitionFormat):
    def __init__(self, nb, nq, d):
        self.nb = nb
        self.nq = nq
        self.d = d
        self.dtype = 'float32'
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, f"random{self.nb}")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        import sklearn.datasets
        import sklearn.model_selection
        from sklearn.neighbors import NearestNeighbors

        print(f"Preparing datasets with {self.nb} random points and {self.nq} queries.")


        X, _ = sklearn.datasets.make_blobs(
            n_samples=self.nb + self.nq, n_features=self.d,
            centers=self.nq, random_state=1)

        data, queries = sklearn.model_selection.train_test_split(
            X, test_size=self.nq, random_state=1)


        with open(os.path.join(self.basedir, self.ds_fn), "wb") as f:
            np.array([self.nb, self.d], dtype='uint32').tofile(f)
            data.astype('float32').tofile(f)
        with open(os.path.join(self.basedir, self.qs_fn), "wb") as f:
            np.array([self.nq, self.d], dtype='uint32').tofile(f)
            queries.astype('float32').tofile(f)

        print("Computing groundtruth")

        nbrs = NearestNeighbors(n_neighbors=100, metric="euclidean", algorithm='brute').fit(data)
        D, I = nbrs.kneighbors(queries)
        with open(os.path.join(self.basedir, self.gt_fn), "wb") as f:
            np.array([self.nq, 100], dtype='uint32').tofile(f)
            I.astype('uint32').tofile(f)
            D.astype('float32').tofile(f)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def __str__(self):
        return f"Random({self.nb})"

DATASETS = {
    'bigann-1B': lambda : BigANNDataset(1000),
    'bigann-100M': lambda : BigANNDataset(100),
    'bigann-10M': lambda : BigANNDataset(10),

    'deep-1B': Deep1BDataset(),
    'deep-10M': Deep1BDataset(10),
    'deep-100M': lambda : Deep1BDataset(100),

    'ssnpp-1B': SSNPPDataset(1000),
    'ssnpp-10M': SSNPPDataset(10),
    'ssnpp-100M': lambda : SSNPPDataset(100),
    'ssnpp-1M': SSNPPDataset(1),

    'text2image-1B': Text2Image1B(),
    'text2image-1M': Text2Image1B(1),
    'text2image-10M': Text2Image1B(10),
    'text2image-100M': lambda : Text2Image1B(100),

    'msturing-1B': MSTuringANNS(1000),
    'msturing-1M': MSTuringANNS(1),
    'msturing-10M': MSTuringANNS(10),
    'msturing-100M': lambda : MSTuringANNS(100),

    'msspacev-1B': MSSPACEV1B(1000),
    'msspacev-10M': MSSPACEV1B(10),
    'msspacev-100M': lambda : MSSPACEV1B(100),
    'msspacev-1M': MSSPACEV1B(1),

    'random-xs': RandomDS(10000, 1000, 20),
    'random-s': RandomDS(100000, 1000, 50),
    'random-s-256': RandomDS(100000, 1000, 256),
    'random-m-256': RandomDS(1000000, 10000, 256),

    'random-xs': lambda : RandomDS(10000, 1000, 20),
    'random-s': lambda : RandomDS(100000, 1000, 50),

    'random-range-xs': lambda : RandomRangeDS(10000, 1000, 20),
    'random-range-s': lambda : RandomRangeDS(100000, 1000, 50),
}
