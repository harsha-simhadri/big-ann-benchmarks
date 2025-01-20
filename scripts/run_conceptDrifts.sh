#!/bin/bash

# Define the algorithms and datasets
ALGORITHMS=("linear" "candy_flann" "candy_lshapg" "candy_mnru" "candy_sptag" "cufe" "diskann" "faiss_fast_scan" "faiss_HNSW" "faiss_IVFPQ" "faiss_lsh" "faiss_NSW" "faiss_onlinepq" "faiss_pq" "puck" "pyanns")
DATASETS=("openimage-streaming")
# Iterate through each combination of algorithm and dataset
for ALGO in "${ALGORITHMS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    echo "Running with algorithm: $ALGO and dataset: $DS"
    python3 run.py --neurips23track congestion --algorithm "$ALGO" --nodocker --rebuild --runbook_path neurips23/runbooks/congestion/conceptDrift/conceptDrift_experiment.yaml --dataset "$DS"
  done
done

echo "All experiments completed."