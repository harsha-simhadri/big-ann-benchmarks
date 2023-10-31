from __future__ import absolute_import

import numpy as np

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS
import pylinscan

# a python wrapper for the linscan algorithm, implemented in rust
# algorithm details: https://arxiv.org/abs/2301.10622
# code: https://github.com/pinecone-io/research-bigann-linscan

# Build parameters: none
# Query parameters: budget (in ms) for computing all the scores
class Linscan(BaseANN):
    def __init__(self, metric, index_params):
        assert metric == "ip"
        self.name = "linscan"
        self._index = pylinscan.LinscanIndex()
        self._budget = np.infty
        print("Linscan index initialized: " + str(self._index))

    def fit(self, dataset): # e.g. dataset = "sparse-small"

        self.ds = DATASETS[dataset]()
        assert self.ds.data_type() == "sparse"

        N_VEC_LIMIT = 100000 # batch size
        it = self.ds.get_dataset_iterator(N_VEC_LIMIT)
        for d in it:
            for i in range(d.shape[0]):
                d1 = d.getrow(i)
                self._index.insert(dict(zip(d1.indices, d1.data)))

        print("Index status: " + str(self._index))


    def load_index(self, dataset):
        return None

    def set_query_arguments(self, query_args):
        self._budget = query_args["budget"]

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        nq = X.shape[0]

        # prepare the queries as a list of dicts
        self.queries = []
        for i in range(nq):
            qc = X.getrow(i)
            q = dict(zip(qc.indices, qc.data))
            self.queries.append(q)

        res = self._index.retrieve_parallel(self.queries, k, self._budget)
        self.I = np.array(res, dtype='int32')

    def get_results(self):
        return self.I
