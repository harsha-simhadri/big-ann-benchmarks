# Practical Vector Search: NeurIPS 2023 Competition

## Table Of Contents

- [Introduction](#introduction)  
- [For Participants](#for_participants) 
  - [Getting Started](#getting_started) 
  - [Starting Your Development](#starting_your_development)
  - [Developing Your Dockerfile](#developing_your_dockerfile)
  - [Developing Your Algorithm](#developing_your_algorithm) 
  - [Measuring your Algorithm](#measuring_your_algorithm)
  - [How To Get Help](#how_to_get_help)
  - [Leaderboard](#leaderboard)
  - [Custom Setups](#custom_setup)
- [For Evaluators](#for_organizers)  

## Introduction

The Practical Vector Search challenge at NeurIPS 2023 has four different tasks: 

**Task Filters**: This task will use the YFCC 100M dataset. 
    We use 10M random images from YFCC100M, for which we extract CLIP embeddings. In addition, we associate to each image a "bag" of tags: words extracted from the description, the camera model, the year the picture was taken and the country. 
    The tags are from a vocabulary of 200386 possible tags. 
    The 100,000 queries consist of one image embedding and one or two tags that must appear in the database elements to be considered.

**Task Streaming:** This task uses 10M slice of the MS Turing data set released in the previous challenge. The index starts with zero points and must implement the "runbook" provided - a sequence of insertion operations, deletion operations, and search commands (roughly 4:2:1 ratio) - within a time bound. In the final run, we will  use a different runbook, and possibly a different data set, to avoid participants over-fitting to this dataset.

**Task Out-Of-Distribution:**  Yandex Text-to-Image 10M represents a cross-modal dataset where the database and query vectors have different distributions in the shared vector space.
    The base set is a 10M subset of the Yandex visual search database of 200-dimensional image embeddings which are produced with the Se-ResNext-101 model. 
    The query embeddings correspond to the user-specified textual search queries.
    The text embeddings are extracted with a variant of the DSSM model.

**Task Sparse:**  This task is based on the common MSMARCO passage retrieval dataset, which has 8,841,823 text passages, encoded into sparse vectors using the SPLADE model. The vectors have a large dimension (less than 100,000), but each vector in the base dataset has an average of approximately 120 nonzero elements. The query set comprises of 6,980 text queries, embedded by the same SPLADE model. The average number of nonzero elements in the query set is approximately 49 (since text queries are generally shorter). Given a sparse query vector, the index should return the top-k results according to the maximal inner product between the vectors.


## Baselines

The baselines were run on an Azure Standard D8lds v5 (8 vcpus, 16 GiB memory) machine. The CPU model is Intel(R) Xeon(R) Platinum 8370C CPU @ 2.80GHz.

| Task | Baseline | Highest Throughput above 90% recall | Command |
|------|----------|---------| --- |
|Sparse| Linear Scan | 101 |  `python3 run.py --dataset sparse-full --algorithm linscan --neurips23track sparse` |
|Filter| faiss | 3200 | `python3 run.py --dataset yfcc-10M --algorithm faiss --neurips23track filter` |
|Streaming| DiskANN | ? |  `python3 run.py --dataset msspacev-10M --algorithm diskann --neurips23track streaming` |
|OOD| DiskANN | 4882 | `python3 run.py --dataset text2image-10M --algorithm diskann --neurips23track ood` | 


## Leaderboards

We will release data points and plots for recall vs QPS separately for the four different tracks. 

## For_Participants

Participants must submit their algorithm via a pull request and (optionally) index file(s) upload (one per participating dataset). 

### Requirements

You will need the following installed on your machine:
* Python ( we tested with Anaconda using an environment created for Python version 3.10 ) and Docker.
* Note that we tested everything on Ubuntu Linux 22.10 but other environments should be possible.

### Getting_Started

This section will present a small tutorial about how to use this framework and several of the key scripts you will use throughout the development of your algorithm and eventual submission.

First, clone this repository and cd into the project directory:
```
git clone <REPO_URL>
cd <REPO_URL>
```
Install the python package requirements:
```
pip install -r requirements_py3.10.txt
```
Create a small, sample dataset.  For example, to create a dataset with 10000 20-dimensional random floating point vectors, run:
```
python create_dataset.py --dataset random-xs
```
To create a smaller slice of the competition datasets (e.g. 10M slice of deep-1B), run:
```
python create_dataset.py --dataset deep-10M
```
To see a complete list of datasets, run the following:
```
python create_dataset.py --help
```

Build the docker container baselines for each track:
```
python install.py --neurips23track filter    --algorithm faiss  
python install.py --neurips23track sparse    --algorithm linscan 
python install.py --neurips23track ood       --algorithm diskann
python install.py --neurips23track streaming --algorithm diskann
```

Test the benchmark and baseline using the algorithm's definition file on small test inputs
```
python run.py --neurips23track filter    --algorithm faiss   --dataset random-filter-s
python run.py --neurips23track sparse    --algorithm linscan --dataset sparse-small
python run.py --neurips23track ood       --algorithm diskann --dataset random-xs
python run.py --neurips23track streaming --algorithm diskann --dataset random-xs
```

For the competition dataset, run commands mentioned in the table above, for example:
```
python run.py --neurips23track filter    --algorithm faiss   --dataset yfcc-10M
python run.py --neurips23track sparse    --algorithm linscan --dataset sparse-full
python run.py --neurips23track ood       --algorithm diskann --dataset text2image-10M
python run.py --neurips23track streaming --algorithm diskann --dataset msspacev-10M
```

For streaming track, download the ground truth (needs azcopy in your binary path):
```
python benchmark/streaming/download_gt.py --runbook_file neurips23/streaming/simple_runbook.yaml --dataset msspacev-10M 
python benchmark/streaming/download_gt.py --runbook_file neurips23/streaming/clustered_runbook.yaml --dataset msturing-10M-clustered 
```
Alternately, to compute ground truth for an arbitrary runbook, [clone and build DiskANN repo](https://github.com/Microsoft/DiskANN) and use the command line tool to compute ground truth at various search checkpoints. The `--gt_cmdline_tool` points to the directory with DiskANN commandline tools.
```
python benchmark/streaming/compute_gt.py --dataset msspacev-10M --runbook neurips23/streaming/simple_runbook.yaml --gt_cmdline_tool ~/DiskANN/build/apps/utils/compute_groundtruth
```
For streaming track, consider also the examples in [clustered runbook](neurips23/streaming/clustered_runbook.yaml). The datasets here are [generated](neurips23/streaming/clustered_data_gen.py) by clustering the original dataset with k-means and packing points in the same cluster into contiguous indices. Then insertions are then performed one cluster at a time. This runbook tests if an indexing algorithm can adapt to data draft.


To make the results available for post-processing, change permissions of the results folder

```
sudo chmod 777 -R results/
```

To plot QPS vs recall, you can use `plot.py` as follows:
```
python plot.py --dataset yfcc-10M 
```
This will place a plot into the *results/* directory.

The following command will summarize all results files into a single csv file `res.csv` suitable for further processing. 

```
python data_export.py --out res.csv
```

### Starting_Your_Development

In the following, we assume that you will use the provided framework as a basis for your development.
Please consult the [guide](#custom_setup) if you want to diverge from this setup.

First, please create a short name for your team without spaces or special characters.  Henceforth in these instructions, this will be referenced as [your_team_name].

Create a custom branch off main in this repository:
```
git checkout -b [task]/[your_team_name]
```

where [task] is _sparse_, _streaming_, _filter_, or _ood_.


### Developing_Your_Dockerfile

This framework evaluates algorithms in Docker containers by default.  Your algorithm's Dockerfile should live in *neurips23/[task]/[your_team_name]/Dockerfile*.  Your Docker file should contain everything needed to install and run your algorithm on a system with the same hardware. 

Please consult [this file](../filter/faiss/Dockerfile) as an example. 

To build your Docker container, run:
```
python install.py --neurips23track [task] --install [your_team_name]
```

### Developing_Your_Algorithm

Develop and add your algorithm's Python class to the `neurips23/[task]/[your_team_name]/` directory.
* You will need to subclass from the [BaseANN class](../benchmark/algorithms/base.py). Each track has its own base class, for example see the [BaseFilterANN class](../neurips23/filter/base.py). 
Implement the functions of that parent class.
* You should consult the examples present in the [neurips23](./) directory.
* If it is difficult to write a Python wrapper, please consult [HttpANN](../benchmark/algorithms/httpann_example.py) for a RESTful API.
* Create a `yaml` file, for example `neurips23/[task]/[your_team_name]/config.yaml`, that specifies how to invoke your implementation.  This file contains the index build parameters and query parameters that will get passed to your algorithm at run-time. 

When you are ready to test on the competition datasets, use the create_dataset.py script as follows:
```
python create_dataset.py --dataset [sparse-full|yfcc-10M|...|...]
```
If your machine is capable of both building and searching an index, you can benchmark your algorithm using the run.py script. 
```
python run.py --algorithm faiss --neurips23track filter --dataset yfcc-10M
```
This will write the results to the toplevel [results](../results) directory.

<!--
To build the index and upload it to Azure cloud storage without querying it:
```
python run.py --algorithm diskann-t2 --dataset deep-1B --upload-index --blob-prefix <your Azure blob container path> --sas-string <your sas string to authenticate to blob>
```
To download the index from cloud storage and query it on another machine:
```
python run.py --algorithm diskann-t2 --dataset deep-1B --download-index --blob-prefix <your Azure blob container path> --sas-string <your sas string to authenticate to blob>
```
-->

### Measuring_Your_Algorithm


Now you can analyze the results using plot.py. Sudo might be required here. To avoid sudo, run `sudo chmod -R 777 results/` before invoking these scripts.
```
python plot.py --dataset [DATASET]
```
This will place a plot of the algorithms performance into the toplevel [results](../results) directory.

The plot.py script supports other benchmarks.  To see a complete list, run:
```
python plot.py --help
```

You can plot additional metrics, e.g. mean SSD IOs vs recall/AP for T2, using:
```
python plot.py --dataset deep-1B -x k-nn -y mean_ssd_ios 
```
### Baseline results

To get a table overview over the best recall achieved over a certain QPS threshold, run 
```
python data_export.py --output res.csv
python eval/show_operating_points.py --algorithm $ALGO --threshold $THRESHOLD res.csv
```

### Submitting_Your_Algorithm

A submission is composed of a pull request to this repo with the following. 
* Your algorithm's python class, inheriting from the task-specific base class, in `neurips23/[task]/[team]/`
* A Dockerfile `neurips23/[task]/[team]/Dockerfile describing how to retrieve, compile and set up requirements for your algorithm.
* A config file `neurips23/[task]/[team]/config.yml` that specifies 
  * 1 index build configuration 
  * 10 search configuration
* Add an entry to [CI test list](../.github/workflows/neurips23.yml) for test dataset of the specific task. We can start working with larger datasets once these tests pass. 
<!--* An URL to download any prebuilt indices placed in `algos-2021.yaml`. **This is optional, but strongly encourages.** This would help us evaluate faster, although we would build your index to verify the time limit. Please see `faiss_t1.py` and `diskann-t2.py` for examples. If you are unable to host the index on your own Azure blob storage, please let us know and we can arrange to have it copied to organizer's account.-->

We will run early PRs on organizer's machines to the extent possible and provide any feedback necessary.

### How_To_Get_Help

There are several ways to get help as you develop your algorithm using this framework:
* You can submit an issue at this github repository.
* Send en email to the competition's googlegroup, big-ann-organizers@googlegroups.com

### Leaderboard

This leaderboard is based on the standard recall@10 vs throughput benchmark that has become a standard benchmark when evaluating and comparing approximate nearest neighbor algorithms. The recall of the baselines at this QPS threshold is listed [above](#measuring_your_algorithm). 

Algorithms will be ranked on how much their recall surpasses the baselines at these QPS thresholds.   We will add up the recall improvements of each algorithm on all tasks it competes on.  
<!--are at an advantage as they can benefit from additional scores. Any recall regression compared to the baseline on the datasets committed to will be subtracted from the final score.-->

## Custom_Setup

While we encourage using our framework for all steps of the evaluation, we consider open-source submissions that diverge from the proposed setup. 
We require the submission of a docker container with an accompanying script to carry out the experimental run.
You are encouraged to submit containers that contain the index for the task to speed up the evaluation. 
This script is supposed to have the same command line arguments for running the experiments as the `run.py` script.
In particular, `--dataset, --neurips23track, --algorithm` have to be supported.
The script takes care of mounting the following directories from the host into the container: `data/` (read-only) and `results` (read-write). It copies a config file `config.yml` that contains index build and search parameters. 

Input data must be read from `data/` as show-cased in [datasets.py](../benchmark/datasets.py) using I/O functions similar to the ones provided in [dataset_io.py](../benchmark/dataset_io.py). Results must be written in a HDF5 format as showcased in [results.py](../benchmark/results.py) in the same folder structure as used by the evaluation framework. 
In particular, all steps mentioned in <#measuring_your_algorithm> must be possible from the result files.



## For_Evaluators

