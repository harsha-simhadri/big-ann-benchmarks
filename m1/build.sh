#!/bin/bash

set -x
set -e

#export DOCKER_BUILDKIT=0

# all
# no platform flag: docker build --progress=plain -f ./Dockerfile.all -t neurips23-filter-faiss .

docker build --progress=plain --platform linux/amd64 -f ./Dockerfile.all -t neurips23-filter-faiss . 

# try arm64 docker build --progress=plain --platform linux/arm64 -f ./Dockerfile.all -t neurips23-filter-faiss . 


