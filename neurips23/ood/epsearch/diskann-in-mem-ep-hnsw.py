from __future__ import absolute_import
import psutil
import os
import time
import numpy as np

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS, download_accelerated

import re
import numpy as np
import pickle

# from sklearn_extra.cluster import KMedoids
import faiss
import hnswlib
import mkl

import diskannpy



class EPSearcherKmeansHNSW:
    def __init__(
        self, dim: int, n_clusters: int,
        index_dir: str, index_name: str
    ) -> None:
        self.dim = dim
        self.n_clusters = n_clusters
        self.index_path = os.path.join(index_dir, index_name)
    
    def fit(self, data: np.ndarray) -> None:
        if os.path.exists(self.index_path):
            self.load_index()
            print(f"ep index loaded from {self.index_path}")
            return
        print(f"ep index not found at {self.index_path}, building...")

        cand_ids_path = f"{self.index_path}.cand_ids_{self.n_clusters}.npy"
        if os.path.exists(cand_ids_path):
            print("candidate ids found, loading...")
            self.cand_ids = np.load(cand_ids_path)
            print("candidate ids loaded")
        else:
            print("candidate ids not found, building...")
            kmeans = faiss.Kmeans(self.dim, self.n_clusters)
            kmeans.verbose = True
            print("training kmeans")
            kmeans.train(data)
            centroids = kmeans.centroids
            print("training kmeans done")
            print(f"centroids: {centroids.shape}")
            print("delete kmeans instance")
            del kmeans

            print("build raw index")
            raw_index = faiss.IndexFlatIP(self.dim)
            raw_index.verbose = True
            raw_index.add(data)
            # cid -> nearest vector
            _, RI = raw_index.search(centroids, 1)
            self.cand_ids = RI[:, 0]
            print("build raw index done")
            print(f"candidate ids: {self.cand_ids.shape}")
            print(self.cand_ids)
            
            assert self.cand_ids.shape[0] == self.n_clusters
        
            print("saving candidate ids...")
            np.save(cand_ids_path, self.cand_ids)
            del raw_index
        
        # search index
        print("build search index")
        self.index = hnswlib.Index(space='ip', dim=self.dim)
        self.index.init_index(
            max_elements=self.n_clusters, ef_construction=200, M=32
        )
        self.index.set_num_threads(8)
        candidate_vecs = data[self.cand_ids]
        print(f"candidate vecs: {candidate_vecs.shape}")
        print("adding items to hnsw index")
        self.index.add_items(candidate_vecs, self.cand_ids) # with ids

        print("build search index done")
        
        print("write index...")
        self.index.save_index(self.index_path)
        print("write index done")

    def load_index(self) -> None:
        print("load index...")
        self.index = hnswlib.Index(space='ip', dim=self.dim)
        self.index.load_index(self.index_path, max_elements=self.n_clusters)
        print("load index done")

    def search(self, query: np.ndarray) -> np.ndarray:
        """Search the nearest entry point for each query.

        Args:
            query (np.ndarray): query batch (n_queries, d)

        Returns:
            np.ndarray: entry point ids (n_queries,)
        """
        labels, _ = self.index.knn_query(query, k=1)
        return labels[:, 0]
    
    def set_num_threads(self, n_threads: int) -> None:
        self.index.set_num_threads(n_threads)
    
    def set_ef(self, efSearch: int) -> None:
        self.index.set_ef(efSearch)

