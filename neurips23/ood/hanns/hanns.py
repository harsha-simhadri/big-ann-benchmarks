
import os
from pathlib import Path

from benchmark.dataset_io import download
from benchmark.datasets import DATASETS
from neurips23.ood.base import BaseOODANN
import hanns
import time


def read_config_and_fill(file_name, **kwargs):
    with open(file_name, 'rb') as f:
        text_bytes = f.read()

    text = text_bytes.decode('utf-8')
    filled_text = text.format(**kwargs)
    return filled_text


class Hanns(BaseOODANN):

    def __init__(self, metric, index_params):
        self.config_id = index_params.get('config_id', None)
        self.download = index_params.get('download', False)
        self.tree_size = index_params.get('tree_size', 40_000)
        self.serialized_dir = 'data/hanns/ood'
        self.remote_dir = 'https://hanns.obs.ap-southeast-1.myhuaweicloud.com/v2'
        print('Init')

    def load_index(self, dataset):
        config_name = "config.pb"
        path = Path(self.serialized_dir)
        path.mkdir(parents=True, exist_ok=True)
        download(f'{self.remote_dir}/{config_name}', f'{self.serialized_dir}/{config_name}')
        if self.download:
            print('Download index.')
            file_list = ['ah_codebook.pb',
                         'bfloat16_dataset.npy',
                         'datapoint_to_token.npy',
                         'hashed_dataset.npy',
                         'hashed_dataset_soar.npy',
                         'assets.pbtxt',
                         'serialized_partitioner.pb']
            for fn in file_list:
                download(f'{self.remote_dir}/{fn}', f'{self.serialized_dir}/{fn}')

        if self.download and os.path.exists(self.serialized_dir):
            print(f'Load index {self.serialized_dir}')
            self.searcher = hanns.hanns_wrap.load_searcher(self.serialized_dir)

    def fit(self, dataset):
        if hasattr(self, 'searcher'):
            print('index already loaded.')
            return
        
        print('start build index')
        build_name = "build.config"
        download(f'{self.remote_dir}/{build_name}', f'{self.serialized_dir}/{build_name}')
        config = read_config_and_fill(f'{self.serialized_dir}/{build_name}', tree_size=self.tree_size)
        ds = DATASETS[dataset]()
        k = ds.default_count()
        self.searcher = (hanns.hanns_wrap.builder(k, 'DotProductDistance', ds.d, ds.nb))
        start = time.time()

        import gc
        filename = ds.get_dataset_fn()
        print(filename)
        self.searcher.load_data(config, filename)
        end = time.time()
        print(f'build index cost time: {end - start}s')
        self.searcher.set_config(f'{self.serialized_dir}/config.pb')
        gc.collect()

    def query(self, X, k):
        self.res = self.searcher.search_batched_parallel(
            X, leaves_to_search=self.leaves_to_search,
            reorder_num=self.reorder,  batch_size=12500
        )[0]

    def set_query_arguments(self, query_args):
        self.leaves_to_search = query_args['leaves_to_search']
        self.reorder = query_args['reorder']

    def __str__(self):
        return f'hanns,tree={self.leaves_to_search}/{self.tree_size},reorder={self.reorder}'
