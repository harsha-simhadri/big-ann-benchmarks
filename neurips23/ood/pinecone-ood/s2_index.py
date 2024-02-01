import pickle
import numpy as np
import os
import time
import requests

from multiprocessing.pool import ThreadPool

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated

import diskannpy

import pys2

def read_fbin(filename, start_idx=0, chunk_size=None):
    with open(filename, "rb") as f:
        nvecs, dim = np.fromfile(f, count=2, dtype=np.int32)
        nvecs = (nvecs - start_idx) if chunk_size is None else chunk_size
        arr = np.fromfile(f, count=nvecs * dim, dtype=np.float32,
                          offset=start_idx * 4 * dim)
    return arr.reshape(nvecs, dim)

def quantize(array, min_v, max_v):
    # Normalize the array
    normalized_array = (array - min_v) / (max_v - min_v)
    # Scale to 8-bit range and convert to uint8
    quantized_array = (normalized_array * 255).astype(np.uint8)
    return quantized_array

class S2_index(BaseOODANN):

    def __init__(self,  metric, index_params):
        
        self.name = 'pinecone-ood'
        self._index_params = index_params
        self._metric = metric
        self.index_path = "data/pinecone/ood/text2image-10M-data/"

        self.L = 225 
        self.R = 32
        
        print(index_params)
        if (index_params.get("index_str")==None):
            print("Error: missing parameter index_str")
            return
        self.index_str = index_params.get("index_str")


    def fit(self, dataset):
        # this version is for evaluating existing indexes only
        raise NotImplementedError()

    def index_name(self):
        return f"R{self.R}_L{self.L}"

    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "ood")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'diskann')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, self.index_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        return index_dir

    def translate_dist_fn(self, metric):
        if metric == 'euclidean':
            return 'l2'
        elif metric == 'ip':
            return 'mips'
        else:
            raise Exception('Invalid metric')

    def translate_dtype(self, dtype:str):
        # if dtype == 'uint8':
        return np.uint8
        # elif dtype == 'int8':
        #     return np.int8
        # elif dtype == 'float32':
        #     return np.float32
        # else:
        #     raise Exception('Invalid data type')


    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build parameters passed during construction.

        If the file does not exist, there is an option to download it from a public url
        """
        ds = DATASETS[dataset]()

        print(f"Loading index (downloading if necessary)")

        # check if index files exist. If not, download them


        bucket_name = 'research-public-storage'
        file_list = ['ood-index/text2image-10M-centroids', 'ood-index/text2image-10M-centroids.fbin', 'ood-index/coip-t2i-10M-vecsofvecs', 'ood-index/text2image-10M-vecs']

        download_multiple_files(bucket_name, file_list, self.index_path)


        index_dir = self.create_index_dir(ds)

        start = time.time()
        data = read_fbin(self.index_path + "text2image-10M-centroids.fbin")
        self.min  = np.amin(data)
        self.max = np.amax(data)
        data = quantize(data, self.min, self.max)
        diskannpy.build_memory_index(
            data = data,
            distance_metric = "l2",
            vector_dtype = self.translate_dtype(ds.dtype),
            index_directory = index_dir,
            index_prefix = self.index_name(),
            complexity= self.L,
            graph_degree= self.R,
            num_threads = 32,
            alpha=1.2,
            use_pq_build=False,
            num_pq_bytes=0, #irrelevant given use_pq_build=False
            use_opq=False
        )
        end = time.time()
        print("DiskANN index built in %.3f s" % (end - start))

        
        print('Loading index..')
        self.centroid_index = diskannpy.StaticMemoryIndex(
            distance_metric = "l2",
            vector_dtype = self.translate_dtype(ds.dtype),
            index_directory = index_dir,
            index_prefix = self.index_name(),
            num_threads = 64, #to allocate scratch space for up to 64 search threads
            initial_search_complexity = 100
        )
        print('Index ready for search')

        self.index = pys2.OODIndexWrapper(ds.d,
                                    self.index_str,
                                    ds.get_dataset_fn(), 
                                    self.index_path + "text2image-10M-centroids", 
                                    self.index_path + "text2image-10M-vecs", 
                                    self.index_path + "coip-t2i-10M-vecsofvecs")
        print(f"Finished loading index")
        return True


    def index_files_to_store(self, dataset):
        """
        Specify a triplet with the local directory path of index files,
        the common prefix name of index component(s) and a list of
        index components that need to be uploaded to (after build)
        or downloaded from (for search) cloud storage.

        For local directory path under docker environment, please use
        a directory under
        data/indices/track(T1 or T2)/algo.__str__()/DATASETS[dataset]().short_name()
        """
        raise NotImplementedError()
    
    def query(self, X, k):
        nq, dim = (np.shape(X))
        
        sc = time.time()        
        ids, _ = self.centroid_index.batch_search(quantize(X, self.min, self.max), self.nprobe, self.Ls, 10)
        tc = time.time()
        elapsed = tc - sc
        print(f"Querying centroids took {elapsed} seconds")

        sp = time.time()
        # self.res = self.index.search_parallel(X, k)
        self.res = self.index.search_parallel_with_partitions(X, ids, self.nprobe, k)
        tp = time.time()
        elapsed = tp - sp
        elapsed_full = tp - sc
        print(f"Querying rest of index took {elapsed} seconds")
        print(f"Full query time took {elapsed_full} seconds")


    def get_results(self):
        return self.res

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        print("setting query args:" + str(query_args))

        self.Ls = 0 if query_args.get("Ls") == None else int(query_args.get("Ls"))

        if "nprobe" in query_args:
            nprobe = query_args.get("nprobe")
            self.index.set_search_param('nprobe', nprobe)
            self.nprobe = int(nprobe)
        else:
            self.index.set_search_param('nprobe', "20")
        if "kfactor" in query_args: 
            self.index.set_search_param('kfactor', query_args.get("kfactor"))
        else: 
            self.index.set_search_param('kfactor', "18")


    def __str__(self):
        return f'pinecone-ood({self.index_str, self._index_params, self._query_args})'

def download_public_gcs_file(bucket_name, source_blob_name, destination_dir):
    """Download a file from Google Cloud Storage if it doesn't exist locally."""
    destination_file_name = os.path.join(destination_dir, os.path.basename(source_blob_name))

    # Check if the file already exists
    if os.path.exists(destination_file_name):
        print(f"File already exists: {destination_file_name}")
        return

    # Download the file
    url = f"https://storage.googleapis.com/{bucket_name}/{source_blob_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)
        
        # Write the file
        with open(destination_file_name, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully: {destination_file_name}")
    else:
        print(f"Failed to download {source_blob_name}: HTTP status code {response.status_code}")

def download_multiple_files(bucket_name, file_list, destination_dir):
    """Download multiple files from GCS to a local directory if they don't already exist."""
    for file_name in file_list:
        download_public_gcs_file(bucket_name, file_name, destination_dir)
