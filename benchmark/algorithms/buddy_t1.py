from __future__ import absolute_import
import numpy as np
import sklearn.preprocessing
import ctypes
import faiss
import os
import time
import random
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

randos = {}
random.seed(505)
for i in [128,256,100,96,200]:
    randos[i] = list(range(i))
    random.shuffle(randos[i])

multicollinearity_buddies = {
    'bigann': [54, 52, 48, 23, 78, 82, 84, 80, 113, 42, 83, 85, 81, 43, 51, 53, 49, 77, 75, 79, 40, 41, 47, 73, 112, 114, 111, 118, 87, 72, 16, 22, 9, 18, 122, 120, 91, 24, 30, 17, 62, 60, 56, 31, 34, 36, 32, 67, 1, 90, 92, 88, 121, 15, 0, 13, 70, 68, 64, 103, 37, 102, 96, 69, 8, 10, 14, 104, 110, 106, 44, 46, 55, 74, 76, 61, 59, 63, 35, 33, 2, 66, 38, 89, 95, 65, 71, 58, 94, 4, 6, 98, 100, 26, 28, 11, 107, 109, 124, 126, 19, 21, 115, 117, 119, 57, 39, 3, 5, 7, 12, 20, 25, 27, 29, 45, 50, 86, 93, 97, 99, 101, 105, 108, 116, 123, 125, 127],
    'deep': [],
    'ssnpp': [210, 2, 110, 161, 230, 180, 26, 80, 114, 119, 142, 144, 192, 212, 17, 12, 15, 18, 167, 207, 224, 234, 97, 32, 54, 232, 10, 34, 98, 164, 233, 56, 72, 75, 100, 245, 1, 57, 92, 115, 122, 160, 217, 183, 11, 69, 86, 117, 208, 255, 155, 43, 74, 137, 37, 214, 247, 30, 62, 213, 77, 21, 44, 52, 84, 145, 189, 5, 13, 96, 112, 127, 251, 82, 23, 113, 166, 174, 3, 85, 125, 220, 254, 48, 105, 150, 191, 202, 140, 7, 53, 60, 99, 132, 177, 250, 146, 6, 28, 65, 120, 236, 182, 253, 168, 58, 79, 87, 88, 170, 185, 228, 111, 24, 35, 243, 78, 8, 41, 81, 89, 159, 169, 201, 237, 135, 40, 152, 190, 226, 136, 9, 90, 139, 0, 46, 133, 179, 204, 235, 73, 198, 209, 239, 134, 103, 131, 27, 45, 71, 130, 157, 165, 14, 31, 240, 101, 249, 39, 106, 246, 178, 50, 126, 218, 200, 199, 216, 147, 193, 194, 61, 102, 229, 66, 76, 47, 248, 4, 19, 196, 94, 162, 242, 25, 129, 59, 153, 36, 64, 163, 95, 206, 221, 215, 116, 203, 93, 118, 128, 211, 175, 197, 107, 67, 104, 143, 38, 109, 238, 33, 176, 231, 83, 148, 171, 205, 16, 244, 29, 20, 141, 222, 172, 49, 156, 187, 241, 186, 22, 42, 51, 195, 188, 219, 63, 158, 154, 225, 55, 68, 70, 91, 108, 121, 123, 124, 138, 149, 151, 173, 181, 184, 223, 227, 252],
    'text2image': [],
    'msturing': [],
    'msspacev': [],
    'random': []
}

def buddy_up(points,dataset_prefix):
    #rearranges the points to put buddy dimensions next to each other.
    #this will be used during PQ to get ideal subvectors without needing to modify Faiss
    #friends is a 1D array of dimension indexes in order of their buddiness.
    #for example if dims 12,17,18,50,52,96,101,113 are buddies, then they would appear as:
    #[...,12,17,18,50,52,96,101,113,...] in the friends param.
    friends = multicollinearity_buddies[dataset_prefix]
    if len(friends):
        print(f'Dataset {dataset_prefix} broadcasting to {friends}')
        buddies = points[:,friends].copy(order='C')
    else:
        print(f'Dataset {dataset_prefix} has no buddy list')
        buddies = points
    return buddies

