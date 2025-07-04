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
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

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

def build_inverted_index(path: Path):
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

def worker_task(args):
    slice_data, = args
    kept_i, kept_l, kept_s = [], [], []
    inv_local = worker_task.inv
    total_base = worker_task.total_base
    min_sel, max_sel = worker_task.min_sel, worker_task.max_sel

    for qidx, raw in slice_data:
        # split labels
        labs = [lab for lab in raw.replace("&", ",").split(",") if lab]
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

def main():
    args = parse_args()
    random.seed(args.rand_seed)
    start_all = time.time()

    # Build index
    inv, total_base = build_inverted_index(args.base_label_file)

    # share these with workers via attributes (copy-on-write on fork)
    worker_task.inv        = inv
    worker_task.total_base = total_base
    worker_task.min_sel    = args.min_selectivity
    worker_task.max_sel    = args.max_selectivity

    # Load all queries into memory
    print("Loading all query labels into RAM …")
    with args.query_label_file.open() as f:
        all_lines = [(i, line.strip()) for i, line in enumerate(f) if line.strip()]

    n = len(all_lines)
    print(f"  {n:,} non-empty queries loaded   [{time.time()-start_all:.2f}s]")

    # Split into chunks for workers
    workers = args.workers or None
    if workers is None:
        import multiprocessing
        workers = multiprocessing.cpu_count()
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

    # Write labels
    t2 = time.time()
    args.out_label_file.write_text("".join(kept_lines[i] for i in picked))
    print(f"Labels written   [{time.time()-t2:.2f}s]")

    # Write vectors in bulk
    t3 = time.time()
    with args.query_vec_file.open("rb") as f:
        num_pts = int(np.fromfile(f, dtype=np.uint32, count=1)[0])
        num_dim = int(np.fromfile(f, dtype=np.uint32, count=1)[0])

    # Support uint8 and float32
    if args.vec_dtype == "uint8":
        dtype = np.uint8
    elif args.vec_dtype == "float32":
        dtype = np.float32
    else:
        raise ValueError(f"Unsupported dtype: {args.vec_dtype}")

    vecs = np.memmap(args.query_vec_file, dtype=dtype,
                     mode="r", offset=8, shape=(num_pts, num_dim))
    selected = vecs[global_rows]  # fancy-index all at once

    with args.out_vec_file.open("wb") as f:
        np.array([args.num_queries], dtype=np.uint32).tofile(f)
        np.array([num_dim],      dtype=np.uint32).tofile(f)
        selected.tofile(f)
    print(f"Vectors written   [{time.time()-t3:.2f}s]")

    print(f"Total runtime: {time.time()-start_all:.2f}s")

if __name__ == "__main__":
    main()
