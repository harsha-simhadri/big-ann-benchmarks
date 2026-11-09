import time

import numpy as np

import writerslogic_warm as warm

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS


class Warm(BaseFilterANN):
    """WARM label-filtered index (writerslogic_warm.FilteredIndex).

    Per-label posting lists route each query by the size of its rarest label: small ones are
    scored exactly over every match, large ones probe a k-means inverted file trained on that
    label's members, skipping members that lack the other query labels. Distances are exact
    integer L2 on the uint8 rows.
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
        # Integer knobs; anything not named keeps the engine default. The boolean and
        # prefetch knobs (sort_queries, block_filter, skip_tombstones, cache_intersections,
        # prefetch) change speed only, never a result.
        ints = ("brute_max", "target", "min_lists", "intersect_max", "prefetch")
        flags = ("sort_queries", "block_filter", "skip_tombstones", "cache_intersections", "wide")
        kwargs = {k: int(query_args[k]) for k in ints if k in query_args}
        kwargs.update({k: bool(query_args[k]) for k in flags if k in query_args})
        self.index.set_search(**kwargs)

    def filtered_query(self, X, filter, k):
        self.res = self.index.search(self._to_u8(X), filter.indptr, filter.indices, k)

    def query(self, X, k):
        raise NotImplementedError("WARM filtered index answers filtered queries only")

    def get_results(self):
        return self.res

    def __str__(self):
        return f"Warm({self._params}, {self._query})"
