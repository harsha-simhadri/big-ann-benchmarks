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
                runbook_paths = []
                if args.output == "gen":
                    runbook_paths = [#'neurips23/runbooks/congestion/simple_runbook_2.yaml',
                                     #'neurips23/runbooks/congestion/simple_runbook.yaml',
                                     #'neurips23/runbooks/congestion/test_experiment.yaml',
                                     'neurips23/runbooks/congestion/general_experiment/general_experiment.yaml'
                                    ]
                if args.output == "batch":
                    runbook_paths = ['neurips23/runbooks/congestion/batchSizes/batch100.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch500.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch1000.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch2500.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch5000.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch10000.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch20000.yaml',
                                     'neurips23/runbooks/congestion/batchSizes/batch50000.yaml',
                                     ]
                if args.output == "event":
                    runbook_paths = ['neurips23/runbooks/congestion/eventRates/event100.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event500.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event1000.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event2500.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event5000.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event10000.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event20000.yaml',
                                     'neurips23/runbooks/congestion/eventRates/event50000.yaml'
                                     ]
                if args.output=='conceptDrift':
                    runbook_paths=['neurips23/runbooks/congestion/conceptDrift/conceptDrift_experiment.yaml']
                if args.output=='randomContamination':
                    runbook_paths=['neurips23/runbooks/congestion/randomContamination/randomContamination0.05.yaml',
                                   'neurips23/runbooks/congestion/randomContamination/randomContamination0.10.yaml',
                                   'neurips23/runbooks/congestion/randomContamination/randomContamination0.15.yaml',
                                   'neurips23/runbooks/congestion/randomContamination/randomContamination0.20.yaml',
                                   'neurips23/runbooks/congestion/randomContamination/randomContamination0.25.yaml']
                if args.output == 'randomDrop':
                    runbook_paths=['neurips23/runbooks/congestion/randomDrop/randomDrop0.05.yaml',
                                   'neurips23/runbooks/congestion/randomDrop/randomDrop0.10.yaml',
                                   'neurips23/runbooks/congestion/randomDrop/randomDrop0.15.yaml',
                                   'neurips23/runbooks/congestion/randomDrop/randomDrop0.20.yaml',
                                   'neurips23/runbooks/congestion/randomDrop/randomDrop0.25.yaml']
                if args.output == 'wordContamination':
                    runbook_paths=['neurips23/runbooks/congestion/wordContamination/wordContamination_experiment.yaml']
                if args.output == 'bulkDeletion':
                    runbook_paths = ['neurips23/runbooks/congestion/bulkDeletion/bulkDeletion0.1.yaml',
                                     'neurips23/runbooks/congestion/bulkDeletion/bulkDeletion0.2.yaml',
                                     'neurips23/runbooks/congestion/bulkDeletion/bulkDeletion0.3.yaml',
                                     'neurips23/runbooks/congestion/bulkDeletion/bulkDeletion0.4.yaml',
                                     'neurips23/runbooks/congestion/bulkDeletion/bulkDeletion0.5.yaml']
                if args.output == 'batchDeletion':
                    runbook_paths = ['neurips23/runbooks/congestion/batchDeletion/batchDeletion0.1.yaml',
                                     'neurips23/runbooks/congestion/batchDeletion/batchDeletion0.2.yaml',
                                     'neurips23/runbooks/congestion/batchDeletion/batchDeletion0.3.yaml',
                                     'neurips23/runbooks/congestion/batchDeletion/batchDeletion0.4.yaml',
                                     'neurips23/runbooks/congestion/batchDeletion/batchDeletion0.5.yaml']
                if args.output == "curseDim":
                    runbook_paths = ['neurips23/runbooks/congestion/dimensions/dimensions_experiment.yaml']
                if args.output == "multiModal":
                    runbook_paths = ['neurips23/runbooks/congestion/multiModal/multiModal_experiment.yaml']

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
