#!/bin/bash

# Define the algorithms and datasets
ALGORITHMS=("linear" "candy_flann" "candy_lshapg" "candy_mnru" "candy_sptag" "cufe" "diskann" "faiss_fast_scan" "faiss_HNSW" "faiss_IVFPQ" "faiss_lsh" "faiss_NSW" "faiss_onlinepq" "faiss_pq" "puck" "pyanns")
# Iterate through each combination of algorithm and dataset

python3 create_dataset.py --dataset "random-plus(5000000,1000,768)"
for ALGO in "${ALGORITHMS[@]}"; do
  echo "Running with algorithm: $ALGO and dataset: RANDOM-PLUS(5000000,1000,768)"
  python3 run.py --neurips23track congestion --algorithm "$ALGO" --nodocker --rebuild --runbook_path neurips23/runbooks/congestion/dataVolumes/dataVolume_experiment.yaml --dataset "random-plus(5000000,1000,768)"
done

echo "All experiments completed."