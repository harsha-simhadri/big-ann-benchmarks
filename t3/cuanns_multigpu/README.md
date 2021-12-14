# T3: Cuanns MultiGPU

## Hardware Configuration And Cost

|Part           |Model                                      |No. |Unit Price                          |Total Price|
|---------------|-------------------------------------------|----|------------------------------------|-----------|
|System         |[NVIDIA DGX A100 640GB]                    |   1|                                    |           |
|Total          |                                           |   1|                                    |           |

Details of the system can be found at https://www.nvidia.com/en-us/data-center/dgx-a100/. However, no price information is provided. Therefore, we will not participate in the leaderboards based on hardware cost.

## Hardware Access

SSH access to the system will be provided to competition organizers.

## No Source Code Declarations

This submission requires the following software components where source-code is not available and/or not part of the source-code for this submission:
* NVIDIA docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* NVIDIA CUDA libraries and host drivers
* the algorithm implementation is provided as a library

## Hardware Setup And Software Installation

### Prerequisites

* Linux Ubuntu 20.04
* CUDA 11.4 or above
* The NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* This cloned project repository

### Setup and Installation Instructions

Note that all the subsequent commands must be run in the top-level directory of this repo on your machine.

First build the docker container:
```
python install.py --dockerfile t3/cuanns_multigpu/Dockerfile
```
Download datasets for competitions supported by cuanns_multigpu. Note that even if you do not build the index files, you still need to download the datasets.
```
python create_dataset.py --dataset [bigann-1B|deep-1B|msturing-1B|msspacev-1B]
```
Donwload index files. The download instructions will be updated as soon as the location of the index files is determined.
```
(to be updated)
```

## Run Competition Algorithm

You can run this algorithm on the competition dataset using the run.py script.
```
python run.py --t3 --definitions t3/cuanns_multigpu/algos.yaml --dataset [bigann-1B|deep-1B|msturing-1B|msspacev-1B]
```

#### Known Issues

The program to build the index file from the competition dataset is not yet implemented in this repo. When the program is ready, we will describe how to build the index.

## Algorithm Description


1. overview
We use 8 NVIDIA Tesla A100-80GB GPUs to handle billion-scale datasets. We divide the dataset into 8 shards of the same size and build a graph for each shard. During the search, each GPU has one shard and its corresponding graph in memory, and the query is sent to every GPU. So we can compute top k results within each shard on every GPU, and then the 8*k results are fetched to one GPU and the final top k results are chosen among them.

2. graph building
We use k-nearest neighbor (k-NN) graph in our implementation. A diversified k-NN graph is generated using heuristic edge selection methods as in FANNG (https://www.cv-foundation.org/openaccess/content_cvpr_2016/html/Harwood_FANNG_Fast_Approximate_CVPR_2016_paper.html). After that, we add reverse edges to the graph.

3. searching
The algorithm is very similar to NSG (https://dl.acm.org/doi/abs/10.14778/3303753.3303754), but the implementation is for GPU and we tailor it to take the advantage of the high parallelism of GPU.
- start the search from 32 random start nodes rather than one
- use 32 threads (called a warp in CUDA) for each query, the calculation of the distance between each pair of vectors is performed by a warp.
- the cost of maintaining a hash table is not trivial on GPU, so unlike the implementation on CPU, we do not use hash table to avoid redundant distance calculations, but only to avoid multiple expansions of a node. So the size of hash table can be much smaller and hence more efficient.


