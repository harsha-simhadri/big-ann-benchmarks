
import os
import numpy as np
from scipy.sparse import csr_matrix

try:
    from ..benchmark import datasets, dataset_io
except ImportError:
    import datasets, dataset_io



ds = datasets.YFCC100MDataset()
print(ds)

todo = "query_vecs"


# for now, we work with random descriptors

# dd if=/dev/urandom of=/scratch/matthijs/tmp/random_yfcc100m_descriptors.384d.uint8 bs=384 count=$((100 * 1000 * 1000))

tmpdir = "/scratch/matthijs/tmp/"

# data generated from external scripts
metadata_dir = "/checkpoint/matthijs/billion-scale-ann-benchmarks/yfcc_metadata/"

all_descriptors = np.memmap(
    tmpdir + "random_yfcc100m_descriptors.384d.uint8", mode='r',
    shape=(10**8, 384), dtype='uint8'
)

# simulate feature extraction failure: we have a flag for each descriptor about validity

all_descriptors_valid = np.fromfile(
    tmpdir + "random_yfcc100m_descriptors.valid.uint8",
    count=10**8, dtype='uint8'
)
# make boolean array
all_descriptors_valid = all_descriptors_valid < 200



if "query_vecs" in todo:
    voc_size = 200000 + 386
    fname = metadata_dir + "query_array.npy"
    print("load query metadata", fname)
    query_array = np.load(fname)
    # format: 200k rows 4 columns with of word1, word2, frequency, query vector id
    # word2 may be -1 for single-word queries
    print("   size", query_array.shape)

    qids = query_array[:, 3]
    # filter out invalid ones
    valid_mask = all_descriptors_valid[qids]

    # public queries: the 100k first ones
    subset = np.where(valid_mask)[0][:100000]

    # pick the descriptors
    descs = all_descriptors[qids[subset]]

    # write out
    fname = os.path.join(ds.basedir, ds.qs_fn)
    print("write", fname)
    dataset_io.u8bin_write(descs, fname)

    # build query term sparse matrix
    is_2word = query_array[:, 1] >= 0
    words_per_q = 1 + is_2word.astype(int)
    nq = len(query_array)
    indptr = np.zeros(nq + 1, dtype=int)
    indptr[1:] = np.cumsum(words_per_q)
    indices = query_array[:, :2].ravel()
    indices = indices[indices >= 0]
    nnz = indices.size
    queries_sparse = csr_matrix(
        (np.ones(nnz, dtype='float32'), indices, indptr),
        shape = (nq, voc_size)
    )

    # write query metadata
    fname = os.path.join(ds.basedir, ds.qs_metadata_fn)
    print("write", fname)
    dataset_io.write_sparse_matrix(queries_sparse[:100000], fname)





