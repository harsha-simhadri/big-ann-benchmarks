#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track ood --algorithm zilliz
python3 run.py --dataset text2image-10M --algorithm zilliz --neurips23track ood 
