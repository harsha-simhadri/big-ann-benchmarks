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



def load_data(path):
    import torch
    with open(path, "rb") as f:
        nb_d = np.fromfile(f, dtype=np.int32, count=2)
        nb, d = nb_d[0], nb_d[1]
        vectors = np.fromfile(f, dtype=np.int32).reshape((nb, d))
    vectors_tensor = torch.tensor(vectors, dtype=torch.float32)
    return nb, d, vectors_tensor

def sample_vectors(vectors, nb, nq):
    import torch
    num = vectors.shape[0]
    if num < nb + nq:
        raise ValueError("Not enough vectors to sample!")

    indices = torch.randperm(nb + nq)

    index_vectors = vectors[indices[:nb]]

    query_vectors = vectors[indices[nb:nb + nq]]
    return index_vectors, query_vectors

def save_data(vectors_index_tensor, dataset=None, type=None, basedir=None):
    import torch
    if basedir is None:
        basedir = Path.cwd()
        if dataset is not None:
            basedir = basedir/'dataset'/dataset
            basedir.mkdir(parents=True, exist_ok=True)

    if isinstance(vectors_index_tensor, np.ndarray):
        vectors_index_tensor = torch.tensor(vectors_index_tensor, dtype=torch.float32)

    # 获取数据的维度
    nb = vectors_index_tensor.shape[0]  # 索引向量的数量
    d = vectors_index_tensor.shape[1]  # 向量的维度

    path = os.path.join(basedir, type + '_' + str(nb) + '_' + str(d))
    # 保存索引数据
    with open(path, "wb") as f:
        # 保存 nb 和 d
        np.array([nb, d], dtype='uint32').tofile(f)
        # 保存索引向量
        vectors_index_tensor.numpy().astype('float32').tofile(f)

    return path

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
        if self.nb != original_size:
            outfile = outfile + '.crop_nb_%d' % self.nb
            
        if os.path.exists(outfile):
            print("file %s already exists" % outfile)
            return
        if self.nb == 10**9:
            download_accelerated(sourceurl, outfile)
        elif self.nb == original_size:
            #if nb vectors is less than 1 billion, can download the whole dataset in the normal fashion without a cropped header
            download(sourceurl, outfile)
        else:
            # download cropped version of file
            file_size = 8 + self.d * self.nb * np.dtype(self.dtype).itemsize
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
        else:
            raise RuntimeError("file %s not found" %fn)

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
        filename = os.path.join(self.basedir, self.qs_private_fn)
        x = xbin_mmap(filename, dtype=self.dtype)
        assert x.shape == (self.private_nq, self.d)
        return sanitize(x)

    def get_private_groundtruth(self, k=None):
        assert self.private_gt_fn is not None
        assert self.search_type() in ("knn", "knn_filtered")

        I, D = knn_result_read(os.path.join(self.basedir, self.private_gt_fn))
        assert I.shape[0] == self.private_nq
        if k is not None:
            assert k <= 100
            I = I[:, :k]
            D = D[:, :k]
        return I, D

class BillionScaleDatasetCompetitionFormat(DatasetCompetitionFormat):

    def get_dataset_fn(self):
        fn = os.path.join(self.basedir, self.ds_fn)
        if self.nb != 10**9:
            fn += '.crop_nb_%d' % self.nb
        if os.path.exists(fn):
            return fn
        else:
            raise RuntimeError("file %s not found" %fn)


subset_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/"

class SSNPPDataset(BillionScaleDatasetCompetitionFormat):
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
        self.private_qs_url = ""#https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/FB_ssnpp_heldout_queries_3307fba121460a56.u8bin"
        self.private_gt_url = ""#https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/GT_1B_final_2bf4748c7817/FB_ssnpp.bin"

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

class BigANNDataset(BillionScaleDatasetCompetitionFormat):
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
        # self.gt_fn = "https://comp21storage.z5.web.core.windows.net/comp21/bigann/public_query_gt100.bin" if self.nb == 10**9 else None
        self.base_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/bigann/"
        self.basedir = os.path.join(BASEDIR, "bigann")

        self.private_nq = 10000
        self.private_qs_url = ""#https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/bigann/query.private.799253207.10K.u8bin"
        self.private_gt_url = ""#https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/GT_1B_final_2bf4748c7817/bigann-1B.bin"


    def distance(self):
        return "euclidean"

