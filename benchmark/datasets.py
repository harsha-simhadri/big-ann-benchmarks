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


def download_accelerated(src, dst):
    """ dowload using an accelerator. Make sure the executable is in the path """
    print('downloading %s -> %s...' % (src, dst))
    if "windows.net" in src:
        cmd = f"azcopy copy {src} {dst}"
    else:
        cmd = f"axel --alternate -n 10 {src} -o {dst}"

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

    def prepare(self):
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


#############################################################################
# Datasets in orginal formats
##############################################################################

class Sift1BOriginalFormat(Dataset):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 128
        self.nq = 10000
        self.ds_fn = "bigann_base.bvecs"
        self.qs_fn = "bigann_query.bvecs"
        self.basedir = os.path.join(BASEDIR, "sift1b")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self):
        import gzip, tarfile
        ds_url = f"ftp://ftp.irisa.fr/local/texmex/corpus/{self.ds_fn}.gz"
        qs_url = f"ftp://ftp.irisa.fr/local/texmex/corpus/{self.qs_fn}.gz"
        gt_fn = "bigann_gnd.tar.gz"
        gt_url = f"ftp://ftp.irisa.fr/local/texmex/corpus/{gt_fn}"

        if not os.path.exists(os.path.join(self.basedir, self.ds_fn)):
            download(ds_url, os.path.join(self.basedir, f"{self.ds_fn}.gz"))
            download(qs_url, os.path.join(self.basedir, f"{self.qs_fn}.gz"))

            for fn in [self.ds_fn, self.qs_fn]:
                with gzip.open(os.path.join(self.basedir, f"{fn}.gz")) as g:
                    with open(os.path.join(self.basedir,  fn), "wb") as f:
                        f.write(g.read())

            download(gt_url, os.path.join(self.basedir,gt_fn))
            with tarfile.open(os.path.join(self.basedir, gt_fn)) as f:
                f.extractall(self.basedir)

    def get_dataset_fn(self):
        return os.path.join(self.basedir, self.ds_fn)

    def get_dataset(self):
        assert self.nb_M < 100, "dataset too large, use iterator"
        return sanitize(bvecs_mmap(self.get_dataset_fn())[:self.nb])

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        xb = bvecs_mmap(self.get_dataset_fn())
        nsplit, rank = split
        i0, i1 = self.nb * rank // nsplit, self.nb * (rank + 1) // nsplit
        for j0 in range(i0, i1, bs):
            yield sanitize(xb[j0: min(j0 + bs, i1)])

    def get_queries(self):
        return sanitize(bvecs_mmap(os.path.join(self.basedir, self.qs_fn))[:])

    def get_groundtruth(self, k=None):
        gt = ivecs_read(os.path.join(self.basedir, 'gnd/idx_%dM.ivecs' % self.nb_M))
        if k is not None:
            assert k <= 100
            gt = gt[:, :k]
        return gt

    def distance(self):
        return "euclidean"

    def search_type(self):
        return "knn"

class Deep1BOriginalFormat(Dataset):
    def __init__(self, nb_M=1000):
        assert nb_M in (10, 1000)
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 96
        self.nq = 10000
        self.ds_fn = "base.1B.fdata"
        self.qs_fn = "query.public.10K.fdata"
        self.gt_fn = "groundtruth.public.10K.idata"
        self.base_url = "https://storage.yandexcloud.net/yandex-research/ann-datasets/DEEP/"
        self.basedir = os.path.join(BASEDIR, "deep1b")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self):
        if os.path.exists(os.path.join(self.basedir, self.ds_fn)):
            print(f"{self} exists?")
            return
        ds_url = self.base_url + self.ds_fn
        qs_url = self.base_url + self.qs_fn
        qt_url = self.base_url + self.gt_fn

        for fn in [self.ds_fn, self.qs_fn, self.gt_fn]:
            download(os.path.join(self.base_url, fn), os.path.join(self.basedir, fn))

    def get_dataset_fn(self):
        return os.path.join(self.basedir, self.ds_fn)

    def get_dataset(self):
        assert self.nb < 10**8, "dataset too large, use iterator"
        return sanitize(read_fdata(self.get_dataset_fn(), self.nb, self.d))

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        nsplit, rank = split
        i0, i1 = self.nb * rank // nsplit, self.nb * (rank + 1) // nsplit
        d = self.d
        f = open(self.get_dataset_fn(), "rb")
        f.seek(i0 * d * 4)
        for j0 in range(i0, i1, bs):
            j1 = min(j0 + bs, i1)
            x = np.fromfile(f, dtype='float32', count=(j1 - j0) * d)
            yield x.reshape(j1 - j0, d)

    def get_queries(self):
        return sanitize(read_fdata(os.path.join(self.basedir, self.qs_fn), self.nq, self.d))

    def get_groundtruth(self, k=None):
        gt = read_idata(os.path.join(self.basedir, self.gt_fn), self.nq, self.d)
        if k is not None:
            assert k <= 100
            gt = gt[:, :k]
        return gt

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def __str__x(self):
        return f"Deep1B"


class RandomDS(Dataset):
    def __init__(self, nb, nq, d):
        self.nb = nb
        self.nq = nq
        self.d = d
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, f"random{self.nb}")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self):
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
            data.tofile(f)
        with open(os.path.join(self.basedir, self.qs_fn), "wb") as f:
            queries.tofile(f)

        print("Computing groundtruth")

        nbrs = NearestNeighbors(n_neighbors=100, metric="euclidean", algorithm='brute').fit(data)
        D, I = nbrs.kneighbors(queries)
        with open(os.path.join(self.basedir, self.gt_fn), "wb") as f:
            I.tofile(f)

    def get_dataset_fn(self):
        return os.path.join(self.basedir, self.ds_fn)

    def get_dataset(self):
        assert self.nb < 10**8, "dataset too large, use iterator"
        with open(self.get_dataset_fn(), "rb") as f:
            X = sanitize(numpy.fromfile(f).reshape((self.nb, self.d)))
        return X

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        raise NotImplementedError()

    def get_queries(self):
        with open(os.path.join(self.basedir, self.qs_fn), "rb") as f:
            X = sanitize(numpy.fromfile(f).reshape((self.nq, self.d)))
        return X

    def get_groundtruth(self, k=None):
        with open(os.path.join(self.basedir, self.gt_fn), "rb") as f:
            gt = numpy.fromfile(f, dtype=numpy.int64).reshape((self.nq, 100))
        if k is not None:
            assert k <= 100
            gt = gt[:, :k]
        return gt

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def __str__(self):
        return f"Random({self.nb})"

DATASETS = {
    'sift-1B': BigANNDataset(1000),
    'sift-10M': BigANNDataset(10),

    'bigann-1B': BigANNDataset(1000),
    'bigann-10M': BigANNDataset(10),

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

    'sift-1M-T3': BigANNDatasetT3(1),
    'sift-10M-T3': BigANNDatasetT3(10)
}
