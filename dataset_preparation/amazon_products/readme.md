This dataset contains around 2M vectors for amazon products. 
The embeddings are generated using cohere-english-light model (https://huggingface.co/Cohere/Cohere-embed-english-light-v3.0)
The base text used for generating embeddings is title + description of products
The queries are modifications of randomly sampled products from the base: after sampling, we prompt GPT-3.5 to output a simple query phrase for which the product is a suitable result, and embed that phrase using the cohere model.
We also choose brands from the appropriate category of the query and provide them as OR filters. The item price of the sampled item is used as indicative for a PRICE range filter.
