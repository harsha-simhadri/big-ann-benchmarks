from __future__ import absolute_import
import numpy as np
import sklearn.preprocessing
import ctypes
import faiss
import os
import time
import gc
import resource
import threading
import json

from multiprocessing.pool import ThreadPool

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

def unwind_index_ivf(index):
    if isinstance(index, faiss.IndexPreTransform):
        assert index.chain.size() == 1
        vt = index.chain.at(0)
        index_ivf, vt2 = unwind_index_ivf(faiss.downcast_index(index.index))
        assert vt2 is None
        return index_ivf, vt
    if hasattr(faiss, "IndexRefine") and isinstance(index, faiss.IndexRefine):
        return unwind_index_ivf(faiss.downcast_index(index.base_index))
    if isinstance(index, faiss.IndexIVF):
        return index, None
    else:
        return None, None

def rate_limited_iter(l):
    'a thread pre-processes the next element'
    pool = ThreadPool(1)
    res = None

    def next_or_None():
        try:
            return next(l)
        except StopIteration:
            return None

    while True:
        res_next = pool.apply_async(next_or_None)
        if res is not None:
            res = res.get()
            if res is None:
                return
            yield res
        res = res_next

def build_index(buildthreads, by_residual, maxtrain, clustering_niter, 
     indexkey, indexfile, add_bs, add_splits, ds, train_on_gpu=True, quantizer_on_gpu_add=True):

    nq, d = ds.nq, ds.d
    nb, d = ds.nq, ds.d

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
    index = faiss.index_factory(d, indexkey, metric_type)

    index_ivf, vec_transform = unwind_index_ivf(index)
    if vec_transform is None:
        vec_transform = lambda x: x
    else:
        vec_transform = faiss.downcast_VectorTransform(vec_transform)

    if by_residual != -1:
        by_residual = by_residual == 1
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

    index.verbose = True
    if index_ivf:
        index_ivf.verbose = True
        index_ivf.quantizer.verbose = True
        index_ivf.cp.verbose = True

    if maxtrain == 0:
        if 'IMI' in indexkey:
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
    if train_on_gpu:
        print("add a training index on GPU")
        train_index = faiss.index_cpu_to_all_gpus(
                faiss.IndexFlatL2(index_ivf.d))
        index_ivf.clustering_index = train_index

    index.train(xt2)
    print("  Total train time %.3f s" % (time.time() - t0))

    if train_index is not None:
        del train_index
        index_ivf.clustering_index = None
        gc.collect()

    print("adding")

    t0 = time.time()

    if not quantizer_on_gpu_add:
        i0 = 0
        for xblock in ds.get_dataset_iterator(bs=add_bs):
            i1 = i0 + len(xblock)
            print("  adding %d:%d / %d [%.3f s, RSS %d kiB] " % (
                i0, i1, ds.nb, time.time() - t0,
                faiss.get_mem_usage_kb()))
            index.add(xblock)
            i0 = i1
    elif True:
        quantizer_gpu = faiss.index_cpu_to_all_gpus(index_ivf.quantizer)

        nsplit = add_splits

        def produce_batches(sno):
            for xblock in ds.get_dataset_iterator(bs=add_bs, split=(nsplit, sno)):
                _, assign = quantizer_gpu.search(xblock, 1)
                yield xblock, assign.ravel()

        i0 = 0
        for sno in range(nsplit):
            print(f"============== SPLIT {sno}/{nsplit}")

            stage2 = rate_limited_iter(produce_batches(sno))
            for xblock, assign in stage2:
                i1 = i0 + len(xblock)
                print("  adding %d:%d / %d [%.3f s, RSS %d kiB] " % (
                    i0, i1, ds.nb, time.time() - t0,
                    faiss.get_mem_usage_kb()))
                index.add_core(
                    len(xblock),
                    faiss.swig_ptr(xblock),
                    None,
                    faiss.swig_ptr(assign)
                )
                i0 = i1
        del quantizer_gpu
        gc.collect()

    print("  add in %.3f s" % (time.time() - t0))
    if indexfile:
        print("storing", indexfile)
        faiss.write_index(index, indexfile)

    return index

class IndexQuantizerOnGPU:
    """ run query quantization on GPU """

    def __init__(self, index, search_bs):
        self.search_bs = search_bs
        index_ivf, vec_transform = unwind_index_ivf(index)
        self.index_ivf = index_ivf
        if vec_transform:
