import time

import numpy as np

import writerslogic_warm as warm

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS


class Warm(BaseFilterANN):
    """WARM label-filtered index (writerslogic_warm.FilteredIndex).

    Labels with more than `ivf_min` members keep k-means lists of their own members, stored as
    4-bit product-quantizer codes (one quantizer for the whole set). A query is routed by its
    rarest label: small ones are scored exactly over every match; larger ones probe the lists,
    screen with the 4-bit codes while skipping members that lack the other query labels, and
    rescore the best `rerank` candidates exactly on the uint8 rows. Probe effort (`target`,
    `rerank`) is set per query class by label count and rarest-label size.
    """

    def __init__(self, metric, index_params):
        if metric != "euclidean":
            raise ValueError(f"WARM filtered index supports euclidean only, got {metric}")
        self._params = dict(index_params)
        self._threads = int(self._params.pop("threads", 0))
        self._scale = None
        self.index = None
        self.res = None
        self._query = {}

    def _rows(self, ds, n):
        fn = ds.get_dataset_fn()
        if ds.dtype == "uint8":
            return np.memmap(fn, dtype=np.uint8, mode="r", offset=8, shape=(n, ds.d))
        # Non-uint8 data (the CI random set): one global affine map onto 0..255, applied to
        # queries too; it preserves L2 order up to rounding.
        x = ds.get_dataset().astype(np.float32)
        lo, hi = float(x.min()), float(x.max())
        self._scale = (lo, 255.0 / max(hi - lo, 1e-12))
        return self._to_u8(x)

    def _to_u8(self, x):
        if self._scale is None:
            return np.ascontiguousarray(x, dtype=np.uint8)
        lo, s = self._scale
        return np.clip(np.rint((np.asarray(x, dtype=np.float32) - lo) * s), 0, 255).astype(np.uint8)

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        meta = ds.get_dataset_metadata()
        meta.sort_indices()
        start = time.time()
        rows = self._rows(ds, meta.shape[0])
        self.index = warm.FilteredIndex(
            rows, meta.indptr, meta.indices, labels=meta.shape[1], threads=self._threads,
            **{k: int(v) for k, v in self._params.items()},
        )
        print(f"WARM FilteredIndex built in {time.time() - start:.1f} s, "
              f"{self.index.memory_bytes() / 2**30:.2f} GiB, {self.index.ivf_labels()} label lists")

    def load_index(self, dataset):
        return False

    def index_files_to_store(self, dataset):
        return None

    def set_query_arguments(self, query_args):
        self._query = dict(query_args)
        bools = {"sort_queries", "wide", "skip_tombstones", "block_filter", "cache_intersections"}
        self.index.set_search(**{k: (bool(v) if k in bools else [int(x) for x in v] if isinstance(v, list) else int(v)) for k, v in query_args.items()})

    def filtered_query(self, X, filter, k):
        self.res = self.index.search(self._to_u8(X), filter.indptr, filter.indices, k)

    def query(self, X, k):
        raise NotImplementedError("WARM filtered index answers filtered queries only")

    def get_results(self):
        return self.res

    def __str__(self):
        return f"Warm({self._params}, {self._query})"
