import argparse
from tqdm import tqdm
import time
import numpy as np
from scipy.sparse import csr_matrix, hstack
from multiprocessing.pool import ThreadPool

# TODO: add the dataset to Datasets
# import benchmark. datasets
# from benchmark.datasets import DATASETS

from benchmark.dataset_io import usbin_write, read_sparse_matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('File location')
    aa('--base_csr_file', required=True, help="location of a .csr file representing the base data")
    aa('--query_csr_file', required=True, help="location of a .csr file representing the query data")
    aa('--output_file', required=True, help="location of the ground truth file to be generated")

    group = parser.add_argument_group('Computation options')
    aa('--k', default=10, type=int, help="number of nearest kNN neighbors to search")
    # aa("--maxRAM", default=100, type=int, help="set max RSS in GB (avoid OOM crash)")
    aa('--nt', type=int, help="# of processes in thread pool. If omitted, then a single thread is used.")

    args = parser.parse_args()

    print("args:", args)
    print('k: ', args.k)

    data = read_sparse_matrix(args.base_csr_file)
    queries = read_sparse_matrix(args.query_csr_file)
    print('data:', data.shape)
    print('queries:', queries.shape)

    # pad the queries with virtual zeros to match the length of the data files
    queries = hstack([queries, csr_matrix((queries.shape[0], data.shape[1] - queries.shape[1]))])
    print('after padding: ')
    print('data:', data.shape)
    print('queries:', queries.shape)

    k = args.k
    nq = queries.shape[0]

    D = np.zeros((nq, k), dtype='float32')
    I = -np.ones((nq, k), dtype='int32')


    def process_single_row(i):
        res = data.dot(queries.getrow(i).transpose())
        ra = res.toarray()
        top_ind = np.argpartition(ra, -k, axis=0)[-k:][:, 0]

        index_and_dot_prod = [(i, ra[i, 0]) for i in top_ind]
        index_and_dot_prod.sort(key=lambda a: a[1], reverse=True)

        return index_and_dot_prod

    start = time.time()
    # single thread
    if args.nt is None:
        print('computing ground truth for', nq, 'queries (single thread):')
        res = []
        for i in tqdm(range(nq)):  # tqdm(range(nq))
            res.append(process_single_row(i))
    else:
        print('computing ground truth for', nq, 'queries (' + str(args.nt) + ' threads):')
        with ThreadPool(processes=args.nt) as pool:
            # Map the function to the array of items
            #   res = pool.map(process_single_row, range(nq))
            res = list(tqdm(pool.imap(process_single_row, range(nq)), total=nq))

    end = time.time()
    elapsed = end - start
    print(f'Elapsed {elapsed}s for {nq} queries ({nq / elapsed} QPS) ')

    # rearrange to match the format of usbin_write:
    for i in range(nq):
        I[i, :] = [p[0] for p in res[i]]
        D[i, :] = [p[1] for p in res[i]]

    print()
    print("Writing result to", args.output_file)

    usbin_write(I, D, args.output_file)