#            print(type(vec_transform),dir(vec_transform))
            self.vec_transform = vec_transform.apply  
        else:
            self.vec_transform = None
        self.quantizer_gpu = faiss.index_cpu_to_all_gpus(self.index_ivf.quantizer)


    def produce_batches(self, x, bs):
        n = len(x)
        nprobe = self.index_ivf.nprobe
        ivf_stats = faiss.cvar.indexIVF_stats
        for i0 in range(0, n, bs):
            xblock = x[i0:i0 + bs]
            t0 = time.time()
            D, I = self.quantizer_gpu.search(xblock, nprobe)
            ivf_stats.quantization_time += 1000 * (time.time() - t0)
            yield i0, xblock, D, I


    def search(self, x, k):

        if x.dtype!=np.float32: #GW- why do we need this now?
            x = x.astype( np.float32 ) 

        bs = self.search_bs
        if self.vec_transform:
            x = self.vec_transform(x)
        nprobe = self.index_ivf.nprobe
        n, d = x.shape
        assert self.index_ivf.d == d
        D = np.empty((n, k), dtype=np.float32)
        I = np.empty((n, k), dtype=np.int64)

        sp = faiss.swig_ptr
        stage2 = rate_limited_iter(self.produce_batches(x, bs))
        t0 = time.time()
        for i0, xblock, Dc, Ic in stage2:
            ni = len(xblock)
            self.index_ivf.search_preassigned(
                ni, faiss.swig_ptr(xblock),
                k, sp(Ic), sp(Dc),
                sp(D[i0:]), sp(I[i0:]),
                False
            )

        return D, I

    def range_search(self, x, radius):

        x = x.astype( np.float32 ) #GW - why do we need this now?

        bs = self.search_bs
        if self.vec_transform:
            x = self.vec_transform(x)
        nprobe = self.index_ivf.nprobe
        n, d = x.shape
        assert self.index_ivf.d == d

        sp = faiss.swig_ptr
        rsp = faiss.rev_swig_ptr
        stage2 = rate_limited_iter(self.produce_batches(x, bs))
        t0 = time.time()
        all_res = []
        nres = 0
        for i0, xblock, Dc, Ic in stage2:
            ni = len(xblock)
            res = faiss.RangeSearchResult(ni)

            self.index_ivf.range_search_preassigned(
                ni, faiss.swig_ptr(xblock),
                radius, sp(Ic), sp(Dc),
                res
            )
            all_res.append((ni, res))
            lims = rsp(res.lims, ni + 1)
            nres += lims[-1]
        nres = int(nres)
        lims = np.zeros(n + 1, int)
        I = np.empty(nres, int)
        D = np.empty(nres, 'float32')

        n0 = 0
        for ni, res in all_res:
            lims_i = rsp(res.lims, ni + 1)
            nd = int(lims_i[-1])
            Di = rsp(res.distances, nd)
            Ii = rsp(res.labels, nd)
            i0 = int(lims[n0])
            lims[n0: n0 + ni + 1] = lims_i + i0
            I[i0:i0 + nd] = Ii
            D[i0:i0 + nd] = Di
            n0 += ni

        return lims, D, I


