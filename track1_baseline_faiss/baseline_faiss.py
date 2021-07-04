import os
import sys
import time
import pdb
import numpy as np
import faiss
import argparse
import resource

import benchmark.datasets
from benchmark.datasets import DATASETS

def two_level_clustering(xt, nc1, nc2, clustering_niter=25):
    d = xt.shape[1]

    print(f"2-level clustering of {xt.shape} nb clusters = {nc1}*{nc2} = {nc1*nc2}")
    print("perform coarse training")

    km = faiss.Kmeans(d, nc1, verbose=True, niter=clustering_niter, max_points_per_centroid=2000)
    km.train(xt)

    print()

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
        km = faiss.Kmeans(d, nc2)
        xtsub = xt[subset]
        km.train(xtsub)
        c2.append(km.centroids)
        i0 = i1
    print(f"done in {time.time() - t0:.2f} s")
    return np.vstack(c2)


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
        elif isinstance(quantizer, faiss.IndexHNSW):
            print("   update quantizer efSearch=", quantizer.hnsw.efSearch, end=" -> ")
            if args.quantizer_add_efSearch > 0:
                quantizer.hnsw.efSearch = args.quantizer_add_efSearch
            else:
                quantizer.hnsw.efSearch = 40 if index_ivf.nlist < 4e6 else 64
            print(quantizer.hnsw.efSearch)
            if args.quantizer_efConstruction != -1:
                print("  update quantizer efConstruction=", quantizer.hnsw.efConstruction, end=" -> ")
                quantizer.hnsw.efConstruction = args.quantizer_efConstruction
                print(quantizer.hnsw.efConstruction)



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

    if args.train_on_gpu:
        print("add a training index on GPU")
        train_index = faiss.index_cpu_to_all_gpus(
                faiss.IndexFlatL2(index_ivf.d))
        index_ivf.clustering_index = train_index

    if args.two_level_clustering:
        sqrt_nlist = int(np.sqrt(index_ivf.nlist))
        assert sqrt_nlist ** 2 == index_ivf.nlist

        centroids_trainset = xt2
        if isinstance(vec_transform, faiss.VectorTransform):
            print("  training vector transform")
            vec_transform.train(xt2)
            print("  transform trainset")
            centroids_trainset = vec_transform.apply_py(centroids_trainset)

        centroids = two_level_clustering(
            centroids_trainset, sqrt_nlist, sqrt_nlist
        )

        if not index_ivf.quantizer.is_trained:
            print("  training quantizer")
            index_ivf.quantizer.train(centroids)

        print("  add centroids to quantizer")
        index_ivf.quantizer.add(centroids)

    index.train(xt2)
    print("  Total train time %.3f s" % (time.time() - t0))

    print("adding")
    t0 = time.time()
    if args.add_bs == -1:
        index.add(sanitize(ds.get_database()))
    else:
        i0 = 0
        for xblock in ds.get_dataset_iterator(bs=args.add_bs):
            i1 = i0 + len(xblock)
            print("  adding %d:%d / %d [%.3f s, RSS %d kiB] " % (
                i0, i1, ds.nb, time.time() - t0,
                faiss.get_mem_usage_kb()))
            index.add(xblock)
            i0 = i1

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




def eval_setting(index, xq, gt, k, inter, min_time):
    nq = xq.shape[0]
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
    print("%12d   " % (ivf_stats.ndis / nrun), end=' ')
    print(nrun)



def run_experiments_autotune(ds, index, args):
    k = args.k

    xq = ds.get_queries()
    gt_I, gt_D = ds.get_groundtruth(k=k)
    gt = gt_I
    nq = len(xq)

    if args.searchthreads == -1:
        print("Search threads:", faiss.omp_get_max_threads())
    else:
        print("Setting nb of threads to", args.searchthreads)
        faiss.omp_set_num_threads(args.searchthreads)

    ps = faiss.ParameterSpace()
    ps.initialize(index)

    ps.n_experiments = args.n_autotune
    ps.min_test_duration = args.min_test_duration

    for kv in args.autotune_max:
        k, vmax = kv.split(':')
        vmax = float(vmax)
        print("limiting %s to %g" % (k, vmax))
        pr = ps.add_range(k)
        values = faiss.vector_to_array(pr.values)
        values = np.array([v for v in values if v < vmax])
        faiss.copy_array_to_vector(values, pr.values)

    for kv in args.autotune_range:
        k, vals = kv.split(':')
        vals = np.fromstring(vals, sep=',')
        print("setting %s to %s" % (k, vals))
        pr = ps.add_range(k)
        faiss.copy_array_to_vector(vals, pr.values)

    # setup the Criterion object
    if args.inter:
        print("Optimize for intersection @ ", args.k)
        crit = faiss.IntersectionCriterion(nq, args.k)
        header = (
            '%-40s     inter@%3d time(ms/q)   nb distances #runs' %
            ("parameters", args.k)
        )
    else:
        print("Optimize for 1-recall @ 1")
        crit = faiss.OneRecallAtRCriterion(nq, 1)
        header = (
            '%-40s     R@1   R@10  R@100  time(ms/q)   nb distances #runs' %
            "parameters"
        )

    # by default, the criterion will request only 1 NN
    crit.nnn = args.k
    crit.set_groundtruth(None, gt.astype('int64'))

    # then we let Faiss find the optimal parameters by itself
    print("exploring operating points, %d threads" % faiss.omp_get_max_threads());
    ps.display()

    t0 = time.time()
    op = ps.explore(index, xq, crit)
    print("Done in %.3f s, available OPs:" % (time.time() - t0))

    op.display()

    print("Re-running evaluation on selected OPs")
    print(header)
    opv = op.optimal_pts
    maxw = max(max(len(opv.at(i).key) for i in range(opv.size())), 40)
    for i in range(opv.size()):
        opt = opv.at(i)

        ps.set_index_parameters(index, opt.key)

        print(opt.key.ljust(maxw), end=' ')
        sys.stdout.flush()
        eval_setting(index, xq, gt, args.k, args.inter, args.min_test_duration)


