#!/bin/bash

#python run.py --t3 --private-query --definitions t3/faiss_t3/algos.yaml --dataset deep-1B --nodocker
python run.py --t3 --private-query --definitions t3/faiss_t3/algos.yaml --dataset bigann-1B --nodocker
#python run.py --t3 --private-query --definitions t3/faiss_t3/algos.yaml --dataset text2image-1B --nodocker
#python run.py --t3 --private-query --definitions t3/faiss_t3/algos.yaml --dataset msturing-1B --nodocker
#python run.py --t3 --private-query --definitions t3/faiss_t3/algos.yaml --dataset msspacev-1B --nodocker
#python run.py --t3 --private-query --definitions t3/faiss_t3/algos.yaml --dataset ssnpp-1B --nodocker

#python run.py --definitions t3/faiss_t3/algos.yaml --dataset deep-1B --t3 --private-query --nodocker --power-capture 192.168.99.110:1237:10
#python run.py --definitions t3/faiss_t3/algos.yaml --dataset bigann-1B --t3 --private-query --nodocker --power-capture 192.168.99.110:1237:10
#python run.py --definitions t3/faiss_t3/algos.yaml --dataset text2image-1B --t3 --private-query --nodocker --power-capture 192.168.99.110:1237:10
#python run.py --definitions t3/faiss_t3/algos.yaml --dataset msturing-1B --t3 --private-query --nodocker --power-capture 192.168.99.110:1237:10
#python run.py --definitions t3/faiss_t3/algos.yaml --dataset msspacev-1B --t3 --private-query --nodocker --power-capture 192.168.99.110:1237:10
#python run.py --definitions t3/faiss_t3/algos.yaml --dataset ssnpp-1B --t3 --private-query --nodocker --power-capture 192.168.99.110:1237:10
