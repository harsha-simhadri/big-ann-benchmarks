# T3: Cuanns IVFPQ

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
python3 install.py --dockerfile t3/cuanns_ivfpq/Dockerfile
```
Setup links to downloaded dataset and pre-built index files.
```
./setup_links.sh
```
Otherwise, download datasets for competitions supported by cuanns_ivfpq.
```
python3 create_dataset.py --dataset [bigann-1B|deep-1B|msturing-1B|msspacev-1B|text2image-1B]
```

## Run Competition Algorithm

You can run this algorithm on the competition dataset using the run.py script.
```
python3 run.py --t3 --definitions t3/cuanns_ivfpq/algos.yaml --dataset [bigann-1B|deep-1B|msturing-1B|msspacev-1B|text2image-1B]
```

#### Known Issues

The program to build the index file from the competition dataset is not yet implemented in this repo. When the program is ready, we will describe how to build the index.
