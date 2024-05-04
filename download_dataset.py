import argparse
from benchmark.datasets import DATASETS

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--dataset',
        choices=DATASETS.keys(),
        required=True)
    parser.add_argument(
        '--num_vectors',
        type=int,
        help='skip downloading base vectors')
    args = parser.parse_args()
    ds = DATASETS[args.dataset]()
    npts = args.num_vectors
    ds.download_slice(num_vectors=npts)
