from __future__ import absolute_import
import psutil
import os
import time
import numpy as np
import wrapper as pann

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS, download_accelerated, BASEDIR
from benchmark.dataset_io import download 

class vamana(BaseOODANN):
    def __init__(self, metric, index_params):
        self.name = "vamana"
        if (index_params.get("R")==None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L")==None):
            print("Error: missing parameter L")
            return
        self._index_params = index_params
        self._metric = self.translate_dist_fn(metric)

        self.R = int(index_params.get("R"))
        self.L = int(index_params.get("L"))
        self.alpha = float(index_params.get("alpha", 1.0))
        self.two_pass = bool(index_params.get("two_pass", False))
        self.use_query_data = bool(index_params.get("use_query_data", False))
        self.compress_vectors = bool(index_params.get("compress", False))


    def index_name(self):
        return f"R{self.R}_L{self.L}_alpha{self.alpha}"
    
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "ood")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'vamana')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return os.path.join(index_dir, self.index_name())
    
    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return 'Euclidian'
        elif metric == 'ip':
            return 'mips'
        else:
            raise Exception('Invalid metric')
        
    def translate_dtype(self, dtype:str):
        if dtype == 'float32':
            return 'float'
        else:
            return dtype

    def prepare_sample_info(self, index_dir):
        if(self.use_query_data):
            #download the additional sample points for the ood index
            self.sample_points_path = "data/text2image1B/query_sample_200000.fbin"
            sample_qs_large_url = "https://storage.yandexcloud.net/yr-secret-share/ann-datasets-5ac0659e27/T2I/query.private.1M.fbin"
            bytes_to_download = 8 + 200000*4*200
            download(sample_qs_large_url, self.sample_points_path, bytes_to_download)
            header = np.memmap(self.sample_points_path, shape=2, dtype='uint32', mode="r+")
            header[0] = 200000

            self.secondary_index_dir = index_dir + ".secondary"
            self.secondary_gt_dir = self.secondary_index_dir + ".gt"
        else:
            self.sample_points_path = ""
            self.secondary_index_dir = ""
            self.secondary_gt_dir = ""

    def prepare_compressed_info(self):
        if(self.compress_vectors):
            self.compressed_vectors_path = "data/text2image1B/compressed_10M.fbin"
        else:
            self.compressed_vectors_path = ""
        
    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        """
        ds = DATASETS[dataset]()
        d = ds.d

        index_dir = self.create_index_dir(ds)

        self.prepare_sample_info(index_dir)
        self.prepare_compressed_info()
        
        if hasattr(self, 'index'):
            print("Index already exists")
            return
        else:
            start = time.time()
            # ds.ds_fn is the name of the dataset file but probably needs a prefix
            pann.build_vamana_index(self._metric, self.translate_dtype(ds.dtype), ds.get_dataset_fn(), self.sample_points_path, 
                self.compressed_vectors_path, index_dir, self.secondary_index_dir, self.secondary_gt_dir, self.R, self.L, self.alpha, 
                self.two_pass)

            end = time.time()
            print("Indexing time: ", end - start)
            print(f"Wrote index to {index_dir}")

        self.index = pann.load_vamana_index(self._metric, self.translate_dtype(ds.dtype), ds.get_dataset_fn(), self.compressed_vectors_path, 
            self.sample_points_path, index_dir, self.secondary_index_dir, self.secondary_gt_dir, ds.nb, d)
        print("Index loaded")

    def query(self, X, k):
        nq, d = X.shape
        self.res, self.query_dists = self.index.batch_search(X, nq, k, self.Ls)

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") is None else query_args.get("Ls")
        self.search_threads = self._query_args.get("T", 16)
        os.environ["PARLAY_NUM_THREADS"] = str(self.search_threads)

    def load_index(self, dataset):
        ds = DATASETS[dataset]()
        d = ds.d

        index_dir = self.create_index_dir(ds)
        self.prepare_sample_info(index_dir)
        self.prepare_compressed_info()

        print("Trying to load...")

        try:
            file_size = os.path.getsize(index_dir)
            print(f"File Size in Bytes is {file_size}")
        except FileNotFoundError:
            file_size = 0
            print("File not found.")

        if file_size != 0:
            try:
                self.index = pann.load_vamana_index(self._metric, self.translate_dtype(ds.dtype), ds.get_dataset_fn(), 
                                                    self.compressed_vectors_path, self.sample_points_path, index_dir, 
                                                    self.secondary_index_dir, self.secondary_gt_dir, ds.nb, d)
                print("Index loaded")
                return True
            except:
                print("Index not found")
                return False
        else:
            print("Index not found")
            return False