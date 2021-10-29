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
    'bigann': [54, 52, 48, 23, 78, 82, 84, 80, 113, 42, 83, 85, 81, 43, 51, 53, 49, 77, 75, 79, 40, 41, 47, 73, 112, 114, 111, 118, 87, 72, 16, 22, 9, 18, 122, 120, 91, 24, 30, 17, 62, 60, 56, 31, 34, 36, 32, 67, 1, 90, 92, 88, 121, 15, 0, 13, 70, 68, 64, 103, 37, 102, 96, 69, 8, 10, 14, 104, 110, 106, 44, 46, 55, 74, 76, 61, 59, 63, 35, 33, 2, 66, 38, 89, 95, 65, 71, 58, 94, 4, 6, 98, 100, 26, 28, 11, 107, 109, 124, 126, 19, 21, 115, 117, 119, 57, 39, 3, 5, 7, 12, 20, 25, 27, 29, 45, 50, 86, 93, 97, 99, 101, 105, 108, 116, 123, 125, 127], #mc
    'deep': [21, 0, 22, 20, 67, 40, 88, 43, 89, 13, 32, 79, 50, 2, 31, 39, 53, 1, 24, 15, 3, 26, 63, 70, 42, 93, 57, 85, 35, 61, 29, 46, 10, 76, 49, 45, 19, 41, 18, 58, 27, 4, 47, 12, 74, 14, 9, 44, 56, 60, 65, 8, 16, 86, 87, 94, 77, 36, 59, 71, 7, 80, 33, 37, 92, 82, 55, 5, 54, 38, 66, 51, 52, 30, 69, 83, 11, 91, 62, 34, 25, 48, 6, 73, 64, 68, 84, 78, 23, 90, 17, 81, 72, 75, 28, 95], #blended
    'ssnpp': [83, 0, 84, 82, 115, 113, 74, 192, 142, 133, 239, 206, 213, 57, 185, 123, 109, 112, 3, 23, 168, 45, 194, 174, 35, 41, 36, 195, 240, 154, 51, 172, 68, 156, 166, 243, 252, 175, 237, 76, 117, 111, 12, 48, 47, 189, 88, 198, 137, 125, 163, 108, 217, 227, 44, 149, 186, 90, 129, 184, 221, 40, 42, 190, 234, 214, 231, 102, 32, 247, 207, 96, 94, 17, 254, 180, 188, 250, 204, 121, 140, 143, 199, 203, 105, 144, 220, 110, 208, 138, 223, 255, 134, 152, 169, 212, 13, 120, 67, 159, 75, 28, 104, 9, 31, 130, 251, 224, 95, 136, 150, 81, 178, 89, 145, 141, 122, 176, 248, 56, 183, 10, 58, 232, 49, 5, 6, 46, 167, 27, 233, 229, 65, 210, 241, 114, 55, 249, 216, 19, 209, 77, 193, 151, 87, 85, 29, 30, 235, 202, 165, 244, 11, 164, 146, 43, 72, 225, 116, 196, 69, 200, 59, 63, 1, 127, 191, 107, 173, 80, 119, 179, 205, 7, 70, 253, 79, 52, 170, 222, 16, 197, 8, 25, 131, 34, 50, 66, 155, 4, 98, 14, 39, 135, 215, 219, 153, 126, 93, 78, 218, 71, 64, 15, 181, 187, 147, 22, 26, 62, 54, 246, 177, 139, 160, 230, 2, 100, 86, 38, 226, 97, 21, 60, 245, 161, 91, 61, 106, 99, 20, 171, 103, 157, 132, 124, 182, 211, 18, 24, 101, 128, 158, 238, 92, 73, 148, 37, 228, 162, 236, 33, 53, 242, 201, 118], #blended
    'text2image': [81, 0, 38, 60, 155, 125, 11, 69, 110, 21, 14, 199, 186, 40, 129, 12, 57, 188, 172, 141, 105, 191, 2, 10, 117, 120, 154, 196, 148, 17, 48, 192, 111, 41, 9, 190, 36, 98, 146, 189, 126, 180, 61, 3, 29, 183, 43, 100, 93, 134, 197, 160, 77, 115, 122, 96, 32, 149, 161, 47, 130, 94, 131, 151, 18, 51, 75, 164, 50, 27, 74, 167, 95, 107, 23, 89, 86, 181, 101, 113, 56, 49, 55, 25, 114, 165, 6, 123, 99, 97, 104, 52, 169, 71, 102, 24, 66, 121, 64, 142, 80, 33, 179, 65, 83, 7, 44, 139, 174, 35, 31, 5, 16, 42, 30, 156, 150, 91, 194, 159, 127, 173, 185, 88, 177, 63, 76, 108, 39, 90, 138, 168, 144, 152, 106, 184, 118, 135, 84, 58, 82, 22, 112, 70, 195, 143, 182, 15, 59, 79, 1, 166, 157, 54, 20, 170, 140, 28, 145, 187, 72, 163, 87, 103, 85, 62, 46, 124, 176, 73, 92, 26, 162, 34, 67, 137, 37, 4, 158, 109, 68, 128, 153, 132, 133, 147, 178, 136, 19, 53, 193, 78, 175, 119, 116, 45, 8, 13, 198, 171], #blended
    'msturing': [20, 0, 19, 4, 41, 98, 49, 88, 79, 15, 48, 21, 64, 34, 63, 36, 44, 29, 66, 28, 43, 17, 35, 50, 24, 92, 71, 2, 78, 22, 59, 9, 23, 46, 58, 53, 55, 60, 94, 61, 16, 27, 14, 69, 72, 40, 7, 6, 62, 68, 81, 8, 91, 38, 11, 73, 1, 97, 96, 77, 10, 93, 30, 67, 31, 82, 52, 47, 80, 90, 76, 74, 51, 25, 75, 87, 33, 26, 3, 39, 95, 32, 45, 42, 84, 18, 37, 65, 54, 5, 99, 85, 13, 56, 89, 57, 83, 70, 12, 86], #blended
    'msspacev': [85, 0, 86, 84, 83, 82, 25, 39, 90, 26, 18, 20, 54, 98, 15, 95, 65, 23, 70, 51, 73, 76, 92, 21, 64, 40, 67, 87, 19, 66, 75, 96, 6, 16, 91, 78, 81, 79, 34, 55, 71, 37, 24, 5, 52, 72, 74, 60, 77, 99, 56, 97, 9, 53, 50, 12, 93, 2, 3, 1, 58, 57, 88, 49, 68, 35, 61, 7, 43, 80, 89, 17, 38, 13, 8, 22, 69, 28, 48, 47, 29, 62, 30, 32, 33, 31, 42, 36, 10, 4, 94, 63, 46, 45, 44, 14, 11, 41, 27, 59], #blended
    'random': []
}

def buddy_up(points,dataset_prefix,copy=True):
    #rearranges the points to put buddy dimensions next to each other.
    #this will be used during PQ to get ideal subvectors without needing to modify Faiss
    #friends is a 1D array of dimension indexes in order of their buddiness.
    #for example if dims 12,17,18,50,52,96,101,113 are buddies, then they would appear as:
    #[...,12,17,18,50,52,96,101,113,...] in the friends param.
    if dataset_prefix=="random":
        return points
        
    friends = multicollinearity_buddies[dataset_prefix]
    if len(friends):
        #print(f'Dataset {dataset_prefix} broadcasting to {friends}')
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

        self.set_dataset(dataset)
        self.dimensions = d

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
        self.set_dataset(dataset)
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
