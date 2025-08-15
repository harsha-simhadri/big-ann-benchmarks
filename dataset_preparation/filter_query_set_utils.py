#!/usr/bin/env python3
"""
filter_utils.py

Utility functions for generating filter query sets.
"""

import numpy as np
import time
from pathlib import Path
from collections import defaultdict

def write_filtered_labels(path, lines):
    """Write filtered label lines to a file.
    
    Args:
        path: Path object for the output label file
        lines: List of label lines to write (should include newlines)
    """
    print(f"Writing filtered labels → {path}")
    with path.open("w") as fout:
        fout.writelines(lines)
    print("Writing filtered labels Done.")

def write_filtered_vectors(query_vec_file, out_vec_file, qualified_idx, vec_dtype="uint8"):
    """Write filtered vectors to a binary file.
    
    Args:
        query_vec_file: Path to the input binary vector file
        out_vec_file: Path to the output binary vector file
        qualified_idx: List of indices of vectors to keep
        vec_dtype: Data type of vectors ("uint8" or "float32")
    """
    print(f"Writing filtered vectors → {out_vec_file}")
    
    # read header
    with query_vec_file.open("rb") as fin:
        num_points = int(np.fromfile(fin, dtype=np.uint32, count=1)[0])
        num_dims = int(np.fromfile(fin, dtype=np.uint32, count=1)[0])
    
    # choose dtype
    if vec_dtype == "uint8":
        dtype = np.uint8
    elif vec_dtype == "float32":
        dtype = np.float32
    else:
        raise ValueError(f"Unsupported dtype: {vec_dtype}")
    
    # memory-map payload
    vecs = np.memmap(query_vec_file, dtype=dtype,
                     mode="r", offset=8, shape=(num_points, num_dims))
    
    selected = vecs[qualified_idx]
    
    # write new file with updated header
    with out_vec_file.open("wb") as fout:
        np.array([len(selected)], dtype=np.uint32).tofile(fout)
        np.array([num_dims], dtype=np.uint32).tofile(fout)
        selected.tofile(fout)
    
    print("Writing filtered vectors Done.")

def build_inverted_index(path: Path):
    """Build an inverted index from a base label file.
    
    Args:
        path: Path to the text file of comma-separated labels for each base vector
        
    Returns:
        tuple: (inverted_index, total_count) where inverted_index is a dict mapping 
               labels to sets of vector indices, and total_count is the number of base vectors
    """
    inv = defaultdict(set)
    total = 0
    t0 = time.time()
    with path.open() as f:
        for idx, line in enumerate(f):
            lbls = line.strip()
            if not lbls:
                continue
            total += 1
            # Rust splits only on commas here
            for lab in lbls.split(","):
                inv[lab].add(idx)
    print(f"Indexed {total:>11} base vectors, {len(inv):>11} distinct labels   [{time.time()-t0:.2f}s]")
    return inv, total

def parse_query_labels(raw_line):
    """Parse query labels from a raw line, handling both ',' and '&' separators.
    
    Args:
        raw_line: Raw line from query file (should be stripped)
        
    Returns:
        list: List of non-empty labels
    """
    return [lab for lab in raw_line.replace("&", ",").split(",") if lab]
