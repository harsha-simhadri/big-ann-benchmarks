import argparse
import os
import numpy as np
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
    data = ds.get_dataset()

    offsets, permutation = cluster_and_permute(data, args.num_clusters)
    
    permuted_data = data[permutation,:]
    operation_list = []
    print(permutation)
    for c in range(args.num_clusters):
        cluster_index_range = range(offsets[c], offsets[c + 1])
        cluster_indices = np.array(permutation[cluster_index_range], dtype=np.uintc)
        print(cluster_index_range)
        entry = [{'operation': 'insert'}, {'start': int(offsets[c])}, {'end': int(offsets[c+1])}]
        operation_list.append((c+1, entry))

    shape = np.shape(permuted_data)
    with open(args.output_data_file, 'wb') as df:
        df.write(shape[0].to_bytes(4, 'little'))
        df.write(shape[1].to_bytes(4, 'little'))
        df.write(permuted_data)

    with open(args.output_yaml_file, 'w') as yf:
        operation_list.sort(key = lambda x: x[0])
        sorted_dict = {}
        for (k, v) in operation_list:
            sorted_dict[k]=v
        yaml_object = {}
        yaml_object[args.dataset] = sorted_dict
        yaml.dump(yaml_object, yf)


if __name__ == '__main__':
    main()
