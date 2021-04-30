# Billion-Scale ANN

<http://big-ann-benchmarks.com/>

## Install

The only prerequisite is Python (tested with 3.6) and Docker. Works with newer versions of Python as well but probably requires an updated `requirements.txt` on the host. (Suggestion: copy `requirements.txt` to `requirements${PYTHON_VERSION}.txt` and remove all fixed versions. `requirements.txt` has to be kept for the docker containers.)

1. Clone the repo.
2. Run `pip install -r requirements.txt`.
3. Run `python install.py` to build all the libraries inside Docker containers.

## Data sets


| Dataset                                                           | Dimensions | Train size | Test size | Neighbors | Distance
| ----------------------------------------------------------------- | ---------: | ---------: | --------: | --------: | --------- |
| [DEEP1B](https://research.yandex.com/datasets/biganns)              |         96 |  1,000,000,000 |    10,000 |       100 | Euclidean 
| [SIFT1B](http://corpus-texmex.irisa.fr/)              |         128 |  1,000,000,000 | 10,000 |       100 | Euclidean
| [Text-to-Image-1B](https://research.yandex.com/datasets/biganns)              |         200 |  1,000,000,000 |    10,000 |       100 | Inner Product

### Dataset Preparation

Before running experiments, datasets have to be downloaded. All preparation can be carried out by calling

```python
python create_dataset.py --dataset [sift-1M | sift-1B | deep-1B | text2image-1B]
```

Note that downloading the datasets can potentially take many hours.

## Running the benchmark

Run `python run.py` (this can take an extremely long time, potentially days)

You can customize the algorithms and datasets if you want to:

* Check that `algos.yaml` contains the parameter settings that you want to test
* To run experiments on SIFT-1M, invoke `python run.py --dataset sift-1M`. See `python run.py --help` for more information on possible settings. Note that index building can take many days. 

## Evaluating the Results
Run `python plot.py --dataset ...` or `python data_export.py --output res.csv` to plot results or dump all of them to csv for further post-processing.

In general, consult the `--help` options of the scripts for more arguments.

## Example run
After running the installation, we can run a quick test using in-memory FAISS on a small sample of SIFT-1B as follows:

1. First, download and setup `SIFT1B` using `python create_dataset.py --dataset sift-1B`. 
2. Next, run `python run.py --dataset sift-1M  --algorithm faiss-ivf`
3. Plot the results using `sudo python plot.py --dataset sift-1M -Y` for a qps/recall plot with y axis in log scale.

## Including your algorithm

1. Add your algorithm into `benchmark/algorithms` by providing a small Python wrapper inheriting from `BaseANN`  defined in `benchmark/algorithms/base.py`.
2. Add a Dockerfile in `install/` 
3. Add it to `algos.yaml with the parameter choices you would like to run.


# Some notes

## Dataset creation

- How do we create query workloads for the actual competition? (Or: Should they be the same?)

## Algorithms

- API proposal in <benchmark/algorithms/base.py>
- Idea: algorithms fit dataset (given path to base vectors and dataset name?) -> write index to disk (separate process, but we should be able to re-run it).
   - Requirement: has to fit in 128GB RAM, so index has to be built out-of-memory as well
- Running experiment: Load index (implementation checks if index is available) -> run queries -> write down metadata (query time etc.) and true answers (what does the algorithm think are the nearest neighbors/the points in the range) as hdf5
- Evaluating: Check hdf5 results against groundtruth data (`plot.py` and `data_export.py` can be used for export)

## TODO

- Include datasets
  - SIFT-1B
  - Deep-1B
  - Text2Image
  - FB dataset?
  - 2 MSR datasets?
- Implement framework
  - a few small todos left
- Implement baselines
   - FAISS: inmem version from ann-benchmarks adapted to the new api.
   - FAISS: Martin can do it based on the FAISS 1B wiki code, only T1? -> Dmitry is going to help.
   - DiskANN: Harsha writes Python wrapper for DiskANN with SSD
- Implement evaluation
  - Martin: What do we need? I can create the plots/website, what about the competition table?
  - for now: ann-benchmarks style png plots, and `data_export.py` to dump everything to csv.
- Test framework
- automatic deployment in the cloud?
- docker vs. singularity:
  - benchmark disk i/o
  - https://www.diva-portal.org/smash/get/diva2:1277794/FULLTEXT01.pdf sees singularity as clear winner for i/o
- will container setup work for t3?
