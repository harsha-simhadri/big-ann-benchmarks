# Query Set Filtering Tools

This repo contains three filtering tools designed to create reduced query sets based on different criteria. 

## Overview

1. **`filter_query_set_by_num_matches.py`** - Filters queries based on the number of matching base vectors
2. **`filter_query_set_by_num_predicates.py`** - Filters queries based on the number of predicates per query
3. **`filter_query_set_by_selectivity.py`** - Filters queries based on selectivity

All tools work with labeled vector datasets where:
- Base vectors have comma-separated labels
- Query vectors have comma/ampersand-separated predicate labels
- Vector data is stored in binary `.u8bin` or `.float32bin` format

All tools produce two output files:
1. **Label file** : Filtered predicate lists, one per line
2. **Vector file** : Binary file with filtered vectors in the same format as input

## Common Input Format

### Label Files
- **Base labels**: Text file with comma-separated labels per line (one line per base vector)
  ```
  label1,label2,label3
  ```

- **Query labels**: Text file with comma or ampersand-separated predicates per line (one line per query vector). **Note: it is _not_ exactly the same as the format for the filter competition dataset.**
  ```
  label1,label2
  label3&label4&label5
  ```

### Vector Files
Binary files with the following structure:
- Header: 8 bytes (2 × uint32)
  - First uint32: Number of vectors
  - Second uint32: Vector dimension
- Data: Vector data in specified format (uint8 or float32)

### Usage

#### 1: filter_query_set_by_num_matches.py
```bash
python filter_query_set_by_num_matches.py \
    --base_label_file base_labels.txt \
    --query_label_file query_labels.txt \
    --query_vec_file query_vectors.u8bin \
    --out_label_file filtered_labels.txt \
    --out_vec_file filtered_vectors.u8bin \
    --min_hits 10 \
    --vec_dtype uint8
```

### Parameters
- `--base_label_file`: Path to base vector labels (comma-separated)
- `--query_label_file`: Path to query vector labels (comma/ampersand-separated)
- `--query_vec_file`: Path to binary query vector file
- `--out_label_file`: Output path for filtered labels
- `--out_vec_file`: Output path for filtered vectors
- `--min_hits`: Minimum number of base vector matches required (default: 10)
- `--log_every`: Progress logging interval (default: 10,000)
- `--vec_dtype`: Vector data type - "uint8" or "float32" (default: "uint8")


#### 2: filter_query_set_by_num_predicates.py

```bash
python filter_query_set_by_num_predicates.py \
    --query_label_file query_labels.txt \
    --query_vec_file query_vectors.u8bin \
    --out_label_file filtered_labels.txt \
    --out_vec_file filtered_vectors.u8bin \
    --min_predicates 2 \
    --max_predicates 5 \
    --vec_dtype uint8
```

### Parameters
- `--query_label_file`: Path to query vector labels
- `--query_vec_file`: Path to binary query vector file
- `--out_label_file`: Output path for filtered labels
- `--out_vec_file`: Output path for filtered vectors
- `--num_queries`: Minimum number of queries to keep (warning if fewer qualify)
- `--min_predicates`: Minimum number of predicates per query (default: 1)
- `--max_predicates`: Maximum number of predicates per query (optional)
- `--pick_from_first`: If query has too many predicates, truncate to first N
- `--log_every`: Progress logging interval (default: 10,000)
- `--vec_dtype`: Vector data type - "uint8" or "float32" (default: "uint8")

#### 3: filter_query_set_by_selectivity.py

```bash
python filter_query_set_by_selectivity.py \
    --base_label_file base_labels.txt \
    --query_label_file query_labels.txt \
    --query_vec_file query_vectors.u8bin \
    --out_label_file filtered_labels.txt \
    --out_vec_file filtered_vectors.u8bin \
    --num_queries 10000 \
    --min_selectivity 0.001 \
    --max_selectivity 0.1 \
    --workers 4
```

### Parameters
- `--base_label_file`: Path to base vector labels
- `--query_label_file`: Path to query vector labels
- `--query_vec_file`: Path to binary query vector file
- `--out_label_file`: Output path for filtered labels
- `--out_vec_file`: Output path for filtered vectors
- `--num_queries`: Number of queries to output (default: 10,000)
- `--min_selectivity`: Minimum selectivity fraction (default: 0.0)
- `--max_selectivity`: Maximum selectivity fraction (default: 1.0)
- `--rand_seed`: Random seed for sampling (default: 42)
- `--log_every`: Progress logging interval (default: 5,000)
- `--workers`: Number of parallel workers (default: CPU count)
- `--vec_dtype`: Vector data type - "uint8" or "float32" (default: "uint8")







