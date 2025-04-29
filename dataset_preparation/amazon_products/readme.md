Amazon Automotive Dataset For Filtered ANN

Model details:

This dataset contains around 2M vectors for amazon products. 
The embeddings are generated using cohere-english-light model (https://huggingface.co/Cohere/Cohere-embed-english-light-v3.0)
The base text used for generating embeddings is title + description of products
The queries are modifications of randomly sampled products from the base: after sampling, we prompt GPT-3.5 to output a simple query phrase for which the product is a suitable result, and embed that phrase using the cohere model.
We also choose appropriate category of the query and provide them as filter. The desired rating is also used as a filter.


Dataset details:

The base vector file contains 2000640 vectors in 384 dimensions, fp32 values.
The query vector file contains 7119 query vectors.

The base label file contains 2000640 rows, one row per vector. The row contains all the labels associated with the corresponding vector as "KEY=VALUE" entries in a comma-separated list.
For example, the first vector has the following attribute meta-data based on which one can filter:
BRAND=Caltric,CAT=Automotive,CAT=MotorcyclePowersports,CAT=Parts,CAT=Filters,CAT=OilFilters,RATING=5

Here there are 3 keys, BRAND, CAT (for category), and RATING.
The product has 1 brand, many categories, and one rating value.

The query label file has one row per query, specifying the filtering predicate. We write it as an AND of ORs.
CAT=ExteriorAccessories
CAT=ExteriorAccessories&&RATING=4||RATING=5
CAT=ExteriorAccessories&&RATING=5
CAT=BumperStickersDecalsMagnets

In the second example above, we want top K vectors among all those which have CAT=ExteriorAccessories and the RATING must be 4 or 5.

The files are here:
base vectors: https://comp21storage.blob.core.windows.net/$web/amazon-automotive/amazon_base.fbin
base labels: https://comp21storage.blob.core.windows.net/$web/amazon-automotive/amazon_base_labels.txt
query vectors: https://comp21storage.blob.core.windows.net/$web/amazon-automotive/amazon_query.fbin
query labels: https://comp21storage.blob.core.windows.net/$web/amazon-automotive/amazon_query_labels.txt
