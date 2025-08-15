#!/usr/bin/env python3
"""
filter_query_set_by_num_matches.py

Create a reduced query set that keeps ONLY those queries whose conjunctive labels return ≥ MIN_HITS base vectors.
Output:
 - a text file of the (possibly truncated) predicate lists per query
 - a binary .u8bin file containing the corresponding vectors
"""

import argparse
import numpy as np
from pathlib import Path
from filter_query_set_utils import write_filtered_labels, write_filtered_vectors, build_inverted_index, parse_query_labels

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

def filter_queries(args, inverted):
    keep_idx   = []
    keep_lines = []

    print("Scanning queries and computing result sizes …")
    with args.query_label_file.open() as fin:
        for qidx, raw in enumerate(fin):
            raw = raw.strip()
            if not raw:
                continue
            if (qidx+1) % args.log_every == 0:
                print(f"  processed {qidx+1:,} queries")

            # parse query labels on BOTH ',' and '&'
            q_labels = set(parse_query_labels(raw))

            # gather the posting‐sets
            postings = [inverted[l] for l in q_labels if l in inverted]
            if len(postings) < len(q_labels):
                hits = 0
            else:
                postings.sort(key=len)
                hits = len(set.intersection(*postings))

            if hits >= args.min_hits:
                keep_idx.append(qidx)
                keep_lines.append(raw + "\n")

    print(f"Total queries               : {qidx+1:,}")
    print(f"Queries with ≥{args.min_hits} hits : {len(keep_idx):,}")
    return keep_idx, keep_lines

def main():
    args = parse_args()
    inverted, total_base = build_inverted_index(args.base_label_file)
    keep_idx, keep_lines = filter_queries(args, inverted)
    write_filtered_labels(args.out_label_file, keep_lines)
    write_filtered_vectors(args.query_vec_file, args.out_vec_file, keep_idx, args.vec_dtype)

if __name__ == "__main__":
    main()
