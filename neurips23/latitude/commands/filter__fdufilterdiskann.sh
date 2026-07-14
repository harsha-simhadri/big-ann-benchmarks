#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm fdufilterdiskann
python3 run.py --dataset yfcc-10M --algorithm fdufilterdiskann --neurips23track filter 
