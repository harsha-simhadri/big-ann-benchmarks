# YFCC-Images Dataset

This file describes a new public vector benchmark based on the images from the widely used [YFCC-100M dataset](https://www.courtlistener.com/help/api/bulk-data). The image-subset of YFCC100M consists of 98.8 million valid images, with rich metadata scraped from the original submissions (e.g., image tags, country, camera make and model, licenses, etc.). Each image is embedded into a single 1280-dimensional vector using a [CLIP-based model](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k). 

This dataset is a larger version of the YFCC dataset released for the [NeurIPS 2023 Practical Vector Search Challenge](https://big-ann-benchmarks.com/neurips23.html), but lacks additional metadata needed for filtered search.


## License
The original dataset is licensed under various [Creative Commons Licenses](http://www.creativecommons.org/) that can be found in the metadata for each image, and the metadata is licensed under the Yahoo Webscope License (see [link](https://multimediacommons.wordpress.com/yfcc100m-core-dataset/)). 
This release does not repackage the original images or the metadata. The license of all embedding and auxiliary files in this release is [CDLA-2.0](https://cdla.dev/permissive-2-0/).

## Files and Format

The embeddings are released using the standard single-vector `fbin` binary format. The header is two `uint32` values describing the number of vectors `N` and dimensionality of the vectors `D`. The rest of the file is a large `N x D` `float32` matrix in row-major form, with one `D`-dimensional vector per row.

A total of 98.8M vectors were generated and were split into a base set with 98.7M vectors and a query set with 100k vectors. The base and query vectors can be downloaded using the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_vecs.fbin           # Base vectors (98.7M)
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_query_vecs.fbin     # Query vectors (100k)
```
This dataset release also comes with two subsets -- one with 1M vectors, and another with 10M vectors -- both randomly sampled from the 98.7M base vectors.

The subsets can be downloaded using the following URLs:
```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_vecs_sampled_1m.fbin    # 1M-subset
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_vecs_sampled_10m.fbin   # 10M-subset
```

Ground truth (top-100 nearest neighbors) for the query set is computed with respect to the full base set, as well as the 1M and 10M subsets using the L2 (Euclidean) distance function. Since the vectors are normalized to unit norm (i.e., $||v||_2 = 1$), the ground-truth remains unchanged when cosine or inner-product distance functions are used instead of the L2 distance function. Ground truth follows the standard format: (a) a header with two `uint32`s describing the number of query vectors (`N_q`) and the `k` value for top-`k` results, followed by (b)  `N_q x k` `uint32` values, where each `k` consecutive entries represent the ranked nearest neighbors' ids, and finally, (c) the `float32` distance values for use in tie-breaking. Ground truth (GT) for all three base vector sets can be downloaded using the folowing urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_query_gt100.bin                # GT for 98.7M base set
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_query_gt100_sampled_1m.bin     # GT for 1M subset
wget https://comp21storage.z5.web.core.windows.net/yfcc100m_images/yfcc100m_query_gt100_sampled_10m.bin    # GT for 10M subset
```

## Development

This section details the development of this dataset which may be useful for interpreting any results from the dataset.

### Dataset Download
The image subset of the dataset was downloaded using the [`yfcc100m`](https://pypi.org/project/yfcc100m/) Python library, totaling about 13TB in size. Images are assigned an ID sequentially from `0 - N` in the order the sub-folders were processed (i.e., no definite ordering between images/vectors). 

### Embedding Generation
Each image is decoded using PIL, then converted to RGB tensor using `torchvision.io.decode_image`, then passed through the following transform:
```python
transform_for_tensor = v2.Compose([
        v2.Resize(size=224, interpolation=v2.InterpolationMode.BICUBIC, antialias=True),
        v2.CenterCrop(size=(224, 224)),
        v2.ToDtype(torch.float32, scale=True),  # Normalize to [0, 1]
        v2.Normalize(mean=[0.48145466, 0.4578275, 0.40821073], 
                     std=[0.26862954, 0.26130258, 0.27577711])
    ])
```
Finally, the image was embedded using `open_clip` library with `hf-hub:laion/CLIP-ViT-bigG-14-laion2B-39B-b160k` model running in FP16 mode and the resulting embedding vector is normalized to unit norm. The output is a 1280-dimensional float32 vector for each image that was successfully embedded.

### Notes
Some images failed to embed because of multiple reasons: (a) the original media files were corrupted during the download, or (b) the image failed to decode. We also omitted all images that were present in the YFCC metadata, but were later taken down by their authors.