class epdiskann(BaseOODANN):
    def __init__(self, metric, index_params):
        self.name = "epdiskann"
        if (index_params.get("R")==None):
            print("Error: missing parameter R")
            return
        if (index_params.get("L")==None):
            print("Error: missing parameter L")
            return
        self._index_params = index_params
        self._metric = metric

        # build params for diskann
        self.R = index_params.get("R")
        self.L = index_params.get("L")
        self.alpha = index_params.get("alpha", 1.0)
        self.use_pq_build = index_params.get("use_pq_build", False)
        self.num_pq_bytes = index_params.get("num_pq_bytes", 0) #irrelevant given use_pq_build=False
        self.use_opq = index_params.get("use_opq", False)
        # build params for ep searcher
        self.n_ep_candidates = index_params.get("n_ep_candidates", 256)
        self.hnsw_M = index_params.get("hnsw_M", 32)
        self.efConstruction = index_params.get("efConstruction", 200)
        
        # path info
        self.diskann_index_name = f"R{self.R}_L{self.L}_alpha{self.alpha}"
        

    def index_name(self):
        return self.diskann_index_name
    
    def index_identifier(self):
        key = "mydiskann-ep-hnsw"
        key += f"_n_ep_candidates{self.n_ep_candidates}_M{self.hnsw_M}_efConstruction{self.efConstruction}"
        return key
        
    def create_index_dir(self, dataset):
        index_dir = os.path.join(os.getcwd(), "data", "indices", "ood")
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, 'diskann')
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        index_dir = os.path.join(index_dir, dataset.short_name())
        os.makedirs(index_dir, mode=0o777, exist_ok=True)
        self.diskann_dir = os.path.join(index_dir, self.diskann_index_name)
        os.makedirs(self.diskann_dir, mode=0o777, exist_ok=True)
        self.diskann_path = os.path.join(self.diskann_dir, self.diskann_index_name)
        index_dir = os.path.join(index_dir, self.index_identifier())
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
        ds = DATASETS[dataset]()
        d = ds.d

        buildthreads = self._index_params.get("buildthreads", -1)
        ep_train = self._index_params.get("ep_train", "id") # ood or id
        print(f"buildthreads: {buildthreads}")
        if buildthreads == -1:
            buildthreads = 0
        if buildthreads > 0:
            faiss.omp_set_num_threads(buildthreads)
        print(f"buildthreads: {buildthreads} set to faiss")

        index_dir = self.create_index_dir(ds)
        
        if  hasattr(self, 'index'):
            print('Index object exists already')
            return

        print(ds.get_dataset_fn())

        start = time.time()
        xb = ds.get_dataset()
        print(f"xb shape: {xb.shape}")
        
        print("Building Entry Point Searcher..")
        ep_index_name = f"ep_{self.index_name()}.index"
        self.ep_searcher = EPSearcherKmeansHNSW(
            dim=d, n_clusters=self.n_ep_candidates,
            index_dir=index_dir, index_name=ep_index_name,
        )
        if ep_train == "id":
            self.ep_searcher.fit(xb)
        elif ep_train == "ood":
            maxn_ood = xb.shape[0]
            ep_train_data = ds.get_query_train(maxn=maxn_ood)
            self.ep_searcher.fit(ep_train_data)
            del ep_train_data
        else:
            raise Exception("Invalid ep_train")
        duration_ep = time.time() - start
        print(f"EP Searcher built in {duration_ep:.3f} s")


        print("Building DiskANN index..")
        
        if not os.path.exists(self.diskann_path):
            print(f"DiskANN index does not exist at {self.diskann_path}, building...")
            diskannpy.build_memory_index(
                data = ds.get_dataset_fn(),
                distance_metric = self.translate_dist_fn(ds.distance()),
                vector_dtype = self.translate_dtype(ds.dtype),
                index_directory = self.diskann_dir,
                index_prefix = self.index_name(),
                complexity=self.L,
                graph_degree=self.R,
                num_threads = buildthreads,
                alpha=self.alpha,
                use_pq_build=self.use_pq_build,
                num_pq_bytes=self.num_pq_bytes,
                use_opq=self.use_opq,
            )
            print(f"DiskANN index built at {self.diskann_path}")
        end = time.time()
        print("DiskANN index built in %.3f s" % (end - start))

        
        print('Loading index..')
        self.index = diskannpy.StaticMemoryIndex(
            distance_metric = self.translate_dist_fn(ds.distance()),
            vector_dtype = self.translate_dtype(ds.dtype),
            index_directory = self.diskann_dir,
            index_prefix = self.index_name(),
            num_threads = 64, #to allocate scratch space for up to 64 search threads
            initial_search_complexity = 110,
        )
        print('Index ready for search')

    def get_index_components(self, dataset):
        index_components = ['', '.data']
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

        print("Loading ep index")
        self.ep_searcher = EPSearcherKmeansHNSW(
            ds.d, n_clusters=self.n_ep_candidates,
            index_dir=index_dir, index_name=f"ep_{self.index_name()}.index"
        )
        self.ep_searcher.load_index()
        print("Loaded ep index")

        print("Loading diskann index")
        self.index = diskannpy.StaticMemoryIndex(
            distance_metric = self.translate_dist_fn(ds.distance()),
            vector_dtype = self.translate_dtype(ds.dtype),
            index_directory = index_dir,
            index_prefix = self.index_name(),
            num_threads = 64, #to allocate scratch space for up to 64 search threads
            initial_search_complexity = 110,
        )
        print ("Load index success.")
        return True
        
    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        ep_ids = self.ep_searcher.search(X)
        self.res, self.query_dists = self.index.batch_search_with_eps(
            X, k, self.Ls, self.search_threads, ep_ids)


    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.Ls = 0 if query_args.get("Ls") == None else query_args.get("Ls")                             
        self.search_threads = self._query_args.get("T")
        self.efSearch = self._query_args.get("efSearch")
        print(f"Setting efSearch to {self.efSearch} for hnsw")
        self.ep_searcher.set_ef(self.efSearch)
        print(f"Setting search threads to {self.search_threads} for diskann")
        print(f"Setting search threads to {self.search_threads} for ep")
        self.ep_searcher.set_num_threads(self.search_threads)
        faiss.omp_set_num_threads(self.search_threads)

    def __str__(self):
        return f'diskann({self.index_name(), self._query_args})'