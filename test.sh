#!/bin/bash
set -e
docker build -t billion-scale-benchmark -f install/Dockerfile .
docker build -t billion-scale-benchmark-http-ann-example -f install/Dockerfile.httpannexample .

#python create_dataset.py --dataset random-range-xs
#python run.py --dataset random-range-xs --algorithm http-ann-example --count 10 --rebuild --runs 5
#sudo chown -R $(whoami):$(whoami) results/
#python plot.py --dataset random-range-xs --count 10 --recompute

python create_dataset.py --dataset random-xs
python run.py --dataset random-xs --algorithm http-ann-example --count 10 --rebuild --runs 5
sudo chown -R $(whoami):$(whoami) results/
python plot.py --dataset random-xs --count 10 --recompute
