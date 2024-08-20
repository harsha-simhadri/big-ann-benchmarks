# Pinecone filter ANN algorithm

Our algorithm is based on the classical IVF architecture, where the data is first divided into geometrical clusters, 
combined with a metadata inverted index: for every metadata tag, we store a list of vectors with that tag.

Given a query, we first evaluate its level of selectivity (i.e., the count of vectors that pass the filter), 
and scan a varying number of clusters for that query. 
We efficiently scan only the relevant vectors based on the inverted index, so the number of operations is 
O(query selectivity) rather than O(# of vectors in the selected clusters). 
The intuition is that for wide queries, the closest vectors are in neighboring clusters, 
and for more selective queries there is a need to scan more clusters. 
Additionally, we make sure that a minimal number of relevant vectors have been scanned, 
to account for queries whose selectivity is less localized.

To accelerate the search, we pre-compute some of the intersections of the inverted lists (based on their size), 
and use AVX for efficient computation of distances. 
To optimize the hyperparameters on the public query set, we formalized the problem as a constrained convex 
optimization problem, assigning the optimal recall value for each selectivity bucket. 
For the most selective queries, it turns out that it is beneficial to simply scan all relevant vectors 
(and ignore the geometrical clustering).