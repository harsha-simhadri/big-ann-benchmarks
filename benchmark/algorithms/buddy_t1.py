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
    'deep': [87, 27, 21, 28, 83, 48, 88, 63, 93, 17, 39, 40, 8, 19, 6, 42, 15, 79, 57, 46, 82, 38, 85, 44, 3, 86, 75, 89, 7, 29, 14, 2, 84, 53, 77, 36, 35, 74, 41, 37, 73, 67, 54, 58, 11, 70, 62, 65, 32, 4, 81, 9, 51, 10, 78, 43, 1, 61, 49, 24, 95, 45, 0, 25, 90, 18, 68, 64, 23, 94, 92, 91, 76, 22, 50, 30, 55, 47, 60, 20, 59, 52, 66, 31, 34, 56, 26, 69, 13, 16, 72, 12, 80, 5, 71, 33],
    'ssnpp': [210, 161, 2, 230, 110, 125, 122, 45, 91, 55, 246, 165, 164, 82, 103, 180, 252, 245, 207, 140, 60, 142, 240, 136, 115, 143, 88, 101, 228, 117, 120, 11, 89, 188, 17, 167, 18, 12, 224, 234, 15, 14, 185, 87, 250, 139, 174, 155, 97, 92, 241, 227, 53, 197, 114, 107, 212, 145, 194, 4, 9, 251, 109, 66, 54, 141, 183, 95, 173, 42, 7, 223, 21, 219, 25, 44, 249, 70, 159, 157, 28, 232, 71, 86, 10, 98, 233, 34, 31, 181, 29, 169, 132, 108, 77, 49, 225, 32, 192, 195, 64, 94, 56, 75, 72, 100, 133, 51, 26, 129, 211, 123, 13, 93, 90, 209, 131, 1, 214, 196, 83, 57, 137, 205, 199, 113, 58, 80, 112, 65, 16, 203, 187, 156, 179, 237, 191, 69, 147, 121, 182, 247, 37, 61, 76, 253, 24, 85, 78, 238, 168, 23, 178, 231, 190, 62, 30, 176, 41, 236, 39, 226, 118, 166, 0, 134, 22, 81, 124, 3, 35, 47, 189, 5, 127, 96, 243, 63, 128, 84, 138, 106, 154, 242, 48, 217, 153, 67, 213, 160, 171, 8, 102, 254, 150, 135, 46, 239, 148, 170, 201, 158, 36, 144, 235, 146, 6, 149, 27, 200, 116, 162, 152, 206, 202, 172, 175, 40, 198, 119, 99, 104, 184, 244, 229, 163, 220, 177, 59, 79, 204, 74, 222, 52, 111, 221, 33, 208, 130, 50, 248, 186, 43, 216, 215, 68, 19, 126, 38, 218, 105, 255, 193, 20, 73, 151],
    'text2image': [37, 59, 81, 149, 20, 154, 109, 195, 168, 117, 13, 28, 187, 48, 68, 92, 133, 110, 147, 145, 124, 180, 10, 88, 11, 198, 166, 125, 188, 176, 189, 179, 99, 167, 171, 23, 55, 2, 140, 47, 39, 1, 116, 159, 35, 148, 175, 155, 97, 122, 178, 119, 128, 74, 16, 163, 8, 42, 85, 120, 31, 191, 87, 153, 127, 56, 186, 173, 52, 82, 193, 139, 157, 27, 7, 80, 72, 177, 22, 50, 151, 156, 199, 67, 95, 194, 183, 165, 90, 101, 131, 197, 181, 141, 60, 66, 61, 132, 12, 142, 138, 174, 44, 170, 123, 137, 83, 24, 76, 6, 19, 115, 41, 134, 94, 25, 162, 5, 106, 63, 150, 64, 70, 45, 51, 144, 146, 78, 58, 113, 4, 3, 136, 34, 111, 121, 0, 15, 17, 77, 49, 9, 103, 182, 130, 14, 143, 196, 161, 169, 53, 112, 38, 129, 102, 40, 104, 93, 164, 107, 91, 26, 192, 71, 54, 57, 98, 89, 62, 184, 75, 79, 108, 190, 18, 158, 73, 160, 21, 29, 30, 32, 33, 36, 43, 46, 65, 69, 84, 86, 96, 100, 105, 114, 118, 126, 135, 152, 172, 185],
    'msturing': [],
    'msspacev': [],
    'random': []
}

def buddy_up(points,dataset_prefix,copy=True):
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

def buddy_random(points,d,copy=True):
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
        B = buddy_up(X,self.dataset_prefix,copy=False)
        if self._query_bs == -1:
            self.res = self.index.search(B, n)
        else:
            self.res = knn_search_batched(self.index, B, n, self._query_bs)

    def range_query(self, X, radius):
        print(f'Range querying {X.shape} and radius {radius} for dataset {self.dataset_prefix}')
        #B = buddy_random(X,X.shape[1])
        B = buddy_up(X,self.dataset_prefix,copy=False)
        if self._query_bs != -1:
            raise NotImplemented
        self.res = self.index.range_search(B, radius)

    def get_results(self):
        D, I = self.res
        return I

    def get_range_results(self):
        return self.res
