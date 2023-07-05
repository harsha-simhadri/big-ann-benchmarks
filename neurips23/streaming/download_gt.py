import argparse
import os

from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
from neurips23.streaming.load_runbook import load_runbook, get_gt_url
from neurips23.streaming.compute_gt import gt_dir


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
    args = parser.parse_args()

    ds = DATASETS[args.dataset]()
    print(args.runbook_file)
    runbook = load_runbook(args.dataset, ds.nb, args.runbook_file)
    gt_url = get_gt_url(args.dataset, args.runbook_file)

    download_dir = gt_dir(ds, args.runbook_file)
    os.makedirs(download_dir, exist_ok=True)
    for step, entry in enumerate(runbook):
        if entry['operation'] == 'search':
            step_url=gt_url + '/step' + str(step+1) + '.gt100'
            download_accelerated(step_url, download_dir)


if __name__ == '__main__':
    main()