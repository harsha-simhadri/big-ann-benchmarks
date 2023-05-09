import argparse

import faiss
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
    aa('--alpha', default=1, type=float, help="fraction of weight of the query to retain before search. Default: 1.0 (exact search)")
    aa('--k', default=10, type=int, help="number of nearest kNN neighbors to search")
    aa('--nt', type=int, help="# of processes in thread pool. If omitted, then a single thread is used.")

    args = parser.parse_args()

    print("args:", args)
    print('k: ', args.k)

    ds = SparseDataset(version=args.dataset_name)

    ds.prepare()

    I_gt,D_gt = ds.get_groundtruth()

    data = ds.get_dataset()
    queries = ds.get_queries()

    print('data:', data.shape)
    print('queries:', queries.shape)

    k = args.k
    a = args.alpha
    nq = queries.shape[0]

    # build index:
    index = BasicSparseIndex(data)

    # prepare location for storing the results of the algorithm
    D = np.zeros((ds.nq, k), dtype='float32')
    I = -np.ones((ds.nq, k), dtype='int32')

    def process_single_row(i):
        res = index.query(q=queries.getrow(i), k=k, alpha=a)
        I[i, :] = [rr[0] for rr in res]
        D[i, :] = [rr[1] for rr in res]

    start = time.time()
    # single thread
    if args.nt is None:
        print('evaluating', nq, 'queries (single thread):')
        for i in tqdm(range(nq)):  # tqdm(range(nq))
            process_single_row(i)
    else:
        print('evaluating', nq, 'queries (' + str(args.nt) + ' threads):')
        with ThreadPool(processes=args.nt) as pool:
            # Map the function to the array of items
            #   res = pool.map(process_single_row, range(nq))
            list(tqdm(pool.imap(process_single_row, range(nq)), total=nq))

    end = time.time()
    elapsed = end - start
    print(f'Elapsed {elapsed}s for {nq} queries ({nq / elapsed} QPS) ')

    # res is now a list of the outputs of every query

    # compute recall:

    recall = faiss.eval_intersection(I_gt, I) / k / ds.nq
    print('recall:', recall)
    print()
    print(f'Results: {a}, {recall}, {nq / elapsed}')

