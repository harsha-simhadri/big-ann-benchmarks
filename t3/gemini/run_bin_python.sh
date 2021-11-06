#!/bin/bash

PATH=/usr/bin:$PATH which python3
PATH=/usr/bin:$PATH python3 -c "import numpy;print('numpy',numpy.version.version)"
PATH=/usr/bin:$PATH pip3 show numpy

PATH=/usr/bin:$PATH python3 -c "import scipy;print('scipy',scipy.version.version)"
PATH=/usr/bin:$PATH pip3 show scipy

PATH=/usr/bin:$PATH python3 -c "import sklearn;print('sklearn',sklearn.__version__)"
PATH=/usr/bin:$PATH pip3 show sklearn

PATH=/usr/bin:$PATH python3 -c "import faiss;print('faiss',faiss.__version__)"
PATH=/usr/bin:$PATH pip3 show faiss

# deep-1B msturing-1B bigann-1B text2image-1B bigann-1B msspacev-1B
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset bigann-1B --runs 5 --power-capture 192.168.99.32:1234:10

#PATH=/usr/bin:$PATH LD_LIBRARY_PATH="/home/silo/BigANN/big-ann-benchmarks/gsl_resources:/home/silo/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="/home/silo/BigANN/big-ann-benchmarks/gsl_resources:/home/silo/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset deep-1B --runs 1
