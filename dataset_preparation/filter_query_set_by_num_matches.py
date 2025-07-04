#!/usr/bin/env python3
"""
filter_query_set_by_num_matches.py

Create a reduced query set that keeps ONLY those queries whose conjunctive labels return ≥ MIN_HITS base vectors.
Output:
 - a text file of the (possibly truncated) predicate lists per query
 - a binary .u8bin file containing the corresponding vectors
"""

import argparse
import re
import numpy as np
from collections import defaultdict
from pathlib import Path

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base_label_file",   type=Path, required=True,
                   help="Path to the text file of comma-separated labels for each base vector")
    p.add_argument("--query_label_file",  type=Path, required=True,
                   help="Path to the text file of comma/&-separated labels for each query vector")
    p.add_argument("--query_vec_file",    type=Path, required=True,
                   help="Path to the binary '.u8bin' file of query vectors")
    p.add_argument("--out_label_file",    type=Path, required=True,
                   help="Path to write the filtered label lines")
    p.add_argument("--out_vec_file",      type=Path, required=True,
                   help="Path to write the filtered vectors")
    p.add_argument("--min_hits",          type=int, default=10,
                   help="Minimum number of matches in the base set to keep a query (default: 10)")
    p.add_argument("--log_every",         type=int, default=10_000,
                   help="How often to print progress (default: 10000)")
    p.add_argument("--vec_dtype", type=str, default="uint8",
                   choices=["uint8", "float32"],
                   help="Data type of query vectors: uint8 or float32 (default: uint8)")
    return p.parse_args()

def build_inverted_index(path):
    inverted = defaultdict(set)
    print("Building inverted index over base corpus …")
    with path.open() as fin:
        for idx, line in enumerate(fin):
            line = line.strip()
            if not line:
                continue
            # split on commas here
            for lab in line.split(','):
                inverted[lab].add(idx)
    print(f"  indexed {idx+1:,} base vectors, {len(inverted):,} distinct labels")
    return inverted

def filter_queries(args, inverted):
    qualified_idx   = []
    qualified_lines = []

    print("Scanning queries and computing result sizes …")
    with args.query_label_file.open() as fin:
        for qidx, raw in enumerate(fin):
            raw = raw.strip()
            if not raw:
                continue
            if (qidx+1) % args.log_every == 0:
                print(f"  processed {qidx+1:,} queries")

            # parse query labels on BOTH ',' and '&'
            q_labels = set(re.split(r"[,&]", raw))

            # gather the posting‐sets
            postings = [inverted[l] for l in q_labels if l in inverted]
            if len(postings) < len(q_labels):
                hits = 0
            else:
                postings.sort(key=len)
                hits = len(set.intersection(*postings))

            if hits >= args.min_hits:
                qualified_idx.append(qidx)
                qualified_lines.append(raw + "\n")

    print(f"Total queries               : {qidx+1:,}")
    print(f"Queries with ≥{args.min_hits} hits : {len(qualified_idx):,}")
    return qualified_idx, qualified_lines

def write_filtered_labels(path, lines):
    print(f"Writing filtered labels → {path}")
    with path.open("w") as fout:
        fout.writelines(lines)

def write_filtered_vectors(args, qualified_idx):
    print(f"Writing filtered vectors → {args.out_vec_file}")
    # read header
    with args.query_vec_file.open("rb") as fin:
        num_points = int(np.fromfile(fin, dtype=np.uint32, count=1)[0])
        num_dims   = int(np.fromfile(fin, dtype=np.uint32, count=1)[0])
            
    # choose dtype
    if args.vec_dtype == "uint8":
        dtype = np.uint8
        offset = 8
        shape = (num_points, num_dims)
    elif args.vec_dtype == "float32":
        dtype = np.float32
        offset = 8
        shape = (num_points, num_dims)
    else:
        raise ValueError(f"Unsupported dtype: {args.vec_dtype}")
    
    # memory-map payload
    vecs = np.memmap(args.query_vec_file, dtype=dtype,
                     mode="r", offset=offset, shape=shape)
    
    selected = vecs[qualified_idx]

    # write new file with updated header
    with args.out_vec_file.open("wb") as fout:
        np.array([len(selected)], dtype=np.uint32).tofile(fout)
        np.array([num_dims],      dtype=np.uint32).tofile(fout)
        selected.tofile(fout)

    print("Done.")

def main():
    args = parse_args()
    inverted = build_inverted_index(args.base_label_file)
    qualified_idx, qualified_lines = filter_queries(args, inverted)
    write_filtered_labels(args.out_label_file, qualified_lines)
    write_filtered_vectors(args, qualified_idx)

if __name__ == "__main__":
    main()
