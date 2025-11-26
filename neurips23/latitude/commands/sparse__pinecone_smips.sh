#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track sparse --algorithm pinecone_smips
python3 run.py --dataset sparse-full --algorithm pinecone_smips --neurips23track sparse 
