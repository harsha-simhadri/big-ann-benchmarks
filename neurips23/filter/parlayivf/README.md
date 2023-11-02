# ParlayANN's IVF&sup2;
## Introduction
This submission is from the team at Carnegie Mellon and the University of Maryland responsible for the [ParlayANN library](https://github.com/cmuparlay/ParlayANN), a collection of algorithms for approximate nearest neighbor search implemented with [ParlayLib](https://github.com/cmuparlay/parlaylib), an efficient library for shared memory parallelism.

## Approach
We leverage the fact that filtered search, especially when using 'and' queries, provides beneficial constraints on the set of points needing to be searched, and the fact that IVF indices can be stored in relatively little memory. The name IVF&sup2; refers to the fact we treat the filters like an actual inverted file index (in contrast to the 'IVF' indices used by faiss, pgvector, etc. for vector search), and the posting lists of the filters are (above a size threshold) themselves IVF indices. 

More details to come.