def buddy_random(points,d):
    #use a random shuffle for the dataset shape
    print(f'Shape {d} of {points.shape} has random broadcast {randos[d]}')
    buddies = points[:,randos[d]].copy(order='C')
    return buddies

def knn_search_batched(index, xq, k, bs):
    D, I = [], []
    for i0 in range(0, len(xq), bs):
        Di, Ii = index.search(xq[i0:i0 + bs], k)
        D.append(Di)
        I.append(Ii)
    return np.vstack(D), np.vstack(I)

def unwind_index_ivf(index):
    if isinstance(index, faiss.IndexPreTransform):
        assert index.chain.size() == 1
        vt = faiss.downcast_VectorTransform(index.chain.at(0))
        index_ivf, vt2 = unwind_index_ivf(faiss.downcast_index(index.index))
        assert vt2 is None
        return index_ivf, vt
    if hasattr(faiss, "IndexRefine") and isinstance(index, faiss.IndexRefine):
        return unwind_index_ivf(faiss.downcast_index(index.base_index))
    if isinstance(index, faiss.IndexIVF):
        return index, None
    else:
        return None, None

def two_level_clustering(xt, nc1, nc2, clustering_niter=25, spherical=False):
    d = xt.shape[1]

    print(f"2-level clustering of {xt.shape} nb clusters = {nc1}*{nc2} = {nc1*nc2}")
    print("perform coarse training")

    km = faiss.Kmeans(
        d, nc1, verbose=True, niter=clustering_niter,
        max_points_per_centroid=2000,
        spherical=spherical
    )
    km.train(xt)

    # coarse centroids
    centroids1 = km.centroids

    print("assigning the training set")
    t0 = time.time()
    _, assign1 = km.assign(xt)
    bc = np.bincount(assign1, minlength=nc1)
    print(f"done in {time.time() - t0:.2f} s. Sizes of clusters {min(bc)}-{max(bc)}")
    o = assign1.argsort()
    del km

    # train sub-clusters
    i0 = 0
    c2 = []
    t0 = time.time()
    for c1 in range(nc1):
        print(f"[{time.time() - t0:.2f} s] training sub-cluster {c1}/{nc1}\r", end="", flush=True)
        i1 = i0 + bc[c1]
        subset = o[i0:i1]
        assert np.all(assign1[subset] == c1)
        km = faiss.Kmeans(d, nc2, spherical=spherical)
        xtsub = xt[subset]
        km.train(xtsub)
        c2.append(km.centroids)
        i0 = i1
    print(f"done in {time.time() - t0:.2f} s")
    return np.vstack(c2)


