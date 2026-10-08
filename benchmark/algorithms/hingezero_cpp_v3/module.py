from pathlib import Path
import ctypes as C
import hashlib
import numpy as np
import faiss
import psutil
from .index_backend import NativeIndexBackend
from .build_native import build

AUTHOR = 'David Duffy'
REFERENCE_CORE_SHA256 = 'dd4c7e82c9823ea6c69b972113ef6a3a132d152d6b319551658fe00333e7bfa8'
STAT_NAMES = ('witness_checks','retention_events','retention_commits','append_checks',
              'candidate_reads','seed_reads','extra_reads','failed_checks',
              'refinement_route_events','refinement_shift_sum','seed_score_regressions',
              'original_metric_evaluations','output_record_checks')
MODES = {'full':0,'without_hz':1,'zero_steps':2,'no_retention':3,'query_expansion':4}

class Parameters(C.Structure):
    _fields_ = [(s,C.c_int32) for s in ('metric','dtype','mode','steps','field_limit','threads')]+[(s,C.c_double) for s in ('alpha','eps','lam','commit_margin','route_mix','retention_mix')]

class HingeZeroCppANN(NativeIndexBackend):
    def __init__(self,metric='euclidean',parameters=None):
        super().__init__(metric,parameters)
        self.name = 'HingeZeroCpp-v3-'+self.mode
        self.batch_size = int(self.parameters.get('batch_size',32))
        self.field_limit = 256
        self.stats = {}
        self.res = None
        path,self.native_build = build()
        self.lib = C.CDLL(str(path))
        self.lib.hz_error.argtypes=[]
        self.lib.hz_error.restype=C.c_char_p
        self.lib.hz_abi_version.argtypes=[]
        self.lib.hz_abi_version.restype=C.c_int
        if self.lib.hz_abi_version()!=3:
            raise RuntimeError('Native library ABI mismatch; rebuild the kernel')
        self.lib.hz_create.argtypes=[C.c_void_p,C.c_int64,C.c_int32,C.c_void_p,C.c_int32,C.c_void_p,C.c_int32,C.c_int32,C.POINTER(Parameters)]
        self.lib.hz_create.restype=C.c_void_p
        self.lib.hz_route.argtypes=[C.c_void_p,C.c_void_p]
        self.lib.hz_route.restype=C.c_int
        self.lib.hz_expand.argtypes=[C.c_void_p,C.c_void_p,C.c_int32,C.c_int32]
        self.lib.hz_expand.restype=C.c_int
        self.lib.hz_finish.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
        self.lib.hz_finish.restype=C.c_int
        self.lib.hz_destroy.argtypes=[C.c_void_p]
        self.lib.hz_destroy.restype=None

    def set_query_arguments(self,arguments):
        p=dict(arguments)
        self.nprobe=int(p.get('nprobe',32))
        self.candidates=int(p.get('candidates',512))
        self.expansion_candidates=int(p.get('expansion_candidates',256))
        self.rounds=int(p.get('rounds',1))
        self.steps=int(p.get('steps',8))
        self.alpha=float(p.get('alpha',4.5))
        self.eps=float(p.get('eps',.10))
        self.lam=float(p.get('lam',.02))
        self.commit_margin=float(p.get('commit_margin',.10))
        self.route_mix=float(p.get('route_mix',.10))
        self.retention_mix=float(p.get('retention_mix',.20))
        self.batch_size=int(p.get('batch_size',self.batch_size))
        if min(self.nprobe,self.candidates,self.batch_size)<1 or min(self.rounds,self.steps,self.expansion_candidates)<0:
            raise ValueError('Invalid query counts')
        if not np.isfinite([self.alpha,self.eps,self.lam,self.commit_margin,self.route_mix,self.retention_mix]).all():
            raise ValueError('Parameters must be finite')
        if min(self.alpha,self.eps,self.commit_margin)<0 or not all(0<=x<=1 for x in (self.lam,self.route_mix,self.retention_mix)):
            raise ValueError('Invalid recurrence or routing parameters')

    def _check(self,result):
        if result!=0:
            message=self.lib.hz_error().decode('utf-8',errors='replace')
            raise RuntimeError('HingeZero C++: '+message)

    def _search(self,queries,count):
        _,ids=self.index.search(self._transform(queries),min(int(count),len(self.bank)))
        self.stats['index_searches']+=len(queries)
        self.stats['faiss_batch_calls']+=1
        return np.ascontiguousarray(ids,np.int64)

    def query(self,queries,k=10):
        if self.index is None or self.bank is None:
            raise RuntimeError('Build or load the index first')
        q=np.ascontiguousarray(queries,np.float32)
        if q.ndim==1: q=q[None,:]
        if q.ndim!=2 or q.shape[1]!=self.bank.shape[1] or not np.isfinite(q).all():
            raise ValueError('Invalid complete query matrix')
        if not 1<=k<=len(self.bank): raise ValueError('k must be within the bank size')
        dtype={np.dtype('float32'):0,np.dtype('uint8'):1,np.dtype('int8'):2}.get(self.bank.dtype)
        if dtype is None or not self.bank.flags.c_contiguous:
            raise ValueError('Native bank must be contiguous float32, uint8 or int8')
        per_query=(max(k,self.candidates)+self.rounds*self.expansion_candidates)*self.bank.shape[1]*4*3
        workspace=per_query*min(self.batch_size,max(1,len(q)))
        if workspace>psutil.virtual_memory().available*.65:
            raise MemoryError('Native batch workspace exceeds available RAM; reduce --batch-size (e.g. 8)')
        self.index.nprobe=min(self.nprobe,self.index.nlist)
        faiss.omp_set_num_threads(self.threads)
        self.stats={name:0 for name in STAT_NAMES}
        self.stats.update(index_searches=0,faiss_batch_calls=0)
        result=np.empty((len(q),k),np.int32)
        steps=0 if self.mode in ('zero_steps','without_hz','query_expansion') else self.steps
        params=Parameters({'euclidean':0,'ip':1,'angular':2}[self.metric],dtype,MODES[self.mode],steps,self.field_limit,self.threads,
                          self.alpha,self.eps,self.lam,self.commit_margin,self.route_mix,self.retention_mix)
        seed_count=max(k,self.candidates)
        for start in range(0,len(q),self.batch_size):
            batch=q[start:start+self.batch_size]
            seeds=self._search(batch,seed_count)
            handle=self.lib.hz_create(C.c_void_p(self.bank.ctypes.data),len(self.bank),self.bank.shape[1],C.c_void_p(batch.ctypes.data),len(batch),
                                      C.c_void_p(seeds.ctypes.data),seeds.shape[1],k,C.byref(params))
            if not handle: raise RuntimeError('HingeZero C++: '+self.lib.hz_error().decode())
            try:
                for round_index in range(self.rounds if self.mode!='without_hz' and self.expansion_candidates else 0):
                    routes=np.empty_like(batch)
                    self._check(self.lib.hz_route(handle,C.c_void_p(routes.ctypes.data)))
                    requested=seed_count+self.expansion_candidates*(round_index+1)
                    expanded=self._search(routes,requested)
                    self._check(self.lib.hz_expand(handle,C.c_void_p(expanded.ctypes.data),expanded.shape[1],self.expansion_candidates))
                values=np.empty(len(STAT_NAMES),np.float64)
                out=result[start:start+len(batch)]
                self._check(self.lib.hz_finish(handle,C.c_void_p(out.ctypes.data),C.c_void_p(values.ctypes.data)))
                for name,value in zip(STAT_NAMES,values): self.stats[name]+=float(value)
            finally:
                self.lib.hz_destroy(handle)
            finished=start+len(batch)
            if start==0 or finished//1000!=start//1000 or finished==len(q):
                print(f'[HZ C++] {self.mode}: {finished:,}/{len(q):,} queries',flush=True)
        self.res=result
        return result

    def get_results(self):
        return self.res

    def get_additional(self):
        n=max(1,len(self.res))
        counters={k:(v if k=='refinement_shift_sum' else int(v)) for k,v in self.stats.items()}
        counters.update(hz_mode=self.mode,hz_steps=(0 if self.mode in ('zero_steps','without_hz','query_expansion') else self.steps),
                        hz_alpha=self.alpha,hz_eps=self.eps,hz_lam=self.lam,hz_rounds=self.rounds,hz_nprobe=self.nprobe,
                        hz_candidates=self.candidates,hz_expansion_candidates=self.expansion_candidates,hz_field_memories=self.field_limit,
                        hz_route_mix=self.route_mix,hz_retention_mix=self.retention_mix,hz_commit_margin=self.commit_margin,
                        hz_softmax=False,hz_reference_core_sha256=REFERENCE_CORE_SHA256,hz_native_sha256=self.native_build['source_sha256'],
                        hz_backend='C++17/OpenMP; batched FAISS IVF/PQ',native_compiler=self.native_build['compiler'],
                        native_threads=self.threads,native_batch_size=self.batch_size,raw_bank_bytes=self.bank.nbytes,
                        index_disk_bytes=(self.cache/'index.faiss').stat().st_size,candidate_backend='FAISS IVF/PQ',
                        bank_storage='read-only disk memmap',mean_candidate_reads=self.stats['candidate_reads']/n,
                        mean_seed_candidate_reads=self.stats['seed_reads']/n,mean_extra_candidate_reads=self.stats['extra_reads']/n,
                        mean_original_metric_evaluations=self.stats['original_metric_evaluations']/n,
                        mean_refinement_shift=self.stats['refinement_shift_sum']/max(1,self.stats['refinement_route_events']))
        return counters
