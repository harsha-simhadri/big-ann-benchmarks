
import os
import numpy as np
import pickle
from multiprocessing.pool import ThreadPool
import faiss

from scipy.sparse import csr_matrix


from benchmark import datasets, dataset_io

ds = datasets.YFCC100MDataset()
print(ds)

todo = "query_vecs query_meta database_vecs database_meta"

# for now, we work with random descriptors

# dd if=/dev/urandom of=/scratch/matthijs/tmp/random_yfcc100m_descriptors.384d.uint8 bs=384 count=$((100 * 1000 * 1000))

tmpdir = "/scratch/matthijs/tmp/"

# data generated from external scripts
metadata_dir = "/checkpoint/matthijs/billion-scale-ann-benchmarks/yfcc_metadata/"

class ClipDescriptors:

    def __init__(self):
        self.local_basedir = "/scratch/matthijs/billion-scale-ann-benchmarks/yfcc100M/dense_decoded/"
        self.basedir = "/checkpoint/matthijs/billion-scale-ann-benchmarks/yfcc100M/"
        self.hdf5_map = np.load(self.basedir + "hdf5_ptr.npy")
        self.mmaps = [None] * 4096
        self.shape = (10**8, 192)
        self.pool = ThreadPool(32)

    def valid(self):
        return self.hdf5_map >= 0

    def get_mmap(self, i):
        mm = self.mmaps[i]
        if mm is not None:
            return mm
        # does not seem useful to add a lock
        mm = np.load(f"{self.local_basedir}//features_{i:03x}.hdf5.tab.npy", mmap_mode="r")
        self.mmaps[i] = mm
        return mm

    def __getitem__(self, items):
        if type(items) == int:
            items = [items]
        subset = self.hdf5_map[items]
        res = np.zeros((len(subset), 192), dtype='float32')
        # for i, j in enumerate(subset):
        def handle(i):
            j = subset[i]
            if j < 0:
                return
            res[i] = self.get_mmap(j >> 16)[j & 0xffff]

        self.pool.map(handle, range(len(subset)))
        return res

print(ds.basedir)

if False:
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
elif False:
    # a bit less dummy descriptros, they come from https://github.com/facebookresearch/low-shot-with-diffusion
    mat = np.memmap("/scratch/matthijs/concatenated_PCAR256.raw", dtype='float32', shape=(10**8, 256), mode='r')
    bad_vec = mat[771]
    PCA = faiss.PCAMatrix(256, 192, 0, True)
    print("train PCA")
    xt = mat[12*10**6:][:20000]
    PCA.train(xt)
    xt = PCA.apply(xt)
    codec = faiss.ScalarQuantizer(192, faiss.ScalarQuantizer.QT_8bit_uniform)
    codec.train(xt)
    all_descriptors = mat
    all_descriptors_valid = np.load("/scratch/matthijs/concatenated_valid.npy")
else: # the real CLIP descriptors from Zilliz
    mat = ClipDescriptors()
    print("train random rotation and quatizer")
    rrot = faiss.RandomRotationMatrix(mat.shape[1], 192)
    rrot.init(5)
    all_descriptors_valid = mat.valid()
    it0 = 12_000_000
    xt = mat[it0:it0 + 30_000][all_descriptors_valid[it0:it0 + 30_000]]
    print("train on", xt.shape)
    xt = rrot.apply(xt)
    codec = faiss.ScalarQuantizer(192, faiss.ScalarQuantizer.QT_8bit_uniform)
    codec.train(xt)
    all_descriptors = mat
    PCA = rrot

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
        descs = codec.compute_codes(PCA.apply(all_descriptors[qids[subset]]))

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
        descs = codec.compute_codes(PCA.apply(all_descriptors[subset]))

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


