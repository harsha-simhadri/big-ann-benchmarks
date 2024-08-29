#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm faissplus
python3 run.py --dataset yfcc-10M --algorithm faissplus --neurips23track filter 
