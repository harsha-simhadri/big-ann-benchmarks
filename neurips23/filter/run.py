from benchmark.algorithms.base_runner import BaseRunner
import time

class FilterRunner(BaseRunner):
    def run_task(algo, ds, distance, count, run_count, search_type, private_query):
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
            elif search_type == "knn_filtered":
                if not private_query:
                    metadata = ds.get_queries_metadata()
                else:
                    metadata = ds.get_private_queries_metadata()
                algo.filtered_query(X, metadata, count)
                total = (time.time() - start)
                results = algo.get_results()
                assert results.shape[0] == X.shape[0]
            else:
                raise NotImplementedError()

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
            "search_times": search_times,
            "private_queries": private_query, 
        }
        additional = algo.get_additional()
        for k in additional:
            attrs[k] = additional[k]
        return (attrs, results)
        
