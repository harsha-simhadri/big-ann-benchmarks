# Pinecone Streaming ANN algorithm

Our solution employs a two-stage retrieval strategy. 
In the initial phase, we use a variant of the DiskANN index for candidate generation to generate a set of k’ >> k 
results through an approximate scoring mechanism over uint8-quantized vectors, 
with accelerated SIMD-based distance calculation. 
The second-stage reranks the candidates using full-precision scoring to enhance the overall accuracy of retrieval. 
It is worth noting that the raw vectors used in the second stage are stored on SSD. 
As such, it is important to optimize the number of disk reads invoked by the reranking stage.