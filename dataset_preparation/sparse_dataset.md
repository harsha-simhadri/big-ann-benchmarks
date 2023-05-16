# Sparse dataset for the 2023 ANN challenge

## Goal
This is a dataset of sparse vectors. These are vectors of very high dimension (~30k), 
but with a small number of nonzero elements. 
A typical example is a way to represent text, where the dimension is the vocabulary, 
and the values correspond to the different words in each document / paragraph that is indexed.

## Dataset details

**Dataset**: sparse embedding of the MS-MARCO passage retrieval dataset. 
The embeddings are based on a deep learning model called SPLADE (specifically, it is the 
 SPLADE CoCondenser EnsembleDistil (`naver/splade-cocondenser-ensembledistil`)).

The base dataset contains  .8M vectors with average sparsity (# of nonzeros): ~130. All nonzero values are positive. 

The common query set (`dev.small`) contains 6980 queries, where the average number of nonzeros is ~49.

Similarity is measured by max dot-product, and the overall retrieval score is Recall@10.
For scoring the approximate algorithms, we will measure the maximal throughput that is attained, 
as long as the recall@10 is at least 90%.

## Dataset location and format:

The big-ann-package contains convenience functions for loading the data and ground truth files. 

The dataset, along with smaller versions for development (with their ground truth files) are located in the following location:

| Name          | Description                | download link                                                                                | #rows     | ground truth                                                                              | 
|:--------------|----------------------------|----------------------------------------------------------------------------------------------|-----------|-------------------------------------------------------------------------------------------|
| `full`        | Full base dataset          | [5.5 GB](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/base_full.csr.gz)   | 8,841,823 | [545K](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/base_full.dev.gt)  |
| `1M`          | 1M slice of base dataset   | [636.3 MB](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/base_1M.csr.gz)   | 1,000,000 | [545K](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/base_1M.dev.gt)    |
| `small`       | 100k slice of base dataset | [64.3 MB](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/base_small.csr.gz) | 100,000   | [545K](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/base_small.dev.gt) |
| `queries.dev` | queries file               | [1.8 MB](https://storage.googleapis.com/ann-challenge-sparse-vectors/csr/queries.dev.csr.gz) | 6,980     | N/A                                                                                       |

---

TODO: 

1. add results of baseline algorithm
2. 

Baseline algorithm
As a baseline algorithm, we propose a basic (but efficient) exact algorithm called linscan. It is based on an inverted index, and can be made faster (and less precise) with an early stopping condition. We (pinecone) can contribute an open source implementation.

Results of the baseline algorithm: 
Llinscan-anytime. Both single-thread and multi-thread:

TODO (plot throughput/recall). Extract max throughput at 90% recall.


Link to open source package (rust with python bindings):

TODO

