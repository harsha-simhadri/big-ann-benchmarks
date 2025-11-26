#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm wm_filter
python3 run.py --dataset yfcc-10M --algorithm wm_filter --neurips23track filter 
