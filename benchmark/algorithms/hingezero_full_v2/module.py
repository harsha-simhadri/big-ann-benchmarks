from pathlib import Path
import hashlib
import json
import os
import time
import psutil
import numpy as np
import faiss
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import xbin_mmap
from . import core

AUTHOR = 'David Duffy'
CORE_SHA256 = hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()

class RoutingWitness(core.HingeZeroWitness):
    def __init__(self, memories, evidence):
        super().__init__(memories, evidence)
        self.last_refined = None

    def refine(self, state):
        refined = super().refine(state)
        self.last_refined = np.asarray(refined, np.float32).copy()
        return refined

class HingeZeroFullANN(BaseANN):
    def __init__(self, metric='euclidean', parameters=None):
        p = {} if parameters is None else dict(parameters)
        self.metric = str(metric)
        if self.metric not in ('euclidean', 'ip', 'angular'):
            raise ValueError('Supported metrics: euclidean, ip, angular')
        self.parameters = p
        self.nlist = int(p.get('nlist', 256))
        self.pq_m = int(p.get('pq_m', 64))
        self.pq_bits = int(p.get('pq_bits', 8))
        self.train_size = int(p.get('train_size', 20000))
        self.add_batch = int(p.get('add_batch', 4096))
        self.threads = int(p.get('threads', 4))
        self.seed = int(p.get('seed', 20261008))
        self.mode = str(p.get('mode', 'full'))
        if self.mode not in ('full', 'without_hz', 'zero_steps', 'no_retention', 'query_expansion'):
            raise ValueError('Unknown comparison mode')
        self.nprobe = 32
        self.candidates = 512
        self.expansion_candidates = 256
        self.rounds = 1
        self.steps = 8
        self.alpha = 4.5
        self.eps = 0.10
        self.lam = 0.02
        self.commit_margin = 0.10
        self.route_mix = 0.10
        self.retention_mix = 0.20
        self.name = 'HingeZeroFull-v2-' + self.mode
        self.index = None
        self.bank = None
        self.res = None
        self.stats = {}
        self.cache = None
        if min(self.nlist, self.pq_m, self.train_size, self.add_batch, self.threads) < 1:
            raise ValueError('Build counts must be positive')
        if not 1 <= self.pq_bits <= 8:
            raise ValueError('pq_bits must be between 1 and 8')
        faiss.omp_set_num_threads(self.threads)

    def get_memory_usage(self):
        statm = Path('/proc/self/statm')
        if statm.is_file():
            pages = int(statm.read_text().split()[1])
            return pages * os.sysconf('SC_PAGE_SIZE') / 1024
        return super().get_memory_usage()

    def track(self):
        return 'T2'

    def _open(self, dataset):
        ds = DATASETS[dataset]() if isinstance(dataset, str) else dataset
        if ds.data_type() != 'dense' or ds.search_type() != 'knn':
            raise ValueError('This adapter supports static dense k-NN datasets')
        if ds.distance() != self.metric:
            raise ValueError('Adapter metric differs from the dataset metric')
        self.bank = xbin_mmap(ds.get_dataset_fn(), ds.dtype, maxn=ds.nb)
        if self.bank.shape != (ds.nb, ds.d):
            raise ValueError('Dataset shape disagrees with its definition')
        self.ds = ds
        self.dataset_name = dataset if isinstance(dataset, str) else ds.short_name()
        f = Path(ds.get_dataset_fn()).resolve()
        build = dict(metric=self.metric, nlist=min(self.nlist, max(1, ds.nb // 40)),
                     pq_m=max(d for d in range(1, min(self.pq_m, ds.d) + 1) if ds.d % d == 0),
                     pq_bits=self.pq_bits, train_size=min(ds.nb, self.train_size),
                     seed=self.seed, n=ds.nb, d=ds.d, dtype=str(ds.dtype),
                     faiss=faiss.__version__, source=str(f), size=f.stat().st_size,
                     mtime_ns=f.stat().st_mtime_ns)
        if build['train_size'] < max(build['nlist'], 2 ** self.pq_bits):
            raise ValueError('Training sample is too small for the IVF/PQ configuration')
        key = hashlib.sha256(json.dumps(build, sort_keys=True).encode()).hexdigest()[:20]
        self.build_metadata = build
        self.cache = Path('data/indices/trackT2/hingezero_full_v1') / key
        estimate = int(ds.nb * (build['pq_m'] * self.pq_bits / 8 + 8) +
                       build['train_size'] * ds.d * 4 * 3 + build['nlist'] * ds.d * 4 + 128 * 1024**2)
        available = psutil.virtual_memory().available
        if estimate > available * 0.70:
            raise MemoryError(f'Estimated index/build workspace {estimate / 1024**3:.2f} GiB exceeds the laptop budget. This in-RAM IVF/PQ backend cannot support that dataset on this machine; use a smaller dataset or a separately tested disk index. Original vectors remain disk-mapped.')
        return ds

    def _transform(self, values):
        x = np.asarray(values, dtype=np.float32).copy(order='C')
        if not np.isfinite(x).all():
            raise ValueError('Nonfinite vectors are not accepted')
        if self.metric == 'angular':
            norms = np.linalg.norm(x, axis=1, keepdims=True)
            np.divide(x, norms, out=x, where=norms > 0)
        return x

    def load_index(self, dataset):
        self._open(dataset)
        index_file = self.cache / 'index.faiss'
        metadata = self.cache / 'metadata.json'
        if not index_file.is_file() or not metadata.is_file():
            return False
        saved = json.loads(metadata.read_text())
        if saved != self.build_metadata:
            return False
        self.index = faiss.read_index(str(index_file))
        if self.index.ntotal != self.ds.nb or self.index.d != self.ds.d:
            raise RuntimeError('Cached index does not match the complete bank')
        print(f'[HZ] Loaded shared IVF/PQ index: {self.index.ntotal:,} vectors', flush=True)
        return True

    def fit(self, dataset):
        ds = self._open(dataset)
        b = self.build_metadata
        self.cache.mkdir(parents=True, exist_ok=True)
        metric = faiss.METRIC_L2 if self.metric == 'euclidean' else faiss.METRIC_INNER_PRODUCT
        self.index = faiss.IndexIVFPQ(faiss.IndexFlat(ds.d, metric), ds.d,
                                     b['nlist'], b['pq_m'], self.pq_bits, metric)
        self.index.cp.seed = self.seed
        self.index.cp.niter = 12
        self.index.pq.cp.seed = self.seed
        self.index.pq.cp.niter = 12
        rng = np.random.default_rng(self.seed)
        sample_ids = np.sort(rng.choice(ds.nb, b['train_size'], replace=False))
        training = self._transform(self.bank[sample_ids])
        print(f'[HZ] Training IVF/PQ on {len(training):,} vectors; original bank is disk-mapped', flush=True)
        self.index.train(training)
        del training
        for start in range(0, ds.nb, self.add_batch):
            end = min(start + self.add_batch, ds.nb)
            self.index.add(self._transform(self.bank[start:end]))
            if start == 0 or end == ds.nb or start % (self.add_batch * 25) == 0:
                print(f'[HZ] Indexed {end:,}/{ds.nb:,}', flush=True)
        temporary = self.cache / 'index.pending.faiss'
        faiss.write_index(self.index, str(temporary))
        os.replace(temporary, self.cache / 'index.faiss')
        self._index_bytes = (self.cache / 'index.faiss').stat().st_size
        temp_metadata = self.cache / 'metadata.pending.json'
        temp_metadata.write_text(json.dumps(b, sort_keys=True, indent=2))
        os.replace(temp_metadata, self.cache / 'metadata.json')

    def set_query_arguments(self, arguments):
        p = dict(arguments)
        self.nprobe = int(p.get('nprobe', 32))
        self.candidates = int(p.get('candidates', 512))
        self.expansion_candidates = int(p.get('expansion_candidates', 256))
        self.rounds = int(p.get('rounds', 1))
        self.steps = int(p.get('steps', 8))
        self.alpha = float(p.get('alpha', 4.5))
        self.eps = float(p.get('eps', 0.10))
        self.lam = float(p.get('lam', 0.02))
        self.commit_margin = float(p.get('commit_margin', 0.10))
        self.route_mix = float(p.get('route_mix', 0.10))
        self.retention_mix = float(p.get('retention_mix', 0.20))
        if min(self.nprobe, self.candidates) < 1 or min(self.rounds, self.steps, self.expansion_candidates) < 0:
            raise ValueError('Invalid search counts')
        if not 0 <= self.route_mix <= 1 or not 0 <= self.retention_mix <= 1 or self.commit_margin < 0:
            raise ValueError('Invalid retention/routing parameters')
        if not np.isfinite([self.alpha, self.eps, self.lam, self.commit_margin, self.route_mix, self.retention_mix]).all():
            raise ValueError('Parameters must be finite')
        if self.eps < 0 or not 0 <= self.lam <= 1 or self.alpha < 0:
            raise ValueError('Invalid recurrence parameters')

    def _scores(self, memories, query):
        a = np.asarray(memories, np.float64)
        q = np.asarray(query, np.float64)
        if self.metric == 'euclidean':
            delta = a - q
            return -np.einsum('ij,ij->i', delta, delta)
        if self.metric == 'angular':
            norms = np.linalg.norm(a, axis=1)
            qnorm = np.linalg.norm(q)
            return np.divide(a @ q, norms * qnorm, out=np.zeros(len(a)), where=norms * qnorm > 0)
        return a @ q

    def _evidence(self, scores):
        if self.metric == 'euclidean':
            return (1.0 / (1.0 + np.maximum(-scores, 0))).astype(np.float32)
        shifted = scores - scores.min()
        scale = float(shifted.max())
        return (shifted / scale if scale > 0 else np.ones_like(shifted)).astype(np.float32)

    def _ordered(self, ids, scores):
        return np.lexsort((ids, -scores))

    def _valid_ids(self, ids):
        ids = np.asarray(ids, np.int64)
        return np.unique(ids[(ids >= 0) & (ids < len(self.bank))])

    def _initial_ids(self, query, count):
        self.stats['index_searches'] = self.stats.get('index_searches', 0) + 1
        self.index.nprobe = min(self.nprobe, self.index.nlist)
        _, ids = self.index.search(self._transform(query[None, :]), min(count, len(self.bank)))
        ids = self._valid_ids(ids[0])
        return ids

    def _witness(self, ids, query):
        raw = np.asarray(self.bank[ids], np.float32)
        scores = self._scores(raw, query)
        witness = RoutingWitness(raw, self._evidence(scores))
        return witness, raw, scores

    def query(self, queries, k=10):
        if self.index is None or self.bank is None:
            raise RuntimeError('Build or load the index first')
        q = np.asarray(queries, np.float32)
        if q.ndim == 1:
            q = q[None, :]
        if q.ndim != 2 or q.shape[1] != self.bank.shape[1] or not np.isfinite(q).all():
            raise ValueError('Invalid query matrix')
        if not 1 <= k <= len(self.bank):
            raise ValueError('k must be within the bank size')
        core.HZ_ALPHA, core.HZ_EPS, core.HZ_LAMBDA = self.alpha, self.eps, self.lam
        core.HZ_STEPS = 0 if self.mode in ('zero_steps', 'without_hz', 'query_expansion') else self.steps
        core.hinge_phi.__defaults__ = (self.alpha,)
        self.stats = dict(witness_checks=0, retention_events=0, retention_commits=0,
                          append_checks=0, candidate_reads=0, seed_reads=0, extra_reads=0, failed_checks=0, index_searches=0, refinement_route_events=0, refinement_shift_sum=0.0, seed_score_regressions=0)
        result = np.empty((len(q), k), np.int32)
        seed_count = max(k, self.candidates)
        budget = min(len(self.bank), seed_count + self.expansion_candidates * self.rounds)
        for qi, original in enumerate(q):
            if self.mode in ('without_hz', 'query_expansion'):
                ids = self._initial_ids(original, seed_count)
                if len(ids) < k:
                    raise RuntimeError('Candidate index returned fewer than k IDs; increase nprobe')
                actual_seed_count = len(ids)
                if self.mode == 'query_expansion' and budget > seed_count:
                    expanded = self._initial_ids(original, budget)
                    extra_ids = np.setdiff1d(expanded, ids, assume_unique=True)
                    if len(extra_ids):
                        extra_scores = self._scores(self.bank[extra_ids], original)
                        extra_ids = extra_ids[self._ordered(extra_ids, extra_scores)[:budget - seed_count]]
                        ids = np.concatenate((ids, extra_ids))
                scores = self._scores(self.bank[ids], original)
                selected = ids[self._ordered(ids, scores)[:k]]
                result[qi] = selected
                self.stats['candidate_reads'] += len(ids)
                self.stats['seed_reads'] += actual_seed_count
                self.stats['extra_reads'] += len(ids) - actual_seed_count
            else:
                ids = self._initial_ids(original, seed_count)
                if len(ids) < k:
                    raise RuntimeError('Candidate index returned fewer than k IDs; increase nprobe')
                witness, raw, scores = self._witness(ids, original)
                seed_ids = ids.copy()
                seed_top_scores = scores[self._ordered(ids, scores)[:k]].copy()
                self.stats['seed_reads'] += len(ids)
                first = int(self._ordered(ids, scores)[0])
                locked = witness.observe(core.HingeZeroState(first, witness.memories[first]))
                loop = core.HingeZeroRetainingLoop(witness, locked, commit_margin=self.commit_margin)
                qnorm = float(np.linalg.norm(original))
                for _ in range(self.rounds if self.expansion_candidates else 0):
                    if self.mode == 'no_retention':
                        route = witness.refine(original)
                    else:
                        event = loop.step(cue=original)
                        self.stats['retention_events'] += 1
                        self.stats['retention_commits'] += int(event['committed'])
                        if witness.last_refined is None:
                            raise RuntimeError('Retaining loop did not produce a refined cue')
                        route = core._unit((1.0 - self.retention_mix) * witness.last_refined + self.retention_mix * event['state'].state)
                    refined = witness.last_refined
                    if refined is None:
                        raise RuntimeError('Candidate expansion lost its refinement output')
                    self.stats['refinement_route_events'] += 1
                    self.stats['refinement_shift_sum'] += float(np.linalg.norm(refined - core._unit(original)))
                    routed = core._unit((1.0 - self.route_mix) * core._unit(original) + self.route_mix * route)
                    routed = routed * qnorm
                    extra_ids = self._initial_ids(routed, self.expansion_candidates)
                    new_ids = np.setdiff1d(extra_ids, ids, assume_unique=True)
                    if len(new_ids):
                        extra_raw = np.asarray(self.bank[new_ids], np.float32)
                        extra_scores = self._scores(extra_raw, original)
                        witness.append_memories(extra_raw, self._evidence(extra_scores))
                        ids = np.concatenate((ids, new_ids))
                        raw = np.vstack((raw, extra_raw))
                        scores = self._scores(raw, original)
                        witness.evidence = self._evidence(scores)
                        witness.field_ids = np.argsort(-witness.evidence, kind='stable')[:min(core.HZ_TOP, len(ids))]
                        witness.field_memories = witness.memories[witness.field_ids]
                        self.stats['append_checks'] += 1
                        if not witness.verify(loop.checkpoint):
                            raise RuntimeError('Appending candidates invalidated a retained checkpoint')
                scores = self._scores(raw, original)
                order = self._ordered(ids, scores)
                if not np.isin(seed_ids, ids).all():
                    raise RuntimeError('Candidate expansion discarded an original seed ID')
                if np.any(scores[order[:k]] < seed_top_scores - 1e-12):
                    self.stats['seed_score_regressions'] += 1
                    raise RuntimeError('Original-metric reranking became worse than the seed result')
                self.stats['extra_reads'] += len(ids) - len(seed_ids)
                chosen_local = int(order[0])
                final = witness.observe(core.HingeZeroState(chosen_local, witness.memories[chosen_local]))
                if final.candidate_index != chosen_local:
                    raise RuntimeError('Witness output differs from the original-metric winner')
                if not witness.verify(final):
                    raise RuntimeError('Final state failed witness verification')
                again = witness.observe(final)
                if not np.array_equal(again.state, final.state) or again.candidate_index != final.candidate_index:
                    raise RuntimeError('Witness idempotence failed')
                selected = ids[order[:k]]
                returned = np.asarray(self.bank[selected], np.float32)
                if not np.array_equal(returned, raw[order[:k]]):
                    raise RuntimeError('Returned global IDs disagree with the stored candidate records')
                self.stats['candidate_reads'] += len(ids)
                self.stats['witness_checks'] += k + 2
                result[qi] = selected
            if len(np.unique(result[qi])) != k:
                raise RuntimeError('Duplicate output IDs')
            if qi == 0 or (qi + 1) % 1000 == 0 or qi + 1 == len(q):
                print(f'[HZ] {self.mode}: {qi + 1:,}/{len(q):,} queries', flush=True)
        self.res = result
        return result

    def get_results(self):
        return self.res

    def get_additional(self):
        values = dict(self.stats)
        values.update(hz_core_sha256=CORE_SHA256, hz_mode=self.mode, hz_steps=(0 if self.mode in ('zero_steps', 'without_hz', 'query_expansion') else self.steps),
                      hz_alpha=self.alpha, hz_nprobe=self.nprobe, hz_candidates=self.candidates,
                      hz_expansion_candidates=self.expansion_candidates, hz_retention_mix=self.retention_mix,
                      hz_rounds=self.rounds, hz_commit_margin=self.commit_margin,
                      hz_route_mix=self.route_mix, hz_softmax=False,
                      raw_bank_bytes=self.bank.nbytes, index_disk_bytes=(self.cache / 'index.faiss').stat().st_size,
                      candidate_backend='FAISS IVF/PQ', bank_storage='read-only disk memmap',
                      mean_candidate_reads=self.stats.get('candidate_reads', 0) / max(1, len(self.res)),
                      mean_seed_candidate_reads=self.stats.get('seed_reads', 0) / max(1, len(self.res)),
                      mean_extra_candidate_reads=self.stats.get('extra_reads', 0) / max(1, len(self.res)),
                      mean_refinement_shift=self.stats.get('refinement_shift_sum', 0) / max(1, self.stats.get('refinement_route_events', 0)))
        return values

    def index_files_to_store(self, dataset):
        if self.cache is None:
            self._open(dataset)
        return str(self.cache), '', ['index.faiss', 'metadata.json']
