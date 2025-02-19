#!/bin/bash

# Define the algorithms and datasets
GENERAL_DATASETS=("glove" "msong" "sun" "trevi" "dpr" "reddit" "random-experiment" "random-plus-experiment" "sift" "msturing-30M-clustered")
GENERAL_DATASETS=("sift")
# Iterate through each combination of algorithm and dataset
for DS in "${GENERAL_DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/algo_optimizations/algo_optimizations.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done