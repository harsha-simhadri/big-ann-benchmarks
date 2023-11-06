
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

### Binary filtering 

The issue is that this callback is relatively slow because (1) it requires to access the $M_\mathrm{meta}$ matrix which causes cache misses and (2) it performs an iterative binary search. 
Since the callback is called in the tightest inner loop of the search function, and since the IVF search tends to perform many vector comparisons, this has non negligible performance impact. 

To speed up this test, we can use a nifty piece of bit manipulation. 
The idea is that the vector ids are 63 bits long (64 bits integers but negative values are reserved, so we cannot use the sign bit). 
However, since $N=10^7$ we use only $\lceil \log_2 N \rceil = 24$ bits of these, leaving 63-24 = 39 bits that are always 0. 

Now, we associate to each word $j$ a 39-bit signature $S[j]$, and the to each set of words the binary `or` of these signatures. 
The query is represented by $s_\mathrm{q} = S[w_1] \vee S[w_2]$. 
Database entry $i$ with words $W_i$ is represented by $s_i = \vee_{w\in W_i} S[w]$. 

Then we have the following implication: if $\\{w_1, w_2\\} \subset W_i$ then all 1 bits of $s_\mathrm{q}$ are also set to 1 in $s_i$. 

$$\\{w_1, w_2\\} \subset W_i \Rightarrow \neg s_i \wedge s_\mathrm{q} = 0$$

Which is equivalent to:

$$\neg s_i \wedge s_\mathrm{q} \neq 0 \Rightarrow \\{w_1, w_2\\} \not\subset W_i $$

Of course, this is an implication, not an equivalence. 
Therefore, it can only rule out database vectors. 
However, the binary test is very cheap to perform (uses a few machine instructions on data that is already in machine registers), so it can be used as a pre-filter to apply the full membership test on candidates. 
This is implemented in the `IDSelectorBOWBin` object. 

The remaining degree of freedom is how to choose the binary signatures, because this rule is always valid, but its filtering ability depends on the choice of the signatures $S$. 
After a few tests (see [this notebook](https://gist.github.com/mdouze/75103e4cef436510ac9b834f9a77496f#file-eval_binary_signatures-ipynb) ) it seems that a random signature with 0.1 probability for 1s filters our 80% of negative tests. 
Asjuting this to the frequency of the words did not seem to yield better results. 

## Choosing between the two implementations 

The two implementations are complementary: the word-first implementation gives exact results, and has a strong filtering ability for rare words. 
The `IndexIVFFlat` implementation gives approximate results and is more relevant for words that are more common, where a significant subset of vectors are indeed relevant. 

Therefore, there should be a rule to choose between the two, and the relevant metric is the size of the subset of vectors to consider. 
We can use statistics on the words, ie. $\mathrm{nocc}[j]$ is the number of times word $j$ appears in the dataset (this is just the column-wise sum of the $M_\mathrm{meta}$). 

For a single query word $w_1$, the fraction of relevant indices is just $f = \mathrm{nocc}[w_1] / N$.
For two query words, it is more complicated to compute but an estimate is given by $f = \mathrm{nocc}[w_1] \times \mathrm{nocc}[w_2] / N^2$ (this estimate assumes words are independent, which is incorrect). 

Therefore, the rule that we use is based on a threshold $\tau$ (called `metadata_threshold` in the code) : 

- if $f < \tau$ then use the word-first search

- otherwise use the IVFFlat based index

Note that the optimal threshold also depends on the target accuracy (since the IVFFlat is not exact, when a higher accuracy is desired), see https://github.com/harsha-simhadri/big-ann-benchmarks/pull/105#issuecomment-1539842223 .


## Code layout 

The code is in faiss.py, with performance critical parts implemented in C++ and wrapped with SWIG in `bow_id_selector.swig`. 
SWIG directly exposes the C++ classes and functions in Python. 

