#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm hwtl_sdu_anns_filter
python3 run.py --dataset yfcc-10M --algorithm hwtl_sdu_anns_filter --neurips23track filter 
