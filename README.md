# Billion-Scale ANN

Singularity vs. Docker?

## Dataset creation

- Do we want to have everything 'automatically' be set up?
  - use the original datasets as they are, wrapped in a class
  - wrappers to move to numpy arrays in `benchmark/datasets.py`
- How do we create query workloads for the actual competition? (Or: Should they be the same?)

## Algorithms

- API proposal in <benchmark/algorithms/base.py>
- Idea: algorithms fit dataset (given a reference to the hdf5 file or the whole dataset?) -> write index to disk (separate process, but we should be able to re-run it).
   - Index can be shared, will usually be build in-memory?
   - On which machine is that supposed to be run?
- Running experiment: Load index (index file name defined in yaml?) -> run queries -> write down metadata (query time etc.) and true answers (what does the algorithm think are the nearest neighbors/the points in the range) as hdf5
- Evaluating: Check hdf5 results against groundtruth data

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
  - for now: ann-benchmarks style png plots.
- Test framework
- automatic deployment in the cloud?
- docker vs. singularity:
  - benchmark disk i/o
  - https://www.diva-portal.org/smash/get/diva2:1277794/FULLTEXT01.pdf sees singularity as clear winner for i/o
