from benchmark.algorithms.base_runner import BaseRunner
from benchmark.datasets import DATASETS
import numpy as np
import time

class StreamingRunner(BaseRunner):
    def build(algo, dataset):
        '''
        Return set up time
        '''
        t0 = time.time()
        ds = DATASETS[dataset]()
        max_pts = ds.nb
        ndims = ds.d
        algo.setup(ds.dtype, max_pts, ndims)
        print('Algorithm set up')
        return time.time() - t0
    
    def run_task(algo, ds, distance, count, run_count, search_type, private_query):
        best_search_time = float('inf')
        search_times = []

        data = ds.get_dataset()
        ids = np.arange(1, ds.nb+1, dtype=np.uint32)

        # Runbook
        algo.insert(data, ids)

        if not private_query:
            X = ds.get_queries()
        else:
            X = ds.get_private_queries()
        
        print(fr"Got {X.shape[0]} queries")

        for i in range(run_count):
            print('Run %d/%d...' % (i + 1, run_count))

            start = time.time()
            if search_type == "knn":
                algo.query(X, count)
                total = (time.time() - start)
                results = algo.get_results()
                assert results.shape[0] == X.shape[0]
            elif search_type == "range":
                algo.range_query(X, count)
                total = (time.time() - start)
                results = algo.get_range_results()
            else:
                raise NotImplementedError(f"Search type {search_type} not available.")

            search_time = total
            best_search_time = min(best_search_time, search_time)
            search_times.append( search_time )

        attrs = {
            "best_search_time": best_search_time,
            "name": str(algo),
            "run_count": run_count,
            "distance": distance,
            "type": search_type,
            "count": int(count),
            "search_times": search_times
        }
        additional = algo.get_additional()
        for k in additional:
            attrs[k] = additional[k]
        return (attrs, results)