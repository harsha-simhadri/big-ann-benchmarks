#!/bin/bash

# Define the algorithms and datasets
DATASETS=("glove" "msong" "sun" "trevi" "dpr" "reddit" "random-experiment" "random-plus-experiment" "sift" "msturing-30M-clustered")


ALGORITHMS=("candy_hnsw" "candy_dco" "candy_lvq" "candy_lsh" "candy_l2h")
DATASETS=("sift")

# Iterate through each combination of algorithm and dataset
for DS in "${DATASETS[@]}"; do
  for ALGO in "${ALGORITHMS[@]}"; do
    echo "Running with algorithm: $ALGO and dataset: $DS"
    python3 run.py --neurips23track congestion --algorithm "$ALGO" --nodocker --rebuild --runbook_path neurips23/runbooks/congestion/algo_optimizations/algo_optimizations.yaml --dataset "$DS"
  done
done

echo "All experiments completed."