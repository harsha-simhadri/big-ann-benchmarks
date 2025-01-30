import argparse
import os
import numpy as np

import sys
[sys.path.append(i) for i in ['.', '..']]

from benchmark.datasets import DATASETS
from benchmark.congestion.load_runbook import load_runbook_congestion

def get_range_start_end(entry, tag_to_id):
    for i in range(entry['end'] - entry['start']):
        tag_to_id[i+entry['start']] = i+entry['start']
    return tag_to_id

def get_next_set(tag_to_id: np.ndarray, entry):
    match entry['operation']:
        case 'initial':
            for i in range(entry['end'] - entry['start']):
                tag_to_id[i + entry['start']] = i + entry['start']
            return tag_to_id
        case 'insert':
            for i in range(entry['end'] - entry['start']):
                tag_to_id[i+entry['start']] = i+entry['start']
            return tag_to_id
        case 'delete':
            # delete is by key 
            for i in range(entry['end'] - entry['start']):
                tag_to_id.pop(i + entry['start'])
            return tag_to_id
        case 'batch_insert':
            for i in range(entry['end'] - entry['start']):
                tag_to_id[i + entry['start']] = i + entry['start']
            return tag_to_id
        case 'replace':
            # replace key with value
            for i in range(entry['tags_end'] - entry['tags_start']):
                tag_to_id[i + entry['tags_start']] = entry['ids_start'] + i
            return tag_to_id
        case 'search':
            return tag_to_id
        case 'startHPC':
            return tag_to_id
        case 'endHPC':
            return tag_to_id
        case 'waitPending':
            return tag_to_id
        case 'enableScenario':
            return tag_to_id
        case _:       
            raise ValueError('Undefined entry in runbook')
        
def gt_dir(ds, runbook_path):
    runbook_filename = os.path.split(runbook_path)[1]
    return os.path.join(ds.basedir, str(ds.nb), runbook_filename)

def output_gt(ds, tag_to_id, step, gt_cmdline, runbook_path):
    ids_list = []
    tags_list = []
    for tag, id in tag_to_id.items():
        ids_list.append(id)
        tags_list.append(tag)

    ids = np.array(ids_list, dtype = np.uint32)
    tags = np.array(tags_list, dtype = np.uint32)


    data = ds.get_data_in_range(0, ds.nb)
    data_slice = data[np.array(ids)]

    dir = gt_dir(ds, runbook_path)
    prefix = os.path.join(dir, 'step') + str(step) 
    os.makedirs(dir, exist_ok=True)

    tags_file = prefix + '.tags'
    data_file = prefix + '.data'
    gt_file = prefix + '.gt100'

    with open(tags_file, 'wb') as tf:
        one = 1
        tf.write(tags.size.to_bytes(4, byteorder='little'))
        tf.write(one.to_bytes(4, byteorder='little'))
        tags.tofile(tf)    
    with open(data_file, 'wb') as f:
        f.write(ids.size.to_bytes(4, byteorder='little')) #npts
        f.write(ds.d.to_bytes(4, byteorder='little'))
        data_slice.tofile(f)
    
    gt_cmdline += ' --base_file ' + data_file 
    gt_cmdline += ' --gt_file ' + gt_file
    gt_cmdline += ' --tags_file ' + tags_file
    print("Executing cmdline: ", gt_cmdline)
    os.system(gt_cmdline)
    print("Removing data file")
    rm_cmdline = "rm " + data_file
    os.system(rm_cmdline)


