#!/bin/bash
DATASETS=("openimage-streaming")
# Iterate through each combination of algorithm and dataset
for DS in "${DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/conceptDrift/conceptDrift_experiment.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done