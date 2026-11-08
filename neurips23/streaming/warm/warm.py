import os
import shutil
import time

import numpy as np

from benchmark.datasets import DATASETS
from writerslogic_warm import UpdatableIndex
from neurips23.streaming.base import BaseStreamingANN
from neurips23.streaming.warm.streaming_io import MSTuring10MRangeReader, MSTuring30MRangeReader

DATASETS.update({"msturing-10M-clustered": MSTuring10MRangeReader,
                 "msturing-30M-clustered": MSTuring30MRangeReader})


class Warm(BaseStreamingANN):
    """WARM's updatable graph index (writerslogic_warm.UpdatableIndex): a memory-mapped
    quantized base graph, an in-memory graph of rows inserted since the last consolidation, and a consolidation
    when the delta or the deleted share passes a threshold. With "merge" the consolidation
    links the delta into the previous base graph and splices deleted rows out of it, and
    rebuilds only once the rows changed by merges reach "rebuild_after" times the live rows;
    otherwise every consolidation rebuilds the base over the live rows.

    "mode": "partition" in the run group (or WARM_MODE=partition in the environment) selects the
    experimental partition tier instead
    (writerslogic_warm.PartitionIndex, docs/research/STREAMING-L22.md): exact brute force until
    the first search with "train_at" live rows, then 5,000 fixed k-means lists with a SOAR spill,
    4-bit PQ residual codes and an exact reorder. Group keys: "reorder" (317), "lists" (5000),
    "train_at" (1000000), "T"; query key: "nprobe" (250). The graph and consolidation keys are
    ignored there. Otherwise the updatable-graph path runs unchanged."""

    def __init__(self, metric, index_params):
        if metric not in ("euclidean", "angular"):
            raise ValueError(f"WARM streaming supports euclidean and angular, not {metric}")
        self.name = "warm"
        self._metric = metric
        self.partition = (os.environ.get("WARM_MODE") == "partition"
                          or index_params.get("mode") == "partition")
        self.R = index_params.get("R", 32)
        self.L = index_params.get("L", 64)
        # alpha is the pruning parameter of the second construction pass. 1.2 (the old
        # UpdatableIndex default) cost 7-9 recall@10 points at degree 32; always pass it.
        self.alpha = float(index_params.get("alpha", 1.0))
        self.threads = index_params.get("T", 0)
        self.delta_ratio = index_params.get("delta_ratio", 1.0)
        self.deleted_ratio = index_params.get("deleted_ratio", 0.3)
        self.min_delta = index_params.get("min_delta", 100_000)
        self.merge = bool(index_params.get("merge", False))
        self.rebuild_after = index_params.get("rebuild_after", 1.0)
        self.nprobe = int(index_params.get("nprobe", 250))
        self.reorder = int(index_params.get("reorder", 317))
        self.lists = int(index_params.get("lists", 5000))
        self.train_at = int(index_params.get("train_at", 1_000_000))
        self.wall0 = None
        self.ef = 64
        self.rerank = 64
        self.index = None
        self._query_args = {}

    def index_name(self):
        if self.partition:
            return f"partition_l{self.lists}_np{self.nprobe}_ro{self.reorder}"
        return f"R{self.R}_L{self.L}"

    def setup(self, dtype, max_pts, ndim):
        self._setup_args = (dtype, max_pts, ndim)
        self._used = False
        if self.partition:
            # Imported here so the graph path still loads on a wheel without it.
            from writerslogic_warm import PartitionIndex
            self.index = PartitionIndex.create(
                ndim, lists=self.lists, train_at=self.train_at, nprobe=self.nprobe,
                reorder=self.reorder, threads=self.threads)
            self.wall0 = time.perf_counter()
            return
        path = os.path.join(os.getcwd(), "data", "indices", "streaming", "warm", self.index_name())
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.rmtree(path, ignore_errors=True)
        self.index = UpdatableIndex.create(
            path, ndim, metric=self._metric, degree=self.R, build_ef=self.L,
            alpha=self.alpha, threads=self.threads)
        self.index.set_query_arguments(self.ef, self.rerank)

    def _maybe_consolidate(self):
        self._used = True
        if self.index.needs_consolidation(self.delta_ratio, self.deleted_ratio, self.min_delta):
            self.index.consolidate(merge=self.merge, rebuild_after=self.rebuild_after)

    def insert(self, X, ids):
        if self.partition:
            self._used = True
            return self.index.insert(ids.astype(np.int64), np.ascontiguousarray(X, dtype=np.float32))
        self.index.insert(np.ascontiguousarray(X, dtype=np.float32), ids.astype(np.int64))
        self._maybe_consolidate()

    def delete(self, ids):
        if self.partition:
            self._used = True
            self.index.delete(ids.astype(np.int64))
            return
        self.index.delete(ids.astype(np.int64))
        self._maybe_consolidate()

    def replace(self, X, ids):
        if self.partition:
            self.delete(ids)
            return self.insert(X, ids)
        self.index.replace(np.ascontiguousarray(X, dtype=np.float32), ids.astype(np.int64))
        self._maybe_consolidate()

    def query(self, X, k):
        self.res = self.index.search(np.ascontiguousarray(X, dtype=np.float32), k)

    def done(self):
        if self.partition and self.index is not None:
            st = self.index.stats()
            # One line per run; the test-B report marks the arm invalid without it.
            print("WARM_MODE partition " + " ".join(
                f"{k}={v:.3f}" if isinstance(v, float) else f"{k}={v}" for k, v in st.items())
                + f" adapter_wall_s={time.perf_counter() - self.wall0:.1f}", flush=True)

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.ef = query_args.get("ef", 64)
        self.rerank = query_args.get("rerank", self.ef)
        if self.index is not None and self._used:
            # The runner replays the whole runbook for each query-argument group.
            self.setup(*self._setup_args)
        if self.partition:
            self.nprobe = int(query_args.get("nprobe", self.nprobe))
            if self.index is not None:
                self.index.set_nprobe(self.nprobe)
        elif self.index is not None:
            self.index.set_query_arguments(self.ef, self.rerank)

    def __str__(self):
        return f"warm({self.index_name()}, {self._query_args})"
