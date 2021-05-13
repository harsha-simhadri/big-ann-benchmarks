# The Facebook SimSearchNet++ dataset

SimSearchNet++ features are extracted from the images.  
In production, the features are used for image copy detection for integrity purposes. 
There is some detail in [this blog post](https://ai.facebook.com/blog/using-ai-to-detect-covid-19-misinformation-and-exploitative-content)

The SSN++ features are intially in 512 dimensions, L2-normalized and in floating-point. 
They are compared with a given threshold (squared L2 < 0.8) and images are deemed to match and input to further processing if the distance between images are below that threshold. 

## Data preparation

This dataset is built form public Instagram images from a variety of countries.
The SSN++ features extracted from the images have been de-duplicated. After deduplication about 1.17B vectors remain.

99% of the dataset is used for the database vectors. 

1% of the dataset is set apart for queries, experiments and PCA training.

### Selecting queries 

We randomly sample 3 sets of 1M vectors from the 1%: A, B and C. 

A are the candidate query vectors. 
We compute the exact range search matches of A into database B with threshold 0.8. 
This yields 124210 results, with a distance historgram that looks like: 

[]




### Compressing the dataset 

To make the dataset less bulky, the features have been reduced to 256 dimensions by PCA and encoded in uint8. 

This means that the comparison threshold is also adjusted to a squared L2 distance of **96237**. 



## License


