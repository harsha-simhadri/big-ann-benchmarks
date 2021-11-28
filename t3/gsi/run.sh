#!/bin/bash

set -x 

LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --nodocker --definitions t3/gsi/algos.yaml --dataset ssnpp-1B --power-capture 192.168.99.32:1236:10

#gdb -ex=r --args env LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --nodocker --definitions t3/gsi/algos.yaml --dataset ssnpp-1B | tee "$LOGFILE"
#| tee "$LOGFILE"
#DT=`date "+%F-%T"`
#LOGFILE="results/text2image_$DT.log"
#LD_LIBRARY_PATH=./gsl_resources_release PYTHONPATH=./gsl_resources_release python3 run.py --t3 --nodocker --definitions t3/gsi/algos.yaml --dataset text2image-1B   --power-capture 192.168.99.32:1236:10  | tee "$LOGFILE"


