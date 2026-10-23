import os
import shutil

import numpy as np

from holographic_memory import UpdatableIndex
from neurips23.streaming.base import BaseStreamingANN


class HMS(BaseStreamingANN):
    """Holographic Memory's updatable graph index: a memory-mapped quantized base graph,
    an in-memory graph of rows inserted since the last consolidation, and a rebuild of the
    base over the live rows when the delta or the deleted share passes a threshold."""

    def __init__(self, metric, index_params):
        if metric not in ("euclidean", "angular"):
            raise ValueError(f"HMS streaming supports euclidean and angular, not {metric}")
        self.name = "hms"
        self._metric = metric
        self.R = index_params["R"]
        self.L = index_params["L"]
        self.alpha = index_params.get("alpha", 1.0)
        self.threads = index_params.get("T", 0)
        self.delta_ratio = index_params.get("delta_ratio", 1.0)
        self.deleted_ratio = index_params.get("deleted_ratio", 0.3)
        self.min_delta = index_params.get("min_delta", 100_000)
        self.ef = 64
        self.rerank = 64
        self.index = None
        self._query_args = {}

    def index_name(self):
        return f"R{self.R}_L{self.L}"

    def setup(self, dtype, max_pts, ndim):
        self._setup_args = (dtype, max_pts, ndim)
        self._used = False
        path = os.path.join(os.getcwd(), "data", "indices", "streaming", "hms", self.index_name())
        os.makedirs(os.path.dirname(path), exist_ok=True)
        shutil.rmtree(path, ignore_errors=True)
        self.index = UpdatableIndex.create(
            path, ndim, metric=self._metric, degree=self.R, build_ef=self.L,
            alpha=self.alpha, threads=self.threads)
        self.index.set_query_arguments(self.ef, self.rerank)

    def _maybe_consolidate(self):
        self._used = True
        if self.index.needs_consolidation(self.delta_ratio, self.deleted_ratio, self.min_delta):
            self.index.consolidate()

    def insert(self, X, ids):
        self.index.insert(np.ascontiguousarray(X, dtype=np.float32), ids.astype(np.int64))
        self._maybe_consolidate()

    def delete(self, ids):
        self.index.delete(ids.astype(np.int64))
        self._maybe_consolidate()

    def replace(self, X, ids):
        self.index.replace(np.ascontiguousarray(X, dtype=np.float32), ids.astype(np.int64))
        self._maybe_consolidate()

    def query(self, X, k):
        self.res = self.index.search(np.ascontiguousarray(X, dtype=np.float32), k)

    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self.ef = query_args.get("ef", 64)
        self.rerank = query_args.get("rerank", self.ef)
        if self.index is not None and self._used:
            # The runner replays the whole runbook for each query-argument group.
            self.setup(*self._setup_args)
        if self.index is not None:
            self.index.set_query_arguments(self.ef, self.rerank)

    def __str__(self):
        return f"hms({self.index_name()}, {self._query_args})"
