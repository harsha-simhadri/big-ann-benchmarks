#!/bin/bash

PATH=/usr/bin:$PATH LD_LIBRARY_PATH=/home/george/Projects/BigANN/harsha/big-ann-benchmarks/gsl_resources PYTHONPATH=/home/george/Projects/BigANN/harsha/big-ann-benchmarks/gsl_resources python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset deep-1B --runs 1
