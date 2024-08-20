# Pinecone Sparse ANN algorithm

Our algorithm for the Sparse track is based on our very own research [[1](https://dl.acm.org/doi/10.1145/3609797), [2](https://arxiv.org/abs/2309.09013)]. 
In particular, we cluster sparse vectors, build an inverted index that is organized using our [novel structure](https://arxiv.org/abs/2309.09013)
 and query the index by first solving the top cluster retrieval problem, then finding the top-k vectors within those clusters using an anytime retrieval algorithm over the inverted index.

We also augment the index above with two additional lightweight components. 
First, we use a k-MIP graph (where every vector is connected to k other vectors that maximize inner product with it) 
to “expand” the set of retrieved top-k vectors from the last step. 
Second, we re-rank the expanded set using a compressed forward index. 
In effect, our final solution is a hybrid of IVF- and graph-based methods, 
where the IVF stage provides a set of entry nodes into the graph.