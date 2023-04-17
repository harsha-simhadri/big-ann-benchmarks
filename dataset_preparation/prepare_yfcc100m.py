
import os
import numpy as np
import pickle
from scipy.sparse import csr_matrix

try:
    from ..benchmark import datasets, dataset_io
except ImportError:
    import datasets, dataset_io



ds = datasets.YFCC100MDataset()
print(ds)

# todo = "query_vecs query_meta database_vecs database_meta"
todo = "query_vecs query_meta"


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
all_descriptors_valid = all_descriptors_valid < 230
print(f"valid descriptors: {all_descriptors_valid.sum()}/{all_descriptors_valid.size}")


fname = metadata_dir + "query_array.npy"
print("load query metadata", fname)
query_array = np.load(fname)
# format: 200k rows 4 columns with of word1, word2, frequency, query vector id
# word2 may be -1 for single-word queries
print("   size", query_array.shape)

qids = query_array[:, 3]
# filter out invalid ones
valid_mask = all_descriptors_valid[qids]
print(f"valid mask size: {valid_mask.sum()}/{valid_mask.size}")
voc_size = 200000 + 386


if "query_vecs" in todo or "query_meta" in todo:

    # public queries: the 100k first ones
    subset = np.where(valid_mask)[0][:200000]

    if "query_vecs" in todo:
        # pick the descriptors
        descs = all_descriptors[qids[subset]]

        # write out
        fname = os.path.join(ds.basedir, ds.qs_fn)
        fname2 = os.path.join(ds.basedir, ds.qs_private_fn)
        print("write", fname, fname2)
        dataset_io.u8bin_write(descs[:100000], fname)
        dataset_io.u8bin_write(descs[100000:200000], fname2)

    if "query_meta" in todo:
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
        print("  queries size: ", queries_sparse.shape)
        queries_sparse = queries_sparse[valid_mask]
        print("  valid queries size: ", queries_sparse.shape)

        # write query metadata
        fname = os.path.join(ds.basedir, ds.qs_metadata_fn)
        fname2 = os.path.join(ds.basedir, ds.qs_private_metadata_fn)
        print("write", fname, fname2)
        dataset_io.write_sparse_matrix(queries_sparse[:100000], fname)
        dataset_io.write_sparse_matrix(queries_sparse[100000:200000], fname2)

if "database_vecs" in todo or "database_meta" in todo:
    available_mask = all_descriptors_valid.copy()
    available_mask[qids] = False

    print(f"Available for use in the database: "
          f"{available_mask.sum()}/{available_mask.size}")

    nb = 10_000_000

    rs = np.random.RandomState(123)
    available = np.where(available_mask)[0]
    subset = rs.choice(available, nb)
    subset.sort()  # may be useful to not randomly access the vectors

    print(f"selected {len(subset)} / {len(available)} vectors")

    if "database_vecs" in todo:
        descs = all_descriptors[subset]

        fname = os.path.join(ds.basedir, ds.ds_fn)
        print("write", fname)
        dataset_io.u8bin_write(descs, fname)

    if "database_meta" in todo:

        # handle metadata
        fname = metadata_dir + "combined_matrix.pickle"
        print("loading", fname)
        combined_data = pickle.load(open(fname, "rb"))

        combined_words = combined_data["combined_words"]
        combined_matrix = combined_data["combined_matrix"]

        print(f"loaded metadta shape {combined_matrix.shape} "
              f"nnz={combined_matrix.nnz}")
        fname = os.path.join(ds.basedir, "words.txt")
        print("write", fname)
        open(fname, "w").write("\n".join(combined_words))

        database_matrix = combined_matrix[subset]
        print(f"subset shape {database_matrix.shape} "
              f"nnz={database_matrix.nnz}")

        fname = os.path.join(ds.basedir, ds.ds_metadata_fn)
        print("write", fname)
        dataset_io.write_sparse_matrix(database_matrix, fname)