class Deep1BDataset(BillionScaleDatasetCompetitionFormat):
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
        self.private_qs_url = "https://comp21storage.z5.web.core.windows.net/comp21/deep1b/query.heldout.30K.fbin"
        self.private_gt_url = "https://comp21storage.z5.web.core.windows.net/comp21/deep1b/gt100-heldout.30K.fbin"

        self.private_nq_large = 1000000
        self.private_qs_large_url = "https://storage.yandexcloud.net/yr-secret-share/ann-datasets-5ac0659e27/DEEP/query.private.1M.fbin"

    def distance(self):
        return "euclidean"



class Text2Image1B(BillionScaleDatasetCompetitionFormat):
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

class MSTuringANNS(BillionScaleDatasetCompetitionFormat):
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
        self.base_url = "https://comp21storage.z5.web.core.windows.net/comp21/MSFT-TURING-ANNS/"
        self.basedir = os.path.join(BASEDIR, "MSTuringANNS")

        self.private_nq = 10000
        self.private_qs_url = "https://comp21storage.z5.web.core.windows.net/comp21/MSFT-TURING-ANNS/testQuery10K.fbin"
        self.private_gt_url = "https://comp21storage.z5.web.core.windows.net/comp21/MSFT-TURING-ANNS/gt100-private10K-queries.bin"

        self.private_nq_large = 99605
        self.private_qs_large_url = "https://comp21storage.z5.web.core.windows.net/comp21/MSFT-TURING-ANNS/testQuery99605.fbin"
        self.private_gt_large_url = "https://comp21storage.z5.web.core.windows.net/comp21/MSFT-TURING-ANNS/gt100-private99605-queries.bin"

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
        
        self.base_url = "https://comp21storage.z5.web.core.windows.net/comp23/clustered_data/msturing-10M-clustered/"
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
        
        self.base_url = "https://comp21storage.z5.web.core.windows.net/comp23/clustered_data/msturing-30M-clustered/"
        self.basedir = os.path.join(BASEDIR, "MSTuring-30M-clustered")

        self.private_gt_url = None
        self.private_qs_url = None

    def distance(self):
        return "euclidean"
    
    def prepare(self, skip_data=False, original_size=10 ** 9):
        return super().prepare(skip_data, original_size = self.nb)

class MSSPACEV1B(BillionScaleDatasetCompetitionFormat):
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
        self.base_url = "https://comp21storage.z5.web.core.windows.net/comp21/spacev1b/"
        self.basedir = os.path.join(BASEDIR, "MSSPACEV1B")

        self.private_nq = 30000
        self.private_qs_url = "https://comp21storage.z5.web.core.windows.net/comp21/spacev1b/private_query_30k.bin"
        self.private_gt_url = "https://comp21storage.z5.web.core.windows.net/comp21/spacev1b/gt100_private_query_30k.bin"

    def distance(self):
        return "euclidean"

'''
The base vectors of Wikipedia-Cohere consist of 35 million cohere embeddings of the title and text of Wikipedia English articles. 
The 5000 query vectors consist of 5000 cohere embeddings of the title and text of Wikipedia simple articles.
See https://huggingface.co/datasets/Cohere/wikipedia-22-12-en-embeddings?row=2 for more details.
'''
class WikipediaDataset(BillionScaleDatasetCompetitionFormat):
    def __init__(self, nb=35000000):
        self.nb = nb
        self.d = 768
        self.nq = 5000
        self.dtype = "float32"
        self.ds_fn = "wikipedia_base.bin"
        self.qs_fn = "wikipedia_query.bin"
        self.gt_fn = (
            "wikipedia-35M" if self.nb == 35000000 else
            "wikipedia-1M" if self.nb == 1000000 else
            "wikipedia-100K" if self.nb == 100000 else
            None
        )
        self.basedir = os.path.join(BASEDIR, "wikipedia_cohere")
        self.base_url = "https://comp21storage.z5.web.core.windows.net/wiki-cohere-35M/"

        self.private_qs_url = None
        self.private_gt_url = None

    def prepare(self, skip_data=False, original_size=35000000):
        return super().prepare(skip_data, 35000000)

    def get_dataset_fn(self):
        fn = os.path.join(self.basedir, self.ds_fn)
        if self.nb != 35000000:
            fn += '.crop_nb_%d' % self.nb
        if os.path.exists(fn):
            return fn
        else:
            raise RuntimeError("file %s not found" %fn)
        
    def get_dataset(self):
        slice = next(self.get_dataset_iterator(bs=self.nb))
        return sanitize(slice)

    def distance(self):
        return "ip"

