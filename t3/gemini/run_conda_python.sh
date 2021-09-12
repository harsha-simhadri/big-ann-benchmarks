#!/bin/bash
set -x

conda activate bigann-silo
which python3
python3 -c "import numpy;print(numpy.version.version)"
python3 -c "import scipy;print(scipy.version.version)"
python3 -c "import sklearn;print(sklearn.__version__)"
python3 -c "import faiss;print(faiss.__version__)"
LD_LIBRARY_PATH=/home/george/Projects/BigANN/harsha/big-ann-benchmarks/gsl_resources PYTHONPATH=/home/george/Projects/BigANN/harsha/big-ann-benchmarks/gsl_resources python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset deep-1B --runs 1
