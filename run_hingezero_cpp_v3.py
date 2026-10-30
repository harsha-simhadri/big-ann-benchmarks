from pathlib import Path
import argparse
import csv
import json
import os
import platform
import shutil
import time
import h5py
import numpy as np
import faiss
from benchmark.datasets import DATASETS
from benchmark.algorithms.definitions import get_definitions
from benchmark.runner import run
from benchmark.results import get_result_filename
from benchmark.plotting.metrics import get_recall_values

p=argparse.ArgumentParser(description='Run every public query using the corrected native HingeZero pipeline. No preflight or synthetic datasets are created.')
p.add_argument('--dataset',default='openai-100K',choices=sorted(DATASETS))
p.add_argument('--all-modes',action='store_true')
p.add_argument('--nprobe',type=int,default=32)
p.add_argument('--candidates',type=int,default=512)
p.add_argument('--expansion-candidates',type=int,default=256)
p.add_argument('--steps',type=int,default=8)
p.add_argument('--rounds',type=int,default=1)
p.add_argument('--threads',type=int,default=4)
p.add_argument('--batch-size',type=int,default=32)
p.add_argument('--route-mix',type=float,default=.10)
p.add_argument('--retention-mix',type=float,default=.20)
p.add_argument('--no-score',action='store_true',help='Produce complete retrieval outputs without reading ground truth.')
a=p.parse_args()
if min(a.nprobe,a.threads,a.batch_size,a.candidates)<1 or min(a.steps,a.rounds,a.expansion_candidates)<0:
    raise SystemExit('Invalid search configuration.')
ds=DATASETS[a.dataset]()
if ds.search_type()!='knn' or ds.data_type()!='dense':
    raise SystemExit('This entry supports dense static k-NN datasets.')
if not Path(ds.get_dataset_fn()).is_file():
    raise SystemExit('Existing dataset bank is missing. No replacement data is generated.')
queries=ds.get_queries()
if queries.shape!=(ds.nq,ds.d):
    raise SystemExit('Public query matrix is incomplete or has an unexpected dimension.')
del queries
print(f'[HZ C++] Full task: {a.dataset}; bank={ds.nb:,}; queries={ds.nq:,}; d={ds.d}; metric={ds.distance()}',flush=True)
names=['hingezero_cpp_full_v3']
if a.all_modes:
    names=['hingezero_cpp_no_hz_v3','hingezero_cpp_full_v3','hingezero_cpp_zero_steps_v3','hingezero_cpp_no_retention_v3','hingezero_cpp_query_expansion_v3']
definitions=get_definitions('hingezero_cpp_v3.yaml',ds.d,a.dataset,ds.distance(),10)
stamp=time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'-'+str(os.getpid())
output=Path('results/hingezero_cpp_v3_reports')/stamp
output.mkdir(parents=True)
records=[]
groundtruth=None
score_available=not a.no_score
for name in names:
    definition=next(x for x in definitions if x.algorithm==name)
    build_args=[dict(x,threads=a.threads,batch_size=a.batch_size) if isinstance(x,dict) else x for x in definition.arguments]
    search=dict(nprobe=a.nprobe,candidates=a.candidates,expansion_candidates=a.expansion_candidates,steps=a.steps,rounds=a.rounds,
                batch_size=a.batch_size,alpha=4.5,eps=.10,lam=.02,commit_margin=.10,route_mix=a.route_mix,retention_mix=a.retention_mix)
    definition=definition._replace(arguments=build_args,query_argument_groups=[[search]])
    result_path=Path(get_result_filename(a.dataset,10,definition,[search])+'.hdf5')
    if result_path.is_file():
        backup=output/'previous_results'/result_path.relative_to('results')
        backup.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(result_path,backup)
    run(definition,a.dataset,10,1,False)
    with h5py.File(result_path) as f:
        neighbors=f['neighbors'][:]
        attrs=dict(f.attrs)
    if neighbors.shape!=(ds.nq,10):
        raise RuntimeError('Runner did not complete every public query.')
    if np.any(neighbors<0) or np.any(neighbors>=ds.nb):
        raise RuntimeError('Runner produced invalid global neighbour IDs.')
    elapsed=float(attrs['best_search_time'])
    rec=dict(algorithm=name,dataset=a.dataset,query_count=ds.nq,bank_count=ds.nb,recall_at_10=None,
             qps=ds.nq/elapsed,search_seconds=elapsed,build_seconds=float(attrs['build_time']),index_delta_kib=float(attrs['index_size']),
             result_file=str(result_path),scope='all public queries; official runner; corrected C++ v3 pipeline',
             python=platform.python_version(),numpy=np.__version__,faiss=faiss.__version__,h5py=h5py.__version__)
    for key,value in attrs.items():
        if key.startswith(('hz_','native_','mean_')) or key in ('witness_checks','retention_events','retention_commits','append_checks','failed_checks',
                'refinement_route_events','seed_score_regressions','original_metric_evaluations','output_record_checks','index_searches',
                'faiss_batch_calls','raw_bank_bytes','index_disk_bytes','candidate_backend','bank_storage'):
            rec[key]=value.item() if hasattr(value,'item') else value
    if score_available:
        if groundtruth is None:
            try:
                groundtruth=ds.get_groundtruth()
            except (FileNotFoundError,OSError) as e:
                print('[HZ C++] Retrieval completed; ground truth unavailable, so recall is unscored: '+str(e),flush=True)
                score_available=False
        if groundtruth is not None:
            if groundtruth[0].shape[0]!=ds.nq or groundtruth[0].min()<0 or groundtruth[0].max()>=ds.nb:
                raise RuntimeError('Ground-truth IDs or query count do not match this bank.')
            recall,_,_,ties=get_recall_values(groundtruth,neighbors,10)
            rec['recall_at_10']=float(recall)
            rec['queries_with_ties']=int(ties)
    records.append(rec)
    keys=sorted(set().union(*(r.keys() for r in records)))
    with (output/'summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(records)
    (output/'summary.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(rec),flush=True)
print('\nSaved report: '+str(output/'summary.csv'),flush=True)
print('All public queries processed. Ground truth was used only after retrieval, for scoring; no sampled preflight or synthetic dataset was run.',flush=True)
