import numpy as np
import faiss
import bow_id_selector

sp = faiss.swig_ptr

from benchmark.datasets import DATASETS

ds = DATASETS["yfcc-10M"]()

print("load dataset + query metadata")
meta_b = ds.get_dataset_metadata()
meta_q = ds.get_queries_metadata()
print("Sort")
meta_b.sort_indices()

#size_t nb, const int64_t *lims, const int32_t *indices,
#        int32_t w1, int32_t w2):


print(meta_b.indptr.dtype)

rs = np.random.RandomState(123)



def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]

print("TEST")

for i in range(500):
    j = rs.choice(meta_b.shape[0])
    row = csr_get_row_indices(meta_b, j)

    if len(row) < 3:
        continue

    w12 = rs.choice(row, 2)

    cc = rs.choice(3)
    if cc == 1:
        w12[1] = -1

    if cc == 2:
        w12[i % 2] += 1
        if w12[i % 2] in row:
            continue

    sel = bow_id_selector.IDSelectorBOW(
        meta_b.shape[0], sp(meta_b.indptr),
        sp(meta_b.indices))

    sel.set_query_words(int(w12[0]), int(w12[1]))

    if cc == 0 or cc == 1:
        assert sel.is_member(int(j))
    else:
        assert not sel.is_member(int(j))


def intersect_sorted(a1, a2):
    n1, = a1.shape
    n2, = a2.shape
    res = np.empty(n1 + n2, dtype=a1.dtype)
    nres = bow_id_selector.intersect_sorted(
        n1, faiss.swig_ptr(a1),
        n2, faiss.swig_ptr(a2),
        faiss.swig_ptr(res)
    )
    return res[:nres]


print(intersect_sorted(
    np.array([1, 3, 6, 8, 10], dtype='int32'),
    np.array([1, 5,8, 10], dtype='int32')
))