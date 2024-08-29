#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track sparse --algorithm sustech-whu
python3 run.py --dataset sparse-full --algorithm sustech-whu --neurips23track sparse 
