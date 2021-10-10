# FAISS Baseline

This README contains information required for T3 Track submissions.

## Hardware Configuration And Cost

|Part                         |Model                                             |No. |Unit Price                          |Total Price|
|-----------------------------|--------------------------------------------------|----|------------------------------------|-----------|
|Chassis and Motherboard      |[Advantech Sky-6200 2U](cost/AdvantechSky6200.pdf)|   1|[5572.42](cost/AdvantechSky6200.pdf)|    5572.42|
|RAM                          |[Advantech 32GB Memory](cost/RAM.pdf)             |  24|              [259.00](cost/RAM.pdf)|    6216.00|
|SSD                          |[2TB SeaGate](cost/SSD.pdf)                       |   1|              [334.48](cost/SSD.pdf)|     334.48|
|GPU                          |[NVidia V100](cost/GPU.pdf)                       |   1|             [9899.00](cost/GPU.pdf)|    9899.00|
|Total                        |                                                  |   1|                                    |   22021.90|

## Hardware Access

This hardware is maintained by the competition organizers.  Please send an email to big-ann-organizers@googlegroups.com to get access to a system or see the section below to build your own system.

## No Source Code Declarations

This submission requires the following software components where source-code is not available and/or not part of the source-code for this submission:
* NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* CUDA 11 libraries and host drivers
* NVidia V100 firmware 

## Hardware Setup And Software Installation

## Prerequisites

* Linux Ubuntu 18.04
* CUDA 11.0
* The NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* This cloned project repository

### Test On A Small Dataset

Note that all the subsequent commands must be run in the top-level directory of this repo on your machine.

First build the faiss_t3 docker container:
```
python install.py --dockerfile t3/faiss_t3/Dockerfile
```
Now create a small random dataset, query set, and associated ground truth:
```
python create_dataset.py --dataset random-xs
```
Now build a FAISS index for this dataset:
```
python run.py --definitions t3/faiss_t3/algos.yaml --dataset random-xs --t3 
```
This may take an hour or so.  When it's done, you can plot the recall-vs-throughput results as follows:
```
python plot.py --definitions t3/faiss_t3/algos.yaml --dataset random-xs
```
You can now run on the competition datasets.

#### Known Issues

The NVidia GPU docker support for various Linux distributions involves a lot of steps.

The run.py script also supports a "--nodocker" flag.  When run in this way, the algorithm is not launched in a docker container. Obviously, this requires having CUDA 11.0 drivers working natively on your system, and the installation of the compatible FAISS GPU library.  

If you take this route, we recommend using the Anaconda distribution of python, creating a python=3.8.5 environment, and installing FAISS using this command:
```
conda install -c pytorch faiss-gpu cudatoolkit=11.0
```
