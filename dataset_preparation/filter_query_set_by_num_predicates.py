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
import time
import numpy as np
from pathlib import Path

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

def main():
    args = parse_args()
    start_all = time.time()

    # Scan label file
    print(f"Scanning queries (keep predicates in "
          f"[{args.min_predicates}, {args.max_predicates if args.max_predicates is not None else '∞'}]) …")
    t_scan = time.time()

    keep_idx = []
    keep_lines = []

    with args.query_label_file.open() as fin:
        for qidx, raw in enumerate(fin):
            line = raw.strip()
            if not line:
                continue
            if (qidx + 1) % args.log_every == 0:
                print(f"  processed {qidx+1:>11} queries")

            # normalize separators & count predicates
            replaced = line.replace("&", ",")
            preds = [s for s in replaced.split(",") if s]
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
          f"{len(keep_idx):>11}   [{time.time() - t_scan:.2f}s]")

    # Enforce num_queries if specified
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

    # Write filtered label file
    t_label = time.time()
    print(f"Writing labels → {args.out_label_file}")
    with args.out_label_file.open("w") as fout:
        fout.writelines(keep_lines)
    print(f"Label file written   [{time.time() - t_label:.2f}s]\n")

    # Write filtered vector file
    t_vec = time.time()
    print(f"Writing vectors → {args.out_vec_file}")
    # read header (u32 little-endian)
    with args.query_vec_file.open("rb") as fin:
        num_pts = int(np.fromfile(fin, dtype=np.uint32, count=1)[0])
        num_dims = int(np.fromfile(fin, dtype=np.uint32, count=1)[0])
        
    # memmap body as uint8 or float32
    if args.vec_dtype == "uint8":
        dtype = np.uint8
    elif args.vec_dtype in ("float32", "float"):
        dtype = np.float32
    else:
        raise ValueError(f"Unsupported dtype: {args.vec_dtype}")

    vecs = np.memmap(
        args.query_vec_file,
        dtype=dtype,
        mode="r",
        offset=8,
        shape=(num_pts, num_dims),
    )

    # write new header + selected rows
    with args.out_vec_file.open("wb") as fout:
        # header
        np.array([len(keep_idx)], dtype=np.uint32).tofile(fout)
        np.array([num_dims],      dtype=np.uint32).tofile(fout)
        # data
        for row in keep_idx:
            fout.write(vecs[row].tobytes())

    print(f"Vector file written   [{time.time() - t_vec:.2f}s]")
    print(f"Total runtime: {time.time() - start_all:.2f}s")

if __name__ == "__main__":
    main()