class FaissT3(BaseANN):
    def __init__(self, metric, index_params):
        self._index_params = index_params
        self._metric = metric

    def track(self):
        return "T3"
        
    def index_name(self, name):
        return f"data/{name}.{self._index_params['indexkey']}.faissindex"

    def fit(self, dataset):
        index_params = self._index_params

        ds = DATASETS[dataset]()
        d = ds.d

        # get build parameters
        buildthreads = index_params.get("buildthreads", -1)
        by_residual = index_params.get("by_residual", -1) 
        maxtrain = index_params.get("maxtrain", 0)
        clustering_niter = index_params.get("clustering_niter", -1)
        indexkey = index_params.get("indexkey", "IVF1048576,SQ8")
        add_bs = index_params.get("add_bs", 100000)
        add_splits = index_params.get("add_splits", 1)
        indexfile = self.index_name(dataset)
              
        # determine how we use the GPU
        #search_type = ds.search_type()
        #if search_type == "knn":
        #    train_on_gpu = True
        #    quantizer_on_gpu_add = True 
        #else: #range
        #    train_on_gpu = False
        #    quantizer_on_gpu_add = False

        index = build_index(buildthreads, by_residual, maxtrain, clustering_niter, indexkey, 
                        indexfile, add_bs, add_splits, ds)

        index_ivf, vec_transform = unwind_index_ivf(index)
        if vec_transform is None:
            vec_transform = lambda x: x
        if index_ivf is not None:
            print("imbalance_factor=", index_ivf.invlists.imbalance_factor())
        
        no_precomputed_tables  = index_params.get("no_precomputed_tables", True)
        if no_precomputed_tables:
            if isinstance(index_ivf, faiss.IndexIVFPQ):
                print("disabling precomputed table")
                index_ivf.use_precomputed_table = -1
                index_ivf.precomputed_table.clear()

        precomputed_table_size = 0
        if hasattr(index_ivf, 'precomputed_table'):
            precomputed_table_size = index_ivf.precomputed_table.size() * 4
        print("precomputed tables size:", precomputed_table_size)

        searchthreads  = index_params.get("searchthreads", -1)
        if searchthreads == -1:
            print("Search threads:", faiss.omp_get_max_threads())
        else:
            print("Setting nb of threads to", searchthreads)
            faiss.omp_set_num_threads(searchthreads)

        parallel_mode  = index_params.get("parallel_mode", 3)
        if parallel_mode != -1:
            print("setting IVF parallel mode to", parallel_mode)
            index_ivf.parallel_mode
            index_ivf.parallel_mode = parallel_mode

        # prep for the searches
 
        self.ps = faiss.ParameterSpace()
        self.ps.initialize(index)

        search_bs  = index_params.get("search_bs", 8192)
        index_wrap = IndexQuantizerOnGPU(index, search_bs)

        self.cpuindex = index
        self.index = index_wrap

    def load_index(self, dataset):

        index_params = self._index_params

        if not os.path.exists(self.index_name(dataset)):
            if 'url' not in self._index_params:
                return False

            print('Downloading index in background. This can take a while.')
            download_accelerated(self._index_params['url'], self.index_name(dataset), quiet=True)

        print("Loading index",self.index_name(dataset))

        index = faiss.read_index(self.index_name(dataset))

        index_ivf, vec_transform = unwind_index_ivf(index)
        if vec_transform is None:
            vec_transform = lambda x: x
        if index_ivf is not None:
            print("imbalance_factor=", index_ivf.invlists.imbalance_factor())

        no_precomputed_tables  = index_params.get("no_precomputed_tables", True)
        if no_precomputed_tables:
            if isinstance(index_ivf, faiss.IndexIVFPQ):
                print("disabling precomputed table")
                index_ivf.use_precomputed_table = -1
                index_ivf.precomputed_table.clear()

        precomputed_table_size = 0
        if hasattr(index_ivf, 'precomputed_table'):
            precomputed_table_size = index_ivf.precomputed_table.size() * 4
        print("precomputed tables size:", precomputed_table_size)

        # prep for the searches

        searchthreads  = index_params.get("searchthreads", -1)
        if searchthreads == -1:
            print("Search threads:", faiss.omp_get_max_threads())
        else:
            print("Setting nb of threads to", searchthreads)
            faiss.omp_set_num_threads(searchthreads)

        parallel_mode  = index_params.get("parallel_mode", 3)
        if parallel_mode != -1:
            print("setting IVF parallel mode to", parallel_mode)
            index_ivf.parallel_mode
            index_ivf.parallel_mode = parallel_mode

        self.ps = faiss.ParameterSpace()
        self.ps.initialize(index)

        search_bs  = index_params.get("search_bs", 8092)
        index_wrap = IndexQuantizerOnGPU(index, search_bs)

        self.cpuindex = index
        self.index = index_wrap

        return True

    def set_query_arguments(self, query_args):
        faiss.cvar.indexIVF_stats.reset()
        self.ps.set_index_parameters(self.cpuindex, query_args)
        self.qas = query_args


    # shall we return something interesting here?
    def get_additional(self):
        return {"dist_comps": faiss.cvar.indexIVF_stats.ndis}

    def __str__(self):
        return f'FaissIVFPQ({self.qas})'

    def query(self, X, n):
        self.res = self.index.search(X, n)

    def range_query(self, X, radius):
        self.res = self.index.range_search(X, radius)

    def get_results(self):
        D, I = self.res
        return I

    def get_range_results(self):
        return self.res
