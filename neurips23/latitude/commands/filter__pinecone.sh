#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track filter --algorithm pinecone
python3 run.py --dataset yfcc-10M --algorithm pinecone --neurips23track filter 
