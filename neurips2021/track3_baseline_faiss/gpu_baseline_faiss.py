import os
import sys
import time
import pdb
import gc
import numpy as np
import faiss
import argparse
import resource
import threading
from multiprocessing.pool import ThreadPool

import benchmark.datasets
from benchmark.datasets import DATASETS
from benchmark.plotting import eval_range_search



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


def build_index(args, ds):
    nq, d = ds.nq, ds.d
    nb, d = ds.nq, ds.d

    if args.buildthreads == -1:
        print("Build-time number of threads:", faiss.omp_get_max_threads())
    else:
        print("Set build-time number of threads:", args.buildthreads)
        faiss.omp_set_num_threads(args.buildthreads)

    metric_type = (
            faiss.METRIC_L2 if ds.distance() == "euclidean" else
            faiss.METRIC_INNER_PRODUCT if ds.distance() in ("ip", "angular") else
            1/0
    )
    index = faiss.index_factory(d, args.indexkey, metric_type)

    index_ivf, vec_transform = unwind_index_ivf(index)
    if vec_transform is None:
        vec_transform = lambda x: x
    else:
        vec_transform = faiss.downcast_VectorTransform(vec_transform)

    if args.by_residual != -1:
        by_residual = args.by_residual == 1
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

    index.verbose = True
    if index_ivf:
        index_ivf.verbose = True
        index_ivf.quantizer.verbose = True
        index_ivf.cp.verbose = True


    maxtrain = args.maxtrain
    if maxtrain == 0:
        if 'IMI' in args.indexkey:
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

    if args.clustering_niter >= 0:
        print(("setting nb of clustering iterations to %d" %
                args.clustering_niter))
        index_ivf.cp.niter = args.clustering_niter

    train_index = None
    if args.train_on_gpu:
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

    if not args.quantizer_on_gpu_add:
        i0 = 0
        for xblock in ds.get_dataset_iterator(bs=args.add_bs):
            i1 = i0 + len(xblock)
            print("  adding %d:%d / %d [%.3f s, RSS %d kiB] " % (
                i0, i1, ds.nb, time.time() - t0,
                faiss.get_mem_usage_kb()))
            index.add(xblock)
            i0 = i1
    elif True:
        quantizer_gpu = faiss.index_cpu_to_all_gpus(index_ivf.quantizer)

        nsplit = args.add_splits

        def produce_batches(sno):
            for xblock in ds.get_dataset_iterator(bs=args.add_bs, split=(nsplit, sno)):
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
    if args.indexfile:
        print("storing", args.indexfile)
        faiss.write_index(index, args.indexfile)

    return index


def compute_inter(a, b):
    nq, rank = a.shape
    ninter = sum(
        np.intersect1d(a[i, :rank], b[i, :rank]).size
        for i in range(nq)
    )
    return ninter / a.size



def eval_setting_knn(index, xq, gt, k, inter, min_time):
    nq = xq.shape[0]
    gt_I, gt_D = gt
    ivf_stats = faiss.cvar.indexIVF_stats
    ivf_stats.reset()
    nrun = 0

    t0 = time.time()
    while True:
        D, I = index.search(xq, k)
        nrun += 1
        t1 = time.time()
        if t1 - t0 > min_time:
            break
    ms_per_query = ((t1 - t0) * 1000.0 / nq / nrun)
    if inter:
        rank = k
        inter_measure = compute_inter(gt[:, :rank], I[:, :rank])
        print("%.4f" % inter_measure, end=' ')
    else:
        for rank in 1, 10, 100:
            n_ok = (I[:, :rank] == gt[:, :1]).sum()
            print("%.4f" % (n_ok / float(nq)), end=' ')
    print("   %9.5f  " % ms_per_query, end=' ')

    if ivf_stats.search_time == 0:
        # happens for IVFPQFastScan where the stats are not logged by default
        print("%12d  %5.2f  " % (ivf_stats.ndis / nrun, 0.0), end=' ')
    else:
        pc_quantizer = ivf_stats.quantization_time / ivf_stats.search_time * 100
        print("%12d  %5.2f  " % (ivf_stats.ndis / nrun, pc_quantizer), end=' ')
    print(nrun)


