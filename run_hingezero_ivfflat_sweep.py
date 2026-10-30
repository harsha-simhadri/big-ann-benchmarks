"""Fair full-corpus IVF-Flat + HingeZero zero-step benchmark on OpenAI-100K."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import traceback

import h5py
import numpy as np

from benchmark.algorithms.definitions import get_definitions
from benchmark.datasets import DATASETS
from benchmark.plotting.metrics import get_recall_values
from benchmark.results import get_result_filename
from benchmark.runner import run

DATASET = "openai-100K"
OUT = Path("results/hz_ivfflat_sweep")
OUT.mkdir(parents=True, exist_ok=True)

# nlist, number of index-training points, nprobe, seed candidates, threads
GRID = [
    (512, 20000, 8, 256, 4),
    (512, 20000, 16, 512, 4),
    (512, 20000, 32, 512, 4),
    (512, 20000, 48, 768, 4),
    (512, 20000, 64, 1024, 4),
    (1024, 40000, 8, 256, 4),
    (1024, 40000, 16, 512, 4),
    (1024, 40000, 32, 512, 4),
    (1024, 40000, 48, 768, 4),
    (1024, 40000, 64, 1024, 4),
    (1024, 40000, 96, 1024, 4),
]
ds = DATASETS[DATASET]()
assert ds.nb == 100000 and ds.nq == 20000 and ds.d == 1536
truth = ds.get_groundtruth()
base = next(x for x in get_definitions(
    "hingezero_cpp_v3.yaml", ds.d, DATASET, ds.distance(), 10
) if x.algorithm == "hingezero_cpp_full_v3")

def save(rows):
    (OUT / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    if rows:
        keys = sorted(set().union(*(r.keys() for r in rows)))
        with (OUT / "summary.csv").open("w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rows)

rows = []
for i, (nlist, train_size, probe, candidates, threads) in enumerate(GRID, 1):
    label = f"ivfflat_n{nlist}_p{probe}_c{candidates}_t{threads}"
    build_args = dict(base.arguments[1], nlist=nlist, train_size=train_size,
                      threads=threads, mode="zero_steps", batch_size=32)
    query_args = dict(nprobe=probe, candidates=candidates, expansion_candidates=0,
                      steps=0, rounds=0, batch_size=32, alpha=4.5, eps=0.1,
                      lam=0.02, commit_margin=0.1, route_mix=0.1, retention_mix=0.2)
    definition = base._replace(
        algorithm="hz_" + label,
        module="benchmark.algorithms.hingezero_cpp_v3.ivfflat",
        constructor="HingeZeroCppIVFFlat",
        arguments=[base.arguments[0], build_args],
        query_argument_groups=[[query_args]])
    result = dict(label=label, nlist=nlist, nprobe=probe, train_size=train_size,
                  candidates=candidates, threads=threads, hz_steps=0, rounds=0,
                  bank_count=ds.nb, query_count=ds.nq, dataset=DATASET)
    print(f"IVFFLAT_START {i}/{len(GRID)} {label}", flush=True)
    try:
        run(definition, DATASET, 10, 1, False)
        result_path = Path(get_result_filename(DATASET, 10, definition, [query_args])+".hdf5")
        with h5py.File(result_path) as file:
            neighbors = file["neighbors"][:]
            attrs = dict(file.attrs)
        assert neighbors.shape == (ds.nq, 10)
        assert np.all((neighbors >= 0) & (neighbors < ds.nb))
        recall, _, _, ties = get_recall_values(truth, neighbors, 10)
        seconds = float(attrs["best_search_time"])
        result.update(status="success", recall_at_10=float(recall), qps=ds.nq/seconds,
                      search_seconds=seconds, failures=int(attrs.get("failed_checks", -1)),
                      seed_regressions=int(attrs.get("seed_score_regressions", -1)),
                      measured_steps=int(attrs.get("hz_steps", -1)),
                      native_threads=int(attrs.get("native_threads", -1)),
                      result_file=str(result_path), ties=int(ties))
        assert result["failures"] == 0 and result["seed_regressions"] == 0
        assert result["native_threads"] == threads and result["measured_steps"] == 0
    except Exception as exc:
        result.update(status="failed", error=repr(exc))
        traceback.print_exc()
    rows.append(result)
    save(rows)
    print("HINGEZERO_IVFFLAT_RESULT "+json.dumps(result, sort_keys=True), flush=True)

valid = [r for r in rows if r["status"] == "success"]
qualifying = [r for r in valid if r["recall_at_10"] >= 0.90]
best = max(qualifying, key=lambda r:r["qps"]) if qualifying else (
    max(valid, key=lambda r:(r["recall_at_10"],r["qps"])) if valid else None)
print("HINGEZERO_IVFFLAT_BEST "+json.dumps(
    dict(reached_90pct=bool(qualifying), best=best, completed=len(valid), total=len(rows)),
    sort_keys=True), flush=True)
if not valid:
    raise SystemExit("All IVFFlat runs failed")
