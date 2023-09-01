
# Faiss baseline for the Filtered search track

The database of size $N=10^7$ can be seen as the combination of:

- a matrix $M$ of size $N \times d$ of embedding vectors (called `xb` in the code). $d=192$.
- a sparse matrix $M_\mathrm{meta}$ of size $N \times v$, entry $i,j$ is set to 1 iff word $j$ is applicable to vector $i$. $v=200386$, called `meta_b` 

The Faiss basleline for the filtered search track is based on two distinct data structures: 

- a term-based inverted file that maps each word to the vectors (docs) that contain that term.
In the code it is a CSR matrix called `docs_per_word` (it's just the transposed version of `meta_b`. 

- a Faiss `IndexIVFFlat` object that can be used to perform vector based search, called `index`. 

Both data structured allow to peform filtered searches in two different ways. 

## Word-based inverted file 




## IndexIVFFlat structure 




## Binary filtering 
