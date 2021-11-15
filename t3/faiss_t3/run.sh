#!/bin/bash

python run.py --dataset deep-1B --definitions t3/faiss_t3/algos.yaml --runs 5 --t3  --nodocker --power-capture 192.168.99.110:1234:10

python run.py --dataset bigann-1B --definitions t3/faiss_t3/algos.yaml --runs 5 --t3  --nodocker --power-capture 192.168.99.110:1234:10

python run.py --dataset msturing-1B --definitions t3/faiss_t3/algos.yaml --runs 5 --t3  --nodocker --power-capture 192.168.99.110:1234:10

python run.py --dataset msspacev-1B --definitions t3/faiss_t3/algos.yaml --runs 5 --t3  --nodocker --power-capture 192.168.99.110:1234:10

python run.py --dataset text2image-1B --definitions t3/faiss_t3/algos.yaml --runs 5 --t3  --nodocker --power-capture 192.168.99.110:1234:10

python run.py --dataset ssnpp-1B --definitions t3/faiss_t3/algos.yaml --runs 5 --t3  --nodocker --power-capture 192.168.99.110:1234:10


