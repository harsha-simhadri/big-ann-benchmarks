#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm pyanns
python3 run.py --dataset yfcc-10M --algorithm pyanns --neurips23track filter 
