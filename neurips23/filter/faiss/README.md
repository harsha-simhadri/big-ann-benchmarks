
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

This is a Faiss [`IndexIVFFlat`](https://github.com/facebookresearch/faiss/wiki/The-index-factory#encodings) called `index`. 

By default the index performs unfiltered search, ie. the nearest vectors to $q$ can be retrieved. 
The accuracy of this search depends on the number of visited centroids of the `IndexIVFFlat` (parameter `nprobe`, the larger the more accurate and the slower). 

One solution would be to over-fetch vectors and perform filtering post-hoc using the words in the result list.
However, it is unclear /how much/ we should overfetch. 

Therefore, another solution is to use the Faiss [filtering functionality](https://github.com/facebookresearch/faiss/wiki/Setting-search-parameters-for-one-query#searching-in-a-subset-of-elements), ie. provide a callback function that is called for each vector id to decide if it should be considered as a result or not. 

The callback function is implemented in C++ in the class `IDSelectorBOW`. 
For vector id $i$ it looks up the row $i$ of $M_\mathrm{meta}$ and peforms a binary search on $w_1$ to check of that word belongs to the words associated to vector $i$.
If $w_2$ is also provided, it does the same for $w_2$. 
The callback returns true only if all terms are present. 

Note that this callback is relatively slow because (1) it requires to access the $M_\mathrm{meta}$ matrix which causes cache misses and (2) it performs the binary search. 
Since the callback is called in the tightest inner loop of the search function, this has non negligible performance impact. 

### Binary filtering 


## Choosing between the two implementations 

## Code layout 