def run_experiments_searchparams(ds, index, args):
    k = args.k

    xq = ds.get_queries()
    gt_I, gt_D = ds.get_groundtruth(k=k)
    gt = gt_I
    nq = len(xq)

    if args.searchthreads == -1:
        print("Search threads:", faiss.omp_get_max_threads())
    else:
        print("Setting nb of threads to", args.searchthreads)
        faiss.omp_set_num_threads(args.searchthreads)

    ps = faiss.ParameterSpace()
    ps.initialize(index)


    # setup the Criterion object
    if args.inter:
        print("Optimize for intersection @ ", args.k)
        header = (
            '%-40s     inter@%3d time(ms/q)   nb distances #runs' %
            ("parameters", args.k)
        )
    else:
        print("Optimize for 1-recall @ 1")
        header = (
            '%-40s     R@1   R@10  R@100  time(ms/q)   nb distances #runs' %
            "parameters"
        )

    searchparams = args.searchparams

    print(f"Running evaluation on {len(searchparams)} searchparams")
    print(header)
    maxw = max(max(len(p) for p in searchparams), 40)
    for params in searchparams:
        ps.set_index_parameters(index, params)

        print(params.ljust(maxw), end=' ')
        sys.stdout.flush()
        eval_setting(index, xq, gt, args.k, args.inter, args.min_test_duration)




def main():

    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('What to do')
    aa('--build', default=False, action="store_true")
    aa('--search', default=False, action="store_true")

    group = parser.add_argument_group('dataset options')
    aa('--dataset', choices=DATASETS.keys(), required=True)

    aa('--prepare', default=False, action="store_true",
        help="call prepare() to download the dataset before computing")
    aa('--basedir', help="override basedir for dataset")

    group = parser.add_argument_group('index consturction')

    aa('--indexkey', default='HNSW32', help='index_factory type')
    aa('--by_residual', default=-1, type=int,
        help="set if index should use residuals (default=unchanged)")
    aa('--M0', default=-1, type=int, help='size of base level')
    aa('--maxtrain', default=0, type=int,
        help='maximum number of training points (0 to set automatically)')
    aa('--indexfile', default='', help='file to read or write index from')
    aa('--add_bs', default=100000, type=int,
        help='add elements index by batches of this size')
    aa('--no_precomputed_tables', action='store_true', default=False,
        help='disable precomputed tables (uses less memory)')
    aa('--clustering_niter', default=-1, type=int,
       help='number of clustering iterations (-1 = leave default)')
    aa('--two_level_clustering', action="store_true", default=False,
       help='perform a 2-level tree clustering')
    aa('--train_on_gpu', default=False, action='store_true',
        help='do training on GPU')
    aa('--quantizer_efConstruction', default=-1, type=int,
        help="override the efClustering of the quantizer")
    aa('--quantizer_add_efSearch', default=-1, type=int,
        help="override the efSearch of the quantizer at add time")
    aa('--buildthreads', default=-1, type=int,
        help='nb of threads to use at build time')

    group = parser.add_argument_group('searching')

    aa('--k', default=10, type=int, help='nb of nearest neighbors')
    aa('--inter', default=True, action='store_true',
        help='use intersection measure instead of 1-recall as metric')
    aa('--searchthreads', default=-1, type=int,
        help='nb of threads to use at search time')
    aa('--searchparams', nargs='+', default=['autotune'],
        help="search parameters to use (can be autotune or a list of params)")
    aa('--n_autotune', default=500, type=int,
        help="max nb of autotune experiments")
    aa('--autotune_max', default=[], nargs='*',
        help='set max value for autotune variables format "var:val" (exclusive)')
    aa('--autotune_range', default=[], nargs='*',
        help='set complete autotune range, format "var:val1,val2,..."')
    aa('--min_test_duration', default=3.0, type=float,
        help='run test at least for so long to avoid jitter')

    group = parser.add_argument_group('computation options')
    aa("--maxRAM", default=100, type=int, help="set max RSS in GB (avoid OOM crash)")


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

        if args.searchparams == ["autotune"]:
            run_experiments_autotune(ds, index, args)
        else:
            run_experiments_searchparams(ds, index, args)

if __name__ == "__main__":
    main()