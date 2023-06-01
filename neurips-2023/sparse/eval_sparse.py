import argparse

import time
import numpy as np
from benchmark.datasets import DATASETS


from linscan import Linscan

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    def aa(*args, **kwargs):
        group.add_argument(*args, **kwargs)

    group = parser.add_argument_group('files')
    aa('--dataset_name', required=True, help="Sparse dataset version, must be in sparse-{'small', '1M', 'full'}.")

    group = parser.add_argument_group('Computation options')
    aa('--budgets',required=True, help="budgets for linscan's score computation part in ms")
    aa('--k', default=10, type=int, help="number of nearest kNN neighbors to search")

    args = parser.parse_args()

    print("args:", args)
    print('k: ', args.k)

    ds = DATASETS[args.dataset_name]()

    ds.prepare()

    I_gt,D_gt = ds.get_groundtruth()

    data = ds.get_dataset()
    queries = ds.get_queries()

    print('data:', data.shape)
    print('queries:', queries.shape)

    k = args.k
    nq = queries.shape[0]

    index = Linscan(metric="ip", index_params={})
    index.fit(args.dataset_name)

    budgets = [float(b) for b in args.budgets.split(',')]
    print(budgets)

    results = []
    for b in budgets:
        print('evaluating', nq, 'queries:')
        start = time.time()
        index.set_query_arguments({"budget": b})
        index.query(queries, k)
        I = index.get_results()
        end = time.time()
        elapsed = end - start
        print(f'Elapsed {elapsed}s for {nq} queries ({nq / elapsed} QPS) ')

        # compute recall:
        recall = np.mean([len(set(I_gt[i,:]).intersection(I[i,:]))/k for i in range(ds.nq)])

        print('recall:', recall)
        results.append(f'Results: {b}, {recall}, {nq / elapsed}')

    for r in results:
        print(r)