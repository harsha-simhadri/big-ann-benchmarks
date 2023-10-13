import argparse
import os
import numpy as np
import random
import yaml

from scipy.cluster.vq import vq, kmeans2
from typing import Tuple
from benchmark.datasets import DATASETS

def cluster_and_permute(
    data, num_clusters
) -> Tuple[np.ndarray[int], np.ndarray[int]]:
    """
    Cluster the data and return permutation of row indices
    that would group indices of the same cluster together
    """
    npts = np.shape(data)[0]
    sample_size = min(100000, npts)
    sample_indices = np.random.choice(range(npts), size=sample_size, replace=False)
    sampled_data = data[sample_indices, :]
    centroids, sample_labels = kmeans2(sampled_data, num_clusters, minit="++", iter=10)
    labels, dist = vq(data, centroids)

    count = np.zeros(num_clusters)
    for i in range(npts):
        count[labels[i]] += 1
    print("Cluster counts")
    print(count)

    offsets = np.zeros(num_clusters + 1, dtype=int)
    for i in range(0, num_clusters, 1):
        offsets[i + 1] = offsets[i] + count[i]

    permutation = np.zeros(npts, dtype=int)
    counters = np.zeros(num_clusters, dtype=int)
    for i in range(npts):
        label = labels[i]
        row = offsets[label] + counters[label]
        counters[label] += 1
        permutation[row] = i

    return offsets, permutation


def write_permuated_data(
        data,
        permutation:np.ndarray[int],
        output_data_file:str
):
    permuted_data = data[permutation,:]

    shape = np.shape(permuted_data)
    with open(output_data_file, 'wb') as df:
        df.write(shape[0].to_bytes(4, 'little'))
        df.write(shape[1].to_bytes(4, 'little'))
        df.write(permuted_data)


def create_runbook(
    dataset_str:str,
    offsets:np.ndarray[int],
    permutation:np.ndarray[int],
    num_clusters:int, 
    output_yaml_file:str
):
    ins_cursor_start = offsets.copy()
    ins_cursor_end = offsets.copy()

    del_cursor_start = offsets.copy()
    del_cursor_end = offsets.copy()

    operation_list = []
    num_operations = 1
    active_points = 0
    max_pts = 0
    active_points_in_cluster = np.zeros(num_clusters)

    num_rounds = 5
    sample = np.random.default_rng().dirichlet((100,15,10,5,3), num_clusters)
    for c in range(num_clusters):
        np.random.default_rng().shuffle(sample[c])
    print(sample)

    for round in range(num_rounds):
        #insertions
        for c in range(num_clusters):
            delta = (int)((offsets[c+1]-offsets[c]) * sample[c,round])
            ins_cursor_end[c] = ins_cursor_start[c] + delta
            active_points += delta
            max_pts = max(max_pts, active_points)
            active_points_in_cluster[c] += delta
            print('ins [', ins_cursor_start[c], ', ', ins_cursor_end[c], 
                  ') active:', int(active_points_in_cluster[c]),
                  'total:', active_points)
            entry = [{'operation': 'insert'}, {'start': int(ins_cursor_start[c])}, {'end': int(ins_cursor_end[c])}]
            operation_list.append((num_operations, entry))
            num_operations += 1
            operation_list.append((num_operations, [{'operation': str('search')}]))
            num_operations += 1
            ins_cursor_start[c] = ins_cursor_end[c]

        #deletions
        for c in range(num_clusters):
            fraction = random.uniform(0.5,0.9)
            delta = (int)(fraction*(ins_cursor_end[c]-del_cursor_start[c]))
            del_cursor_end[c] = del_cursor_start[c] + delta
            active_points -= delta
            active_points_in_cluster[c] -= delta
            print('del [', del_cursor_start[c], ',', del_cursor_end[c],
                  ') active:', int(active_points_in_cluster[c]),
                  'total:', active_points)
            entry = [{'operation': 'delete'}, {'start': int(del_cursor_start[c])}, {'end': int(del_cursor_end[c])}]
            operation_list.append((num_operations, entry))
            num_operations += 1
            operation_list.append((num_operations, [{'operation': 'search'}]))
            num_operations += 1
            del_cursor_start[c] = del_cursor_end[c]


    with open(output_yaml_file, 'w') as yf:
        operation_list.sort(key = lambda x: x[0])
        sorted_dict = {}
        sorted_dict['max_pts'] = int(max_pts)
        for (k, v) in operation_list:
            sorted_dict[k]=v
        yaml_object = {}
        yaml_object[dataset_str] = sorted_dict
        yaml.dump(yaml_object, yf)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(
        '--dataset',
        choices=DATASETS.keys(),
        required=True)
    parser.add_argument(
        '-c', '--num_clusters',
        type=int,
        required=True
    )
    parser.add_argument(
        '-o', '--output_data_file',
        required=True
    )
    parser.add_argument(
        '-y', '--output_yaml_file',
        required=True
    )
    args = parser.parse_args()

    ds = DATASETS[args.dataset]()
    if ds.nb <= 10**7:
        data = ds.get_dataset()
    else:
        data = next(ds.get_dataset_iterator(bs=ds.nb))
    print(np.shape(data))

    offsets, permutation = cluster_and_permute(data, args.num_clusters)
    print(permutation)

    write_permuated_data(data=data, 
                         permutation=permutation,
                         output_data_file=args.output_data_file)

    create_runbook(dataset_str=args.dataset,
                   offsets=offsets,
                   permutation=permutation, 
                   num_clusters=args.num_clusters,
                   output_yaml_file=args.output_yaml_file)


if __name__ == '__main__':
    main()
