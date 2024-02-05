# Pinecone OOD ANN algorithm

Our solution for the OOD track is based on three main components – 
an inverted-file (IVF) index on the vector collection using a clustering algorithm tailored for inner-product search, 
a k-MIP (max inner product) graph constructed using the co-occurence of vectors as nearest neighbors for a set of 
training queries, and, quantization tailored for SIMD-based acceleration for fast scoring and retrieval.

We perform retrieval in three stages. 
First, we retrieve a small number of candidates from top clusters by scoring quantized vectors. 
Next, we use the k-MIP graph to “expand” the set of retrieved candidates by adding their neighbors 
in the graph to the candidate set. 
Finally, we score all the candidates by computing their distance to the query using a 
fine-grained quantized representation of the vectors. 
In addition, in order to accelerate the search, we process the queries in a batch to take advantage of cache locality.