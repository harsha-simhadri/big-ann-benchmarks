import gzip
import shutil
import math
import numpy
import os
import random
import sys
import struct
import time

import numpy as np
from scipy.sparse import csr_matrix

from urllib.request import urlretrieve

from .dataset_io import (
    xbin_mmap, download_accelerated, download, sanitize,
    knn_result_read, range_result_read, read_sparse_matrix,
    write_sparse_matrix,
)


BASEDIR = "data/"


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
    def get_private_queries(self):
        """
        Return (private_nq, d) array containing the private_nq private queries.
        """
        pass
    def get_groundtruth(self, k=None):
        """
        Return (nq, k) array containing groundtruth indices
        for each query."""
        pass

    def search_type(self):
        """
        "knn" or "range" or "knn_filtered"
        """
        pass

    def distance(self):
        """
        "euclidean" or "ip" or "angular"
        """
        pass

    def data_type(self):
        """
        "dense" or "sparse"
        """
        pass

    def default_count(self):
        """ number of neighbors to return """
        return 10

    def short_name(self):
        return f"{self.__class__.__name__}-{self.nb}"
    
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

    def prepare(self, skip_data=False, original_size=10**9):
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

        # private qs url
        if self.private_qs_url:
            outfile = os.path.join(self.basedir, self.private_qs_url.split("/")[-1])
            if os.path.exists(outfile):
                print("file %s already exists" % outfile)
            else:
                download(self.private_qs_url, outfile)

        # private gt url
        if self.private_gt_url:
            outfile = os.path.join(self.basedir, self.private_gt_url.split("/")[-1])
            if os.path.exists(outfile):
                print("file %s already exists" % outfile)
            else:
                download(self.private_gt_url, outfile)

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
            
            assert header[0] == original_size
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

    def get_data_in_range(self, start, end):
        assert start >= 0
        assert end <= self.nb
        filename = self.get_dataset_fn()
        x = xbin_mmap(filename, dtype=self.dtype, maxn=self.nb)
        return x[start:end]

    def search_type(self):
        return "knn"
    
    def data_type(self):
        return "dense"

    def get_groundtruth(self, k=None):
        assert self.gt_fn is not None
        fn = self.gt_fn.split("/")[-1]   # in case it's a URL
        assert self.search_type() in ("knn", "knn_filtered")

        I, D = knn_result_read(os.path.join(self.basedir, fn))
        assert I.shape[0] == self.nq
        if k is not None:
            assert k <= 100
            I = I[:, :k]
            D = D[:, :k]
        return I, D

    def get_dataset(self):
        assert self.nb <= 10**7, "dataset too large, use iterator"
        slice = next(self.get_dataset_iterator(bs=self.nb))
        return sanitize(slice)

    def get_queries(self):
        filename = os.path.join(self.basedir, self.qs_fn)
        x = xbin_mmap(filename, dtype=self.dtype)
        assert x.shape == (self.nq, self.d)
        return sanitize(x)

    def get_private_queries(self):
        assert self.private_qs_url is not None
        fn = self.private_qs_url.split("/")[-1]   # in case it's a URL
        filename = os.path.join(self.basedir, fn)
        x = xbin_mmap(filename, dtype=self.dtype)
        assert x.shape == (self.private_nq, self.d)
        return sanitize(x)

    def get_private_groundtruth(self, k=None):
        assert self.private_gt_url is not None
        fn = self.private_gt_url.split("/")[-1]   # in case it's a URL
        assert self.search_type() == "knn"

        I, D = knn_result_read(os.path.join(self.basedir, fn))
        assert I.shape[0] == self.private_nq
        if k is not None:
            assert k <= 100
            I = I[:, :k]
            D = D[:, :k]
        return I, D

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

        self.private_nq = 100000
        self.private_qs_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/FB_ssnpp_heldout_queries_3307fba121460a56.u8bin"
        self.private_gt_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/GT_1B_final_2bf4748c7817/FB_ssnpp.bin"

    def search_type(self):
        return "range"

    def default_count(self):
        """ for range search, this returns the squared range search radius """
        return 96237

    def distance(self):
        return "euclidean"

    def get_groundtruth(self, k=None):
        """ override the ground-truth function as this is the only range search dataset """
        assert self.gt_fn is not None
        fn = self.gt_fn.split("/")[-1]   # in case it's a URL
        return range_result_read(os.path.join(self.basedir, fn))

    def get_private_groundtruth(self, k=None):
        """ override the ground-truth function as this is the only range search dataset """
        assert self.private_gt_url is not None
        fn = self.private_gt_url.split("/")[-1]   # in case it's a URL
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

        self.private_nq = 10000
        self.private_qs_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/bigann/query.private.799253207.10K.u8bin"
        self.private_gt_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/GT_1B_final_2bf4748c7817/bigann-1B.bin"


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

        self.private_nq = 30000
        self.private_qs_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/deep1b/query.heldout.30K.fbin"
        self.private_gt_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/deep1b/gt100-heldout.30K.fbin"

        self.private_nq_large = 1000000
        self.private_qs_large_url = "https://storage.yandexcloud.net/yr-secret-share/ann-datasets-5ac0659e27/DEEP/query.private.1M.fbin"

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

        self.private_nq = 30000
        self.private_qs_url = "https://storage.yandexcloud.net/yandex-research/ann-datasets/T2I/query.heldout.30K.fbin"
        self.private_gt_url = "https://storage.yandexcloud.net/yandex-research/ann-datasets/T2I/gt100-heldout.30K.fbin"

        self.private_nq_large = 1000000
        self.private_qs_large_url = "https://storage.yandexcloud.net/yr-secret-share/ann-datasets-5ac0659e27/T2I/query.private.1M.fbin"

    def distance(self):
        return "ip"

    def get_query_train(self, maxn=10**6):
        xq_train = np.memmap(
            BASEDIR + "/text2image1B/query.learn.50M.fbin", offset=8,
            dtype='float32', shape=(maxn, 200), mode='r')
        return np.array(xq_train)

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
            "msturing-gt-100M" if self.nb_M == 100 else # back up subset_url + "GT_100M/msturing-100M"
            "msturing-gt-10M" if self.nb_M == 10 else # back up subset_url + "GT_100M/msturing-10M"
            "msturing-gt-1M" if self.nb_M == 1 else
            None
        )
        self.base_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/MSFT-TURING-ANNS/"
        self.basedir = os.path.join(BASEDIR, "MSTuringANNS")

        self.private_nq = 10000
        self.private_qs_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/MSFT-TURING-ANNS/testQuery10K.fbin"
        self.private_gt_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/MSFT-TURING-ANNS/gt100-private10K-queries.bin"

        self.private_nq_large = 99605
        self.private_qs_large_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/MSFT-TURING-ANNS/testQuery99605.fbin"
        self.private_gt_large_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/MSFT-TURING-ANNS/gt100-private99605-queries.bin"

    def distance(self):
        return "euclidean"