'''
The MSMarco Web Search dataset has 100,924,960 base vectors consisting of embeddings of web documents 
from the ClueWeb22 document dataset, while its 9,374 queries correspond to web queries collected from 
the Microsoft Bing search engine.
See https://github.com/microsoft/MS-MARCO-Web-Search for more details.
'''
class MSMarcoWebSearchDataset(BillionScaleDatasetCompetitionFormat):
    def __init__(self, nb=101070374):
        self.nb = nb
        self.d = 768
        self.nq = 9376
        self.dtype = "float32"
        self.ds_fn = "vectors.bin"
        self.qs_fn = "query.bin"
        self.gt_fn = (
            "msmarco-100M-gt100" if self.nb == 101070374 else
            "msmarco-10M-gt100" if self.nb == 10000000 else
            "msmarco-1M-gt100" if self.nb == 1000000 else
            None
        )
        self.basedir = os.path.join(BASEDIR, "msmarco_websearch")
        self.base_url = "https://msmarco.z22.web.core.windows.net/msmarcowebsearch/vectors/SimANS/passage_vectors/vectors.bin"
        self.query_url = "https://msmarco.z22.web.core.windows.net/msmarcowebsearch/vectors/SimANS/query_vectors/vectors.bin"
        self.gt_url = "https://comp21storage.z5.web.core.windows.net/msmarcowebsearch/"

    def prepare(self, skip_data=False, original_size=101070374):
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        qs_outfile = os.path.join(self.basedir, self.qs_fn)
        download(self.query_url, qs_outfile)

        gt_outfile = os.path.join(self.basedir, self.gt_fn)
        groundtruth_url = os.path.join(self.gt_url, self.gt_fn)
        download(groundtruth_url, gt_outfile)

        if skip_data:
            return

        fn = self.ds_fn
        sourceurl = self.base_url
        outfile = os.path.join(self.basedir, fn)
        if os.path.exists(outfile):
            print("file %s already exists" % outfile)
            return
        if self.nb == original_size:
            download(self.base_url, outfile)
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
        if self.nb != 101070374:
            fn += '.crop_nb_%d' % self.nb
        if os.path.exists(fn):
            return fn
        else:
            raise RuntimeError("file %s not found" %fn)
        
    def get_dataset(self):
        slice = next(self.get_dataset_iterator(bs=self.nb))
        return sanitize(slice)

    def distance(self):
        return "ip"

