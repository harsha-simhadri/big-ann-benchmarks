#!/bin/bash

python3 run.py --t3 --definitions t3/diskann-bare-metal/algos.yaml --dataset deep-1B
python3 run.py --t3 --definitions t3/diskann-bare-metal/algos.yaml --dataset bigann-1B
python3 run.py --t3 --definitions t3/diskann-bare-metal/algos.yaml --dataset text2image-1B
python3 run.py --t3 --definitions t3/diskann-bare-metal/algos.yaml --dataset msturing-1B
python3 run.py --t3 --definitions t3/diskann-bare-metal/algos.yaml --dataset msspacev-1B