class MSTuringClustered10M(DatasetCompetitionFormat):
    def __init__(self):
        self.nb = 10**6 * 10
        self.d = 100
        self.nq = 10000
        self.dtype = "float32"
        self.ds_fn = "msturing-10M-clustered.fbin"
        self.qs_fn = "testQuery10K.fbin"
        self.gt_fn = "clu_msturing10M_gt100"
        
        self.base_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp23/clustered_data/msturing-10M-clustered/"
        self.basedir = os.path.join(BASEDIR, "MSTuring-10M-clustered")

        self.private_gt_url = None
        self.private_qs_url = None

    def distance(self):
        return "euclidean"
    
    def prepare(self, skip_data=False, original_size=10 ** 9):
        return super().prepare(skip_data, original_size = self.nb)
    
class MSTuringClustered30M(DatasetCompetitionFormat):
    def __init__(self):
        self.nb = 29998994
        self.d = 100
        self.nq = 10000
        self.dtype = "float32"
        self.ds_fn = "30M-clustered64.fbin"
        self.qs_fn = "testQuery10K.fbin"
        self.gt_fn = "clu_msturing30M_gt100"
        
        self.base_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp23/clustered_data/msturing-30M-clustered/"
        self.basedir = os.path.join(BASEDIR, "MSTuring-30M-clustered")

        self.private_gt_url = None
        self.private_qs_url = None

    def distance(self):
        return "euclidean"
    
    def prepare(self, skip_data=False, original_size=10 ** 9):
        return super().prepare(skip_data, original_size = self.nb)

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
            "msspacev-gt-100M" if self.nb_M == 100 else # backup subset_url + "GT_100M/msspacev-100M"
            "msspacev-gt-10M" if self.nb_M == 10 else # backup subset_url + "GT_10M/msspacev-10M"
            "msspacev-gt-1M" if self.nb_M == 1 else
            None
        )
        self.base_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/spacev1b/"
        self.basedir = os.path.join(BASEDIR, "MSSPACEV1B")

        self.private_nq = 30000
        self.private_qs_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/spacev1b/private_query_30k.bin"
        self.private_gt_url = "https://comp21storage.blob.core.windows.net/publiccontainer/comp21/spacev1b/gt100_private_query_30k.bin"

    def distance(self):
        return "euclidean"

