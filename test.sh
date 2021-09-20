#!/bin/bash
set -e
sudo chown -R $(whoami):$(whoami) results/
docker build -t billion-scale-benchmark -f install/Dockerfile .
docker build --build-arg cachebust=$RANDOM -t billion-scale-benchmark-language-agnostic -f install/Dockerfile.languageagnostic .
python create_dataset.py --dataset bigann-10M
python run.py --dataset bigann-10M --algorithm language-agnostic
