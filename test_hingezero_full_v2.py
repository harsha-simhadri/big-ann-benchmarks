from pathlib import Path
import hashlib
import json
import tempfile
import os
import numpy as np
import faiss
import h5py
import sys
from benchmark.dataset_io import xbin_write
from benchmark.datasets import DatasetCompetitionFormat
from benchmark.algorithms.definitions import get_definitions, instantiate_algorithm
from benchmark.algorithms.hingezero_full_v2.module import HingeZeroFullANN, CORE_SHA256
from benchmark.algorithms.hingezero_full_v2 import core

EXPECTED = 'dd4c7e82c9823ea6c69b972113ef6a3a132d152d6b319551658fe00333e7bfa8'
assert CORE_SHA256 == EXPECTED
rng = np.random.default_rng(20261008)
checks = 0
report = {}
class LocalDataset(DatasetCompetitionFormat):
    def __init__(self, filename, metric):
        self.filename = filename
        self.metric = metric
        self.nb = 2048
        self.d = 16
        self.dtype = 'float32'
    def get_dataset_fn(self):
        return self.filename
    def distance(self):
        return self.metric

def exact(bank, q, metric, k):
    if metric == 'euclidean':
        delta = bank.astype(np.float64) - q.astype(np.float64)
        s = -np.einsum('ij,ij->i',delta,delta)
    elif metric == 'ip':
        s = bank.astype(np.float64) @ q.astype(np.float64)
    else:
        a = bank.astype(np.float64)
        norm = np.linalg.norm(a,axis=1)*np.linalg.norm(q.astype(np.float64))
        s = np.divide(a @ q.astype(np.float64), norm, out=np.zeros(len(a)),where=norm>0)
    return np.lexsort((np.arange(len(bank)), -s))[:k]

