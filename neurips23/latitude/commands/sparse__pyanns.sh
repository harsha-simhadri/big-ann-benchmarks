#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track sparse --algorithm pyanns
python3 run.py --dataset sparse-full --algorithm pyanns --neurips23track sparse 
