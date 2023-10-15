from __future__ import absolute_import

import h5py
import json
import os
import re
import traceback

def get_result_filename(dataset=None, count=None, definition=None,
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
    if definition:
        d.append(definition.algorithm)
        build_args = definition.arguments
        try:
            for args in build_args:
                if type(args) == dict and 'indexkey' in args:
                    build_args = [args['indexkey']]
        except:
                pass
        data = build_args + query_arguments
        data = re.sub(r'\W+', '_', json.dumps(data, sort_keys=True)).strip('_')
        if len(data) > 150:
            data = data[-149:]
        d.append(data)
    return os.path.join(*d)


def add_results_to_h5py(f, search_type, results, count, suffix = ''):
    if search_type == "knn" or search_type == "knn_filtered":
        neighbors = f.create_dataset('neighbors' + suffix, (len(results), count), 'i', data = results)
    elif search_type == "range":
        lims, D, I= results
        f.create_dataset('neighbors' + suffix, data=I)
        f.create_dataset('lims' + suffix, data=lims)
        f.create_dataset('distances' + suffix, data=D)
    else:
        raise NotImplementedError()

def store_results(dataset, count, definition, query_arguments,
        attrs, results, search_type, neurips23track=None, runbook_path=None):
    fn = get_result_filename(
        dataset, count, definition, query_arguments, neurips23track, runbook_path) + '.hdf5'
    head, tail = os.path.split(fn)
    if not os.path.isdir(head):
        os.makedirs(head)
    f = h5py.File(name=fn, mode='w', libver='latest')
    for k, v in attrs.items():
        f.attrs[k] = v

    if neurips23track == 'streaming':
        for i, step_results in enumerate(results):
            step = attrs['step_' + str(i)]
            add_results_to_h5py(f, search_type, step_results, count, '_step' + str(step))
    else:
        add_results_to_h5py(f, search_type, results, count)
    f.close()


def load_all_results(dataset=None, count=None, neurips23track=None, runbook_path=None):
    """
    A generator for all result files.
    """
    for root, _, files in os.walk(get_result_filename(dataset, count, \
                                                      neurips23track=neurips23track, \
                                                    runbook_path=runbook_path)):
        for fn in files:
            if os.path.splitext(fn)[-1] != '.hdf5':
                continue
            try:
                f = h5py.File(name=os.path.join(root, fn), mode='r+', libver='latest')
                properties = dict(f.attrs)
                yield properties, f
                f.close()
            except:
                print('Was unable to read', fn)
                traceback.print_exc()


def get_unique_algorithms():
    return set(properties['algo'] for properties, _ in load_all_results())
