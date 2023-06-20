from __future__ import absolute_import

from scipy.sparse import csr_matrix
import numpy as np

from multiprocessing.pool import ThreadPool

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS

# given a vector x, returns another vector with the minimal number of largest elements of x,
# s.t. their sum is at most a times the sum of the elements in x.
#
# The goal is to sparsify the vector further,
# but at the same time try and preserve as much of the original vector as possible.
def largest_elements(x, a):
    # Compute the sum of elements of x
    x_sum = np.sum(x)

    # Compute the indices and values of the largest elements of x
    ind = np.argsort(-x.data)
    cs = np.cumsum(x.data[ind] / x_sum)

    n_elements = min(sum(cs < a) + 1, x.nnz)  # rounding errors sometimes results in n_elements > x.nnz

    new_ind = x.indices[ind[:n_elements]]
    new_data = x.data[ind[:n_elements]]
    return csr_matrix((new_data, new_ind, [0, n_elements]), shape=x.shape)


# a basic sparse index based on sparse matrix multiplication
# methods:
# 1. init: from a csr matrix of data.
# 2. query:
#    - k (# of neighbors),
#    - alpha (fraction of the sum of the vector elements to maintain. alpha=1 is exact search).
class SparseMatMul(BaseANN):
    def __init__(self, metric, index_params):
        print(metric, index_params)
        self.name = "spmat"
        self.nt = index_params.get("threads", 1)

    def fit(self, dataset):
        self.ds = DATASETS[dataset]()
        self.data_csc = self.ds.get_dataset().tocsc()
    
    def load_index(self, dataset):
        return None

    def set_query_arguments(self, query_args):
        self._alpha = query_args["alpha"]

    def _process_single_row(self, i):     
        res = self._single_query(q=self.queries.getrow(i))
        self.I[i, :] = [rr[0] for rr in res]         


    def _single_query(self, q, k=10):
        if self._alpha == 1:
                q = q.transpose()
        else:
            q = largest_elements(q, self._alpha).transpose()
        # perform (sparse) matrix-vector multiplication
        res = self.data_csc.dot(q)

        if res.nnz <= k:  # if there are less than k elements with nonzero score, simply return them
            return  list(zip(res.indices, res.data))
        # extract the top k from the res sparse array directly
        indices = np.argpartition(res.data, -(k + 1))[-k:]
        results = []
        for index in indices:
            results.append((res.data[index], index))
        results.sort(reverse=True)
        return [(res.indices[b], a) for a, b in results]

    def query(self, X, k):  # Carry out a batch query for k-NN of query set X.

        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int32')
        self.queries = X

        if self.nt is None:
            for i in range(nq):
                self._process_single_row(i)
        else:
            with ThreadPool(processes=self.nt) as pool:
                # Map the function to the array of items
                list(pool.imap(self._process_single_row, range(nq)))

    def get_results(self):
        return self.I


