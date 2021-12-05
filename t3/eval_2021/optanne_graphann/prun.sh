#!/bin/bash

#python run.py --algorithm graphann --definitions t3/optanne_graphann/algos.yaml --t3 --private-query --nodocker --dataset bigann-1B --power-capture 192.168.0.121:14118:10
#python run.py --algorithm graphann --definitions t3/optanne_graphann/algos.yaml --t3 --private-query --nodocker --dataset msspacev-1B --power-capture 192.168.0.121:14118:10
#python run.py --algorithm graphann --definitions t3/optanne_graphann/algos.yaml --t3 --private-query --nodocker --dataset deep-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --definitions t3/optanne_graphann/algos.yaml --t3 --private-query --nodocker --dataset msturing-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --definitions t3/optanne_graphann/algos.yaml --t3 --private-query --nodocker --dataset text2image-1B --power-capture 192.168.0.121:14118:10

