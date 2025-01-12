import argparse
from benchmark.datasets import DATASETS
from benchmark.random_datasets_utils import parse_dataset

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        # choices=DATASETS.keys(),
        required=True)
    parser.add_argument(
        '--skip-data',
        action='store_true',
        help='skip downloading base vectors')
    parser.add_argument(
        '--eventrate',
        type=int,
        help='Event rate for congestion scenarios'
    )
    parser.add_argument(
        '--batchsize',
        type=int,
        help='Batch size for congestion scenarios'
    )

    args = parser.parse_args()
    ds = parse_dataset(args)
    ds.prepare(True if args.skip_data else False)
