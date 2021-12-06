#!/bin/bash

set -x

python run.py --definitions t3/cuanns_ivfpq/algos.yaml --dataset msspacev-1B --t3 --private-query --power-capture 10.150.170.104:1235:10
#python run.py --definitions t3/cuanns_ivfpq/algos.yaml --dataset deep-1B --t3  --private-query --power-capture 10.150.170.104:1235:10
#python run.py --definitions t3/cuanns_ivfpq/algos.yaml --dataset msturing-1B --t3 --private-query  --power-capture 10.150.170.104:1235:10
#python run.py --definitions t3/cuanns_ivfpq/algos.yaml --dataset msspacev-1B --t3 --private-query --power-capture 10.150.170.104:1235:10
#python run.py --definitions t3/cuanns_ivfpq/algos.yaml --dataset bigann-1B --t3 --private-query --power-capture 10.150.170.104:1235:10
#python run.py --definitions t3/cuanns_ivfpq/algos.yaml --dataset text2image-1B --t3 --private-query --power-capture 10.150.170.104:1235:10

