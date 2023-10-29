from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import index_mystery

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS, download_accelerated

from urllib.request import urlopen
import requests
import numpy as np
import os
import time

def download_train(src, dst=None, max_size=None):
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

class mysteryann(BaseOODANN):
    def __init__(self, metric, index_params):
        self.name = "mysteryann"
        if (index_params.get("M_pjbp")==None):
            print("Error: missing parameter M_pjbp")
            return
        if (index_params.get("L_pjpq")==None):
            print("Error: missing parameter L_pjpq")
            return
        if (index_params.get("NoP")==None):
            print("Error: missing parameter NoP")
            return
        if (index_params.get("T")==None):
            print("Error: missing parameter T for set threads")
            return
        if (index_params.get("NoT")==None):
            print("Error: missing parameter NoT")
            return
        if (index_params.get("EoP")==None):
            print("Error: missing parameter EoP")
            return

        self._index_params = index_params
        self._metric = metric

        self.M_pjbp = index_params.get("M_pjbp")
        self.L_pjpq = index_params.get("L_pjpq")
        self.NoT = index_params.get("NoT")
        self.EoP = index_params.get("EoP")
        self.NoP = index_params.get("NoP")
        self.T = index_params.get("T")


    def index_name(self):
        return f"M_bp{self.M_pjbp}_L_pq{self.L_pjpq}_NoT{self.NoT}_ord"
        
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "ood")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'mysteryann')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir

    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return index_mystery.L2
        elif metric == 'ip':
            return index_mystery.IP
        elif metric == 'ip_build':
            return index_mystery.IP_BUILD
        elif metric == 'cosine':
            return index_mystery.COSINE
        else:
            raise Exception('Invalid metric')
        
    def translate_dtype(self, dtype:str):
        if dtype == 'uint8':
            return np.uint8
        elif dtype == 'int8':
            return np.int8
        elif dtype == 'float32':
            return np.float32
        else:
            raise Exception('Invalid data type')

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        """
        self.ds = DATASETS[dataset]()
        ds = DATASETS[dataset]()

        # buildthreads = self._index_params.get("buildthreads", -1)
        print('threads: ', self.T)
        # if buildthreads == -1:
            # buildthreads = 0

        index_dir = self.create_index_dir(ds)
        save_name = f'learn.{self.NoT}M.fbin'
        # save_path = os.path.join(ds.basedir, save_name)
        save_path = os.path.join(index_dir, save_name)
        max_size = self.NoT * 1000000 * 200 * 4 + 8
        src_url = 'https://storage.yandexcloud.net/yandex-research/ann-datasets/T2I/query.learn.50M.fbin'
        print(src_url, save_path, max_size)
        
        if ds.d == 200:
            download_train(src_url, save_path, max_size)

            with open(save_path, 'rb+') as f:
                npts = self.NoT * 1000000
                f.write(int(npts).to_bytes(4, byteorder='little'))
                f.close()


        if  hasattr(self, 'index'):
            print('Index object exists already')
            return

        print(ds.get_dataset_fn())

        start = time.time()
        if ds.d == 200:
            m = self.translate_dist_fn(str(ds.distance()+'_build'))
        else:
            print('small dataset')
            save_path = ''
            m = self.translate_dist_fn(str(ds.distance()))

        print('m:', m)
        index_abs_path = os.path.join(index_dir, self.index_name())
        index_mystery.buildST2(self.M_pjbp, self.L_pjpq, self.T, os.path.join(os.getcwd(), ds.get_dataset_fn()), m, save_path, self.EoP, self.NoT, index_abs_path)
        end = time.time()
        print("MysteryANN index built in %.3f s" % (end - start))

        
        print('Loading index..')
        m = self.translate_dist_fn(ds.distance())
        data_abs_path = os.path.join(index_dir, self.index_name() + '.data')
        self.index = index_mystery.load(index_abs_path, data_abs_path, m)

        print('Index ready for search')

    def get_index_components(self, dataset):
        index_components = ['', '.data', '.order', '.original_order', '.quant']
        ds = DATASETS[dataset]()
        if ds.distance() == "ip":
            index_components = index_components + []
        return index_components

    def index_files_to_store(self, dataset):
        return [self.create_index_dir(DATASETS[dataset]()), self.index_name(), self.get_index_components(dataset)]

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        self.ds = DATASETS[dataset]()
        ds = DATASETS[dataset]()

        index_dir = self.create_index_dir(ds)        
        if not (os.path.exists(index_dir)) and 'url' not in self._index_params:
            return False

        index_path = os.path.join(index_dir, self.index_name())
        index_components = self.get_index_components(dataset)

        for component in index_components:
            index_file = index_path + component
            if not (os.path.exists(index_file)):
                if 'url' in self._index_params:
                    index_file_source = self._index_params['url'] + '/' + self.index_name() + component
                    print(f"Downloading index in background. This can take a while.")
                    download_accelerated(index_file_source, index_file, quiet=True)
                else:
                    return False

        print("Loading index")

        index_abs_path = os.path.join(index_dir, self.index_name())
        data_abs_path = os.path.join(index_dir, self.index_name() + '.data')
        m = self.translate_dist_fn(ds.distance())
        self.index = index_mystery.load(index_abs_path, data_abs_path, m)
        print ("Load index success.")
        return True
        
    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        # nq, dim = (np.shape(X))
        # self.res, self.query_dists = self.index.batch_search(
            # X, k, self.Ls, self.search_threads)
        self.res = np.zeros((X.shape[0], k), dtype=np.uint32, order='C')
        self.index.search(X, k, self.L_pq, self.res, X.shape[0], self.search_threads, True)
        # self.index.search(X, k, self.L_pq, self.res, len(X), self.search_threads)
        # self.res, self.query_dists = self.index.batch_search(
        #     X, k, self.Ls, self.search_threads)
     

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.L_pq = 83 if query_args.get("L_pq") == None else query_args.get("L_pq")                             
        self.search_threads = self._query_args.get("T")
        self.topk = 10
        self.index.setThreads(self.search_threads)
        # self.res = np.zeros((self.ds.nq, self.topk), dtype=np.uint32, order='C')

    def __str__(self):
        return f'mystery_order_sq8({self.index_name(), self._query_args})'