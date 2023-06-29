import numpy as np
import time
import yaml

from benchmark.algorithms.base_runner import BaseRunner
from benchmark.datasets import DATASETS


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


    def run_task(algo, ds, distance, count, run_count, search_type, private_query, runbook):
        best_search_time = float('inf')
        search_times = []
        all_results = []

        data = ds.get_dataset()
        ids = np.arange(1, ds.nb+1, dtype=np.uint32)

        Q = ds.get_queries() if not private_query else ds.get_private_queries()
        print(fr"Got {Q.shape[0]} queries")  

        # Load Runbook
        result_map = {}
        num_searches = 0
        for step, entry in enumerate(runbook):
            start = time.time()
            match entry['operation']:
                case 'insert':
                    ids = np.arange(entry['start'], entry['end']+1, dtype=np.uint32)
                    algo.insert(data[ids-1,:], ids)
                case 'delete':
                    ids = np.arange(entry['start'], entry['end']+1, dtype=np.uint32)
                    algo.delete(ids)
                case 'search':
                    if search_type == 'knn':
                        algo.query(Q, count)
                        results = algo.get_results()
                    elif search_type == 'range':
                        algo.range_query(Q, count)
                        results = algo.get_range_results()
                    else:
                        raise NotImplementedError(f"Search type {search_type} not available.")
                    all_results.append(results)
                    result_map[num_searches] = step + 1
                    num_searches += 1
                case _:
                    raise NotImplementedError('Invalid runbook operation.')
            step_time = (time.time() - start)
            print(f"Step {step+1} took {step_time}s.")

        attrs = {
            "name": str(algo),
            "run_count": run_count,
            "distance": distance,
            "type": search_type,
            "count": int(count),
            "search_times": search_times,
            "num_searches": num_searches
        }

        for k, v in result_map.items():
            attrs['step_' + str(k)] = v
            
        additional = algo.get_additional()
        for k in additional:
            attrs[k] = additional[k]
        return (attrs, all_results)