from __future__ import absolute_import

import numpy as np
import os
import requests


from benchmark.algorithms.base import BaseANN
import py_pinecone_smips

# a python wrapper for Pinecone's SMIPS algorithm, implemented in rust.

# Build parameters: index_path, num_threads
# Query parameters: nprobe, top_kprime
class PineconeSMIPS(BaseANN):
    def __init__(self, metric, index_params):
        assert metric == "ip"
        self.name = "pinecone_smips"
        self.index_path = index_params.get("index_path", None)
        self.num_threads = index_params.get("num_threads", 8)
        self._nprobe = np.infty
        self._top_kprime = np.infty
        self._ip_budget = np.infty
        print("Pinecone SMIPS index initialized. Index path: " + self.index_path)

    def fit(self, dataset): # e.g. dataset = "sparse-small"
        # this version is for evaluating existing indexes only
        raise NotImplementedError()

    def load_index(self, dataset):

        # download index files, if needed
        print(f"Preparing to load index (downloading 2 files if necessary, this may take a few minutes)")

        # check if index files exist. If not, download them

        bucket_name = 'ann-challenge-sparse-vectors'
        file_list = ['pinecone-sparse-index/ivf-index', 'pinecone-sparse-index/forward-index']

        download_multiple_files(bucket_name, file_list, self.index_path)

        self._index = py_pinecone_smips.PineconeIndex(
            ivf_index_path=self.index_path + 'ivf-index',
            forward_index_path=self.index_path + 'forward-index',
            num_threads=self.num_threads,
        )
        return True

    def set_query_arguments(self, query_args):
        self._top_kprime = query_args["top_kprime"]
        self._nprobe = query_args["nprobe"]
        self._ip_budget = query_args["ip_budget"]

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        res = self._index.retrieve_parallel(X.shape, X.indptr, X.indices, X.data, self._nprobe, self._top_kprime, k, self._ip_budget)
        self.I = np.array(res, dtype='int32')

    def get_results(self):
        return self.I


def download_public_gcs_file(bucket_name, source_blob_name, destination_dir):
    """Download a file from Google Cloud Storage in chunks to avoid OOM error."""
    destination_file_name = os.path.join(destination_dir, os.path.basename(source_blob_name))

    # Check if the file already exists
    if os.path.exists(destination_file_name):
        print(f"File already exists: {destination_file_name}")
        return

    # Download the file in chunks
    url = f"https://storage.googleapis.com/{bucket_name}/{source_blob_name}"
    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(destination_file_name), exist_ok=True)

            # Write the file in chunks
            with open(destination_file_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            print(f"File downloaded successfully: {destination_file_name}")
        else:
            print(f"Failed to download {source_blob_name}: HTTP status code {response.status_code}")

def download_multiple_files(bucket_name, file_list, destination_dir):
    """Download multiple files from GCS to a local directory if they don't already exist."""
    for file_name in file_list:
        download_public_gcs_file(bucket_name, file_name, destination_dir)
