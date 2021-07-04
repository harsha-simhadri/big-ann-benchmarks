# Running the Faiss baselines 

## Installing software 

In addition to this repository, running the baseline code requires a conda install with Faiss

```bash
wget  https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

bash  Anaconda3-2020.11-Linux-x86_64.sh

# follow instructions and run profile.sh to get a working conda

conda create -n faiss_1.7.1 python=3.8
conda activate faiss_1.7.1
conda install -c pytorch faiss-cpu
```

All instructions below are supposed to be run from the root of the repository. 
To make the package accessible, set `export PYTHONPATH=.`

## Downloading the data 

To download the data (database files, query files and ground truth, do 
```
mkdir data/    # this is where all the data goes, a symlink is fine
python  track1_baseline_faiss/baseline_faiss.py --dataset deep-1B --prepare
```
The available datasets are bigann-1B deep-1B ssnpp-1B text2image-1B msturing-1B msspacev-1B. 
To download the largest files, `--prepare` will use axel or azcopy. Make sure that they are in the path.

Replace the -1B suffix with -100M or -10M to get a subset of each dataset (only the relevant fraction of the database will be downloaded). 
This is useful for small-scale experiments.

## Building the index 

TODO 

## Running the evaluation

### Getting the pre-built indexes 

Pre-built indexes are available. 
To download them 

```bash
wget https://dl.fbaipublicfiles.com/billion-scale-ann-benchmarks/track1_baseline_faiss/deep-1B.IVF1M_2level_PQ64x4fsr.faissindex -P data/
```
(replace deep-1B with the relevant dataset name)

### Running the evaluation

The evaluation proceeds by loading the index and looping over a set of search-time parameters that obtain different speed-accuracy tradeoffs. 

This writes as: 
```bash

params="

"


python  track1_baseline_faiss/baseline_faiss.py --dataset deep-1B --indexfile deep-1B.IVF1M_2level_PQ64x4fsr.faissindex --search --searchparams $params

```


### Results 




