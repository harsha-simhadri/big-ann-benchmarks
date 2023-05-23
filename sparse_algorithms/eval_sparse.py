import argparse
from linscan import LinscanIndex

from tqdm import tqdm
import time
import numpy as np
from multiprocessing.pool import ThreadPool

from benchmark.datasets import SparseDataset
from sparse_algorithms.basic_sparse_index import BasicSparseIndex

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('files')
    aa('--dataset_name', required=True, help="Sparse dataset version, must be in {'small', '1M', 'full'}.")
#     aa('--output_file', required=True, help="location of the results file")

    group = parser.add_argument_group('Computation options')
    # aa('--alpha', default=1, type=float, help="fraction of weight of the query to retain before search. Default: 1.0 (exact search)")
    aa('--budgets', default=1, type=str, help="list of budgets (comma separated) for computing the scores, in ms.")
    aa('--k', default=10, type=int, help="number of nearest kNN neighbors to search")
    aa('--nt', type=int, help="# of processes in thread pool. If omitted, then a single thread is used.")

    args = parser.parse_args()

    print("args:", args)
    print('k: ', args.k)

    ds = SparseDataset(version=args.dataset_name)

    ds.prepare()

    I_gt,D_gt = ds.get_groundtruth()

    print('data:', ds.nb)
    print('queries:', ds.nq)

    queries = ds.get_queries()

    k = args.k
    budgets = [float(s) for s in args.budgets.split(',')]

    nq = queries.shape[0]

    index = LinscanIndex(args.nt)

    N_VEC_LIMIT = 500000
    it = ds.get_dataset_iterator(N_VEC_LIMIT)
    for d in tqdm(it, total=ds.nb/N_VEC_LIMIT):
        for i in range(d.shape[0]):
            d1 = d.getrow(i)
            index.insert(dict(zip(d1.indices, d1.data)))
    print(index)

    queries_vec = []
    for i in range(nq):
        qc = queries.getrow(i)
        q = dict(zip(qc.indices, qc.data))
        queries_vec.append(q)

    results = []
    for b in budgets:
        print('evaluating', nq, 'queries (' + str(args.nt) + ' threads):')
        start = time.time()
        res = index.retrieve_parallel(queries_vec, k, b)
        I = np.array(res)
        end = time.time()
        elapsed = end - start
        print(f'Elapsed {elapsed}s for {nq} queries ({nq / elapsed} QPS) ')

        # compute recall:
        recall = np.mean([len(set(I_gt[i,:]).intersection(I[i,:]))/k for i in range(ds.nq)])

        print('recall:', recall)
        results.append(f'Results: {b}, {recall}, {nq / elapsed}')
    print("Results: (budget[ms], recall, QPS)")
    for r in results:
        print(r)


