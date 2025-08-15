#!/usr/bin/env python3
"""
filter_query_set_by_num_predicates.py

Keep only those queries whose number of predicates falls within the specified range.
Output:
 - a text file of the (possibly truncated) predicate lists per query
 - a binary .u8bin file containing the corresponding vectors
"""

import argparse
import sys
import numpy as np
from pathlib import Path
from filter_query_set_utils import write_filtered_labels, write_filtered_vectors, build_inverted_index, parse_query_labels

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query_label_file", type=Path, required=True,
                   help="Path to the text file with comma-/ampersand-separated labels for each query vector")
    p.add_argument("--query_vec_file",   type=Path, required=True,
                   help="Path to the binary .u8bin file containing query vectors")
    p.add_argument("--out_label_file",   type=Path, required=True,
                   help="Path to write the filtered label lines")
    p.add_argument("--out_vec_file",     type=Path, required=True,
                   help="Path to write the filtered vectors (.u8bin)")
    p.add_argument("--num_queries",      type=int, default=None,
                   help="Minimum number of queries to keep; warnning if fewer qualify")
    p.add_argument("--min_predicates",   type=int, default=1,
                   help="Keep queries with at least this many predicates")
    p.add_argument("--max_predicates",   type=int, default=None,
                   help="Keep queries with at most this many predicates (optional)")
    p.add_argument("--pick_from_first",  action="store_true",
                   help="If a query has > max_predicates and this flag is set, truncate to the first max_predicates")
    p.add_argument("--log_every",        type=int, default=10_000,
                   help="Log progress every N queries (default: 10000)")
    p.add_argument("--vec_dtype", type=str, default="uint8",
                   choices=["uint8", "float32"],
                   help="Data type of query vectors: uint8 or float32 (default: uint8)")
    return p.parse_args()

def filter_queries_by_predicate_count(args):
    """Filter queries based on the number of predicates they contain."""
    keep_idx = []
    keep_lines = []

    print(f"Scanning queries (keep predicates in "
          f"[{args.min_predicates}, {args.max_predicates if args.max_predicates is not None else '∞'}]) …")

    with args.query_label_file.open() as fin:
        for qidx, raw in enumerate(fin):
            line = raw.strip()
            if not line:
                continue
            if (qidx + 1) % args.log_every == 0:
                print(f"  processed {qidx+1:>11} queries")

            # normalize separators & count predicates
            preds = parse_query_labels(line)
            count = len(preds)

            # decide whether to keep
            if args.max_predicates is not None:
                in_range = args.min_predicates <= count <= args.max_predicates
            else:
                in_range = count >= args.min_predicates

            too_many = (args.pick_from_first
                        and args.max_predicates is not None
                        and count > args.max_predicates
                        and count >= args.min_predicates)

            if in_range or too_many:
                if too_many:
                    preds = preds[: args.max_predicates]
                    out_line = ",".join(preds) + "\n"
                else:
                    out_line = line + "\n"

                keep_idx.append(qidx)
                keep_lines.append(out_line)

    print(f"Rows kept with ≥{args.min_predicates} predicates : "
          f"{len(keep_idx):>11}")
    
    return keep_idx, keep_lines

def validate_query_count(args, keep_idx):
    """Validate that we have enough queries and print status."""
    if args.num_queries is not None:
        if len(keep_idx) < args.num_queries:
            print(
                f"Warning: only {len(keep_idx)} rows satisfy ≥{args.min_predicates} predicates, "
                f"but --num-queries was {args.num_queries}. Outputting all available rows."
            )
        else:
            print(f"All kept ({len(keep_idx):,} rows) ≥ required {args.num_queries}.")
    else:
        print(f"All kept ({len(keep_idx):,} rows) (no --num-queries).")

def main():
    args = parse_args()
    keep_idx, keep_lines = filter_queries_by_predicate_count(args)
    validate_query_count(args, keep_idx)
    write_filtered_labels(args.out_label_file, keep_lines)
    write_filtered_vectors(args.query_vec_file, args.out_vec_file, keep_idx, args.vec_dtype)

if __name__ == "__main__":
    main()
