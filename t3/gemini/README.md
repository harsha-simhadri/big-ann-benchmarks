# Gemini
  
This README contains information required for T3 Track submissions.

## Hardware Configuration And Cost

|Part                         |Model                                             |No. |Unit Price                          |Total Price|
|-----------------------------|--------------------------------------------------|----|------------------------------------|-----------|
|Chassis and Motherboard      |[Advantech Sky-6200 2U](cost/AdvantechSky6200.pdf)|   1|[5572.42](cost/AdvantechSky6200.pdf)|    5572.42|
|RAM                          |[Advantech 64GB Memory](cost/RAM.pdf)             |  24|              [409.99](cost/RAM.pdf)|    9839.76|
|SSD                          |[2TB SeaGate](cost/SSD.pdf)                       |   1|              [334.48](cost/SSD.pdf)|     334.48|
|APU                          |[LedaE APU](cost/APU.pdf)                         |   4|            [35000.00](cost/APU.pdf)|  140000.00|
|GPU                          |[NVidia V100](cost/GPU.pdf)                       |   1|             [9899.00](cost/GPU.pdf)|    9899.00|
|Total                        |                                                  |   1|                                    |  165645.66|

## Hardware Access

This hardware is maintained by the GSI Technology, one of the competition organizers.  Please send an email to big-ann-organizers@googlegroups.com or gwilliams@gsitechnology.com to get access to a system or see the section below to build your own system.

## No Source Code Declarations

This submission requires the following software components where source-code is not available and/or not part of the source-code for this submission:
* NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* CUDA 11 libraries and host drivers
* NVidia V100 firmware compatible with CUDA 11
* Gemini Software system software and host drivers (version TBD)
* Gemini pyGSL vector search library (version TBD)
* LedaE PCIe board firmware (version TBD)

## Hardware Setup And Software Installation

### Prerequisites

* Linux Ubuntu 18.04
* Python 3.69 
* Python package requirements in [requirements.txt](requirements.txt)
* CUDA 11.0
* The NVidia docker container runtime ( https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html )
* Gemini system software and host drivers ( please follow the instructions that came with your Leda hardware.)
* This cloned project repository

### Test Your Leda Hardware

At the command line run the following diagnostic program to make sure your boards are operational:

```dev_diagnostic --iter 1 --run-all-cards 1```

### pyGSL Libraries

Download the pyGSL libraries from [here](https://storage.googleapis.com/bigann/gemini/gsl_resources.tar.gz.1) and unpack into the toplevel directory of the cloned repository.

### Competition Index Files

Currently the competition index files must be downloaded and installed manually.

Download all the index files from [here](tbd) (TBD) and unpack into the cloned repo's data directory.

## Run The Competition Algorithm

In the top-level directory of the cloned repository, run the following command:

```t3/gemini/run_bin_python.sh```

Note that it will take a few minutes for all the index files to load, so be patient.

