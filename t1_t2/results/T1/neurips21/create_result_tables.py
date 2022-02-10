from math import ceil
import pandas as pd
import sys

def get_pareto_frontier(df, x, y, split, ascending=False):
    # removes all rows that don't lie on the pareto frontier
    to_plot = df.sort_values(y,ascending=ascending).reset_index(drop=True)
    d = {} # store last x values
    drop_list = []
    for algo in set(df[split]):
        d[algo] = 0
    for i in range(len(to_plot)):
        x_ = to_plot.iloc[i][x]
        y_ = to_plot.iloc[i][y]
        algo = to_plot.iloc[i][split]
        if x_ > d[algo]:
            d[algo] = x_
        else:
            drop_list.append(i)
    to_plot.drop(drop_list, inplace=True)

    return to_plot

df = pd.read_csv(sys.argv[1])
outputdir = sys.argv[2]

df['dslabel'] = df.apply(lambda row: row.dataset + str(row["count"]), axis = 1)
df['qps*buildtime'] = df.apply(lambda row: row.qps * row.build, axis = 1)

datasets = set(df.dataset)
algorithms = set(df.algorithm)

for dataset in datasets:
    for count in [10]:
        for x_metric in ['recall_ap' ]:
            for y_metric in ['qps']:
                test_df = df[(df.dataset == dataset) & (df["count"] == count)]
                test_df = get_pareto_frontier(test_df, x_metric, y_metric, "algorithm", y_metric == 'queriessize')
                for algorithm in set(test_df.algorithm):
                    fn = "%s_%d_%s_%s_%s" % (dataset, count, algorithm, x_metric, y_metric)
                    with open("%s/%s" % (outputdir, fn), 'w') as f:
                        for x, y in test_df[test_df.algorithm == algorithm][[x_metric, y_metric]].itertuples(index=False):
                            f.write("%f %f\n" % (x, y))

algorithms = set(df.algorithm)

for algorithm in algorithms:
        for x_metric in ['recall_ap' ]:
            for y_metric in ['qps', 'build', 'queriessize', 'qps*buildtime']:
                test_df = df[(df.algorithm == algorithm)]
                test_df = get_pareto_frontier(test_df, x_metric, y_metric, "dslabel", y_metric == 'queriessize')
                for dataset in set(test_df.dataset):
                    for count in [10, 100]:
                        fn = "%s_%s_%d_%s_%s" % (algorithm, dataset, count, x_metric, y_metric)
                        with open("%s/%s" % (outputdir, fn), 'w') as f:
                            for x, y in test_df[(test_df.dataset == dataset) & (test_df["count"] == count)][[x_metric, y_metric]].itertuples(index=False):
                                f.write("%f %f\n" % (x, y))


