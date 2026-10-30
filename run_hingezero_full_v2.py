from pathlib import Path
import argparse
import json
import time
import os
import csv
import h5py
import numpy as np
from benchmark.datasets import DATASETS
from benchmark.algorithms.definitions import get_definitions, instantiate_algorithm
from benchmark.runner import run
from benchmark.results import get_result_filename
from benchmark.plotting.metrics import get_recall_values

p = argparse.ArgumentParser()
p.add_argument('--dataset', default='openai-100K', choices=sorted(DATASETS))
p.add_argument('--preflight', action='store_true')
p.add_argument('--sweep', action='store_true')
p.add_argument('--runs', type=int, default=1)
p.add_argument('--nprobe', type=int, default=32)
p.add_argument('--all-modes', action='store_true')
p.add_argument('--candidates',type=int,default=512)
p.add_argument('--expansion-candidates',type=int,default=256)
p.add_argument('--steps',type=int,default=8)
p.add_argument('--rounds',type=int,default=1)
p.add_argument('--route-mix',type=float,default=.10)
p.add_argument('--retention-mix',type=float,default=.20)
a = p.parse_args()
if a.runs < 1 or a.nprobe < 1 or a.candidates < 10 or min(a.expansion_candidates,a.steps,a.rounds)<0:
    raise SystemExit('runs and nprobe must be positive')
ds = DATASETS[a.dataset]()
if ds.search_type() != 'knn' or ds.data_type() != 'dense':
    raise SystemExit('This package supports dense static k-NN datasets.')
try:
    filename = ds.get_dataset_fn()
except (RuntimeError, FileNotFoundError) as error:
    raise SystemExit(str(error) + '\nPrepare this dataset with create_dataset.py before running.')
if not Path(filename).is_file():
    raise SystemExit('Dataset file is missing: '+ str(filename))
queries = ds.get_queries()
groundtruth = ds.get_groundtruth()
if queries.shape != (ds.nq,ds.d) or groundtruth[0].shape[0] != len(queries):
    raise SystemExit('Query or ground-truth shape disagrees with the dataset definition.')
if groundtruth[0].min() < 0 or groundtruth[0].max() >= ds.nb:
    raise SystemExit('Ground truth contains IDs outside this dataset subset.')
print(f'Dataset: {a.dataset}, bank={ds.nb:,}, dimension={ds.d}, queries={ds.nq:,}, metric={ds.distance()}',flush=True)
definitions = get_definitions('hingezero_full_v2.yaml',ds.d,a.dataset,ds.distance(),10)
wanted = ['hingezero_no_hz_v2','hingezero_full_v2']
if a.all_modes:
    wanted += ['hingezero_zero_steps_v2','hingezero_no_retention_v2','hingezero_query_expansion_v2']
definitions = [next(d for d in definitions if d.algorithm == name) for name in wanted]
stamp = time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()) + '-' + str(os.getpid())
output = Path('results/hingezero_full_v2_reports') / (stamp + ('-preflight' if a.preflight else '-benchmark'))
output.mkdir(parents=True)
records = []
if a.preflight:
    ids = np.linspace(0,len(queries)-1,min(64,len(queries)),dtype=np.int64)
    for definition in definitions:
        algo = instantiate_algorithm(definition)
        build_start = time.perf_counter()
        loaded = algo.load_index(a.dataset)
        if not loaded:
            algo.fit(a.dataset)
        build_seconds = time.perf_counter()-build_start
        search = dict(nprobe=a.nprobe,candidates=a.candidates,expansion_candidates=a.expansion_candidates,retention_mix=a.retention_mix,rounds=a.rounds,steps=a.steps,alpha=4.5,eps=.10,lam=.02,commit_margin=.10,route_mix=a.route_mix)
        algo.set_query_arguments(search)
        start = time.perf_counter()
        neighbors = algo.query(queries[ids],10)
        elapsed = time.perf_counter()-start
        recall,_,_,ties = get_recall_values((groundtruth[0][ids],groundtruth[1][ids]),neighbors,10)
        rec = dict(algorithm=definition.algorithm,dataset=a.dataset,query_count=len(ids),recall_at_10=float(recall),qps=len(ids)/elapsed,search_seconds=elapsed,build_or_load_seconds=build_seconds,index_loaded=loaded,nprobe=a.nprobe,queries_with_ties=ties,scope='64-query preflight sample, not a full benchmark')
        rec.update(algo.get_additional())
        records.append(rec)
        print(json.dumps(rec),flush=True)
        algo.done()
        del algo
else:
    del queries
    for definition in definitions:
        groups = definition.query_argument_groups if a.sweep else [[dict(nprobe=a.nprobe,candidates=a.candidates,expansion_candidates=a.expansion_candidates,retention_mix=a.retention_mix,rounds=a.rounds,steps=a.steps,alpha=4.5,eps=.10,lam=.02,commit_margin=.10,route_mix=a.route_mix)]]
        definition = definition._replace(query_argument_groups=groups)
        targets = [Path(get_result_filename(a.dataset,10,definition,g)+'.hdf5') for g in groups]
        for file in targets:
            if file.is_file():
                old = output / 'previous_results' / file.relative_to('results')
                old.parent.mkdir(parents=True,exist_ok=True)
                import shutil
                shutil.copy2(file,old)
        run(definition,a.dataset,10,a.runs,False)
        for args,file in zip(groups,targets):
            with h5py.File(file) as f:
                neighbors = f['neighbors'][:]
                if neighbors.shape != (ds.nq,10):
                    raise RuntimeError('Runner returned an incomplete result matrix')
                mean,_,_,ties = get_recall_values(groundtruth,neighbors,10)
                attrs = dict(f.attrs)
            rec = dict(algorithm=definition.algorithm,dataset=a.dataset,query_count=ds.nq,recall_at_10=float(mean),qps=ds.nq/float(attrs['best_search_time']),search_seconds=float(attrs['best_search_time']),build_seconds=float(attrs['build_time']),index_delta_kib=float(attrs['index_size']),nprobe=args[0]['nprobe'],queries_with_ties=ties,result_file=str(file),scope='full public query set; official runner; local hardware')
            for key,value in attrs.items():
                if key.startswith('hz_') or key in ('raw_bank_bytes','index_disk_bytes','candidate_backend','bank_storage','witness_checks','retention_events','retention_commits','append_checks','failed_checks','mean_candidate_reads','mean_seed_candidate_reads','mean_extra_candidate_reads','mean_refinement_shift','refinement_route_events','index_searches','seed_score_regressions'):
                    rec[key] = value.item() if hasattr(value,'item') else value
            records.append(rec)
            print(json.dumps(rec),flush=True)
keys = sorted(set().union(*(r.keys() for r in records)))
with (output/'summary.csv').open('w',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=keys)
    writer.writeheader()
    writer.writerows(records)
(output/'summary.json').write_text(json.dumps(records,indent=2))
print('\nSaved report:', output/'summary.csv',flush=True)
print('Preflight is a sampled check. Full runs include every public query. No query labels are used by the algorithm.',flush=True)
