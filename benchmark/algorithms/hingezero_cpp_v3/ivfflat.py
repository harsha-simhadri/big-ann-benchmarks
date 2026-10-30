"""Experimental full-corpus FAISS IVF-Flat candidate search with HingeZero native verification.

Unlike IVF/PQ, IVFFlat keeps exact vectors in each searched inverted list,
avoiding product-quantisation ranking errors. This is a candidate-index
experiment, not evidence of an isolated recurrence advantage.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path

import faiss
import numpy as np
from .module import HingeZeroCppANN


class HingeZeroCppIVFFlat(HingeZeroCppANN):
    def __init__(self, metric="euclidean", parameters=None):
        super().__init__(metric, parameters)
        self.name = "HingeZeroCppIVFFlat-" + self.mode

    def _open(self, dataset):
        ds = super()._open(dataset)
        self.build_metadata = dict(self.build_metadata, backend="IVFFlat")
        key = hashlib.sha256(
            json.dumps(self.build_metadata, sort_keys=True).encode()
        ).hexdigest()[:20]
        self.cache = Path("data/indices/trackT2/hingezero_ivfflat") / key
        return ds

    def fit(self, dataset):
        ds = self._open(dataset)
        b = self.build_metadata
        self.cache.mkdir(parents=True, exist_ok=True)
        metric = faiss.METRIC_L2 if self.metric == "euclidean" else faiss.METRIC_INNER_PRODUCT
        base = faiss.IndexFlatL2(ds.d) if metric == faiss.METRIC_L2 else faiss.IndexFlatIP(ds.d)
        self.index = faiss.IndexIVFFlat(base, ds.d, b["nlist"], metric)
        self.index.cp.seed = self.seed
        self.index.cp.niter = 12
        faiss.omp_set_num_threads(self.threads)
        rng = np.random.default_rng(self.seed)
        training_ids = np.sort(rng.choice(ds.nb, b["train_size"], replace=False))
        sample = self._transform(self.bank[training_ids])
        print(f"[HZ IVF-Flat] Train: {len(training_ids):,}, nlist={b['nlist']}", flush=True)
        self.index.train(sample)
        del sample
        for start in range(0, ds.nb, self.add_batch):
            end = min(start + self.add_batch, ds.nb)
            self.index.add(self._transform(self.bank[start:end]))
        assert self.index.ntotal == ds.nb
        temporary = self.cache / "index.pending.faiss"
        faiss.write_index(self.index, str(temporary))
        os.replace(temporary, self.cache / "index.faiss")
        tmp_meta = self.cache / "metadata.pending.json"
        tmp_meta.write_text(json.dumps(b, sort_keys=True, indent=2))
        os.replace(tmp_meta, self.cache / "metadata.json")
        print(f"[HZ IVF-Flat] Indexed {self.index.ntotal:,} exact corpus vectors", flush=True)

    def get_additional(self):
        info = super().get_additional()
        info["candidate_backend"] = "FAISS IVF-Flat full corpus (exact stored vectors)"
        info["hz_backend"] = "C++17/OpenMP HingeZero verifier; FAISS IVF-Flat candidate lookup"
        return info
