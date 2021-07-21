import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--algorithm',
        required=True)
    parser.add_argument(
        '--threshold',
        default=10000,
        help='minimum QPS (10,000 T1/2,000 T2)',
        type=int)
    parser.add_argument(
        'csv',
        metavar='CSV',
        help='input csv')

    args = parser.parse_args()
    df = pd.read_csv(args.csv)

    print(df[(df.qps > args.threshold) & (df.algorithm == args.algorithm)].groupby(['algorithm', 'dataset']).max()[['recall/ap']])