'''
The OpenAI-ArXiv dataset consists of 2321096 1536-dimensional OpenAI ada-002 
embeddings of the abstracts of ArXiv papers, with 20000 queries drawn from the same source. 
The ArXiv dataset was released by Cornell University and can be found here:
https://www.kaggle.com/datasets/Cornell-University/arxiv
'''
class OpenAIArXivDataset(DatasetCompetitionFormat):
    def __init__(self, nb=2321096):
        self.nb = nb
        self.d = 1536
        self.nq = 20000
        self.dtype = "float32"
        self.ds_fn =  "openai_base.bin"
        self.qs_fn = "openai_query.bin"
        self.gt_fn = (
            "openai-2M" if self.nb == 2321096 else
            "openai-100K" if self.nb == 100000 else
            None
        )
        self.basedir = os.path.join(BASEDIR, "OpenAIArXiv")
        self.base_url = "https://comp21storage.z5.web.core.windows.net/arxiv-openaiv2-2M"

        self.private_qs_url = None
        self.private_gt_url = None

    def prepare(self, skip_data=False, original_size=2321096):
        return super().prepare(skip_data, 2321096)

    def get_dataset_fn(self):
        fn = os.path.join(self.basedir, self.ds_fn)
        if self.nb != 2321096:
            fn += '.crop_nb_%d' % self.nb
        if os.path.exists(fn):
            return fn
        else:
            raise RuntimeError("file %s not found" %fn)
        
    def get_dataset(self):
        slice = next(self.get_dataset_iterator(bs=self.nb))
        return sanitize(slice)

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

        self.base_url="https://comp21storage.z5.web.core.windows.net/comp23/clustered_data/random-xs-clustered/"

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
        private_key = 2727415019
        self.gt_private_fn = ""

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
                self.gt_private_fn = "GT.private.%d.ibin" % private_key
            else:
                self.gt_fn = "unfiltered.GT.public.ibin"      

            self.private_gt_fn = "GT.private.%d.ibin" % private_key

            # data is uploaded but download script not ready.
        self.base_url = "https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/yfcc100M/"
        self.basedir = os.path.join(BASEDIR, "yfcc100M")

        self.private_nq = 100000
        self.private_qs_url = self.base_url + self.qs_private_fn
        self.private_gt_url = self.base_url + self.gt_private_fn

        self.metadata_base_url = self.base_url + self.ds_metadata_fn
        self.metadata_queries_url = self.base_url + self.qs_metadata_fn
        self.metadata_private_queries_url = self.base_url + self.qs_private_metadata_fn

    def prepare(self, skip_data=False):
        super().prepare(skip_data, 10**7)
        for fn in (self.metadata_base_url, self.metadata_queries_url, 
                   self.metadata_private_queries_url):
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
                    "full": (8841823, "base_full.csr.gz", "base_full.dev.gt"),
                    }

        assert version in versions, f'version="{version}" is invalid. Please choose one of {list(versions.keys())}.'

        self.nb = versions[version][0]
        self.nq = 6980
        self.private_nq = 7000

        self.ds_fn = versions[version][1]
        self.qs_fn = "queries.dev.csr.gz"

        self.qs_private_fn = "queries.hidden.csr.gz"

        self.base_url = "https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/"
        self.basedir = os.path.join(BASEDIR, "sparse")

        self.gt_fn = versions[version][2]
        self.private_gt = "base_full.hidden.gt"
        self.private_gt_url = self.base_url + self.private_gt

        self.d = np.nan # this is only for compatibility with printing the name of the class

    def prepare(self, skip_data=False):
        # downloads the datasets and unzips (if necessary).

        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        # start with the small ones...
        for fn in [self.qs_fn, self.gt_fn, self.qs_private_fn, self.private_gt]:
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
        assert self.qs_private_fn
        filename = os.path.join(self.basedir, self.qs_private_fn)
        print(filename)
        x = read_sparse_matrix(_strip_gz(filename), do_mmap=False)  # read the queries file. It is a small file, so no need to mmap
        assert x.shape[0] == self.private_nq
        return x
    
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


class OpenAIEmbedding1M(DatasetCompetitionFormat):
    def __init__(self, query_selection_random_seed):
        self.seed = query_selection_random_seed
        self.basedir = os.path.join(BASEDIR, "openai-embedding-1M")
        self.d = 1536
        self.nb = 1000000
        self.nq = 100000
        self.ds_fn = "base1m.fbin"
        self.qs_fn = "queries_100k.fbin"
        self.gt_fn = "gt_1m_100k.bin"

    def prepare(self, skip_data=False):
        from datasets import load_dataset
        import tqdm
        import numpy as np
        import faiss

        os.makedirs(self.basedir, exist_ok=True)

        print("Downloading dataset...")
        dataset = load_dataset("KShivendu/dbpedia-entities-openai-1M", split="train")

        print("Converting to competition format...")
        data = []
        for row in tqdm.tqdm(dataset, desc="Collecting vectors", unit="vector"):
            data.append(np.array(row["openai"], dtype=np.float32))
        data = np.array(data)
        with open(os.path.join(self.basedir, self.ds_fn), "wb") as f:
            np.array(data.shape, dtype=np.uint32).tofile(f)
            data.tofile(f)

        print(f"Selecting queries using random seed: {self.seed}...")
        rand = np.random.RandomState(self.seed)
        rand.shuffle(data)
        queries = data[:100000]
        with open(os.path.join(self.basedir, self.qs_fn), "wb") as f:
            np.array(queries.shape, dtype=np.uint32).tofile(f)
            queries.tofile(f)

        k = 100
        batch_size = 1000
        print(f"Computing groundtruth for k = {k} using batch_size = {batch_size}...")
        index = faiss.IndexFlatIP(data.shape[1])
        index.add(data)
        ids = np.zeros((len(queries), k), dtype=np.uint32)
        distances = np.zeros((len(queries), k), dtype=np.float32)
        for i in tqdm.tqdm(
            range(0, len(queries), batch_size),
            total=len(queries) // batch_size,
            desc="Brute force scan using FAISS",
            unit=" batch",
        ):
            D, I = index.search(queries[i : i + batch_size], k)
            ids[i : i + batch_size] = I
            distances[i : i + batch_size] = D
        with open(os.path.join(self.basedir, self.gt_fn), "wb") as f:
            np.array(ids.shape, dtype=np.uint32).tofile(f)
            ids.tofile(f)
            distances.tofile(f)

        print(f"Done. Dataset files are in {self.basedir}.")

    def search_type(self):
        """
        "knn" or "range" or "knn_filtered"
        """
        return "knn"

    def distance(self):
        """
        "euclidean" or "ip" or "angular"
        """
        return "eculidean"

    def data_type(self):
        """
        "dense" or "sparse"
        """
        return "dense"

    def default_count(self):
        """number of neighbors to return"""
        return 10

    def short_name(self):
        return f"{self.__class__.__name__}-{self.nb}"

