# FAISS T3 Baseline

These are instructions for setting up the FAISS T3 baseline on a new machine.

## Prerequisites

* A machine with a CUDA 11.0 compatible GPU
* We tested on Linux Ubuntu 18.04 ( other Linux configurations should be possible )
* The NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* This cloned project repository.

## Test On A Small Dataset

Note that all the subsequent commands must be run in the top-level directory of this repo on your machine.

First build the faiss_t3 docker container:
```
python install.py --dockerfile t3/faiss_t3/Dockerfile
```
Now create a small random dataset, query set, and associated ground truth:
```
python setup.py --dataset random-xs
```
Now build a FAISS index for this dataset:
```
python run.py --definitions t3/faiss_t3/algos.yaml --dataset random-xs --t3 
```
This will take an hour or so.  When it's done, you can plot the recall-vs-throughput results as follows:
```
python plot.py --definitions t3/faiss_t3/algos.yaml --dataset random-xs
```
You can now run on the competition datasets.

### Known Issues

The NVidia GPU docker support for various Linux distributions can be rough around the edges.

The run.py script also supports a "--nodocker" flag.  When run in this way, the algorithm is not launched in a docker container. Obviously, this requires having CUDA 11.0 drivers working natively on your system, and the installation of the compatible FAISS GPU library.

If you take this route, we recommend using the Anaconda distribution of python, creating a python=3.8.5 environment, and installing FAISS using this command:
```
conda install -c pytorch faiss-gpu cudatoolkit=11.0
```
