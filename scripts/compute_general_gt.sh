#!/bin/bash

# Define the algorithms and datasets
GENERAL_DATASETS=("glove" "msong" "sun" "trevi" "dpr" "reddit" "random-experiment" "random-plus-experiment" "sift" "msturing-30M-clustered")

# Iterate through each combination of algorithm and dataset
for DS in "${GENERAL_DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/general_experiment/general_experiment.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done


DATASETS=("random-plus-experiment" "sift")
RUNBOOKS=("100.yaml" "500.yaml" "1000.yaml" "2500.yaml" "5000.yaml" "10000.yaml" "20000.yaml")
# Iterate through each combination of algorithm and dataset
for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/batchSizes/batch"$RUN" --dataset "$DS"
  done
done


DATASETS=("openimage-streaming")
# Iterate through each combination of algorithm and dataset
for DS in "${DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/conceptDrift/conceptDrift_experiment.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done

DATASETS=("random-plus-experiment" "sift")
RUNBOOKS=("100.yaml" "500.yaml" "1000.yaml" "2500.yaml" "5000.yaml" "10000.yaml" "20000.yaml" "50000.yaml")

# Iterate through each combination of algorithm and dataset
for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/eventRates/event"$RUN" --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
  done
done

DATASETS=("sift")
RUNBOOKS=("0.05.yaml" "0.10.yaml" "0.15.yaml" "0.20.yaml" "0.25.yaml")
# Iterate through each combination of algorithm and dataset

for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/randomContamination/randomContamination"$RUN" --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
  done
done



DATASETS=("sift")
RUNBOOKS=("0.05.yaml" "0.10.yaml" "0.15.yaml" "0.20.yaml" "0.25.yaml")
# Iterate through each combination of algorithm and dataset

for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/randomDrop/randomDrop"$RUN" --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
  done
done

DATASETS=("wte-0.05" "wte-0.1" "wte-0.2" "wte-0.4" "wte-0.6" "wte-0.8")
# Iterate through each combination of algorithm and dataset
for DS in "${DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/wordContamination/wordContamination_experiment.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done

DATASETS=("coco" "cirr")
# Iterate through each combination of algorithm and dataset
for DS in "${DATASETS[@]}"; do
  python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/multiModal/multiModal_experiment.yaml --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
done

DATASETS=("sift")
RUNBOOKS=("0.1.yaml" "0.2.yaml" "0.3.yaml" "0.4.yaml" "0.5.yaml")
# Iterate through each combination of algorithm and dataset

for RUN in "${RUNBOOKS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    python3 benchmark/congestion/compute_gt.py --runbook neurips23/runbooks/congestion/bulkDeletion/bulkDeletion"$RUN" --dataset "$DS" --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
  done
done



