import numpy as np
import prism_ann

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS


class Prism(BaseFilterANN):

    def __init__(self, metric, index_params):
        self._metric = metric
        self._index_params = index_params
        self.n_clusters = index_params.get('n_clusters', 4000)
        self.kmeans_iters = index_params.get('kmeans_iters', 5)
        self.ef = 50
        self.nprobe = 60
        self.binary_rerank = 0
        self.index = None

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        xb = ds.get_dataset()
        meta = ds.get_dataset_metadata()
        meta.sort_indices()

        self.index = prism_ann.IvfIndex(
            n_clusters=self.n_clusters,
            kmeans_iters=self.kmeans_iters,
        )
        self.index.build(
            xb,
            meta.indptr.astype(np.int64),
            meta.indices.astype(np.int32),
            meta.shape[1],
        )

    def load_index(self, dataset):
        return False

    def filtered_query(self, X, filter, k):
        self.I = self.index.search(
            X,
            filter.indptr.astype(np.int64),
            filter.indices.astype(np.int32),
            k=k,
            ef=self.ef,
            nprobe=self.nprobe,
            binary_rerank=self.binary_rerank,
        )

    def get_results(self):
        return self.I

    def set_query_arguments(self, query_args):
        self.ef = query_args.get('ef', 50)
        self.nprobe = query_args.get('nprobe', 60)
        self.binary_rerank = query_args.get('binary_rerank', 0)

    def __str__(self):
        return f'prism_c{self.n_clusters}_ef{self.ef}_np{self.nprobe}'
