#!/bin/bash

# Define the algorithms and datasets
ALGORITHMS=("linear" "candy_flann" "candy_lshapg" "candy_mnru" "candy_sptag" "cufe" "diskann" "faiss_fast_scan" "faiss_HNSW" "faiss_IVFPQ" "faiss_lsh" "faiss_NSW" "faiss_onlinepq" "faiss_pq" "puck" "pyanns")
DIMS=("1024" "2048" "4096" "8192" "16384")
# Iterate through each combination of algorithm and dataset

for DIM in "${DIMS[@]}"; do
  python3 create_dataset.py --dataset "random-plus(500000,1000,$DIM)"
  for ALGO in "${ALGORITHMS[@]}"; do
    echo "Running with algorithm: $ALGO and dataset: RANDOM-PLUS(500000,1000,$DIM)"
    python3 run.py --neurips23track congestion --algorithm "$ALGO" --nodocker --rebuild --runbook_path neurips23/runbooks/congestion/dimensions/dimensions_experiment.yaml --dataset "random-plus(500000,1000,$DIM)"
  done
done

echo "All experiments completed."