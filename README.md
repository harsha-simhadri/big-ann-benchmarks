# Billion-Scale ANN

<http://big-ann-benchmarks.com/>

## Install

The only prerequisite is Python (tested with 3.6) and Docker. Works with newer versions of Python as well but probably requires an updated `requirements.txt` on the host. (Suggestion: copy `requirements.txt` to `requirements${PYTHON_VERSION}.txt` and remove all fixed versions. `requirements.txt` has to be kept for the docker containers.)

1. Clone the repo.
2. Run `pip install -r requirements.txt` (Use `requirements_py38.txt` if you have Python 3.8.)
3. Install docker by following instructions [here](https://docs.docker.com/engine/install/ubuntu/).
You might also want to follow the post-install steps for running docker in non-root user mode.
3. Run `python install.py` to build all the libraries inside Docker containers.

## Storing Data

The framework assumes that all data is stored in `data/`.
Please use a symlink if your datasets and indices are supposed to be stored somewhere else.
The location of the linked folder matters a great deal for T2 (SSD-based search) performance. 
A local SSD such as the one found on Azure Ls-series VMs are better than remote disks, even premium ones.
See [T1/T2](t1_t2/README.md) for more details.

## Data sets

See <http://big-ann-benchmarks.com/> for details on the different datasets.

### Dataset Preparation

Before running experiments, datasets have to be downloaded. All preparation can be carried out by calling

```python
python create_dataset.py --dataset [bigann-1B | deep-1B | text2image-1B | ssnpp-1B | msturing-1B | msspacev-1B]
```

Note that downloading the datasets can potentially take many hours.

For local testing, there exist smaller random datasets `random-xs` and `random-range-xs`. 
Furthermore, most datasets have 1M, 10M and 100M versions, run `python create_dataset -h` to get an overview.


## Running the benchmark

Run `python run.py --dataset $DS --algorithm $ALGO` where `DS` is the dataset you are running on,
and `ALGO` is the name of the algorithm. (Use `python run.py --list-algorithms`) to get an overview.
`python run.py -h` provides you with further options.

The parameters used by the implementation to build and query the index can be found in `algos.yaml`.

## Running the track 1 baseline
After running the installation, we can evaluate the baseline as follows.

```bash

for DS in bigann-1B  deep-1B  text2image-1B  ssnpp-1B  msturing-1B  msspacev-1B;
do
    python run.py --dataset $DS --algorithm faiss-t1;
done
```

On a 28-core Xeon E5-2690 v4 that provided 100MB/s downloads, carrying out the baseline experiments took roughly 7 days.

To evaluate the results, run
```bash
sudo chmod -R 777 results/
python data_export.py --output res.csv
python3.8 eval/show_operating_points.py --algorithm faiss-t1 --threshold 10000
```

## Including your algorithm and Evaluating the Results

See [Track T1/T2](t1_t2/README.md) for more details on evaluation for Tracks T1 and T2.

See [Track T3](t3/README.md) for more details on evaluation for Track T3.