class RandomClusteredDS(DatasetCompetitionFormat):
    def __init__(self, basedir="random-clustered"):
        self.nb = 10000
        self.nq = 1000
        self.d = 20
        self.dtype = 'float32'
        self.ds_fn = f"clu-random.fbin"
        self.qs_fn = f"queries_1000_20.fbin"
        self.gt_fn = f"clu_random_gt100"

        self.base_url="https://comp21storage.blob.core.windows.net/publiccontainer/comp23/clustered_data/random-xs-clustered/"

        self.basedir = os.path.join(BASEDIR, f"{basedir}{self.nb}")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        self.private_gt_url = None
        self.private_qs_url = None

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def __str__(self):
        return f"RandomClustered({self.nb})"

    def default_count(self):
        return 10
    
    def prepare(self, skip_data=False, original_size=10 ** 9):
        return super().prepare(skip_data, original_size = self.nb)

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

class YFCC100MDataset(DatasetCompetitionFormat):
    """ the 2023 competition """

    def __init__(self, filtered=True, dummy=False):
        self.filtered = filtered
        nb_M = 10
        self.nb_M = nb_M
        self.nb = 10**6 * nb_M
        self.d = 192
        self.nq = 100000
        self.dtype = "uint8"
        private_key = 12345
        if dummy:
            # for now it's dummy because we don't have the descriptors yet
            self.ds_fn = "dummy2.base.10M.u8bin"
            self.qs_fn = "dummy2.query.public.100K.u8bin"
            self.qs_private_fn = "dummy2.query.private.%d.100K.u8bin" % private_key
            self.ds_metadata_fn = "dummy2.base.metadata.10M.spmat"
            self.qs_metadata_fn = "dummy2.query.metadata.public.100K.spmat"
            self.qs_private_metadata_fn = "dummy2.query.metadata.private.%d.100K.spmat" % private_key
            if filtered:
                # no subset as the database is pretty small.
                self.gt_fn = "dummy2.GT.public.ibin"
            else:
                self.gt_fn = "dummy2.unfiltered.GT.public.ibin"

        else:
            # with Zilliz' CLIP descriptors
            self.ds_fn = "base.10M.u8bin"
            self.qs_fn = "query.public.100K.u8bin"
            self.qs_private_fn = "query.private.%d.100K.u8bin" % private_key
            self.ds_metadata_fn = "base.metadata.10M.spmat"
            self.qs_metadata_fn = "query.metadata.public.100K.spmat"
            self.qs_private_metadata_fn = "query.metadata.private.%d.100K.spmat" % private_key
            if filtered:
                # no subset as the database is pretty small.
                self.gt_fn = "GT.public.ibin"
            else:
                self.gt_fn = "unfiltered.GT.public.ibin"

            # data is uploaded but download script not ready.
        self.base_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/yfcc100M/"
        self.basedir = os.path.join(BASEDIR, "yfcc100M")

        self.private_nq = 100000
        self.private_qs_url = self.base_url + ""
        self.private_gt_url = self.base_url + ""

        self.metadata_base_url = self.base_url + self.ds_metadata_fn
        self.metadata_queries_url = self.base_url + self.qs_metadata_fn
        self.metadata_private_queries_url = ""

    def prepare(self, skip_data=False):
        super().prepare(skip_data, 10**7)
        for fn in (self.metadata_base_url, self.metadata_queries_url, self.metadata_private_queries_url):
            if fn:
                outfile = os.path.join(self.basedir, fn.split("/")[-1])
                if os.path.exists(outfile):
                    print("file %s already exists" % outfile)
                else:
                    download(fn, outfile)

    def get_dataset_metadata(self):
        return read_sparse_matrix(os.path.join(self.basedir, self.ds_metadata_fn))

    def get_queries_metadata(self):
        return read_sparse_matrix(os.path.join(self.basedir, self.qs_metadata_fn))
    
    def get_private_queries_metadata(self):
        return read_sparse_matrix(os.path.join(self.basedir, self.qs_private_metadata_fn))
    
    def distance(self):
        return "euclidean"

    def search_type(self):
        if self.filtered:
            return "knn_filtered"
        else:
            return "knn"


