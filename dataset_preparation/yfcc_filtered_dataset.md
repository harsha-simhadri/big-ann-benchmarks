# YFCC Dataset Supplemental Filters and Groundtruth

This document details the design and download instructions for a supplemental set of metadata filters and filtered groundtruth for the YFCC dataset of 10 million CLIP descriptors of images used in the NeurIPS'23 filtered search competition. While the competition dataset used labels describing the contents of the images, this set of metadata and filters is limited to four components: "year", "month", "camera", and "country." The filter predicates are a mix of equality on a single label and a logical AND of equality on two labels.

The base and query vectors with non-filtered groundtruth can be downloaded using `create_dataset` utility in the main repository:

```bash
python3.10 create_dataset.py --dataset yfcc-10M
```

They can also be downloaded, along with a million-sized slice and groundtruth, from the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/base.10M.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/base.1M.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/query.public.100K.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/groundtruth.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/groundtruth_1M.bin
```

The filter metadata, query filters, and filtered groundtruth can be downloaded from the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/base.10M.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/base.1M.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/query.public.100K.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/groundtruth_filtered.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/groundtruth_filtered_1M.bin
```

For convenience, we have also produced five subsets of the query filters of size 10K, which are separated by both match rate and filter type (single predicate or AND of two predicates). The filter and query files for these subsets, along with groundtruth with respect to the 1M and 10M slices of YFCC, are found below.

Single filters, match rate range .0001-.001:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-low/query_10k.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-low/query_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-low/GT.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-low/GT_1M.bin
```

Single filters, match rate range .005-.036:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-medium/query_10k.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-medium/query_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-medium/GT.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-medium/GT_1M.bin
```

Single filters, match rate range .11-.34:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-high/query_10k.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-high/query_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-high/GT.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/single-high/GT_1M.bin
```

Two filters, match rate range .0001-.001:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-low/query_10k.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-low/query_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-low/GT.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-low/GT_1M.bin
```

Two filters, match rate range .006-.05:

```bash
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-medium/query_10k.u8bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-medium/query_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-medium/GT.bin
wget https://comp21storage.z5.web.core.windows.net/yfcc/multiple-medium/GT_1M.bin
```

The license of the original images used in this dataset is mix of [CC {BY, BY-SA, BY-ND, BY-NC, NY-NC-SA, BY-NC-ND}](https://code.flickr.net/2014/10/15/the-ins-and-outs-of-the-yahoo-flickr-100-million-creative-commons-dataset/). This additional processed metadata and groundtruth are released under the same license as the image they represent.



