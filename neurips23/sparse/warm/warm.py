import time

import numpy as np

import writerslogic_warm as warm

from benchmark.datasets import DATASETS
from neurips23.sparse.base import BaseSparseANN


class Warm(BaseSparseANN):
    """WARM learned-sparse index (writerslogic_warm.SparseIndex).

    A blocked inverted index over statically pruned posting lists, one summary vector per
    block, and a byte forward index. A query walks its heaviest coordinates, scores a
    block only when its summary can still reach the current k-th score, and scores every
    candidate exactly against the forward index.
    """

    def __init__(self, metric, index_params):
        if metric != "ip":
            raise ValueError(f"WARM sparse index supports ip only, got {metric}")
        self._params = dict(index_params)
        self.index = None
        self.res = None
        self._query = {}

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        assert ds.data_type() == "sparse"
        start = time.time()
        self.index = warm.SparseIndex(**self._params)
        self.index.build_from_spmat(ds.get_dataset_fn())
        nbytes, blocks, postings = self.index.stats()
        print(f"WARM SparseIndex built in {time.time() - start:.1f} s, {nbytes / 2**30:.2f} GiB, "
              f"{blocks} blocks, {postings} postings")

    def load_index(self, dataset):
        return False

    def index_files_to_store(self, dataset):
        return None

    def set_query_arguments(self, query_args):
        self._query = dict(query_args)
        self.index.set_search(**self._query)

    def query(self, X, k):
        X = X.tocsr()
        self.res = self.index.search(
            np.ascontiguousarray(X.indptr, dtype=np.int64),
            np.ascontiguousarray(X.indices, dtype=np.int32),
            np.ascontiguousarray(X.data, dtype=np.float32),
            k,
        )

    def get_results(self):
        return self.res

    def __str__(self):
        return f"Warm({self._params}, {self._query})"
