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
        '--csv',
        metavar='CSV',
        help='input csv')
    parser.add_argument(
        '--dataset',
        required=False)

    args = parser.parse_args()
    df = pd.read_csv(args.csv)

    if args.algorithm:
        df = df[df.algorithm == args.algorithm]
    if args.dataset:
        df = df[df.dataset == args.dataset]

    if args.metric == "qps":
        print(df[(df.qps > args.threshold)].groupby(['dataset', 'algorithm']).max()[['recall/ap']])
    elif args.metric == "recall":
        print(df[(df['recall/ap'] > args.threshold)].groupby(['dataset', 'algorithm']).max()[['qps']].sort_values(by=["dataset", "qps"], ascending=False))





