import os
import numpy as np

from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS

import pys2

class PineconeIndex(BaseFilterANN):

    def __init__(self,  metric, index_params):
        self._index_params = index_params
        self._metric = metric
        print(index_params)
        self.indexkey = index_params.get("indexkey", "FilterIVFFlatU8")
        self.nt = index_params.get("threads", 1)
        self.qas = {}

    def fit(self, dataset):
        ds = DATASETS[dataset]()

        if ds.search_type() != "knn_filtered":
            raise NotImplementedError()

        print(f"Building index")
        index = pys2.FilterIndexWrapper(ds.d,
                                        self.indexkey,
                                        self._index_params,
                                        ds.get_dataset_fn(),
                                        os.path.join(ds.basedir, ds.ds_metadata_fn))

        self.index = index

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build parameters passed during construction.

        If the file does not exist, there is an option to download it from a public url
        """
        filename = dataset + '.index'

        if not os.path.exists(filename):
            return False

        print("Loading index from " + filename)
        self.index = pys2.load_filter_ivf_index(filename)
        return True


    def index_files_to_store(self, dataset):
        """
        Specify a triplet with the local directory path of index files,
        the common prefix name of index component(s) and a list of
        index components that need to be uploaded to (after build)
        or downloaded from (for search) cloud storage.

        For local directory path under docker environment, please use
        a directory under
        data/indices/track(T1 or T2)/algo.__str__()/DATASETS[dataset]().short_name()
        """
        raise NotImplementedError()
    
    def query(self, X, k):
        raise NotImplementedError()

    def filtered_query(self, X, filter, k):

        if (X.dtype.kind == 'f'):
            print('data type of X is ' + str(X.dtype))
            X = X*10 + 128
            X = X.astype(np.uint8)
            padding_size = 192 - X.shape[1]
            X = np.pad(X, ((0, 0), (0, padding_size)), mode='constant')


        results_tuple = self.index.search_parallel(X, filter.indptr, filter.indices, k) # this returns a tuple: (results_array, query_time, post_processing_time)
        self.I = results_tuple[0]
        print("query and postprocessing times: ", results_tuple[1:])


    def get_results(self):
        return self.I

    def set_query_arguments(self, query_args):
        self.qas = query_args
        print("setting query args:" + str(self.qas))

        if "skip_clustering_threshold" in query_args:
            self.skip_clustering_threshold = query_args['skip_clustering_threshold']
            self.index.set_search_param('skip_clustering_threshold', str(self.skip_clustering_threshold))
            self.qas = query_args
        else:
            self.skip_clustering_threshold = 0

        if "fraction_coefficient" in query_args:
            self.fraction_coefficient = query_args['fraction_coefficient']
            self.index.set_search_param('fraction_coefficient', str(self.fraction_coefficient))
            self.qas = query_args
        else:
            self.fraction_coefficient = 18.0

        if "fraction_exponent" in query_args:
            self.fraction_exponent = query_args['fraction_exponent']
            self.index.set_search_param('fraction_exponent', str(self.fraction_exponent))
            self.qas = query_args
        else:
            self.fraction_coefficient = 0.65


    def __str__(self):
        return f'pinecone_filter({self.indexkey, self._index_params, self.qas})'

   
