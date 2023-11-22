import argparse
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--algorithm',
        required=False)
    parser.add_argument(
        '--metric',
        choices=['qps', 'recall'],
        default='recall')
    parser.add_argument(
        '--threshold',
        default=0.9,
        help='threshold',
        type=float)
    parser.add_argument(
        'csv',
        metavar='CSV',
        help='input csv')

    args = parser.parse_args()
    df = pd.read_csv(args.csv)

    if args.algorithm:
        df == df[df.algorithm == args.algorithm]

    if args.metric == "qps":
        print(df[(df.qps > args.threshold)].groupby(['dataset', 'algorithm']).max()[['recall/ap']])
    elif args.metric == "recall":
        print(df[(df['recall/ap'] > args.threshold)].groupby(['dataset', 'algorithm']).max()[['qps']])





