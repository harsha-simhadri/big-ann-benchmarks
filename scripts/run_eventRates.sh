#!/bin/bash

# Define the algorithms and datasets
ALGORITHMS=("linear" "candy_flann" "candy_lshapg" "candy_mnru" "candy_sptag" "cufe" "diskann" "faiss_fast_scan" "faiss_HNSW" "faiss_IVFPQ" "faiss_lsh" "faiss_NSW" "faiss_onlinepq" "faiss_pq" "puck" "pyanns")
DATASETS=("random-plus-experiment" "msturing-10M-clustered")
RUNBOOKS=("100.yaml" "500.yaml" "1000.yaml" "2500.yaml" "5000.yaml" "10000.yaml" "20000.yaml" "50000.yaml")

# Iterate through each combination of algorithm and dataset
for RUN in "${RUNBOOKS[@]}"; do
  for ALGO in "${ALGORITHMS[@]}"; do
    for DS in "${DATASETS[@]}"; do
      echo "Running with algorithm: $ALGO and dataset: $DS Using $DS"
      python3 run.py --neurips23track congestion --algorithm "$ALGO" --nodocker --rebuild --runbook_path neurips23/runbooks/congestion/eventRates/event"$RUN" --dataset "$DS"
    done
  done
done

