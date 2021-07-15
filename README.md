# Billion-Scale ANN

<http://big-ann-benchmarks.com/>

## Install

The only prerequisite is Python (tested with 3.6) and Docker. Works with newer versions of Python as well but probably requires an updated `requirements.txt` on the host. (Suggestion: copy `requirements.txt` to `requirements${PYTHON_VERSION}.txt` and remove all fixed versions. `requirements.txt` has to be kept for the docker containers.)

1. Clone the repo.
2. Run `pip install -r requirements.txt` (Use `requirements_py38.txt` if you have Python 3.8.)
3. Install docker by following instructions [here](https://docs.docker.com/engine/install/ubuntu/).
4. Run `python install.py` to build all the libraries inside Docker containers.

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

Run `python run.py --dataset $DS --algorithm $ALGO --rebuild`, where `DS` is the dataset you are running on,
and `ALGO` is the name of the algorithm. (Use `python run.py --list-algorithms`) to get an overview.
`python run.py -h` provides you with further options.

The parameters used by the implementation to build and query the index can be found in `algos.yaml`.


## Evaluating the Results
Run `sudo python plot.py --dataset ...` or `sudo python data_export.py --output res.csv` to plot results or dump all of them to csv for further post-processing. 
To avoid sudo, run `sudo chmod -R 777 results/` before invoking these scripts.


## Running the track 1 baseline 
After running the installation, we can evaluate the baseline as follows.

```bash

for DS in bigann-1B  deep-1B  text2image-1B  ssnpp-1B  msturing-1B  msspacev-1B;
do
    python create_dataset.py --dataset $DS;
    python run.py --dataset $DS --algorithm faiss-t1;
done
```

On a 28-core Xeon that provided 100MB/s downloads, carrying out the baseline experiments took roughly 7 days.

## Including your algorithm

1. Add your algorithm into `benchmark/algorithms` by providing a small Python wrapper inheriting from `BaseANN`  defined in `benchmark/algorithms/base.py`. See `benchmark/algorithm/faiss_t1.py` for an example.
2. Add a Dockerfile in `install/` 
3. Edit `algos.yaml with the parameter choices you would like to test.