def _strip_gz(filename):
    if not filename.endswith('.gz'):
        raise RuntimeError(f"expected a filename ending with '.gz'. Received: {filename}")
    return filename[:-3]


def _gunzip_if_needed(filename):
    if filename.endswith('.gz'):
        print('unzipping', filename, '...', end=" ", flush=True)

        with gzip.open(filename, 'rb') as f_in, open(_strip_gz(filename), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

        os.remove(filename)
        print('done.')


class SparseDataset(DatasetCompetitionFormat):
    """ the 2023 competition
        Sparse vectors for sparse max inner product search
        Data is based on MSMARCO passage retrieval data (text passages and queries),
        embedded via the SPLADE model.

        The class overrides several methods since the sparse format is different than other datasets.
    """

    def __init__(self, version="small"):

        versions = {"small": (100000, "base_small.csr.gz", "base_small.dev.gt"),
                    "1M": (1000000, "base_1M.csr.gz", "base_1M.dev.gt"),
                    "full": (8841823, "base_full.csr.gz", "base_full.dev.gt")}

        assert version in versions, f'version="{version}" is invalid. Please choose one of {list(versions.keys())}.'

        self.nb = versions[version][0]
        self.nq = 6980
        self.private_nq = 0  # TBD

        self.ds_fn = versions[version][1]
        self.qs_fn = "queries.dev.csr.gz"

        self.qs_private_fn = ""  # TBD

        self.base_url = "https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/"
        self.basedir = os.path.join(BASEDIR, "sparse")

        self.gt_fn = versions[version][2]
        self.private_gt = ""  # TBD

        self.d = np.nan # this is only for compatibility with printing the name of the class

    def prepare(self, skip_data=False):
        # downloads the datasets and unzips (if necessary).

        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        # start with the small ones...
        for fn in [self.qs_fn, self.gt_fn]:
            if fn is None:
                continue

            sourceurl = os.path.join(self.base_url, fn)
            outfile = os.path.join(self.basedir, fn)
            if outfile.endswith('.gz'):
                # check if the unzipped file already exists
                if os.path.exists(_strip_gz(outfile)):
                    print("unzipped version of file %s already exists" % outfile)
                    continue

            if os.path.exists(outfile):
                print("file %s already exists" % outfile)
                _gunzip_if_needed(outfile)
                continue
            download(sourceurl, outfile)
            _gunzip_if_needed(outfile)
        # # private qs url: todo

        if skip_data:
            return

        fn = self.ds_fn
        sourceurl = os.path.join(self.base_url, fn)
        outfile = os.path.join(self.basedir, fn)
        if outfile.endswith('.gz'):
            # check if the unzipped file already exists
            unzipped_outfile = _strip_gz(outfile)
            if os.path.exists(unzipped_outfile):
                print("unzipped version of file %s already exists" % outfile)
                return
        if os.path.exists(outfile):
            print("file %s already exists" % outfile)
            _gunzip_if_needed(outfile)
            return
        download(sourceurl, outfile)
        _gunzip_if_needed(outfile)

    def get_dataset_fn(self):
        fn = _strip_gz(os.path.join(self.basedir, self.ds_fn))
        if os.path.exists(fn):
            return fn
        raise RuntimeError("file not found")

    def get_dataset_iterator(self, bs=512, split=(1, 0)):
        assert split == (1,0), 'No sharding supported yet.'  # todo

        filename = self.get_dataset_fn()

        x = read_sparse_matrix(filename, do_mmap=True)
        assert x.shape[0] == self.nb

        for j0 in range(0, self.nb, bs):
            j1 = min(j0 + bs, self.nb)
            yield x[j0:j1, :]

        # i0, i1 = self.nb * rank // nsplit, self.nb * (rank + 1) // nsplit
        # x = xbin_mmap(filename, dtype=self.dtype, maxn=self.nb)
        # assert x.shape == (self.nb, self.d)

        # for j0 in range(i0, i1, bs):
        #     j1 = min(j0 + bs, i1)
        #     yield sanitize(x[j0:j1])


    def get_groundtruth(self, k=None):
        assert self.gt_fn is not None
        assert self.search_type() == "knn"

        I, D = knn_result_read(os.path.join(self.basedir, self.gt_fn))
        assert I.shape[0] == self.nq
        if k is not None:
            assert k <= 10
            I = I[:, :k]
            D = D[:, :k]
        return I, D

    def get_dataset(self):
        assert self.nb <= 10 ** 6, "dataset too large, use iterator"
        return next(self.get_dataset_iterator(bs=self.nb))

    def get_queries(self):
        filename = os.path.join(self.basedir, self.qs_fn)
        print(filename)
        x = read_sparse_matrix(_strip_gz(filename), do_mmap=False)  # read the queries file. It is a small file, so no need to mmap
        assert x.shape[0] == self.nq
        return x

    def get_private_queries(self):
        raise RuntimeError("not implemented yet")

    def get_private_groundtruth(self, k=None):
        raise RuntimeError("not implemented yet")

    def distance(self):
        return "ip"

    def search_type(self):
        return "knn"
    
    def data_type(self):
        return "sparse"


class RandomDS(DatasetCompetitionFormat):
    def __init__(self, nb, nq, d, basedir="random"):
        self.nb = nb
        self.nq = nq
        self.d = d
        self.dtype = 'float32'
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, f"{basedir}{self.nb}")
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

    def default_count(self):
        return 10
    

