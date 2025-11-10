#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm zilliz
python3 run.py --dataset yfcc-10M --algorithm zilliz --neurips23track filter 
