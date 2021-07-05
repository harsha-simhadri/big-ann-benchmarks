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
nprobe=1,quantizer_efSearch=4
nprobe=2,quantizer_efSearch=4
...
nprobe=512,quantizer_efSearch=256
nprobe=512,quantizer_efSearch=512
nprobe=1024,quantizer_efSearch=512
"

python  track1_baseline_faiss/baseline_faiss.py \
   --dataset deep-1B --indexfile data/deep-1B.IVF1M_2level_PQ64x4fsr.faissindex \
   --search --searchparams $params

```

The sets of parameters per dataset are listed in [this GIST](https://gist.github.com/mdouze/bb71032f0b3bf3cc9bdaa6ff1287c144). 
They are ordered from fastest / least accurate to slowest / most accurate.

### Results 

The results should look like: 

```
parameters                               inter@ 10 time(ms/q)   nb distances #runs
nprobe=1,quantizer_efSearch=4            0.1738      0.00327       12210374    92
nprobe=2,quantizer_efSearch=4            0.2394      0.00424       24328050    71
nprobe=2,quantizer_efSearch=8            0.2879      0.00545       24278048    56
...
nprobe=512,quantizer_efSearch=256        0.6877      0.75883     5896044691    1
nprobe=512,quantizer_efSearch=512        0.6886      0.77421     5890639041    1
nprobe=1024,quantizer_efSearch=512       0.6886      1.46841    11607413418    1
```

This means that by setting the parameters `nprobe=2,quantizer_efSearch=4`, we obtain 0.2394 recall @ 10 (aka inter @10) for that dataset, the search will take  0.00327 ms per query (305810 QPS). 
The total number of distances computed for all queries is 24328050 and this measurement was obtained in 71 runs (to reduce jitter in time measurements).

The speed-accuracy tradeoff plots are here (with 32 threads on a given 2.2Ghz machine): 

![](plots/bigann-1B.png)

![](plots/deep-1B.png)

![](plots/msturing-1B.png)

![](plots/msspace-1B.png)



