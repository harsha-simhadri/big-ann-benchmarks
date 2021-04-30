# Billion-Scale ANN

## Dataset creation

- Do we want to have everything 'automatically' be set up?
  - use the original datasets as they are, wrapped in a class
  - wrappers to move to numpy arrays in `benchmark/datasets.py`
- How do we create query workloads for the actual competition? (Or: Should they be the same?)

## Algorithms

- API proposal in <benchmark/algorithms/base.py>
- Idea: algorithms fit dataset (given a reference to the hdf5 file or the whole dataset?) -> write index to disk (separate process, but we should be able to re-run it).
   - Index can be shared, will usually be build in-memory? (Requirement: has to fit in 128GB RAM, so has to be built out-of-memory as well)
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
