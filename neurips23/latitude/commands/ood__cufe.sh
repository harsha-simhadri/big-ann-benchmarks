#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track ood --algorithm cufe
python3 run.py --dataset text2image-10M --algorithm cufe --neurips23track ood 