def output_gt_batch(ds, tag_to_id, num_batch_insert, step, gt_cmdline, runbook_path, batchSize):
    if batchSize==2500 and runbook_path!='neurips23/runbooks/congestion/test_experiment.yaml' and runbook_path!="neurips23/runbooks/congestion/general_experiment/general_experiment.yaml":
        return

    ids_list = []
    tags_list = []
    for tag, id in tag_to_id.items():
        ids_list.append(id)
        tags_list.append(tag)

    ids = np.array(ids_list, dtype=np.uint32)
    tags = np.array(tags_list, dtype=np.uint32)

    data = ds.get_data_in_range(0, ds.nb)
    data_slice = data[np.array(ids)]

    dir = gt_dir(ds, runbook_path)
    prefix = os.path.join(dir, 'batch') + str(num_batch_insert)+"_"+str(step)
    os.makedirs(dir, exist_ok=True)

    tags_file = prefix + '.tags'
    data_file = prefix + '.data'
    gt_file = prefix + '.gt100'

    with open(tags_file, 'wb') as tf:
        one = 1
        tf.write(tags.size.to_bytes(4, byteorder='little'))
        tf.write(one.to_bytes(4, byteorder='little'))
        tags.tofile(tf)
    with open(data_file, 'wb') as f:
        f.write(ids.size.to_bytes(4, byteorder='little'))  # npts
        f.write(ds.d.to_bytes(4, byteorder='little'))
        data_slice.tofile(f)

    gt_cmdline += ' --base_file ' + data_file
    gt_cmdline += ' --gt_file ' + gt_file
    gt_cmdline += ' --tags_file ' + tags_file
    print("Executing cmdline: ", gt_cmdline)
    os.system(gt_cmdline)
    print("Removing data file")
    rm_cmdline = "rm " + data_file
    os.system(rm_cmdline)

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--dataset',
        choices=DATASETS.keys(),
        help=f'Dataset to benchmark on.',
        required=True)
    parser.add_argument(
        '--runbook_file',
        help='Runbook yaml file path'
    )
    parser.add_argument(
        '--private_query',
        action='store_true'
    )
    parser.add_argument(
        '--gt_cmdline_tool',
        required=True
    )
    parser.add_argument(
        '--download',
        action='store_true'
    )
    args = parser.parse_args()

    ds = DATASETS[args.dataset]()
    max_pts, runbook = load_runbook_congestion(args.dataset, ds.nb, args.runbook_file)
    query_file = ds.qs_fn if args.private_query else ds.qs_fn
    
    common_cmd = args.gt_cmdline_tool + ' --dist_fn ' 
    match ds.distance():
        case 'euclidean':
            common_cmd += 'l2'
        case 'ip':
            common_cmd += 'mips'
        case _:
            raise RuntimeError('Invalid metric')
    common_cmd += ' --data_type '
    match ds.dtype:
        case 'float32':
            common_cmd += 'float'
        case 'int8':
            common_cmd += 'int8'
        case 'uint8':
            common_cmd += 'uint8'
        case _:
            raise RuntimeError('Invalid datatype')
    common_cmd += ' --K 100'
    common_cmd += ' --query_file ' + os.path.join(ds.basedir, query_file)

    step = 1
    ids = np.empty(0, dtype=np.uint32)
    num_batch_insert = 0
    for entry in runbook[1:]:
        # the first step must be an HPC and second must be initial
        if step == 1:
            tag_to_id = get_range_start_end(entry, {})
        elif (entry['operation']!='batch_insert'):
            tag_to_id = get_next_set(tag_to_id, entry)
        if (entry['operation'] == 'search'):
            output_gt(ds, tag_to_id, step, common_cmd, args.runbook_file)
        if (entry['operation'] == 'batch_insert'):
            batchSize = entry['batchSize']
            end = entry['end']
            start = entry['start']
            batch_step = (end - start) // batchSize
            continuous_counter = 0
            for i in range(batch_step):


                for j in range(start+i*batchSize,start+(i+1)*batchSize):
                    tag_to_id[j] = j

                continuous_counter+=batchSize
                if(continuous_counter>=(end-start)/100):
                    print(f"{i}: {start + i * batchSize}~{start + (i + 1) * batchSize} output gt")
                    output_gt_batch(ds, tag_to_id, num_batch_insert, i, common_cmd, args.runbook_file, batchSize)
                    continuous_counter = 0

            if (start + batch_step * batchSize < end and start + (batch_step + 1) * batchSize > end):

                for j in range(start+batch_step*batchSize,end):
                    tag_to_id[j] = j

                continuous_counter+=batchSize
                if(continuous_counter>=(end-start)/100):
                    print(f"{batch_step}: {start + batch_step * batchSize}~{end} output gt")
                    output_gt_batch(ds, tag_to_id, num_batch_insert, batch_step, common_cmd, args.runbook_file, batchSize)
                    continuous_counter = 0

            num_batch_insert += 1

        step += 1

if __name__ == '__main__':
    main()