#!/bin/bash

set -x 

#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset bigann-1B 
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset msturing-1B 
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset text2image-1B 
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset ssnpp-1B 
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset msspacev-1B 
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset deep-1B 

#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset text2image-1B --power-capture 192.168.99.32:1236:10
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset deep-1B --power-capture 192.168.99.32:1236:10
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset bigann-1B --power-capture 192.168.99.32:1236:10
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset msturing-1B --power-capture 192.168.99.32:1236:10
LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset msspacev-1B --power-capture 192.168.99.32:1236:10
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --private-query --nodocker --definitions t3/gsi/algos.yaml --dataset ssnpp-1B --power-capture 192.168.99.32:1236:10