def eval_setting_range(index, xq, gt, radius=0, inter=False, min_time=3.0, query_bs=-1):
    nq = xq.shape[0]
    gt_nres, gt_I, gt_D = gt
    gt_lims = np.zeros(nq + 1, dtype=int)
    gt_lims[1:] = np.cumsum(gt_nres)
    ivf_stats = faiss.cvar.indexIVF_stats
    ivf_stats.reset()
    nrun = 0
    t0 = time.time()
    while True:
        lims, D, I = index.range_search(xq, radius)
        nrun += 1
        t1 = time.time()
        if t1 - t0 > min_time:
            break
    ms_per_query = ((t1 - t0) * 1000.0 / nq / nrun)

    ap = eval_range_search.compute_AP((gt_lims, gt_I, gt_D), (lims, I, D))
    print("%.4f" % ap, end=' ')
    print("   %9.5f  " % ms_per_query, end=' ')

    print("%12d  %5d  " % (ivf_stats.ndis / nrun, D.size), end=' ')
    print(nrun)


class IndexQuantizerOnGPU:
    """ run query quantization on GPU """

    def __init__(self, index, search_bs):
        self.search_bs = search_bs
        index_ivf, vec_transform = unwind_index_ivf(index)
        self.index_ivf = index_ivf
        self.vec_transform = vec_transform
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


def run_experiments_searchparams(ds, index, args):
    k = args.k

    xq = ds.get_queries()

    nq = len(xq)

    ps = faiss.ParameterSpace()
    ps.initialize(index)


    # setup the Criterion object
    if args.inter:
        print("Optimize for intersection @ ", args.k)
        header = (
            '%-40s     inter@%3d time(ms/q)   nb distances %%quantization #runs' %
            ("parameters", args.k)
        )
    else:
        print("Optimize for 1-recall @ 1")
        header = (
            '%-40s     R@1   R@10  R@100  time(ms/q)   nb distances %%quantization #runs' %
            "parameters"
        )

    searchparams = args.searchparams

    print(f"Running evaluation on {len(searchparams)} searchparams")
    print(header)
    maxw = max(max(len(p) for p in searchparams), 40)

    if args.quantizer_on_gpu_search:
        index_wrap = IndexQuantizerOnGPU(index, args.search_bs)
    else:
        index_wrap = index

    for params in searchparams:
        ps.set_index_parameters(index, params)

        print(params.ljust(maxw), end=' ')
        sys.stdout.flush()

        if ds.search_type() == "knn":
            eval_setting_knn(
                index_wrap, xq, ds.get_groundtruth(k=args.k),
                k=args.k, inter=args.inter, min_time=args.min_test_duration
            )
        else:
            eval_setting_range(
                index_wrap, xq, ds.get_groundtruth(),
                radius=args.radius, inter=args.inter,
                min_time=args.min_test_duration
            )