class Buddy(BaseANN):
    def __init__(self, metric, index_params):
        self._index_params = index_params
        self._metric = metric
        self._query_bs = -1
        self.indexkey = index_params.get("indexkey", "OPQ32_128,IVF65536_HNSW32,PQ32")

        if 'query_bs' in index_params:
            self._query_bs = index_params['query_bs']

    def track(self):
        return "T1"

    def index_name(self, name):
        return f"data/{name}.buddy.multicollinearity.{self.indexkey}.faissindex"

    def set_dataset(self, dataset):
        self.dataset = dataset
        self.dataset_prefix = dataset[:dataset.rfind('-')]

    def fit(self, dataset):
        index_params = self._index_params

        ds = DATASETS[dataset]()
        d = ds.d

        self.dataset_prefix = dataset[:dataset.rfind('-')]
        self.dimensions = d
        print(self.dataset_prefix,self.dimensions)

        # get build parameters
        buildthreads = index_params.get("buildthreads", -1)
        by_residual = index_params.get("by_residual", -1)
        maxtrain = index_params.get("maxtrain", 0)
        clustering_niter = index_params.get("clustering_niter", -1)
        add_bs = index_params.get("add_bs", 100000)
        add_splits = index_params.get("add_splits", 1)
        efSearch = index_params.get("quantizer_add_efSearch", 80)
        efConstruction = index_params.get("quantizer_efConstruction", 200)
        use_two_level_clustering = index_params.get("two_level_clustering", True)
        indexfile = self.index_name(dataset)

        if buildthreads == -1:
            print("Build-time number of threads:", faiss.omp_get_max_threads())
        else:
            print("Set build-time number of threads:", buildthreads)
            faiss.omp_set_num_threads(buildthreads)

        metric_type = (
                faiss.METRIC_L2 if ds.distance() == "euclidean" else
                faiss.METRIC_INNER_PRODUCT if ds.distance() in ("ip", "angular") else
                1/0
        )
        index = faiss.index_factory(d, self.indexkey, metric_type)

        index_ivf, vec_transform = unwind_index_ivf(index)
        if vec_transform is None:
            vec_transform = lambda x: x
        else:
            vec_transform = faiss.downcast_VectorTransform(vec_transform)

        if by_residual != -1:
            by_residual = by_residual == 1
            print("setting by_residual = ", by_residual)
            index_ivf.by_residual   # check if field exists
            index_ivf.by_residual = by_residual

        if index_ivf:
            print("Update add-time parameters")
            # adjust default parameters used at add time for quantizers
            # because otherwise the assignment is inaccurate
            quantizer = faiss.downcast_index(index_ivf.quantizer)
            if isinstance(quantizer, faiss.IndexRefine):
                print("   update quantizer k_factor=", quantizer.k_factor, end=" -> ")
                quantizer.k_factor = 32 if index_ivf.nlist < 1e6 else 64
                print(quantizer.k_factor)
                base_index = faiss.downcast_index(quantizer.base_index)
                if isinstance(base_index, faiss.IndexIVF):
                    print("   update quantizer nprobe=", base_index.nprobe, end=" -> ")
                    base_index.nprobe = (
                        16 if base_index.nlist < 1e5 else
                        32 if base_index.nlist < 4e6 else
                        64)
                    print(base_index.nprobe)
            elif isinstance(quantizer, faiss.IndexHNSW):
                print("   update quantizer efSearch=", quantizer.hnsw.efSearch, end=" -> ")
                if index_params.get("quantizer_add_efSearch", 80) > 0:
                    quantizer.hnsw.efSearch = efSearch
                else:
                    quantizer.hnsw.efSearch = 40 if index_ivf.nlist < 4e6 else 64
                print(quantizer.hnsw.efSearch)
                if efConstruction != -1:
                    print("  update quantizer efConstruction=", quantizer.hnsw.efConstruction, end=" -> ")
                    quantizer.hnsw.efConstruction = efConstruction
                    print(quantizer.hnsw.efConstruction)


        index.verbose = True
        if index_ivf:
            index_ivf.verbose = True
            index_ivf.quantizer.verbose = True
            index_ivf.cp.verbose = True


        if maxtrain == 0:
            if 'IMI' in self.indexkey:
                maxtrain = int(256 * 2 ** (np.log2(index_ivf.nlist) / 2))
            elif index_ivf:
                maxtrain = 50 * index_ivf.nlist
            else:
                # just guess...
                maxtrain = 256 * 100
            maxtrain = max(maxtrain, 256 * 100)
            print("setting maxtrain to %d" % maxtrain)

        # train on dataset
        print(f"getting first {maxtrain} dataset vectors for training")

        xt2 = next(ds.get_dataset_iterator(bs=maxtrain))
        #xt2 = buddy_random(xt2,d)
        xt2 = buddy_up(xt2,self.dataset_prefix)

        print("train, size", xt2.shape)
        assert np.all(np.isfinite(xt2))

        t0 = time.time()

        if (isinstance(vec_transform, faiss.OPQMatrix) and
            isinstance(index_ivf, faiss.IndexIVFPQFastScan)):
            print("  Forcing OPQ training PQ to PQ4")
            ref_pq = index_ivf.pq
            training_pq = faiss.ProductQuantizer(
                ref_pq.d, ref_pq.M, ref_pq.nbits
            )
            vec_transform.pq
            vec_transform.pq = training_pq

        if clustering_niter >= 0:
            print(("setting nb of clustering iterations to %d" %
                    clustering_niter))
            index_ivf.cp.niter = clustering_niter

        train_index = None

        if use_two_level_clustering:
            sqrt_nlist = int(np.sqrt(index_ivf.nlist))
            assert sqrt_nlist ** 2 == index_ivf.nlist

            centroids_trainset = xt2
            if isinstance(vec_transform, faiss.VectorTransform):
                print("  training vector transform")
                vec_transform.train(xt2)
                print("  transform trainset")
                centroids_trainset = vec_transform.apply_py(centroids_trainset)

            centroids = two_level_clustering(
                centroids_trainset, sqrt_nlist, sqrt_nlist,
                spherical=(metric_type == faiss.METRIC_INNER_PRODUCT)
            )

            if not index_ivf.quantizer.is_trained:
                print("  training quantizer")
                index_ivf.quantizer.train(centroids)

            print("  add centroids to quantizer")
            index_ivf.quantizer.add(centroids)

        index.train(xt2)
        print("  Total train time %.3f s" % (time.time() - t0))

        if train_index is not None:
            del train_index
            index_ivf.clustering_index = None
            gc.collect()

        print("adding")

        t0 = time.time()
        add_bs = index_params.get("add_bs", 10000000)
        if add_bs == -1:
            index.add(ds.get_database())
        else:
            i0 = 0
            for xblock in ds.get_dataset_iterator(bs=add_bs):
                #xblock = buddy_random(xblock,d)
                xblock = buddy_up(xblock,self.dataset_prefix)
                i1 = i0 + len(xblock)
                print("  adding %d:%d / %d [%.3f s, RSS %d kiB] " % (
                    i0, i1, ds.nb, time.time() - t0,
                    faiss.get_mem_usage_kb()))
                index.add(xblock)
                i0 = i1

        print("  add in %.3f s" % (time.time() - t0))
        print("storing", )
        faiss.write_index(index, self.index_name(dataset))

        self.index = index
        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.index)

    def load_index(self, dataset):
        if not os.path.exists(self.index_name(dataset)):
            if 'url' not in self._index_params:
                return False

            print('Downloading index in background. This can take a while.')
            download_accelerated(self._index_params['url'], self.index_name(dataset), quiet=True)

        print("Loading index")

        self.index = faiss.read_index(self.index_name(dataset))

        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.index)

        return True

    def set_query_arguments(self, query_args):
        faiss.cvar.indexIVF_stats.reset()
        self.ps.set_index_parameters(self.index, query_args)
        self.qas = query_args


    # shall we return something interesting here?
    def get_additional(self):
        return {"dist_comps": faiss.cvar.indexIVF_stats.ndis}

    def __str__(self):
        return f'FaissIVFPQ({self.qas})'



    def query(self, X, n):
        print(f'Querying {X.shape} for dataset {self.dataset_prefix}')
        #B = buddy_random(X,X.shape[1])
        B = buddy_up(X,self.dataset_prefix)
        if self._query_bs == -1:
            self.res = self.index.search(B, n)
        else:
            self.res = knn_search_batched(self.index, B, n, self._query_bs)

    def range_query(self, X, radius):
        print(f'Range querying {X.shape} and radius {radius} for dataset {self.dataset_prefix}')
        #B = buddy_random(X,X.shape[1])
        B = buddy_up(X,self.dataset_prefix)
        if self._query_bs != -1:
            raise NotImplemented
        self.res = self.index.range_search(B, radius)

    def get_results(self):
        D, I = self.res
        return I

    def get_range_results(self):
        return self.res
