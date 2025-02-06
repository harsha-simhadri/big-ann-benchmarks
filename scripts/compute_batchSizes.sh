#!/bin/bash
DATASETS=("random-plus-experiment" "sift")
RUNBOOKS=("100.yaml" "500.yaml" "5000.yaml" "20000.yaml" "50000.yaml")
# Iterate through each combination of algorithm and dataset
for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/batchSizes/batch"$RUN" --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
  done
done