# T1 and T2 Tracks

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
- [For Evaluators](#for_organizers)  

## Introduction

The T1 and T2 tracks evaluate algorithms on standardized Azure CPU servers.

**Track 1**: In-memory indices with [FAISS](https://github.com/facebookresearch/faiss) as the baseline. Search would use Azure [Standard_F32s_v2 VMs](https://docs.microsoft.com/en-us/azure/virtual-machines/fsv2-series) with 32 vCPUs and 64GB RAM.

**Track 2:** Out-of-core indices with [DiskANN](https://github.com/Microsoft/diskann) as the baseline. In addition to the limited DRAM in T1, index can use an SSD for search. Search would use Azure [Standard_L8s_v2 VMs](https://docs.microsoft.com/en-us/azure/virtual-machines/lsv2-series) with 8 vCPUS, 64GB RAM and a local SSD Index constrained to 1TB.

Index construction for both tracks would use Azure [Standard_F64s_v2 VM](https://docs.microsoft.com/en-us/azure/virtual-machines/fsv2-series) with 64vCPUs, 128GB RAM and an additional [4TB of Premium SSD](https://docs.microsoft.com/en-us/azure/virtual-machines/disks-types) to be used for storing the data, index and other intermediate data. There is a **time limit for 4 days per dataset** for index build. 

Queries will be supplied in one shot and the algorithm can execute the queries in any order. 

We will release plots for recall vs QPS separately for tracks T1 and T2.
Additionally, we will release leaderboards for T1 and T2. The  metric for the leaderboard in each track will be the sum of improvements in recall over the baseline at the target QPS over all datasets. **The target recall
for T1 is 10000 QPS and for T2 is 1500 QPS.**

Participants must submit their algorithm via a pull request and (optionally) index file(s) upload (one per participating dataset).  


## For_Participants

### Requirements

You will need the following installed on your machine:
* Python ( we tested with Anaconda using an environment created for Python version 3.8 ) and Docker.
* Note that we tested everything on Ubuntu Linux 18.04 but other environments should be possible.

### Getting_Started

This section will present a small tutorial about how to use this framework and several of the key scripts you will use throughout the development of your algorithm and eventual submission.

First, clone this repository and cd into the project directory:
```
git clone <REPO_URL>
cd <REPO_URL>
```
Install the python package requirements:
```
pip install -r requirements_py38.txt
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

For T2, set up the local SSD on Azure Ls8v2 machine by running the following under sudo.
```
parted /dev/nvme0n1 mklabel gpt mkpart primary 0% 100%;
mkfs -t ext4 /dev/nvme0n1;
mkdir /nvme;
mount /dev/nvme0n1 /nvme/;
echo "/dev/nvme0n1 /nvme  ext4   defaults    0   0" >> /etc/fstab;
```
You might also want to create a symbolic link to a folder under `/nvme`
```
sudo mkdir /nvme/data
sudo chmod 777 /nvme/data
ln -s /nvme/data data
```

Build the docker container for the T1 or T2 baselines:
```
#for T1
python install.py --algorithm faissconda  
#for T2
python install.py --algorithm diskann
```
Run a benchmark evaluation using the algorithm's definition file:
```
python run.py --algorithm faiss_t1 --dataset random-xs
python run.py --algorithm diskann-t2 --dataset random-xs
```

For the competition dataset (e.g. deep-1B), running the following command downloads a prebuilt index and runs the queries locally.
```
python run.py --algorithm faiss_t1 --dataset deep-1B
python run.py --algorithm diskann-t2 --dataset deep-1B
```

Now plot QPS vs recall:
```
python plot.py --algorithm faiss_t1 --dataset random-xs
python plot.py --algorithm diskann-t2 --dataset random-xs
```
This will place a plot into the *results/* directory.

### Starting_Your_Development

First, please create a short name for your team without spaces or special characters.  Henceforth in these instructions, this will be referenced as [your_team_name].

Create a custom branch off main in this repository:
```
# For t1
git checkout -b t1/[your_team_name]
# For t2
git checkout -b t2/[your_team_name]
```


### Developing_Your_Dockerfile

This framework evaluates algorithms in Docker containers by default.  Your algorithm's Dockerfile should live in *install/Docker.[your_team_name]*.  Your Docker file should contain everything needed to install and run your algorithm on a system with the same hardware. 

Please consult the Dockerfiles [here](../install/Dockerfile.faissconda) and [here](../install/Dockerfile.diskann) for examples.

To build your Docker container, run:
```
python install.py --install [your_team_name]
```

### Developing_Your_Algorithm

Develop and add your algorithm's python class to the [benchmark/algorithms](../benchmark/algorithms) directory.
* You will need to subclass from the [BaseANN class](../benchmark/algorithms/base.py) and implement the functions of that parent class.
* You should consult the examples already in the directory.
* If it is difficult to write a Python wrapper, please consult [HttpANN](../benchmark/algorithms/httpann_example.py) for a RESTful API.


When you are ready to test on the competition datasets, use the create_dataset.py script as follows:
```
python create_dataset.py --dataset [sift-1B|bigann-1B|text2image-1B|msturing-1B|msspacev-1B|ssnpp-1B]
```
To benchmark your algorithm, first create an algorithm configuration yaml in your teams directory called *algos.yaml.*  This file contains the index build parameters and query parameters that will get passed to your algorithm at run-time.  Please look at [algos.yaml](../algos.yaml).

If your machine is capable of both building and searching an index, you can benchmark your algorithm using the run.py script. 
```
python run.py --algorithm diskann-t2 --dataset deep-1B
```
This will write the results to the toplevel [results](../results) directory.

To build the index and upload it to Azure cloud storage without querying it:
```
python run.py --algorithm diskann-t2 --dataset deep-1B --upload-index --blob-prefix <your Azure blob container path> --sas-string <your sas string to authenticate to blob>
```
To download the index from cloud storage and query it on another machine:
```
python run.py --algorithm diskann-t2 --dataset deep-1B --download-index --blob-prefix <your Azure blob container path> --sas-string <your sas string to authenticate to blob>
```

### Measuring_Your_Algorithm


Now you can analyze the results using plot.py. Sudo might be required here. To avoid sudo, run `sudo chmod -R 777 results/` before invoking these scripts.
```
python plot.py --algorithm [your_team_name] --dataset deep-1B
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


Here are all the FAISS baseline recall@10 (AP for SSNPP) vs throughput plots for T1:
* [msturing-1B](results/T1/msturing-1B.png)
* [bigann-1B](results/T1/bigann-1B.png)
* [text2image-1B](results/T1/text2image-1B.png)
* [deep-1B](results/T1/deep-1B.png)
* [msspacev-1B](results/T1/msspacev-1B.png)
* [ssnpp-1B](results/T1/ssnpp-1B.png)

Here are all the DiskANN baseline recall@10 (AP for SSNPP) vs throughput plots for T2:
* [msturing-1B](results/T2/msturing-1B.png)
* [bigann-1B](results/T2/bigann-1B.png)
* [text2image-1B](results/T2/text2image-1B.png)
* [deep-1B](results/T2/deep-1B.png)
* [msspacev-1B](results/T2/msspacev-1B.png)
* [ssnpp-1B](results/T2/ssnpp-1B.png)


Here are all the DiskANN baseline recall@10 (AP for SSNPP) vs mean SSD IOs plots for T2:
* [msturing-1B](results/T2/msturing-1B-IO.png)
* [bigann-1B](results/T2/bigann-1B-IO.png)
* [text2image-1B](results/T2/text2image-1B-IO.png)
* [deep-1B](results/T2/deep-1B-IO.png)
* [msspacev-1B](results/T2/msspacev-1B-IO.png)
* [ssnpp-1B](results/T2/ssnpp-1B-IO.png)

To get a table overview over the best recall/ap achieved over a certain QPS threshold, run 
```
python3 data_export.py --output res.csv
python3 eval/show_operating_points.py --algorithm $ALGO --threshold $THRESHOLD res.csv
```

For the track1 baseline, the output, this led to

```
                         recall/ap
algorithm dataset
faiss-t1  bigann-1B       0.634510
          deep-1B         0.650280
          msspacev-1B     0.728861
          msturing-1B     0.703611
          ssnpp-1B        0.753780
          text2image-1B   0.069275
```

For the track2 baseline, this led to

```
                         recall/ap
algorithm   dataset
diskann-t2  bigann-1B       0.94913
            deep-1B         0.93706
            msspacev-1B     0.90095
            msturing-1B     0.93564
            ssnpp-1B        0.16274
            text2image-1B   0.48854
```

### Submitting_Your_Algorithm

A submission is composed of a pull request to this repo with the following. 
* Your algorithm's python class, inheriting from `BaseANN`, placed in the [benchmark/algorithms/](../benchmark/algorithms) directory.
* A Dockerfile in `install/` describing how to retrieve, compile and set up requirements for your algorithm.
* For each dataset you are participating in, add to [algos.yaml](../algos.yaml)
  * 1 index build configuration 
  * 10 search configuration
* Add an entry to [CI test list](../.github/workflows/benchmarks.yml) for the random-xs dataset, and for the random-range-xs dataset if your algorithm supports range search. We can start working with larger datasets once these tests pass. 
* An URL to download any prebuilt indices placed in `algos.yaml`. **This is optional, but strongly encourages.** This would help us evaluate faster, although we would build your index to verify the time limit. Please see `faiss_t1.py` and `diskann-t2.py` for examples. If you are unable to host the index on your own Azure blob storage, please let us know and we can arrange to have it copied to organizer's account.

We will run early PRs on organizer's machines to the extent possible and provide any feedback necessary.

### How_To_Get_Help

There are several ways to get help as you develop your algorithm using this framework:
* You can submit an issue at this github repository.
* Send an email to the competition's T1/T2 organizer, harsha.v.simhadri@gmail.com
* Send en email to the competition's googlegroup, big-ann-organizers@googlegroups.com

### Leaderboard

This leaderboard is based on the standard recall@10 vs throughput benchmark that has become a standard benchmark when evaluating and comparing approximate nearest neighbor algorithms. We have run FAISS and DiskANN as baselines for T1 and T2 respectively, and for each dataset chosen the best recall amongst configurations providing at least **10K QPS for T1 and 1500 QPS for T2**.  The recall of the baselines at this QPS threshold is listed [above](#measuring_your_algorithm). 

Algorithms will be ranked on how much their recall surpasses the baselines at these QPS thresholds.   We will add up the recall improvements of each algorithm on all data sets it competes on. Participants are required to commit to at least 3 datasets, and ideally more. Algorithms that work on more datasets are at an advantage as they can benefit from additional scores. Any recall regression compared to the baseline on the datasets committed to will be subtracted from the final score.

#### Results for T1
The table lists best Recall/AP obtained at at least 10,000 QPS by algorithms in pull requests submitted before Nov 2021. All non-empty cells are derived from author-published indices that succesfully ran on the standardized hardware with author-provided query configurations. Recall for bigann-1B does not count ties. This result is on the public query set.

A complete set of runs can be found [here](results/T1/neurips21/t1.csv) and QPS vs recall plots are [here](results/T1/neurips21/)


| PR  | Name      |bigann-1B  | deep-1B |	msspacev-1B |	msturing-1B |	ssnpp-1B  |	text2image-1B  |
|-----|-----------|-----------|---------|-------------|-------------|-----------|----------------|
| 58	| team11		|           | 0.64955 |             |	0.712211    |           |                |
| 60	| puck-t1		| 0.71468   |	0.72255 |				      | 0.793812*   |           |   0.160987*    |
| 66	| ngt-t1		|					  |         |				      |             |           |                |
| 69	| kst_ann_t1|	0.71219	  | 0.71219	| 0.764542    |	0.756419    |           |                |
| 71  | buddy-t1	|	0.62765		|         |				      |             |           |                |
|-----|-----------|-----------|---------|-------------|-------------|-----------|----------------|	
|     | baseline  |	0.63451   | 0.65028 |	0.728861    | 0.703611    |	0.75378   |	0.069275       |
|-----|-----------|-----------|---------|-------------|-------------|-----------|----------------|
* results for entries submitted after deadline.


#### Results for T2
The table lists best Recall/AP obtained at at least 1,500 QPS by algorithms in pull requests submitted before Nov 2021. All non-empty cells are derived from author-published indices that succesfully ran on the standardized hardware with author-provided query configurations. Recall for bigann-1B does not count ties. This result is on the public query set.

A complete set of runs can be found [here](results/T2/neurips21/t2.csv) and QPS vs recall plots are [here](results/T2/neurips21/)

| PR | Name      |bigann-1B  | deep-1B |	msspacev-1B |	msturing-1B |	ssnpp-1B  |	text2image-1B |
|----|-----------|-----------|---------|-------------|-------------|-----------|----------------|
| 62	| kota-t2	  |	0.950859	|         | 0.904001	  | 0.939817	  | 0.18212	  |               |
| 66	| ngt-t2		|					  |         |				      |             |           |               |					
| 70	| bbann	    |           |         |   0.7602		|             |   0.88573	| 0.495423      |
|----|-----------|-----------|---------|-------------|-------------|-----------|----------------|
|    | baseline |  0.94913	  | 0.93706 |	0.90095	    | 0.93564	    | 0.16274   |	0.48854       |
|----|-----------|-----------|---------|-------------|-------------|-----------|----------------|

## For_Evaluators

