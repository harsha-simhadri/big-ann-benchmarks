# T3: Cuanns IVFPQ

## Hardware Configuration And Cost

|Part           |Model                                      |No. |Unit Price                          |Total Price|
|---------------|-------------------------------------------|----|------------------------------------|-----------|
|System         |[NVIDIA DGX A100 640GB]                    |   1|                                    |           |
|Total          |                                           |   1|                                    |           |

Note that we don't know the list price of NVIDIA DGX A100 640GB, so we can't list it. Therefore, we will not participate in the leaderboards based on hardware cost.

## Hardware Access

This hardware is maintained by NVIDIA employees, including member of the Cuanns team. Please send an email to anaruse@nvidia.com and/or yongw@nvidia.com to get access to a system.

## No Source Code Declarations

This submission requires the following software components where source-code is not available and/or not part of the source-code for this submission:
* NVIDIA docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* NVIDIA CUDA libraries (including library for fast ANNS) and host drivers

## Hardware Setup And Software Installation

## Prerequisites

* Linux Ubuntu 20.04
* CUDA 11.4 or above
* The NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* This cloned project repository

### Setup and Installation Instructions

Note that all the subsequent commands must be run in the top-level directory of this repo on your machine.

First build the cuanns_ivfpq docker container:
```
python install.py --dockerfile t3/cuanns_ivfpq/Dockerfile
```
Download datasets for competitions supported by cuanns_ivfpq. Note that even if you do not build the index files, you still need to download the datasets.
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
python run.py --t3 --definitions t3/cuanns_ivfpq/algos.yaml --dataset [bigann-1B|deep-1B|msturing-1B|msspacev-1B]
```

#### Known Issues

The program to build the index file from the competition dataset is not yet implemented in this repo. When the program is ready, we will describe how to build the index.
