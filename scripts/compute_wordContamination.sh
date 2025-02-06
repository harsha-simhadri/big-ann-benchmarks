#!/bin/bash
DATASETS=("wte-0.05" "wte-0.1" "wte-0.2" "wte-0.4" "wte-0.6" "wte-0.8")
# Iterate through each combination of algorithm and dataset
for DS in "${DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/wordContamination/wordContamination_experiment.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done