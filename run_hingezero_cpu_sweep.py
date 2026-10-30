"""Official OpenAI-100K HingeZero CPU throughput/recall sweep.

All 20,000 official public queries; exact supplied ground truth is used only
after each query batch completes. Never claim these are organizer-certified.
"""
from __future__ import annotations
import csv
import json
import os
from pathlib import Path
import time
import traceback

import h5py
import numpy as np

from benchmark.algorithms.definitions import get_definitions
from benchmark.datasets import DATASETS
from benchmark.plotting.metrics import get_recall_values
from benchmark.results import get_result_filename
from benchmark.runner import run

DATASET = "openai-100K"
K = 10
OUT = Path("results/hingezero_cpu_sweep")
OUT.mkdir(parents=True, exist_ok=True)

# Label, native/FAISS CPU threads, IVF probes, initial candidates,
# expansion rounds, additional candidates per round, recurrent steps.
# The original zero-step/one-thread result (88.619%, 250.789 QPS)
# is deliberately not run again on this shared machine.
SWEEP = [
    ("t4_p16_c512", 4, 16, 512, 0, 0, 0),
    ("t4_p32_c512", 4, 32, 512, 0, 0, 0),
    ("t4_p48_c512", 4, 48, 512, 0, 0, 0),
    ("t4_p64_c512", 4, 64, 512, 0, 0, 0),
    ("t4_p64_c768", 4, 64, 768, 0, 0, 0),
    ("t4_p64_c1024", 4, 64, 1024, 0, 0, 0),
    ("t4_p96_c768", 4, 96, 768, 0, 0, 0),
    ("t4_p96_c1024", 4, 96, 1024, 0, 0, 0),
    ("t4_p128_c1024", 4, 128, 1024, 0, 0, 0),
    ("t4_p128_c1536", 4, 128, 1536, 0, 0, 0),
    ("t4_p192_c1536", 4, 192, 1536, 0, 0, 0),
    ("t4_p256_c2048", 4, 256, 2048, 0, 0, 0),
    ("t2_p64_c768", 2, 64, 768, 0, 0, 0),
    ("t2_p128_c1024", 2, 128, 1024, 0, 0, 0),
    ("t4_p64_c512_expand0", 4, 64, 512, 1, 256, 0),
    ("t4_p64_c512_expand2", 4, 64, 512, 1, 256, 2),
    ("t4_p64_c512_expand8", 4, 64, 512, 1, 256, 8),
]

def save(rows):
    (OUT / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    if rows:
        keys = sorted(set().union(*(set(row) for row in rows)))
        with (OUT / "summary.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)

ds = DATASETS[DATASET]()
assert (ds.nb, ds.nq, ds.d, ds.distance()) == (100000, 20000, 1536, "euclidean")
truth = ds.get_groundtruth()
definitions = get_definitions("hingezero_cpp_v3.yaml", ds.d, DATASET, ds.distance(), K)
base = next(x for x in definitions if x.algorithm == "hingezero_cpp_full_v3")
assert os.getenv("OMP_NUM_THREADS") == "4"
rows = []
for number, (label, threads, nprobe, candidates, rounds, extras, steps) in enumerate(SWEEP, 1):
    params = dict(base.arguments[1], threads=threads, batch_size=32,
                  mode=("zero_steps" if steps == 0 else "full"))
    query_args = dict(nprobe=nprobe, candidates=candidates,
                      expansion_candidates=extras, steps=steps, rounds=rounds,
                      batch_size=32, alpha=4.5, eps=0.1, lam=0.02,
                      commit_margin=0.1, route_mix=0.1, retention_mix=0.2)
    definition = base._replace(
        algorithm="hingezero_sweep_" + label,
        arguments=[base.arguments[0], params],
        query_argument_groups=[[query_args]])
    print(f"SWEEP_START {number}/{len(SWEEP)} {label}", flush=True)
    result = dict(label=label, threads=threads, nprobe=nprobe,
                  candidates=candidates, rounds=rounds,
                  expansion_candidates=extras, steps=steps, dataset=DATASET,
                  query_count=ds.nq, bank_count=ds.nb)
    try:
        start = time.perf_counter()
        run(definition, DATASET, K, 1, False)
        result_path = Path(get_result_filename(DATASET, K, definition, [query_args]) + ".hdf5")
        with h5py.File(result_path) as f:
            neighbors = f["neighbors"][:]
            attrs = dict(f.attrs)
        assert neighbors.shape == (ds.nq, K), neighbors.shape
        assert np.all((neighbors >= 0) & (neighbors < ds.nb))
        recall, _, _, ties = get_recall_values(truth, neighbors, K)
        seconds = float(attrs["best_search_time"])
        result.update(
            status="success",
            recall_at_10=float(recall),
            qps=float(ds.nq / seconds),
            search_seconds=seconds,
            wall_seconds=float(time.perf_counter() - start),
            failures=int(attrs.get("failed_checks", -1)),
            seed_regressions=int(attrs.get("seed_score_regressions", -1)),
            measured_steps=int(attrs.get("hz_steps", -1)),
            measured_rounds=int(attrs.get("hz_rounds", -1)),
            native_threads=int(attrs.get("native_threads", -1)),
            ties=int(ties),
            result_file=str(result_path))
        assert result["failures"] == 0 and result["seed_regressions"] == 0
        assert result["measured_steps"] == steps and result["native_threads"] == threads
    except Exception as e:
        result.update(status="failed", error=repr(e))
        traceback.print_exc()
    rows.append(result)
    save(rows)
    print("HINGEZERO_SWEEP_RESULT " + json.dumps(result, sort_keys=True), flush=True)

valid = [r for r in rows if r["status"] == "success"]
eligible = [r for r in valid if r["recall_at_10"] >= 0.90]
best = max(eligible, key=lambda r: r["qps"]) if eligible else (
    max(valid, key=lambda r: (r["recall_at_10"], r["qps"])) if valid else None)
print("HINGEZERO_SWEEP_BEST " + json.dumps(
    dict(target_met=bool(eligible), best=best, succeeded=len(valid), total=len(rows)),
    sort_keys=True), flush=True)
if not valid:
    raise SystemExit("All configurations failed")
