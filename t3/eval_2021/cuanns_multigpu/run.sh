#!/bin/bash

set -x

python run.py --definitions t3/cuanns_multigpu/algos.yaml --dataset deep-1B --t3  --power-capture 10.150.170.104:1235:10
python run.py --definitions t3/cuanns_multigpu/algos.yaml --dataset msturing-1B --t3  --power-capture 10.150.170.104:1235:10
python run.py --definitions t3/cuanns_multigpu/algos.yaml --dataset msspacev-1B --t3 --power-capture 10.150.170.104:1235:10
python run.py --definitions t3/cuanns_multigpu/algos.yaml --dataset bigann-1B --t3 --power-capture 10.150.170.104:1235:10

