import h5py
import numpy
import os
import random
import sys
import progressbar
import struct

from urllib.request import urlopen
from urllib.request import urlretrieve

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def download(src, dst=None):
    if not dst:
        dst = "data/" + src.split("/")[-1]
    if not os.path.exists(dst):
        print('downloading %s -> %s...' % (src, dst))
        urlretrieve(src, dst, show_progress)


# Everything below this line is related to creating datasets
# TODO: This is supposed to be carried out in a docker container

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

    def query_type(self):
        """
        "knn" or "range"
        """
        pass

    def __str__(self):
        """
        Return identifier.
        """
        pass

def bvecs_mmap(fname):
    x = numpy.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def ivecs_read(fname):
    a = numpy.fromfile(fname, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy()

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

class Sift1B(Dataset):
    def __init__(self, nb_M=1000):
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 128
        self.nq = 10000

    def prepare(self):
        import gzip, tarfile
        ds_fn = "bigann_base.bvecs"
        ds_url = f"ftp://ftp.irisa.fr/local/texmex/corpus/{ds_fn}.gz"
        qs_fn = "bigann_query.bvecs"
        qs_url = f"ftp://ftp.irisa.fr/local/texmex/corpus/{qs_fn}.gz"
        gt_fn = "bigann_gnd.tar.gz"
        gt_url = f"ftp://ftp.irisa.fr/local/texmex/corpus/{gt_fn}"

        for fn in [ds_fn, qs_fn]:
            download(ds_url, f"data/{fn}.gz")
            with gzip.open(f"data/{fn}.gz") as g:
                with open(f"data/{fn}", "wb") as f:
                    f.write(g.read())

        download(gt_url, f"data/{gt_fn}")
        with tarfile.open(f"data/{gt_fn}") as f:
            f.extractall("data/")

    def get_dataset_fn(self):
        return 'data/bigann_base.bvecs'

    def get_dataset(self):
        assert self.nb_M < 100, "dataset too large, use iterator"
        return sanitize(bvecs_mmap('data/bigann_base.bvecs')[:self.nb])

    def get_dataset_iterator(self, bs=512, split=(1,0)):
        xb = bvecs_mmap('data/bigann_base.bvecs')
        nsplit, rank = split
        i0, i1 = self.nb * rank // nsplit, self.nb * (rank + 1) // nsplit
        for j0 in range(i0, i1, bs):
            yield sanitize(xb[j0: min(j0 + bs, i1)])

    def get_queries(self):
        return sanitize(bvecs_mmap('data/bigann_query.bvecs')[:])

    def get_groundtruth(self, k=None):
        gt = ivecs_read('data/gnd/idx_%dM.ivecs' % self.nb_M)
        if k is not None:
            assert k <= 100
            gt = gt[:, :k]
        return gt

    def distance(self):
        return "Euclidean"

    def query_type(self):
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

    def query_type(self):
        return "knn"

    def distance(self):
        return "Euclidean"

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
        return "IP"

    def __str__(self):
        return f"TextToImage"

DATASETS = {
    'sift-1B': Sift1B(1000),
    'sift-1M': Sift1B(1),
    'deep-1B': Deep1B(),
    'text-to-image-1B': Text2Image1B(),
}
