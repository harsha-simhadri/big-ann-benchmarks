# Billion-Scale ANN

<http://big-ann-benchmarks.com/>

## Basic idea 
we propose a new network structure called Learnable Compression Network with Transformer (LCNT) to  compress  the  feature  into  a  low  dimensional  space,  and an anisotropic neighborhood relationship preserving loss that focuses on maintaining distances of point pairs that are closein original feature space. For graphs-based methods,using LCNT reduces index construction time cost and memory usage, while improving search speed. For PQ related approaches, using LCNT improves search speed and accuracy significantly.

## Dependences

Faiss
Pytorch > 1.2

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


## Evaluating the Results
Run `sudo python plot.py --dataset ...` or `sudo python data_export.py --output res.csv` to plot results or dump all of them to csv for further post-processing.
To avoid sudo, run `sudo chmod -R 777 results/` before invoking these scripts.

To get a table overview over the best recall/ap achieved over a certain threshold, run `python3 eval/show_operating_points.py --algorithm $ALGO --threshold $THRESHOLD res.csv`, where `res.csv` is the file produced by running `data_export.py` above.

For the track1 baseline, the output `python3 eval/show_operating_points.py --algorithm faiss-t1 --threshold 10000 res.csv` led to

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

## Including your algorithm

1. Add your algorithm into `benchmark/algorithms` by providing a small Python wrapper inheriting from `BaseANN`  defined in `benchmark/algorithms/base.py`. See `benchmark/algorithm/faiss_t1.py` for an example.
2. Add a Dockerfile in `install/` 
3. Edit `algos.yaml with the parameter choices you would like to test.
4. (Add an option to download pre-built indexes as seen in `faiss_t1.py`.)

