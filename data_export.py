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


def cleaned_run_metric(run_metrics):
    cleaned = []
    for run_metric in run_metrics:
        run_metric['track'] = track
        if 'k-nn' in run_metric:
            run_metric['recall/ap'] = run_metric['k-nn']
            del run_metric['k-nn']
        if 'ap' in run_metric:
            run_metric['recall/ap'] = run_metric['ap']
            del run_metric['ap']
        if args.sensors:
            if 'wspq' not in run_metric:
                print('Warning: wspq sensor data not available.')
        if args.search_times:
            search_times = run_metric['search_times'] 
            if 'search_times' in run_metric:
                # create a space separated list suitable as column for a csv
                run_metric['search_times'] = \
                    " ".join( [str(el) for el in search_times ] )

            if args.detect_caching != None:
                print("%s: Checking for response caching for these search times->" % dataset_name, search_times)
                percent_improvement = (search_times[0]-search_times[-1])/search_times[0]
                caching = percent_improvement > args.detect_caching
                run_metric['caching'] = "%d %f %f" % ( 1 if caching else 0, args.detect_caching, percent_improvement )
                if caching:
                    print("Possible caching discovered: %.3f > %.3f" % ( percent_improvement, args.detect_caching) )
                else:
                    print("No response caching detected.")

            else:
                print("Warning: 'search_times' not available.")
        cleaned.append(run_metric)
    return cleaned


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        help='Path to the output csv file',
        required=True)

    parser.add_argument(
        '--track',
        choices=['streaming', 'congestion'],
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

    neurips23tracks = ['streaming', 'none', 'congestion']
    tracks = [args.track]
    is_first = True
    # datasets = ['random-xs']
    for track in tracks:
        for dataset_name in datasets:
            print(f"Looking at track:{track}, dataset:{dataset_name}")
            dataset = DATASETS[dataset_name]()
            runbook_paths = [None]
            if track == 'streaming':
                runbook_paths = ['neurips23/runbooks/streaming/simple_runbook.yaml'
                                    # 'neurips23/runbooks/streaming/simple_replace_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/random_replace_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/clustered_replace_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/clustered_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/clustered_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/delete_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/final_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/msturing-10M_slidingwindow_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/wikipedia-35M_expirationtime_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/wikipedia-1M_expiration_time_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/wikipedia-35M_expiration_time_replace_only_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/wikipedia-1M_expiration_time_replace_only_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/wikipedia-35M_expiration_time_replace_delete_runbook.yaml',
                                    # 'neurips23/runbooks/streaming/wikipedia-1M_expiration_time_replace_delete_runbook.yaml',
                                    #'neurips23/runbooks/streaming/msmarco-100M_expirationtime_runbook.yaml'
                                    ]
            if track == 'congestion':
                runbook_paths = ['neurips23/runbooks/congestion/simple_runbook_2.yaml',
                                 'neurips23/runbooks/congestion/simple_runbook.yaml'
                                ]
            for runbook_path in runbook_paths:
                print("Looking for runbook ", runbook_path)
                results = load_all_results(dataset_name, neurips23track=track, runbook_path=runbook_path)
                results = compute_metrics_all_runs(dataset, dataset_name, results, args.recompute, \
                    args.sensors, args.search_times, args.private_query, \
                    neurips23track=track, runbook_path=runbook_path)
                results = cleaned_run_metric(results)
                if len(results) > 0:
                    dfs.append(pd.DataFrame(results))

    dfs = [e for e in dfs if len(e) > 0]
    if len(dfs) > 0:
        data = pd.concat(dfs)
        data = data.sort_values(by=["algorithm", "dataset", "recall/ap"])        
        data.to_csv(args.output+"-"+args.track+".csv", index=False)
