#!/bin/bash
set -x # echo the command
set -e # stop script on error

python install.py --neurips23track streaming --algorithm pinecone
python3 run.py --dataset msturing-30M-clustered --algorithm pinecone --neurips23track streaming --runbook_file neurips23/streaming/final_runbook.yaml
