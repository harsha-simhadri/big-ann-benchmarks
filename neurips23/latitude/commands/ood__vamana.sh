#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track ood --algorithm vamana
python3 run.py --dataset text2image-10M --algorithm vamana --neurips23track ood 
