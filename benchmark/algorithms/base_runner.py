from __future__ import absolute_import
import time

class BaseRunner():
    def build(algo, dataset):
        t0 = time.time()
        algo.fit(dataset)
        return time.time() - t0
    
    def run_task(algo, ds, distance, count, run_count, search_type, private_query, runbook=None):
        best_search_time = float('inf')
        search_times = []

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
            if search_time < best_search_time:
                best_search_time = search_time
                best_results = results

            search_times.append( search_time )

        attrs = {
            "best_search_time": best_search_time,
            "name": str(algo),
            "run_count": run_count,
            "distance": distance,
            "type": search_type,
            "count": int(count),
            "search_times": search_times,
            "private_queries": private_query, 
        }
        additional = algo.get_additional()
        for k in additional:
            attrs[k] = additional[k]
        return (attrs, best_results)
        