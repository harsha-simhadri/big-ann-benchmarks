#!/bin/bash

DIMS=("1024" "2048" "4096" "8192" "16384")
# Iterate through each combination of algorithm and dataset

for DIM in "${DIMS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/dimensions/dimensions_experiment.yaml --dataset "random-plus(500000,1000,$DIM)" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done

echo "All experiments completed."