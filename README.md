# Billion-Scale ANN 

Singularity vs. Docker?

## Dataset creation

- Do we want to have everything 'automatically' be set up? (see <benchmark/datasets.py>)
- What is contained in a dataset:
  - HDF5 with 1B vectors, 10k query vectors
  - 1B vectors split up into 100 batches of 10M
  - Groundtruth: List of (true) nearest neighbors and their distances? (A bit annoying: lists have dynamic size for range queries)
  - How do we create query workloads for the actual competition? (Or: Should they be the same?)

## Algorithms

- API proposal in <benchmark/algorithms/base.py>
- Idea: algorithms fit dataset (given a reference to the hdf5 file or the whole dataset?) -> write index to disk (separate process, but we should be able to re-run it). 
   - Index can be shared, will usually be build in-memory?
   - On which machine is that supposed to be run?
- Running experiment: Load index (index file name defined in yaml?) -> run queries -> write down metadata (query time etc.) and true answers (what does the algorithm think are the nearest neighbors/the points in the range) as hdf5
- Evaluating: Check hdf5 results against groundtruth data

## TODO

- Implement baselines
   - FAISS: Martin can do it based on the FAISS 1B wiki code, only T1?
   - DiskANN: Use ann-benchmarks implementation, unsure about the T1/T2 setup.
- Include datasets
  - SIFT-1B (takes around 12h to preprocess in 100x10M batches)
  - ...
- Implement framework
  - pretty easy, most ann-benchmarks code can be re-used
- Implement evaluation
  - Martin: What do we need? I can create the plots/website, what about the competition table?
- Test framework
