#!/bin/bash

python run.py --algorithm graphann --t3 --nodocker --dataset bigann-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset msspacev-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset deep-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset msturing-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset text2image-1B --power-capture 192.168.0.121:14118:10

