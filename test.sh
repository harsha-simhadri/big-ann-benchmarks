#!/bin/bash
set -e
sudo chown -R $(whoami):$(whoami) results/
docker build -t billion-scale-benchmark -f install/Dockerfile .
docker build -t billion-scale-benchmark-http-ann-example -f install/Dockerfile.httpannexample .
python create_dataset.py --dataset bigann-10M
python run.py --dataset bigann-10M --algorithm http-ann-example --count 10 --rebuild --runs 1
sudo chown -R $(whoami):$(whoami) results/
python plot.py --dataset bigann-10M --count 10 --recompute