class GLOVE(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 100
        self.nb = 1192514
        self.nq = 200
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "GLOVE")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("GLOVE has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1m06VVmXmklHr7QZzdz6w8EtYmuRGIl9s?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors  = load_data(self.basedir+'/data_1192514_100')
            index_vectors, query_vectors = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class MSONG(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 420
        self.nb = 992272
        self.nq = 200
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "MSONG")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("MSONG has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1TnLNJNVqyFrEzKGfQVdvUC8Al-tmjVg0?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_992272_420')
            index_vectors, query_vectors = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class SUN(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 512
        self.nb = 79106
        self.nq = 200
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "SUN")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("SUN has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1gNK1n-do-7d5N-Z1tuAoXe5Xq3I8fZIH?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_79106_512')
            index_vectors, query_vectors = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class DPR(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 768
        self.nb = 100000
        self.nq = 100
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "DPR")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)


    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("DPR has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1-zF1brIbWv209I8qU_InTfHbQQXbHMi2?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir + '/data_100000_768')
            index_vectors, query_vectors = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class REDDIT(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 768
        self.nb = 100000
        self.nq = 2000
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"query_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "REDDIT")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)


    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("REDDIT has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1Q2DWWtEnCuh3_lB_UonU7l5EHGy7pBmG?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_100000_768')
            index_vectors, _ = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)

            num, dim, vectors = load_data(self.basedir+'/queries_2000_768')
            _, query_vectors = sample_vectors(vectors, 0, self.nq)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class COCO(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 768
        self.nb = 10000
        self.nq = 100
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "COCO")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)


    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("COCO has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1Hp6SI8YOFPdWbmC1a4_-1dZWxZH3CHMS?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir + '/data_100000_768')
            index_vectors, query_vectors = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class CIRR(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 768
        self.nb = 10000
        self.nq = 100
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "CIRR")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("CIRR has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = " https://drive.google.com/drive/folders/1zCZWG3DX_4xnAC0kZv1IxEqLD0qv6kOy?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir + '/data_101335_768')
            index_vectors, _ = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)

            num, dim, vectors = load_data(self.basedir + '/queries_4181_768query')
            _, query_vectors = sample_vectors(vectors, 0, self.nq)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class TREVI(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 4096
        self.nb = 99900
        self.nq = 200
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "TREVI")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("TREVI has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1MEhmUP_1H01JUdWTs80PCIq6880jkf-H?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_99900_4096')
            index_vectors, query_vectors = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class WTE(DatasetCompetitionFormat):
    def __init__(self, dataset_name):
        self.d = 768
        self.nb = 100000
        self.nq = 100
        self.dtype = "float32"
        self.dataset_name = dataset_name
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "WTE" + str(dataset_name))
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)


    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("WTE" + self.dataset_name + " has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url_dict = {'-0.05':'https://drive.google.com/drive/folders/1W26G6ZiI37uPy9sy80t-LsoA9BwYivnu?usp=sharing'
                                , '-0.1':'https://drive.google.com/drive/folders/1W0HTj3XBBpPHMymYDAqKS8R0-ENhgTMC?usp=sharing'
                                , '-0.2':'https://drive.google.com/drive/folders/1riZJIAA_lIEIC3ohNCuPR0dvhOTO67W2?usp=sharing'
                                , '-0.4':'https://drive.google.com/drive/folders/1SmKVC-3SUR3n7NDxO33kD4axNqrB7HvR?usp=sharing'
                                , '-0.6':'https://drive.google.com/drive/folders/1x5U3LdJZgGIamK0rkb41MGzqaQnfoVL8?usp=sharing'
                                , '-0.8':'https://drive.google.com/drive/folders/10JrpQPvbQegMF-VrJOD7PkMOjWYjlzDH?usp=sharing'}
            folder_url = folder_url_dict[str(self.dataset_name)]
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_100000_768')
            index_vectors, _ = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)

            num, dim, vectors = load_data(self.basedir+'/queries_100000_768')
            _, query_vectors = sample_vectors(vectors, 0, self.nq)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class SIFTSMALL(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 128
        self.nb = 10000
        self.nq = 100
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "SIFTSMALL")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)


    def prepare(self, skip_data=False):
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("SIFTSMALL has already installed!")
                return

        import gdown
        folder_url = "https://drive.google.com/drive/folders/1XbvrSjlP-oUZ5cixVpfSTn0zE-Cim0NK?usp=sharing"
        gdown.download_folder(folder_url, output=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class SIFT(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 128
        self.nb = 1000000
        self.nq = 10000
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "SIFT")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("SIFT has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1PngXRH9jnN86T8RNiU-QyGqOillfQE_p?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_1000000_128')
            index_vectors, _ = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)

            num, dim, vectors = load_data(self.basedir+'/queries_10000_128')
            _, query_vectors = sample_vectors(vectors, 0, self.nq)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class OPENIMAGESTREAMING(DatasetCompetitionFormat):
    def __init__(self):
        self.d = 512
        self.nb = 1000000
        self.nq = 10000
        self.dtype = "float32"
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, "openimage-streaming")
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        downloadflag = 0
        for item in os.listdir(self.basedir):
            item_path = os.path.join(self.basedir, item)
            if os.path.isdir(item_path) or os.path.isfile(item_path):
                print("openimage-streaming has already installed!")
                downloadflag = 1
                break
        if downloadflag == 0:
            import gdown
            folder_url = "https://drive.google.com/drive/folders/1ZkWOrja-0A6C9yh3ysFoCP6w5u7oWjQx?usp=sharing"
            gdown.download_folder(folder_url, output=self.basedir)

        prepocessflag = 0
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)

        if os.path.exists(data_file_path) and os.path.exists(queries_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            prepocessflag = 1

        if prepocessflag == 0:
            num, dim, vectors = load_data(self.basedir+'/data_1000000_512')
            index_vectors, _ = sample_vectors(vectors, self.nb, self.nq)
            save_data(index_vectors, type='data', basedir=self.basedir)

            num, dim, vectors = load_data(self.basedir+'/queries_10000_512')
            _, query_vectors = sample_vectors(vectors, 0, self.nq)
            save_data(query_vectors, type='queries', basedir=self.basedir)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def default_count(self):
        return 10

class RandomPlus(DatasetCompetitionFormat):
    def __init__(self, nb, nq, d, seed=7758258, drift_position=0, drift_offset=0.5, query_noise_fraction=0, basedir="randomplus"):
        self.nb = nb
        self.nq = nq
        self.d = d
        self.dtype = 'float32'
        self.ds_fn = f"data_{self.nb}_{self.d}"
        self.qs_fn = f"queries_{self.nq}_{self.d}"
        self.gt_fn = f"gt_{self.nb}_{self.nq}_{self.d}"
        self.basedir = os.path.join(BASEDIR, f"{basedir}{self.nb}")
        self.drift_position = drift_position
        self.drift_offset = drift_offset
        self.query_noise_fraction = query_noise_fraction
        self.seed = seed

        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

    def prepare(self, skip_data=False):
        data_file_path = os.path.join(self.basedir, self.ds_fn)
        queries_file_path = os.path.join(self.basedir, self.qs_fn)
        gt_file_path = os.path.join(self.basedir, self.gt_fn)
        if os.path.exists(data_file_path) and os.path.exists(queries_file_path) and os.path.exists(gt_file_path):
            print("Preprocessed data already exists. Skipping data generation.")
            return

        from sklearn.neighbors import NearestNeighbors
        import torch

        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        data = torch.rand((self.nb, self.d), dtype=torch.float32)

        if self.drift_position > 0 and self.drift_position < self.nb:
            print(f"I will introduce concept drift from {self.drift_position}, drift offset={self.drift_offset}")
            data[self.drift_position:] = data[self.drift_position:] * (1.0 - self.drift_offset)

        indices = torch.randperm(data.size(0))[:self.nq]
        queries = data[indices]

        if self.query_noise_fraction > 0:
            queries = (1 - self.query_noise_fraction) * queries + self.query_noise_fraction * torch.rand_like(queries)

        # print(os.path.join(self.basedir, self.ds_fn))
        with open(os.path.join(self.basedir, self.ds_fn), "wb") as f:
            np.array([self.nb, self.d], dtype='uint32').tofile(f)
            data.numpy().astype('float32').tofile(f)

        # print(os.path.join(self.basedir, self.qs_fn))
        with open(os.path.join(self.basedir, self.qs_fn), "wb") as f:
            np.array([self.nq, self.d], dtype='uint32').tofile(f)
            queries.numpy().astype('float32').tofile(f)

        nbrs = NearestNeighbors(n_neighbors=100, metric="euclidean", algorithm='brute').fit(data.numpy())
        D, I = nbrs.kneighbors(queries.numpy())

        # print(os.path.join(self.basedir, self.gt_fn))
        with open(os.path.join(self.basedir, self.gt_fn), "wb") as f:
            np.array([self.nq, 100], dtype='uint32').tofile(f)
            I.astype('uint32').tofile(f)
            D.astype('float32').tofile(f)

    def search_type(self):
        return "knn"

    def distance(self):
        return "euclidean"

    def __str__(self):
        return f"RandomPlus({self.nb})"

    def default_count(self):
        return 10

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

    'wikipedia-35M': lambda : WikipediaDataset(35000000),
    'wikipedia-1M': lambda : WikipediaDataset(1000000),
    'wikipedia-100K': lambda : WikipediaDataset(100000),

    'msmarco-100M': lambda : MSMarcoWebSearchDataset(101070374),
    'msmarco-10M': lambda : MSMarcoWebSearchDataset(10000000),
    'msmarco-1M': lambda : MSMarcoWebSearchDataset(1000000),

    'openai-2M': lambda : OpenAIArXivDataset(2321096),
    'openai-100K': lambda : OpenAIArXivDataset(100000),

    'random-xs': lambda : RandomDS(10000, 1000, 20),
    'random-s': lambda : RandomDS(100000, 1000, 50),

    'random-xs-clustered': lambda: RandomClusteredDS(),

    'random-range-xs': lambda : RandomRangeDS(10000, 1000, 20),
    'random-range-s': lambda : RandomRangeDS(100000, 1000, 50),

    'random-filter-s': lambda : RandomFilterDS(100000, 1000, 50),

    'openai-embedding-1M': lambda: OpenAIEmbedding1M(93652),

    "random-plus": lambda: RandomPlus(10000,1000,20),

    "random-plus-experiment": lambda: RandomPlus(500000,1000,20),
    "random-experiment": lambda: RandomDS(500000,1000,20),

    'sift-small': lambda: SIFTSMALL(),
    'glove': lambda: GLOVE(),
    'sift': lambda: SIFT(),
    'msong': lambda: MSONG(),
    'sun': lambda: SUN(),
    'dpr': lambda: DPR(),
    'reddit': lambda: REDDIT(),
    'trevi': lambda: TREVI(),

    'coco': lambda: COCO(),
    'cirr': lambda: CIRR(),

    'wte-0.05': lambda: WTE('-0.05'),
    'wte-0.1': lambda: WTE('-0.1'),
    'wte-0.2': lambda: WTE('-0.2'),
    'wte-0.4': lambda: WTE('-0.4'),
    'wte-0.6': lambda: WTE('-0.6'),
    'wte-0.8': lambda: WTE('-0.8'),

    'openimage-streaming': lambda: OPENIMAGESTREAMING(),

}
