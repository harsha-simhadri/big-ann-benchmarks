import scipy.sparse
from scipy.sparse import csr_matrix, vstack
import numpy as np

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


# a basic sparse index.
# methods:
# 1. init: from a csr matrix of data.
# 2. query a singe vector, with parameters:
#    - k (# of neighbors),
#    - alpha (fraction of the sum of the vector to maintain. alpha=1 is exact search).
class BasicSparseIndex(object):
    # build an index from the inout vectors. If none are supplied, default to an empty matrix.
    def __init__(self, data_csr=csr_matrix((0, 0))):
        self.data_csc = data_csr.tocsc()


    # append the incoming vector to the index (not very efficient)
    def append(self, new_data_csr):
        self.data_csc = vstack((self.data_csc, new_data_csr), format='csc')

    def query(self, q, k, alpha=1):  # single query, assumes q is a row vector
        if alpha == 1:
            q2 = q.transpose()
        else:
            q2 = largest_elements(q, alpha).transpose()

        # perform (sparse) matrix-vector multiplication
        res = self.data_csc.dot(q2)

        if res.nnz <= k:  # if there are less than k elements with nonzero score, simply return them
            return list(zip(res.indices, res.data))

        # extract the top k from the res sparse array directly
        indices = np.argpartition(res.data, -(k + 1))[-k:]
        results = []
        for index in indices:
            results.append((res.data[index], index))
        results.sort(reverse=True)
        return [(res.indices[b], a) for a, b in results]
