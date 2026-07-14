#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track sparse --algorithm nle
python3 run.py --dataset sparse-full --algorithm nle --neurips23track sparse 
