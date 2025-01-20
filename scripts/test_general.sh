#!/bin/bash

# Define the algorithms and datasets
ALGORITHMS=("candy_flann" "candy_lshapg" "candy_mnru" "candy_sptag" "cufe" "diskann" "faiss_fast_scan" "faiss_HNSW" "faiss_IVFPQ" "faiss_lsh" "faiss_NSW" "faiss_onlinepq" "faiss_pq" "puck" "pyanns")
DATASETS=("glove" "msong" "sun" "trevi" "dpr" "reddit" "random-experiment" "random-plus-experiment" "sift" "msturing-10M-clustered")
ALGORITHMS=("candy_flann")
DATASETS=("msturing-10M-clustered")
# Iterate through each combination of algorithm and dataset
for ALGO in "${ALGORITHMS[@]}"; do
  for DS in "${DATASETS[@]}"; do
    echo "Running with algorithm: $ALGO and dataset: $DS"
    python3 run.py --neurips23track congestion --algorithm "$ALGO" --nodocker --rebuild --runbook_path neurips23/runbooks/congestion/test_experiment.yaml --dataset "$DS"
  done
done

echo "All experiments completed."
