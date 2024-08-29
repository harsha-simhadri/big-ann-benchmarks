#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track sparse --algorithm cufe
python3 run.py --dataset sparse-full --algorithm cufe --neurips23track sparse 
