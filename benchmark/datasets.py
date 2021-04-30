import numpy
import os
import random
import sys
import struct
import time

from urllib.request import urlopen
from urllib.request import urlretrieve

BASEDIR = "data/"

# https://blog.shichao.io/2012/10/04/progress_speed_indicator_for_urlretrieve_in_python.html
def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()

start_time = None

def download(src, dst=None):
    if not os.path.exists(dst):
        print('downloading %s -> %s...' % (src, dst))
        urlretrieve(src, dst, reporthook)

def bvecs_mmap(fname):
    x = numpy.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def ivecs_read(fname):
    a = numpy.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()

# TODO also memmap those?
def read_fdata(filename, nvecs, dim):
    with open(filename, 'rb') as f:
        buf = f.read(dim * 4 * nvecs)
        vecs = numpy.array(struct.unpack('f' * dim * nvecs, buf))
    return vecs.reshape((nvecs, dim))


def read_idata(filename, nvecs, dim):
    with open(filename, 'rb') as f:
        buf = f.read(dim * 4 * nvecs)
        vecs = numpy.array(struct.unpack('i' * dim * nvecs, buf))
    return vecs.reshape((nvecs, dim))

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
    def get_dataset_iterator(self, bs=512):
        """
        Return iterator over blocks of dataset..
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

    def __str__(self):
        """
        Return identifier.
        """
        pass


class Sift1B(Dataset):
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

    def __str__(self):
        return f"Sift1B(M={self.nb_M})"

class Deep1B(Dataset):
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

    def prepare(self):
        ds_url = self.base_url + self.ds_fn
        qs_url = self.base_url + self.qs_fn
        qt_url = self.base_url + self.gt_fn

        for fn in [ds_url, qs_url, qt_url]:
            download(fn)

    def get_dataset_fn(self):
        return 'data/' + self.ds_fn

    def get_dataset(self):
        assert self.nb < 10**8, "dataset too large, use iterator"
        return sanitize(read_fdata('data/' + self.ds_fn, self.nq, self.d))

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        pass

    def get_queries(self):
        return sanitize(read_fdata('data/' + self.qs_fn, self.nq, self.d))

    def get_groundtruth(self, k=None):
        gt = read_idata('data/' + self.gt_fn, self.nq, self.d)
        if k is not None:
            assert k <= 100
            gt = gt[:, :k]
        return gt

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def __str__(self):
        return f"Deep1B"

class Text2Image1B(Deep1B):
    def __init__(self, nb_M=1000):
        assert nb_M in (10, 1000)
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 200
        self.nq = 100000
        self.ds_fn = "base.1B.fdata"
        self.qs_fn = "query.public.100K.fdata"
        self.gt_fn = "groundtruth.public.100K.idata"
        self.base_url = "https://storage.yandexcloud.net/yandex-research/ann-datasets/T2I/"

    def distance(self):
        return "ip"

    def __str__(self):
        return f"TextToImage"

DATASETS = {
    'sift-1B': Sift1B(1000),
    'sift-1M': Sift1B(1),
    'deep-1B': Deep1B(),
    'text-to-image-1B': Text2Image1B(),
}
