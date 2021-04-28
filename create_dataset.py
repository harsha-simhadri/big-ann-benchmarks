import argparse
from benchmark.datasets import DATASETS, get_dataset_fn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        choices=DATASETS.keys(),
        required=True)
    parser.add_argument(
        '--batchsize',
        default=10000000,
        type=int
        )
    args = parser.parse_args()
    fn = get_dataset_fn(args.dataset)
    DATASETS[args.dataset](fn, args.batchsize)
