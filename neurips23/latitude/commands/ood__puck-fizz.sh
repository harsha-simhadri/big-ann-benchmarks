#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track ood --algorithm puck-fizz
python3 run.py --dataset text2image-10M --algorithm puck-fizz --neurips23track ood 
