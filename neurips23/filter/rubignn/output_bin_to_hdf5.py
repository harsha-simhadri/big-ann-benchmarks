from __future__ import absolute_import

import h5py
import json
import os
import re
import numpy as np
import sys
import pandas as pd

def load_bin_result(path):
  results = np.fromfile(path,dtype=np.uint32)
  results = results[2:]
  results = results.reshape((-1,10))
  return results

def get_result_filename(dataset=None, count=None, build_args=None,algorithm=None,
                      query_arguments=None, neurips23track=None, runbook_path=None):
  d = ['results']
  if neurips23track and neurips23track != 'none':
      d.append('neurips23')
      d.append(neurips23track)
      if neurips23track == 'streaming':
          if runbook_path == None:
              raise RuntimeError('Need runbook_path to store results')
          else:
              d.append(os.path.split(runbook_path)[1])
  if dataset:
      d.append(dataset)
  if count:
      d.append(str(count))
  if algorithm:
      d.append(algorithm)

  if build_args:
    data = build_args + str(query_arguments)
    data = re.sub(r'\W+', '_', json.dumps(data, sort_keys=True)).strip('_')
    if len(data) > 150:
        data = data[-149:]
    d.append(data)
  return os.path.join(*d)

def add_results_to_h5py(f, search_type, results, count, suffix = ''):
    if search_type == "knn" or search_type == "knn_filtered":
        neighbors = f.create_dataset('neighbors' + suffix, (len(results), count), 'i', data = results)
    else:
        raise NotImplementedError()


def store_results(dataset, count, definition, query_arguments,
        attrs, results, search_type, neurips23track='filter', runbook_path=None):
    fn = get_result_filename(
        dataset, count, definition, query_arguments, neurips23track, runbook_path) + '.hdf5'
    head, tail = os.path.split(fn)
    if not os.path.isdir(head):
        os.makedirs(head)
    f = h5py.File(name=fn, mode='w', libver='latest')
    for k, v in attrs.items():
        f.attrs[k] = v


    add_results_to_h5py(f, search_type, results, count)
    f.close()

if __name__=="__main__":
  args=sys.argv[1:]
  #TODO: load metadata and bin result
  search_metadata_path = args[0]
  result_prefix=args[1]
  search_metadata=pd.read_csv(search_metadata_path,names=['result_bin_path','build_time','index_size','algo','dataset','best_search_time','name','query_argument','run_count','distance','type','count','search_times'])
  for _,row in search_metadata.iterrows():
    fn = get_result_filename(row['dataset'], row['count'], "R16_L80_SR80_",row['algo'],  row['query_argument'], 'filter', None) + '.hdf5'
    fn = os.path.join(result_prefix,fn)
    head, tail = os.path.split(fn)
    print(fn)
    name_with_para = "rubignn(('R16_L80_SR80', {{'search_list': {} }}))".format(row['query_argument'])
    attrs = {
        "best_search_time": row['best_search_time'],
        "name": name_with_para,
        "run_count": row['run_count'],
        "distance": row['distance'],
        "type": row['type'],
        "count": int(row['count']),
        "search_times": [float(x_) for x_ in str(row['search_times']).split(" ")],
        "build_time":row['build_time'],
        "index_size":row['index_size'],
        "algo":row['algo'],
        "dataset":row['dataset']
    }

    results = load_bin_result(row['result_bin_path'])
    if not os.path.isdir(head):
        os.makedirs(head)
    f = h5py.File(name=fn, mode='w', libver='latest')
    for k, v in attrs.items():
        f.attrs[k] = v
    add_results_to_h5py(f, row['type'], results, int(row['count']))
    f.close()




