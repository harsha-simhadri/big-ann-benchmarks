# DINO Dataset

This file describes a public dense-vector benchmark of 1024-dimensional `uint8`
vectors extracted from image patches in the
[YFCC100M dataset](https://multimediacommons.wordpress.com/yfcc100m-core-dataset/)
using a [DINOv3 ViT-L/16 model](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m).

The full corpus contains 10 billion vectors, making it one of the largest
publicly available dense-vector benchmarks for approximate nearest neighbor
search. Within this framework we expose **subsets of up to 2 billion vectors**
(`dino-1M` … `dino-2B`). 2B is the largest size whose vector count still fits
the 32-bit header of the competition `.u8bin` format (max ≈ 4.29B).


## License

The original YFCC100M images are licensed under various
[Creative Commons Licenses](http://www.creativecommons.org/) (see the metadata
for each image). The embedding vectors and auxiliary files are released by Meta
under the [Creative Commons Attribution-NonCommercial 4.0 (CC BY-NC) license](https://creativecommons.org/licenses/by-nc/4.0/).


## Dataset Properties

| Property | Value |
|----------|-------|
| Base vectors | up to 2,000,000,000 (2B) in this framework (10B corpus available) |
| Dimensions | 1024 |
| Data type | uint8 |
| Query vectors | 100,000 |
| Training vectors | 99,000,000 |
| Distance metric | L2 (Euclidean) |
| Ground truth | Top-100 nearest neighbors |


## Using the dataset in this framework

The dataset is registered in `benchmark/datasets.py` as `DINO10BDataset`
(a subclass of `BillionScaleDatasetCompetitionFormat`). Prepare a size with:

```bash
python create_dataset.py --dataset dino-1M       # base + queries + ground truth
python create_dataset.py --dataset dino-1M --skip-data   # queries + ground truth only
```

Registered sizes:

| name | base vectors | source file | download |
|------|--------------|-------------|----------|
| `dino-100K` | 100,000       | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-200K` | 200,000       | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-500K` | 500,000       | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-1M`   | 1,000,000     | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-5M`   | 5,000,000     | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-10M`  | 10,000,000    | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-20M`  | 20,000,000    | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-50M`  | 50,000,000    | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-100M` | 100,000,000   | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-200M` | 200,000,000   | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-500M` | 500,000,000   | `dino_vitl_1B_base.u8bin` | first-N prefix (cropped) |
| `dino-1B`   | 1,000,000,000 | `dino_vitl_1B_base.u8bin` | full file (accelerated) |
| `dino-2B`   | 2,000,000,000 | `dino_vitl_2B_base.u8bin` | full file (accelerated) |

For every size below 1B, only the **first N vectors** of the 1B file are
downloaded (an 8-byte header plus `N × 1024` bytes), and the header's vector
count is rewritten to N. This means a researcher on a small machine never has
to fetch the whole 1B file — e.g. `dino-1M` downloads ~1 GB rather than ~1 TB.
Sizes of exactly 1B or 2B download the corresponding complete file with the
[Axel download accelerator](https://github.com/axel-download-accelerator/axel)
(`axel`), so make sure it is on your `PATH` for those sizes.


## Sizes beyond 2B (5B and 10B)

This framework intentionally stops at **2B**. The competition ground-truth format
stores neighbor indices as `int32`, whose maximum value (≈ 2.147B) cannot address a
5B or 10B database, and the `.u8bin` base header is a single `uint32` (max ≈ 4.29B).
So the 5B and 10B subsets cannot be represented in the competition `.bin`/`.u8bin`
files, and no loader is provided for them here (the `gts_bin/` `.bin` ground truth is
published only for sizes ≤ 2B).

The **full 10B corpus is still available** and can be used directly through the
[faiss](https://github.com/facebookresearch/faiss) library, whose dataset class reads
the chunked base and `int64` ground truth, so 5B/10B neighbor IDs are represented
correctly:

- faiss `contrib/datasets.py` → `DatasetDINO10B` (supports 100K … 10B).

It streams the base from the chunked `.bvecs` files under
`dino_vitl_10B/chunked_base_10B/chunk_*.bvecs` and reads ground truth from the `int64`
`.npy` files under `dino_vitl_10B/gts/gts_dino_patch_<nb>_k10.npy` (rather than the
`gts_bin/` `.bin` files this framework uses). Ground truth on that path is top-10 (k ≤ 10).


## Files and Format

All files live under
`http://dl.fbaipublicfiles.com/large_objects/dino_vitl_10B/`.

**Base vectors** use the competition `.u8bin` format: an 8-byte header of two
little-endian `uint32` values (`n`, `d`), followed by `n × d` `uint8` bytes
(row-major). The two published files are:

```bash
# 1B vectors  (header [1000000000, 1024]; ~1 TB)
wget http://dl.fbaipublicfiles.com/large_objects/dino_vitl_10B/dino_vitl_1B_base.u8bin
# 2B vectors  (header [2000000000, 1024]; ~2 TB)
wget http://dl.fbaipublicfiles.com/large_objects/dino_vitl_10B/dino_vitl_2B_base.u8bin
```

**Queries** use the `.bvecs` format (each vector is a 4-byte little-endian
`int32` dimension followed by `d` `uint8` bytes). There are 100,000 queries,
shared across all sizes:

```bash
wget http://dl.fbaipublicfiles.com/large_objects/dino_vitl_10B/queries_clean.bvecs
```

**Ground truth** is pre-computed per size (always the first N vectors of the
corpus). Files use the standard competition KNN format: a header of two
`uint32` values (`nq`, `k`), then `nq × k` `int32` neighbor indices, then
`nq × k` `float32` (squared) L2 distances. Each file has 100,000 queries × 100 neighbors:

```bash
wget http://dl.fbaipublicfiles.com/large_objects/dino_vitl_10B/gts_bin/gts_dino_patch_{nb}_k100.bin
# e.g. nb = 1000000, 200000000, 1000000000, 2000000000, ...
```

Ground-truth files are available for: 100K, 200K, 500K, 1M, 5M, 10M, 20M, 50M,
100M, 200M, 500M, 1B, and 2B.


## Development

### Embedding Generation

Image patches from the YFCC100M dataset were processed through a DINOv3
ViT-L/16 model
([facebook/dinov3-vitl16-pretrain-lvd1689m](https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m)).
The resulting embeddings were quantized to `uint8` and stored in the `.u8bin`
competition format.

### Training Set

A training set
([`train_queries_99M.bvecs`](http://dl.fbaipublicfiles.com/large_objects/dino_vitl_10B/train_queries_99M.bvecs),
~100 GB) containing 99 million vectors is available for training quantizers or
other index structures.
