from pathlib import Path
import hashlib
import json
import os
import psutil
import numpy as np
import faiss
from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import xbin_mmap

class NativeIndexBackend(BaseANN):

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
        self.eps = 0.1
        self.lam = 0.02
        self.commit_margin = 0.1
        self.route_mix = 0.1
        self.retention_mix = 0.2
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
        build = dict(metric=self.metric, nlist=min(self.nlist, max(1, ds.nb // 40)), pq_m=max((d for d in range(1, min(self.pq_m, ds.d) + 1) if ds.d % d == 0)), pq_bits=self.pq_bits, train_size=min(ds.nb, self.train_size), seed=self.seed, n=ds.nb, d=ds.d, dtype=str(ds.dtype), faiss=faiss.__version__, source=str(f), size=f.stat().st_size, mtime_ns=f.stat().st_mtime_ns)
        if build['train_size'] < max(build['nlist'], 2 ** self.pq_bits):
            raise ValueError('Training sample is too small for the IVF/PQ configuration')
        key = hashlib.sha256(json.dumps(build, sort_keys=True).encode()).hexdigest()[:20]
        self.build_metadata = build
        self.cache = Path('data/indices/trackT2/hingezero_full_v1') / key
        estimate = int(ds.nb * (build['pq_m'] * self.pq_bits / 8 + 8) + build['train_size'] * ds.d * 4 * 3 + build['nlist'] * ds.d * 4 + 128 * 1024 ** 2)
        available = psutil.virtual_memory().available
        if estimate > available * 0.7:
            raise MemoryError(f'Estimated index/build workspace {estimate / 1024 ** 3:.2f} GiB exceeds the laptop budget. This in-RAM IVF/PQ backend cannot support that dataset on this machine; use a smaller dataset or a separately tested disk index. Original vectors remain disk-mapped.')
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
        self.index = faiss.IndexIVFPQ(faiss.IndexFlat(ds.d, metric), ds.d, b['nlist'], b['pq_m'], self.pq_bits, metric)
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

    def index_files_to_store(self, dataset):
        if self.cache is None:
            self._open(dataset)
        return (str(self.cache), '', ['index.faiss', 'metadata.json'])
