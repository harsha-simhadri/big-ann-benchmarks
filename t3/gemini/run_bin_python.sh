#!/bin/bash

#
# check versions of critical dependencies
#
#PATH=/usr/bin:$PATH which python3
#PATH=/usr/bin:$PATH python3 -c "import numpy;print('numpy',numpy.version.version)"
#PATH=/usr/bin:$PATH pip3 show numpy
#PATH=/usr/bin:$PATH python3 -c "import scipy;print('scipy',scipy.version.version)"
#PATH=/usr/bin:$PATH pip3 show scipy
#PATH=/usr/bin:$PATH python3 -c "import sklearn;print('sklearn',sklearn.__version__)"
#PATH=/usr/bin:$PATH pip3 show sklearn
#PATH=/usr/bin:$PATH python3 -c "import faiss;print('faiss',faiss.__version__)"
#PATH=/usr/bin:$PATH pip3 show faiss

#
# run all 1B datasets
#

# deep-1B 
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset deep-1B --runs 5 --power-capture 192.168.99.32:1234:10

# msturing-1B
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset msturing-1B --runs 5 --power-capture 192.168.99.32:1234:10

# bigann-1B
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset bigann-1B --runs 5 --power-capture 192.168.99.32:1234:10

# text2image-1B
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset text2image-1B --runs 5 --power-capture 192.168.99.32:1234:10

# msspacev-1B
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset msspacev-1B --runs 5 --power-capture 192.168.99.32:1234:10

# ssnpp-1B
PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_prof:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset ssnpp-1B --runs 5 --power-capture 192.168.99.32:1234:10

