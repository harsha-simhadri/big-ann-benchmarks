import argparse
import numpy as np

from benchmark.datasets import DATASETS
from neurips23.streaming.load_runbook import load_runbook

def get_range_start_end(entry):
    return np.arange(entry['start']-1,  entry['end'], dtype=np.uint32)

def get_next_set(ids: np.ndarray, entry):
    range = get_range_start_end(entry)
    match entry['operation']:
        case 'insert':
            return np.union1d(ids, range)
        case 'delete':
            return np.setdiff1d(ids, range, assume_unique=True)
        case 'search':
            return ids
        case _:       
            raise ValueError('Undefined entry in runbook')

def output_gt(data, ids, Q, step):
    return

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
    args = parser.parse_args()

    ds = DATASETS[args.dataset]()
    max_pts = ds.nb
    ndims = ds.d
    runbook = load_runbook(args.dataset, max_pts, args.runbook_file)

    data = ds.get_dataset()
    ids = np.empty(0, dtype=np.uint32)

    if not args.private_query:
        Q = ds.get_queries()
    else:
        Q = ds.get_private_queries()

    step = 1
    for entry in runbook:
        if step == 1:
            ids = get_range_start_end(entry)
        else:
            ids = get_next_set(ids, entry)
        print(ids)
        output_gt(data[ids], ids, Q, step)
        step += 1

if __name__ == '__main__':
    main()