import argparse
import os
import numpy as np
import yaml

import sys
[sys.path.append(i) for i in ['.', '..', '../..']]

from scipy.cluster.vq import vq, kmeans2
from typing import Tuple
from benchmark.datasets import DATASETS
from benchmark.streaming.load_runbook import load_runbook

#extract cluster information from msturing-10M-clustered
def extract_clusters(runbook_path, max_pts, ds_name):    
    max_pts, run_list = load_runbook(ds_name, max_pts, runbook_path)
    clusters = []
    for entry in run_list:
        match entry['operation']:
            case 'insert':
                clusters.append((entry['start'], entry['end']))
            case _:
                continue
    return clusters
            


# runbook will do the following: 
# 1) insert a random fraction > .5 of each of the 32 clusters with searches interleaved
# 2) for each cluster, replace its beginning prefix with a random fraction of the remaining 
#    points with searches interleaved
def write_replace_clustered_runbook(clusters, output_yaml_file, dataset_str):
    inserted_clusters = []
    operation_list = []
    max_pts = 0
    num_operations = 1
    active_points = 0
    # add seed to make operation deterministic
    np.random.seed(0)

    #step 1: insert
    for cluster in clusters:
        fraction = np.random.uniform(.5, .9)
        delta = int(fraction*(cluster[1]-cluster[0]))
        active_points += delta
        max_pts = max(max_pts, active_points)
        cluster_to_insert = (cluster[0], cluster[0]+delta)
        inserted_clusters.append(cluster_to_insert)
        entry = {'operation': 'insert','start': int(cluster_to_insert[0]), 'end': int(cluster_to_insert[1])}
        operation_list.append((num_operations, entry))
        num_operations += 1
        operation_list.append((num_operations, {'operation': str('search')}))
        num_operations += 1

    #step 2: replace
    for inserted_cluster, full_cluster in zip(inserted_clusters, clusters):
        fraction = np.random.uniform(0,1.0)
        delta = int(fraction*(full_cluster[1] - inserted_cluster[1]))
        assert delta <= inserted_cluster[1] - inserted_cluster[0]
        replace_tags_start = inserted_cluster[0]
        replace_tags_end = replace_tags_start + delta
        replace_ids_start = inserted_cluster[1]
        replace_ids_end =  inserted_cluster[1] + delta
        entry = {'operation': 'replace', 'tags_start': replace_tags_start, 'tags_end': replace_tags_end, 'ids_start': replace_ids_start, 'ids_end': replace_ids_end}
        operation_list.append((num_operations, entry))
        num_operations += 1
        operation_list.append((num_operations, {'operation': str('search')}))
        num_operations += 1

    #write to yaml file
    with open(output_yaml_file, 'w') as yf:
        operation_list.sort(key = lambda x: x[0])
        sorted_dict = {}
        sorted_dict['max_pts'] = int(max_pts)
        for (k, v) in operation_list:
            sorted_dict[k]=v
        yaml_object = {}
        yaml_object[dataset_str] = sorted_dict
        yaml.dump(yaml_object, yf)



# runbook will do the following:
# 1) insert a random fraction > .5 of each of the 32 clusters with searches interleaved
# 2) for each cluster, select a *random* cluster and replace its beginning prefix 
#    with a random fraction of remaining points in that cluster with searches interleaved
def write_replace_random_runbook(clusters, output_yaml_file, dataset_str):
    inserted_clusters = []
    operation_list = []
    max_pts = 0
    num_operations = 1
    active_points = 0
    # add seed to make operation deterministic
    np.random.seed(1)

    #step 1: insert
    for cluster in clusters:
        fraction = np.random.uniform(.5, .9)
        delta = int(fraction*(cluster[1]-cluster[0]))
        active_points += delta
        max_pts = max(max_pts, active_points)
        cluster_to_insert = (cluster[0], cluster[0]+delta)
        inserted_clusters.append(cluster_to_insert)
        entry = {'operation': 'insert','start': int(cluster_to_insert[0]), 'end': int(cluster_to_insert[1])}
        operation_list.append((num_operations, entry))
        num_operations += 1
        operation_list.append((num_operations, {'operation': str('search')}))
        num_operations += 1

    cluster_ids = np.random.permutation(32)

    #step 2: replace
    for c in range(32):
        fraction = np.random.uniform(0,1.0)
        full_cluster_random = clusters[cluster_ids[c]]
        inserted_cluster_random = inserted_clusters[cluster_ids[c]]
        this_cluster = inserted_clusters[c]
        this_cluster_size = this_cluster[1] - this_cluster[0]
        delta = min(this_cluster_size, int(fraction*(full_cluster_random[1] - inserted_cluster_random[1])))
        assert delta <= this_cluster[1] - this_cluster[0]
        replace_tags_start = this_cluster[0]
        replace_tags_end = replace_tags_start + delta
        replace_ids_start = inserted_cluster_random[1]
        replace_ids_end =  replace_ids_start + delta  
        entry = {'operation': 'replace', 'tags_start': replace_tags_start, 'tags_end': replace_tags_end, 'ids_start': replace_ids_start, 'ids_end': replace_ids_end}
        operation_list.append((num_operations, entry))
        num_operations += 1
        operation_list.append((num_operations, {'operation': str('search')}))
        num_operations += 1

    #write to yaml file
    with open(output_yaml_file, 'w') as yf:
        operation_list.sort(key = lambda x: x[0])
        sorted_dict = {}
        sorted_dict['max_pts'] = int(max_pts)
        for (k, v) in operation_list:
            sorted_dict[k]=v
        yaml_object = {}
        yaml_object[dataset_str] = sorted_dict
        yaml.dump(yaml_object, yf)


ds = DATASETS['msturing-10M-clustered']
cluster_runbook_path='clustered_runbook.yaml'
clustered_replace_yaml='clustered_replace_runbook.yaml'
clustered_random_yaml='random_replace_runbook.yaml'
clusters = extract_clusters(cluster_runbook_path, 10000000, 'msturing-10M-clustered')
write_replace_clustered_runbook(clusters, clustered_replace_yaml, 'msturing-10M-clustered')
write_replace_random_runbook(clusters, clustered_random_yaml, 'msturing-10M-clustered')