class RandomFilterDS(RandomDS):
    def __init__(self, nb, nq, d):
        super().__init__(nb, nq, d, "random-filter")
        self.ds_metadata_fn = f"data_metadata_{self.nb}_{self.d}"
        self.qs_metadata_fn = f"queries_metadata_{self.nb}_{self.d}"

    def prepare(self, skip_data=False):
        import sklearn.datasets
        import sklearn.model_selection
        from sklearn.neighbors import NearestNeighbors

        print(f"Preparing datasets with {self.nb} random points, {self.nq} queries, and two filters.")

        X, _ = sklearn.datasets.make_blobs(
            n_samples=self.nb + self.nq, n_features=self.d,
            centers=self.nq, random_state=1)

        data, queries = sklearn.model_selection.train_test_split(
            X, test_size=self.nq, random_state=1) 

        filter1 = [1, 2]
        filter2 = [3, 4]       

        assert self.nb % 2 == 0

        # simple filters, first half of the data matches second 
        # half of the queries, and vice versa

        data_filters = [filter1] * (self.nb // 2) + [filter2] * (self.nb // 2)
        query_filters = [filter2] * (self.nq // 2) + [filter1] * (self.nq // 2)

        assert len(data_filters) == data.shape[0]

        with open(os.path.join(self.basedir, self.ds_fn), "wb") as f:
            np.array([self.nb, self.d], dtype='uint32').tofile(f)
            data.astype('float32').tofile(f)
        with open(os.path.join(self.basedir, self.qs_fn), "wb") as f:
            np.array([self.nq, self.d], dtype='uint32').tofile(f)
            queries.astype('float32').tofile(f) 

        data_indices = np.array(data_filters).flatten()
        data_indptr = [2 * i for i in range(self.nb)] + [2 * self.nb]
        data_data = [1] * self.nb * 2
        data_metadata_sparse = csr_matrix((data_data, data_indices, data_indptr))

        query_indices = np.array(query_filters).flatten()
        query_indptr = [2 * i for i in range(self.nq)] + [2 * self.nq]
        query_data = [1] * self.nq * 2
        query_metadata_sparse = csr_matrix((query_data, query_indices, query_indptr))

        write_sparse_matrix(data_metadata_sparse, 
                            os.path.join(self.basedir, self.ds_metadata_fn))
        write_sparse_matrix(query_metadata_sparse, 
                            os.path.join(self.basedir, self.qs_metadata_fn))

        print("Computing groundtruth")

        n_neighbors = 100

        nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean", algorithm='brute').fit(data[:self.nb // 2])
        DD, II = nbrs.kneighbors(queries[self.nq // 2:])

        nbrs = NearestNeighbors(n_neighbors=n_neighbors, metric="euclidean", algorithm='brute').fit(data[self.nb // 2: ])
        D, I = nbrs.kneighbors(queries[:self.nq // 2])

        D = np.concatenate((D, DD))
        I = np.concatenate((I + self.nb // 2, II))

        with open(os.path.join(self.basedir, self.gt_fn), "wb") as f:
            np.array([self.nq, n_neighbors], dtype='uint32').tofile(f)
            I.astype('uint32').tofile(f)
            D.astype('float32').tofile(f)

    def get_dataset_metadata(self):
        return read_sparse_matrix(os.path.join(self.basedir, self.ds_metadata_fn))

    def get_queries_metadata(self):
        return read_sparse_matrix(os.path.join(self.basedir, self.qs_metadata_fn))
    
    def search_type(self):
        return "knn_filtered"

    def __str__(self):
        return f"RandomFilter({self.nb})"



DATASETS = {
    'bigann-1B': lambda : BigANNDataset(1000),
    'bigann-100M': lambda : BigANNDataset(100),
    'bigann-10M': lambda : BigANNDataset(10),

    'deep-1B': lambda : Deep1BDataset(),
    'deep-100M': lambda : Deep1BDataset(100),
    'deep-10M': lambda : Deep1BDataset(10),

    'ssnpp-1B': lambda : SSNPPDataset(1000),
    'ssnpp-10M': lambda : SSNPPDataset(10),
    'ssnpp-100M': lambda : SSNPPDataset(100),
    'ssnpp-1M': lambda : SSNPPDataset(1),

    'text2image-1B': lambda : Text2Image1B(),
    'text2image-1M': lambda : Text2Image1B(1),
    'text2image-10M': lambda : Text2Image1B(10),
    'text2image-100M': lambda : Text2Image1B(100),

    'msturing-1B': lambda : MSTuringANNS(1000),
    'msturing-100M': lambda : MSTuringANNS(100),
    'msturing-10M': lambda : MSTuringANNS(10),
    'msturing-1M': lambda : MSTuringANNS(1),

    'msturing-10M-clustered': lambda: MSTuringClustered10M(),
    'msturing-30M-clustered': lambda: MSTuringClustered30M(),

    'msspacev-1B': lambda : MSSPACEV1B(1000),
    'msspacev-100M': lambda : MSSPACEV1B(100),
    'msspacev-10M': lambda : MSSPACEV1B(10),
    'msspacev-1M': lambda : MSSPACEV1B(1),

    'yfcc-10M': lambda: YFCC100MDataset(),
    'yfcc-10M-unfiltered': lambda: YFCC100MDataset(filtered=False),
    'yfcc-10M-dummy': lambda: YFCC100MDataset(dummy=True),
    'yfcc-10M-dummy-unfiltered': lambda: YFCC100MDataset(filtered=False, dummy=True),

    'sparse-small': lambda: SparseDataset("small"),
    'sparse-1M': lambda: SparseDataset("1M"),
    'sparse-full': lambda: SparseDataset("full"), 

    'random-xs': lambda : RandomDS(10000, 1000, 20),
    'random-s': lambda : RandomDS(100000, 1000, 50),

    'random-xs-clustered': lambda: RandomClusteredDS(),

    'random-range-xs': lambda : RandomRangeDS(10000, 1000, 20),
    'random-range-s': lambda : RandomRangeDS(100000, 1000, 50),

    'random-filter-s': lambda : RandomFilterDS(100000, 1000, 50),

}