def main():

    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('What to do')
    aa('--build', default=False, action="store_true")
    aa('--search', default=False, action="store_true")
    aa('--prepare', default=False, action="store_true",
        help="call prepare() to download the dataset before computing")

    group = parser.add_argument_group('dataset options')
    aa('--dataset', choices=DATASETS.keys(), required=True)
    aa('--basedir', help="override basedir for dataset")

    group = parser.add_argument_group('index consturction')

    aa('--indexkey', default='IVF1204,Flat', help='index_factory type')
    aa('--by_residual', default=-1, type=int,
        help="set if index should use residuals (default=unchanged)")
    aa('--maxtrain', default=0, type=int,
        help='maximum number of training points (0 to set automatically)')
    aa('--indexfile', default='', help='file to read or write index from')
    aa('--add_bs', default=100000, type=int,
        help='add elements index by batches of this size')
    aa('--no_precomputed_tables', action='store_true', default=False,
        help='disable precomputed tables (uses less memory)')
    aa('--clustering_niter', default=-1, type=int,
       help='number of clustering iterations (-1 = leave default)')
    aa('--train_on_gpu', default=False, action='store_true',
        help='do training on GPU')
    aa('--buildthreads', default=-1, type=int,
        help='nb of threads to use at build time')
    aa('--quantizer_on_gpu_add', action="store_true", default=False,
        help="use GPU coarse quantizer at add time")
    aa('--add_splits', default=1, type=int,
        help="Do adds in this many splits (otherwise risk of OOM with GPU based adds)")

    group = parser.add_argument_group('searching')

    aa('--k', default=10, type=int, help='nb of nearest neighbors')
    aa('--radius', default=96237, type=float, help='radius for range search')
    aa('--inter', default=True, action='store_true',
        help='use intersection measure instead of 1-recall as metric')
    aa('--searchthreads', default=-1, type=int,
        help='nb of threads to use at search time')
    aa('--searchparams', nargs='+', default=['autotune'],
        help="search parameters to use (can be autotune or a list of params)")
    aa('--min_test_duration', default=3.0, type=float,
        help='run test at least for so long to avoid jitter')
    aa('--quantizer_on_gpu_search', action="store_true", default=False,
        help="use GPU coarse quantizer at search time")
    aa('--parallel_mode', default=-1, type=int,
        help="set search-time parallel mode for IVF indexes")
    aa('--search_bs', default=8192, type=int,
        help='search time batch size (for GPU/CPU tiling)')

    group = parser.add_argument_group('computation options')
    aa("--maxRAM", default=-1, type=int, help="set max RSS in GB (avoid OOM crash)")


    args = parser.parse_args()

    if args.basedir:
        print("setting datasets basedir to", args.basedir)
        benchmark.datasets.BASEDIR
        benchmark.datasets.BASEDIR = args.basedir

    if args.maxRAM > 0:
        print("setting max RSS to", args.maxRAM, "GiB")
        resource.setrlimit(
            resource.RLIMIT_DATA, (args.maxRAM * 1024 ** 3, resource.RLIM_INFINITY)
        )

    os.system('echo -n "nb processors "; '
          'cat /proc/cpuinfo | grep ^processor | wc -l; '
          'cat /proc/cpuinfo | grep ^"model name" | tail -1')

    ds = DATASETS[args.dataset]()
    print(ds)

    nq, d = ds.nq, ds.d
    nb, d = ds.nq, ds.d

    if args.prepare:
        print("downloading dataset...")
        ds.prepare()
        print("dataset ready")

    if not (args.build or args.search):
        return

    if args.build:
        print("build index, key=", args.indexkey)
        index = build_index(args, ds)
    else:
        print("reading", args.indexfile)
        index = faiss.read_index(args.indexfile)

    index_ivf, vec_transform = unwind_index_ivf(index)
    if vec_transform is None:
        vec_transform = lambda x: x

    if index_ivf is not None:
        print("imbalance_factor=", index_ivf.invlists.imbalance_factor())

    if args.no_precomputed_tables:
        if isinstance(index_ivf, faiss.IndexIVFPQ):
            print("disabling precomputed table")
            index_ivf.use_precomputed_table = -1
            index_ivf.precomputed_table.clear()

    if args.indexfile:
        print("index size on disk: ", os.stat(args.indexfile).st_size)

    print("current RSS:", faiss.get_mem_usage_kb() * 1024)

    precomputed_table_size = 0
    if hasattr(index_ivf, 'precomputed_table'):
        precomputed_table_size = index_ivf.precomputed_table.size() * 4

    print("precomputed tables size:", precomputed_table_size)

    if args.search:

        if args.searchthreads == -1:
            print("Search threads:", faiss.omp_get_max_threads())
        else:
            print("Setting nb of threads to", args.searchthreads)
            faiss.omp_set_num_threads(args.searchthreads)

        if args.parallel_mode != -1:
            print("setting IVF parallel mode to", args.parallel_mode)
            index_ivf.parallel_mode
            index_ivf.parallel_mode = args.parallel_mode

        if args.searchparams == ["autotune"]:
            run_experiments_autotune(ds, index, args)
        else:
            run_experiments_searchparams(ds, index, args)

if __name__ == "__main__":
    main()