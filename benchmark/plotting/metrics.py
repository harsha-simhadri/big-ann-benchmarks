from __future__ import absolute_import
import numpy as np


def get_recall_values(true_nn, run_nn, count):
    true_nn = true_nn[:, :count]
    assert true_nn.shape == run_nn.shape
    recalls = np.zeros(len(run_nn))
    # TODO probably not very efficient
    for i in range(len(run_nn)):
        recalls[i] = len(set(true_nn[i]) & set(run_nn[i]))
    return (np.mean(recalls) / float(count),
            np.std(recalls) / float(count),
            recalls)

def knn(true_nn, run_nn, count, metrics):
    if 'knn' not in metrics:
        print('Computing knn metrics')
        knn_metrics = metrics.create_group('knn')
        mean, std, recalls = get_recall_values(true_nn, run_nn, count)
        knn_metrics.attrs['mean'] = mean
        knn_metrics.attrs['std'] = std
        knn_metrics['recalls'] = recalls
    else:
        print("Found cached result")
    return metrics['knn']


def queries_per_second(queries, attrs):
    return len(queries) / attrs["best_search_time"]


def index_size(queries, attrs):
    return attrs.get("index_size", 0)


def build_time(queries, attrs):
    return attrs.get("build_time", 1e6)


def dist_computations(queries, attrs):
    return attrs.get("dist_comps", 0) / (attrs['run_count'] * len(queries))

def watt_seconds_per_query(queries, attrs):

    # query set was run many times ( queries )
    tot_queries = len(queries) * attrs["power_run_count"]

    # power consumption during that time ( watt * seconds )
    tot_power_cons = attrs["power_consumption"]

    # we want (watt*second)/query
    # ie, energy use per query
    calc = tot_power_cons/tot_queries

    return calc

all_metrics = {
    "k-nn": {
        "description": "Recall",
        "function": lambda true_nn, run_nn, metrics, run_attrs: knn(true_nn, run_nn, run_attrs["count"], metrics).attrs['mean'],  # noqa
        "worst": float("-inf"),
        "lim": [0.0, 1.03]
    },
    "qps": {
        "description": "Queries per second (1/s)",
        "function": lambda true_nn, run_nn, metrics, run_attrs: queries_per_second(true_nn, run_attrs),  # noqa
        "worst": float("-inf")
    },
    "distcomps": {
        "description": "Distance computations",
        "function": lambda true_nn, run_nn,  metrics, run_attrs: dist_computations(true_nn, run_attrs), # noqa
        "worst": float("inf")
    },
    "build": {
        "description": "Build time (s)",
        "function": lambda true_nn, run_nn, metrics, run_attrs: build_time(true_nn, run_attrs), # noqa
        "worst": float("inf")
    },
    "indexsize": {
        "description": "Index size (kB)",
        "function": lambda true_nn, run_nn, metrics, run_attrs: index_size(true_nn, run_attrs),  # noqa
        "worst": float("inf")
    },
    "queriessize": {
        "description": "Index size (kB)/Queries per second (s)",
        "function": lambda true_nn, run_nn, metrics, run_attrs: index_size(true_nn, run_attrs) / queries_per_second(true_nn, run_attrs), # noqa
        "worst": float("inf")
    },
    "wspq": {
        "description": "Watt seconds per query (watt*s/query)",
        "function": lambda true_nn, run_nn, metrics, run_attrs: watt_seconds_per_query(true_nn, run_attrs),  # noqa
        "worst": float("-inf")
    },

}
