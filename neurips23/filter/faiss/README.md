
# Faiss baseline for the Filtered search track

The database of size $N=10^7$ can be seen as the combination of:

- a matrix $M$ of size $N \times d$ of embedding vectors (called `xb` in the code). $d=192$.
- a sparse matrix $M_\mathrm{meta}$ of size $N \times v$, entry $i,j$ is set to 1 iff word $j$ is applicable to vector $i$. $v=200386$, called `meta_b` in the code (a [CSR matrix](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html))

The Faiss basleline for the filtered search track is based on two distinct data structures, a word-based inverted file and a Faiss `IndexIVFFlat`. 
Both data structured allow to peform filtered searches in two different ways. 

The search is based on a query vector $q\in \mathbb{R}^d$ and associated query words $w_1, w_2$ (there are one or two query words). 
The search results are the database vectors that include /all/ query words and that are nearest to $q$ in $L_2$ distance. 

## Word-based inverted file 

This is term-based inverted file that maps each word to the vectors (docs) that contain that term.
In the code it is a CSR matrix called `docs_per_word` (it's just the transposed version of `meta_b`). 

At search time, the subset (`subset`) of vectors eligible for results depends on the number of query words: 

- if there is a single word $w_1$ then it's just the set of non-0 entries in row $w_1$ of the `docs_per_word` matrix.
This can be extracted at no cost

- if there are two words $w_1$ and $w_2$ then the sets of non-0 entries of rows $w_1$ and $w_2$ are intersected.
This is done with `np.intersect1d` or the C++ function `intersect_sorted`, that is faster (linear in nb of non-0 entries of the two rows).

When this subset is selected, the result is found by searching the top-k vectors in this subset of rows of $M$. 
The result is exact and the search is most efficient when the subset is small (ie. the words are discriminative enough to filter the results well). 

## IndexIVFFlat structure 


This is a Faiss `IndexIVFFlat` called `index`. 

### Binary filtering 


## Choosing between the two implementations 


