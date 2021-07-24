import argparse
from benchmark.datasets import DATASETS

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        choices=DATASETS.keys(),
        required=True)
    parser.add_argument(
        '--skip-data',
        action='store_true',
        help='skip downloading base vectors')
    args = parser.parse_args()
    ds = DATASETS[args.dataset]()
    ds.prepare(True if args.skip_data else False)
