#!/bin/bash

#
# script to run 1 1B dataset
#

PATH=/usr/bin:$PATH LD_LIBRARY_PATH="./gsl_resources_release:$HOME/.local/lib/python3.6/site-packages/faiss" PYTHONPATH="./gsl_resources_release:$HOME/.local/lib/python3.6/site-packages/faiss" python3 run.py --t3  --nodocker --definitions t3/gemini/algos.yaml --dataset text2image-1B --runs 5 --power-capture 192.168.99.32:1234:10

