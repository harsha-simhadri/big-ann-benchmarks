#!/usr/bin/env python3
"""
filter_query_set_by_selectivity.py

Keep only those queries whose selectivity falls within the specified range.
Output:
 - a text file of the (possibly truncated) predicate lists per query
 - a binary .u8bin file containing the corresponding vectors
"""



import sys
import argparse
import time
import random
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from filter_query_set_utils import write_filtered_labels, write_filtered_vectors, build_inverted_index, parse_query_labels

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base_label_file",  type=Path, required=True,
                   help="Path to the text file of comma-separated labels for each base vector")
    p.add_argument("--query_label_file", type=Path, required=True,
                   help="Path to the text file of comma/&-separated labels for each query vector")
    p.add_argument("--query_vec_file",   type=Path, required=True,
                   help="Path to the binary '.u8bin' file of query vectors")
    p.add_argument("--out_label_file",   type=Path, required=True,
                   help="Path to write the filtered label lines")
    p.add_argument("--out_vec_file",     type=Path, required=True,
                   help="Path to write the filtered vectors")
    p.add_argument("--num_queries",      type=int,   default=10_000,
                   help="Number of queries to output (default: 10000)")
    p.add_argument("--min_selectivity",  type=float, default=0.0,
                   help="Minimum selectivity (fraction of base vectors matched) to keep a query (default: 0.0)")
    p.add_argument("--max_selectivity",  type=float, default=1.0,
                   help="Maximum selectivity (fraction of base vectors matched) to keep a query (default: 1.0)")
    p.add_argument("--rand_seed",        type=int,   default=42,
                   help="Random seed for sampling (default: 42)")
    p.add_argument("--log_every",        type=int,   default=5_000,
                   help="How often to print progress (default: 5000)")
    p.add_argument("--workers",          type=int,   default=None,
                   help="Number of parallel workers (default: CPU count)")
    p.add_argument("--vec_dtype", type=str, default="uint8",
                   choices=["uint8", "float32"],
                   help="Data type of query vectors: uint8 or float32 (default: uint8)")
    return p.parse_args()

def worker_task(args):
    slice_data, = args
    kept_i, kept_l, kept_s = [], [], []
    inv_local = worker_task.inv
    total_base = worker_task.total_base
    min_sel, max_sel = worker_task.min_sel, worker_task.max_sel

    for qidx, raw in slice_data:
        # split labels
        labs = parse_query_labels(raw)
        # gather postings, bail on missing
        try:
            posts = [inv_local[lab] for lab in labs]
        except KeyError:
            continue

        hits = len(set.intersection(*posts))
        if hits == 0:
            continue

        frac = hits / total_base
        if min_sel <= frac <= max_sel:
            kept_i.append(qidx)
            kept_l.append(raw + "\n")
            kept_s.append(frac)

    return kept_i, kept_l, kept_s

def load_query_labels(args):
    """Load all query labels into memory."""
    print("Loading all query labels into RAM …")
    with args.query_label_file.open() as f:
        all_lines = [(i, line.strip()) for i, line in enumerate(f) if line.strip()]
    
    n = len(all_lines)
    print(f"  {n:,} non-empty queries loaded")
    return all_lines

def filter_queries_by_selectivity(args, inv, total_base, all_lines):
    """Filter queries based on their selectivity using parallel processing."""
    # share these with workers via attributes (copy-on-write on fork)
    worker_task.inv        = inv
    worker_task.total_base = total_base
    worker_task.min_sel    = args.min_selectivity
    worker_task.max_sel    = args.max_selectivity

    # Split into chunks for workers
    workers = args.workers or None
    if workers is None:
        import multiprocessing
        workers = multiprocessing.cpu_count()
    
    n = len(all_lines)
    chunk_size = (n + workers - 1) // workers
    chunks = [all_lines[i : i + chunk_size] for i in range(0, n, chunk_size)]

    # Parallel filtering
    print(f"Filtering in parallel on {workers} workers …")
    kept_idx, kept_lines, sel_stats = [], [], []
    t1 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as exe:
        # map each chunk to a worker
        for ki, kl, ks in exe.map(worker_task, [(chunk,) for chunk in chunks]):
            kept_idx.extend(ki)
            kept_lines.extend(kl)
            sel_stats.extend(ks)
    print(f"  Qualified {len(kept_idx):,} queries   [{time.time()-t1:.2f}s]")
    
    return kept_idx, kept_lines, sel_stats

def sample_qualified_queries(args, kept_idx, kept_lines, sel_stats):
    """Sample the required number of queries from qualified ones."""
    # check qualify
    if len(kept_idx) < args.num_queries:
        sys.exit(f"Need {args.num_queries}, but only {len(kept_idx)} qualify.")

    if len(kept_idx) < args.num_queries:
        print(f"Warning: Need {args.num_queries}, but only {len(kept_idx)} qualify. Outputting all qualified queries.")
        picked = list(range(len(kept_idx)))
        global_rows = [kept_idx[i] for i in picked]
    else: #Sample exactly N
        order = list(range(len(kept_idx)))
        random.shuffle(order)
        picked = order[: args.num_queries]
        global_rows = [kept_idx[i] for i in picked]

    mn = min(sel_stats); mean = sum(sel_stats)/len(sel_stats); mx = max(sel_stats)
    print(f"Selected {args.num_queries} queries   (min/mean/max sel = "
          f"{mn:.6f}/{mean:.6f}/{mx:.6f})")
    
    return picked, global_rows

def main():
    args = parse_args()
    random.seed(args.rand_seed)
    start_time = time.time()
    inv, total_base = build_inverted_index(args.base_label_file)
    all_lines = load_query_labels(args)
    kept_idx, kept_lines, sel_stats = filter_queries_by_selectivity(args, inv, total_base, all_lines)
    picked, global_rows = sample_qualified_queries(args, kept_idx, kept_lines, sel_stats)
    keep_lines_all = [kept_lines[i] for i in picked]
    write_filtered_labels(args.out_label_file, keep_lines_all)
    write_filtered_vectors(args.query_vec_file, args.out_vec_file, global_rows, args.vec_dtype)
    end_time = time.time()
    print(f"Total runtime: {end_time - start_time:.2f}s")

if __name__ == "__main__":
    main()
