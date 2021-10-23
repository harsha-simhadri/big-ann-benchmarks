#!/bin/bash
#set -x

#conda activate bigann-silo-py369
which python3
which pip3

python3 -c "import numpy;print('numpy',numpy.version.version)"
pip3 show numpy

python3 -c "import scipy;print('scipy',scipy.version.version)"
pip3 show scipy

python3 -c "import sklearn;print('sklearn',sklearn.__version__)"
pip3 show sklearn

python3 -c "import faiss;print('faiss',faiss.__version__)"
pip3 show faiss

LD_LIBRARY_PATH=./gsl_resources PYTHONPATH=./gsl_resources python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset deep-1B --runs 1
