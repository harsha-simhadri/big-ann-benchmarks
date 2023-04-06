import pandas as pd
import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse
import bz2
import sys

from benchmark.datasets import DATASETS
from benchmark.plotting.utils  import compute_metrics_all_runs
from benchmark.results import load_all_results, get_unique_algorithms

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        help='Path to the output csv file',
        required=True)
    parser.add_argument(
        '--recompute',
        action='store_true',
        help='Path to the output csv file')
    parser.add_argument(

        '--private-query',
        help='Use the private queries and ground truth',
        action='store_true')
    parser.add_argument(
        '--sensors',
        action='store_true',
        help='Export sensors data if available')
    parser.add_argument(
        '--search-times',
        action='store_true',
        help='Export search times data if available')
    parser.add_argument(
        '--detect-caching',
        type=float,
        default=None,
        metavar="THRESHOLD",
        help='Try to detect query response caching by analyzing search times.  Supply a threshold betwee 0 and 1, such as 0.3.')
    args = parser.parse_args()

    if args.detect_caching!=None and not args.search_times:
        print("Error: --detect_caching requires the --search_times flag")
        sys.exit(1)

    datasets = DATASETS.keys()
    dfs = []

    is_first = True
    for dataset_name in datasets:
        print("Looking at dataset", dataset_name)
        dataset = DATASETS[dataset_name]()
        results = load_all_results(dataset_name)
        results = compute_metrics_all_runs(dataset, results, args.recompute, \
                args.sensors, args.search_times, args.private_query)
        cleaned = []
        for result in results:
            if 'k-nn' in result:
                result['recall/ap'] = result['k-nn']
                del result['k-nn']
            if 'ap' in result:
                result['recall/ap'] = result['ap']
                del result['ap']
            if args.sensors:
                if 'wspq' not in result:
                    print('Warning: wspq sensor data not available.')
            if args.search_times:
                search_times = result['search_times']
                if 'search_times' in result:
                    # create a space separated list suitable as column for a csv
                    result['search_times'] = \
                        " ".join( [str(el) for el in search_times ] )

                    if args.detect_caching != None:  
                        print("%s: Checking for response caching for these search times->" % dataset_name, search_times) 
                        percent_improvement = (search_times[0]-search_times[-1])/search_times[0]
                        caching = percent_improvement > args.detect_caching
                        result['caching'] = "%d %f %f" % ( 1 if caching else 0, args.detect_caching, percent_improvement )
                        if caching:
                            print("Possible caching discovered: %.3f > %.3f" % ( percent_improvement, args.detect_caching) )
                        else:
                            print("No response caching detected.")

                else:
                    print("Warning: 'search_times' not available.")
            cleaned.append(result)
        dfs.append(pd.DataFrame(cleaned))
    if len(dfs) > 0:
        data = pd.concat(dfs)
        data.to_csv(args.output, index=False)

