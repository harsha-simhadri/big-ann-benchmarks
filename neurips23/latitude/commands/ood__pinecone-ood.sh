#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track ood --algorithm pinecone-ood
python3 run.py --dataset text2image-10M --algorithm pinecone-ood --neurips23track ood 