oldcwd = Path.cwd()
with tempfile.TemporaryDirectory() as temporary:
    os.chdir(temporary)
    bank = rng.normal(size=(2048,16)).astype(np.float32)
    bank *= rng.uniform(.15,3,size=(2048,1)).astype(np.float32)
    bank[1] = bank[0]
    bank[2] = 0
    xbin_write(bank, 'vectors.bin')
    queries = np.vstack([bank[:3],rng.normal(size=(8,16)).astype(np.float32)])
    params = dict(nlist=8,pq_m=4,pq_bits=4,train_size=2048,threads=1)
    for metric in ['euclidean','ip','angular']:
        ds = LocalDataset('vectors.bin',metric)
        base = HingeZeroFullANN(metric,dict(params,mode='without_hz'))
        base.fit(ds)
        full = HingeZeroFullANN(metric,dict(params,mode='full'))
        assert full.load_index(ds)
        narrow = dict(nprobe=8,candidates=32,expansion_candidates=16,rounds=1,steps=8)
        base.set_query_arguments(narrow)
        full.set_query_arguments(narrow)
        original = queries.copy()
        base_result = base.query(queries,10)
        full_result = full.query(queries,10)
        assert np.array_equal(queries,original)
        assert base.stats['seed_reads'] == full.stats['seed_reads'] == len(queries)*32
        assert full.stats['seed_score_regressions'] == 0
        for query, baseline_ids, full_ids in zip(queries,base_result,full_result):
            assert np.all(full._scores(bank[full_ids],query) >= base._scores(bank[baseline_ids],query) - 1e-12)
            checks += 1
        assert full.stats['refinement_route_events'] == len(queries)
        checks += 3
        for algo in [base,full]:
            results = algo.get_results()
            assert results.shape == (len(queries),10)
            assert results.min() >= 0 and results.max() < len(bank)
            for q, ids in zip(queries,results):
                assert len(set(ids.tolist())) == 10
                scored = algo._scores(bank[ids],q)
                assert np.all(np.diff(scored) <= 1e-12)
                checks += 1
        full.set_query_arguments(dict(nprobe=8,candidates=2048,rounds=1,steps=8))
        full_result = full.query(queries,10)
        for q, ids in zip(queries,full_result):
            assert np.array_equal(ids, exact(bank,q,metric,10))
            checks += 1
        assert full.stats['retention_events'] == len(queries)
        assert full.stats['witness_checks'] == len(queries)*12
        assert full.stats['failed_checks'] == 0
        report[metric] = {'queries':len(queries),'all_candidate_exact_checks':len(queries),'witness_checks':full.stats['witness_checks']}
        for mode in ['zero_steps','no_retention','query_expansion']:
            control = HingeZeroFullANN(metric,dict(params,mode=mode))
            assert control.load_index(ds)
            control.set_query_arguments(dict(nprobe=8,candidates=64,rounds=1,steps=8))
            assert control.query(queries[:2],10).shape == (2,10)
            checks += 1
    route_outputs = {}
    for mode in ['full','zero_steps']:
        algo = HingeZeroFullANN('euclidean',dict(params,mode=mode))
        assert algo.load_index(LocalDataset('vectors.bin','euclidean'))
        algo.set_query_arguments(dict(nprobe=8,candidates=32,expansion_candidates=16,rounds=1,steps=8,commit_margin=100.0,route_mix=0.5,retention_mix=0.2))
        captured = []
        def fake_search(query,count):
            captured.append(np.asarray(query).copy())
            return np.arange(32,dtype=np.int64) if len(captured)==1 else np.arange(32,48,dtype=np.int64)
        algo._initial_ids = fake_search
        output = algo.query(queries[3:4],10)
        assert algo.stats['retention_commits']==0 and len(captured)==2
        assert algo.stats['seed_reads']==32 and algo.stats['extra_reads']==16
        route_outputs[mode] = captured[1]
        if mode=='full':assert algo.get_additional()['mean_refinement_shift'] > 1e-6
        else:assert algo.get_additional()['mean_refinement_shift'] < 1e-6
        checks += 3
    assert not np.allclose(route_outputs['full'],route_outputs['zero_steps'],rtol=1e-6,atol=1e-6)
    checks += 1
    for rounds,expansion in [(0,16),(1,0),(2,4)]:
        algo=HingeZeroFullANN('euclidean',dict(params,mode='full'))
        assert algo.load_index(LocalDataset('vectors.bin','euclidean'))
        algo.set_query_arguments(dict(nprobe=8,candidates=32,expansion_candidates=expansion,rounds=rounds,steps=8))
        assert algo.query(queries[3:5],10).shape==(2,10)
        assert algo.stats['seed_score_regressions']==0
        assert algo.stats['refinement_route_events']==2*(rounds if expansion else 0)
        checks += 3
    w = core.HingeZeroWitness(bank[:32],np.ones(32,np.float32))
    state = w.observe(core.HingeZeroState(0,w.memories[0]))
    loop = core.HingeZeroRetainingLoop(w,state)
    old = w.memories.copy()
    w.append_memories(bank[32:40])
    assert np.array_equal(old,w.memories[:32]) and w.verify(state)
    assert loop.step(disturbance=-2*state.state)['rolled_back']
    assert w.verify(loop.checkpoint)
    checks += 3
    os.chdir(oldcwd)
for mode in ['hingezero_full_v2','hingezero_no_hz_v2','hingezero_zero_steps_v2','hingezero_no_retention_v2','hingezero_query_expansion_v2']:
    definitions = get_definitions('hingezero_full_v2.yaml',1536,'openai-100K','euclidean',10)
    definitions = [d for d in definitions if d.algorithm==mode]
    assert len(definitions)==1 and len(definitions[0].query_argument_groups)==3
    instantiate_algorithm(definitions[0])
    checks += 1
summary = dict(passed=True, checks=checks, core_sha256=CORE_SHA256, metrics=report,
               data='synthetic correctness fixtures; no OpenAI/CASMI performance claims',
               versions=dict(python=sys.version.split()[0], numpy=np.__version__, faiss=faiss.__version__, h5py=h5py.__version__))
Path('hingezero_full_v2_test_results.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
