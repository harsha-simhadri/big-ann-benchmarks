#!/bin/bash
DATASETS=("sift")
RUNBOOKS=("0.1.yaml" "0.2.yaml" "0.3.yaml" "0.4.yaml" "0.5.yaml")
# Iterate through each combination of algorithm and dataset

for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/batchDeletion/batchDeletion"$RUN" --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
  done
done