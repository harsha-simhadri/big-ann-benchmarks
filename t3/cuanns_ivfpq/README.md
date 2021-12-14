# T3: Cuanns IVFPQ (Single GPU)

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

## Algorithm Description

1. Overview

 

We use a GPU-accelerated implementation of the so-called IVFPQ method, which partitions dataset vectors into clusters using k-means and compresses the residual vectors from each cluster centroid using product quantization (PQ). Since a single A100-80GB GPU is used for the search, the index file for each billion-scale dataset is created to fit into 80GB of GPU memory to minimize the amount of data transfer between CPU and GPU during the search.

When searching, the GPU approximates more results than the specified number (topk), and then the CPU refines the results using the original dataset mapped in the host memory, thus achieving both high performance and high recall.

 

2. Indexing

 

The clusters for partitioning are trained using 10% of vectors randomly selected from the dataset. The number of clusters is chosen to be 250,000 for most of the billion-scale datasets so that the average number of vectors in each cluster is around a few thousand. Since naïve k-means clustering on this scale is very time consuming, our implementation employs GPU-accelerated hierarchical k-means.

 

Important parameters of the PQ method are the number of sub-space and the bit length of each element. In general, the number of dimensions of the dataset should be multiple of the number of sub-space in the PQ method. In order to be able to select an arbitrary number of sub-spaces, if the above condition cannot be met, our implementation uses the vector rotated by a rotation matrix randomly created after expanding the dimension of the original vector by 0 elements as the input to the PQ method. In addition, as far as we know, existing PQ implementations for GPU only support 8-bit as the bit length of each element, but our implementation supports also 4-bit, 5-bit, 6-bit and 7-bit, making it easy to adjust the size of index file according to the requirements.

 

3. Searching

 

In our implementation, the search procedure consists of the following fine steps, where steps 1 to 4 are performed on the GPU and step 5 is performed on the CPU.

 

               1) Calculate the distance from the query vectors to the cluster centroids.

               2) Select a specified number of clusters (num_probes) with close distances based on the results of step 1).

               3) Calculate the approximate similarity between the query vectors and the dataset vectors in the clusters selected in step 2).

               4) Select a specified number (topk * refine_ratio) of dataset vectors with high similarity based on the results of step 3).

               5) Calculate the similarity between the query vectors and the dataset vectors selected in step 4) using the original dataset, and select a specified number (topk) of vectors with high similarity.

 

When the number of query vectors is large, as in this challenge, the execution time of the matrix-matrix multiplication becomes the performance limiter in step 1). We keep the cluster centroids with single precision. Therefor, the matrix-matrix multiplication here is usually done with single precision. However, we have confirmed that there is almost no loss of accuracy when this distance is calculated using TF32, which is supported by TensorCore units on A100 GPUs, so we have applied TF32 here to improve the performance.

 

Steps 2) and 4) are the process of selecting the top K elements with the smallest or the largest values from the array, also known as select-k. For small values of K, the partial sort based select-k implementation is known to be fast even on GPUs, but this method is not suitable for GPUs for large values of K, which is somewhat problematic in Step 2) in this challenge. We have implemented a radix-based select-k highly optimized for GPUs, which we use here. Our select-k implementation does not cause a significant performance degradation even when the value of K is increased. As a result, we are able to mitigate the performance degradation when selecting a relatively large number of clusters in Step 2).

 

The approximate similarity calculation in Step 3) is basically implemented using the same approach as the Faiss GPU. First, for a selected cluster, the partial similarity between all PQ codes and the target query vector is calculated for each sub-space, the results are stored in the GPU's shared memory, and the final similarity of each dataset vector in the cluster is calculated by adding the results stored in the shared memory. In the Faiss GPU, static shared memory is used, so the similarity calculation must be performance with half precision when the number of sub-space is large and the amount of shared memory required exceeds 48 KB. However, our implementation uses dynamic shared memory and can effectively use shared memory, which has increased in recent GPUs, so there is no need to reduce the accuracy of the similarity calculation even in cases where the number of sub-space is large. Also, as explained above, our implementation supports not only 8-bit length but also 4-bit, 5-bit, 6-bit, and 7-bit length, so the number of sub-space can be further increased by shortening the bit length and reducing the amount of shared memory required.

 

The refinement calculation of the similarity in Step 5) is done on the CPU due to its relatively low computational complexity, and it is thread parallelized using OpenMP.

