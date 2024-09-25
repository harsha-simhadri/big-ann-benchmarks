import os
from pathlib import Path

from benchmark.dataset_io import download
from benchmark.dataset_io import read_fbin
from benchmark.datasets import DATASETS
from google.protobuf import text_format
from neurips23.ood.base import BaseOODANN
import numpy as np
import scann
from scann.proto import scann_pb2
import multiprocessing


class Scann(BaseOODANN):

    def __init__(self, metric, index_params):
        self.config_id = index_params.get('config_id', None)
        self.download = index_params.get('download', False)
        self.tree_size = index_params.get('tree_size', 40_000)
        self.serialized_dir = 'data/scann/ood'
        # To account for hyper-threading.
        self.num_cpus = multiprocessing.cpu_count() // 2
        print('ScaNN: Init')

    def load_index(self, dataset):

        # if self.download and not os.path.exists(self.serialized_dir):
        if self.download:
            # Try downloading if the directory does not exist.
            print('ScaNN: Download serialized searcher.')
            path = Path(self.serialized_dir)
            path.mkdir(parents=True, exist_ok=True)
            remote_dir = 'https://storage.googleapis.com/scann/big-ann-2023/ood'
            file_list = ['ah_codebook.pb',
                         'bfloat16_dataset.npy',
                         'datapoint_to_token.npy',
                         'hashed_dataset.npy',
                         'hashed_dataset_soar.npy',
                         'scann_assets.pbtxt',
                         'scann_config.pb',
                         'scann_config.pb.0',
                         'scann_config.pb.1',
                         'scann_config.pb.2',
                         'serialized_partitioner.pb']
            for fn in file_list:
                download(f'{remote_dir}/{fn}', f'{self.serialized_dir}/{fn}')

        if os.path.exists(self.serialized_dir):
            # Load if data exists.
            print(f'ScaNN: Load serialized searcher {self.serialized_dir}')
            if self.config_id is not None:
                src = Path(self.serialized_dir) / \
                    Path(f'scann_config.pb.{self.config_id}')
                dst = Path(self.serialized_dir) / Path(f'scann_config.pb')
                os.rename(src, dst)
            self.searcher = scann.scann_ops_pybind.load_searcher(
                self.serialized_dir)
            self.searcher.set_num_threads(self.num_cpus)

    def fit(self, dataset):
        if hasattr(self, 'searcher'):
            print('ScaNN: Searcher already loaded.')
            return
        print('ScaNN: Training')
        print('This requires more than 16GB of RAM.')
        print('Please download the serialized searcher or use a higher RAM VM.')
        config = f"""
      num_neighbors: 10
      distance_measure {{
        distance_measure: "DotProductDistance"
      }}
      partitioning {{
        num_children: { self.tree_size }
        max_clustering_iterations: 40
        min_cluster_size: 10
        partitioning_distance {{
          distance_measure: "SquaredL2Distance"
        }}
        num_cpus: 8
        database_spilling {{
          spilling_type: TWO_CENTER_ORTHOGONALITY_AMPLIFIED
          orthogonality_amplification_lambda: 1.3
          overretrieve_factor: 1.2
        }}
        query_spilling {{
          spilling_type: FIXED_NUMBER_OF_CENTERS
          max_spill_centers: 35
        }}
        partitioning_type: GENERIC
        query_tokenization_distance_override {{
          distance_measure: "DotProductDistance"
        }}
        query_tokenization_type: FLOAT
        balancing_type: UNBALANCED_FLOAT32
        single_machine_center_initialization: RANDOM_INITIALIZATION
        avq: 1.6
      }}
      hash {{
        asymmetric_hash {{
          projection {{
            projection_type: CHUNK
            num_blocks: 100
            num_dims_per_block: 2
            input_dim: 200
          }}
          num_clusters_per_block: 16
          max_clustering_iterations: 30
          quantization_distance {{
            distance_measure: "SquaredL2Distance"
          }}
          lookup_type: INT8_LUT16
          use_residual_quantization: true
          noise_shaping_threshold: 0.1
          expected_sample_size: 100000
          use_global_topn: true
        }}
      }}
      exact_reordering {{
        approx_num_neighbors: 150
        bfloat16 {{
          enabled: true
          noise_shaping_threshold: 0.2
        }}
      }}
      custom_search_method: "experimental_top_level_partitioner:700,20,3.0,2.5,1.8"
    """

        ds = DATASETS[dataset]()
        k = ds.default_count()
        self.searcher = (scann.scann_ops_pybind.builder(
            np.zeros([0, ds.d]).astype('float32'), k, 'dot_product')
            .score_brute_force()
            .build())
        self.searcher.reserve(10_000_000)

        # Avoid loading the full database..
        import gc
        s = 0
        trained = False
        for data in ds.get_dataset_iterator(bs=100_000):
            print(f'ScaNN: Read datapoints: {s}')
            self.searcher.searcher.upsert([None] * len(data), data, len(data))
            s += len(data)
            del data
            gc.collect()
            if not trained and s >= 8_000_000:
                self.searcher.set_num_threads(self.num_cpus)
                self.searcher.rebalance(config)
                self.searcher.set_num_threads(self.num_cpus)
                trained = True
        del ds
        # path = Path(self.serialized_dir)
        # path.mkdir(parents=True, exist_ok=True)
        # self.searcher.serialize(self.serialized_dir)
        gc.collect()

    def query(self, X, k):
        self.res = self.searcher.search_batched_parallel(
            X,
            leaves_to_search=self.leaves_to_search,
            pre_reorder_num_neighbors=self.reorder,
            batch_size=(X.shape[0] // self.num_cpus)
        )[0]

    def set_query_arguments(self, query_args):
        self.leaves_to_search = query_args['leaves_to_search']
        self.reorder = query_args['reorder']

    def __str__(self):
        return f'ScaNN,tree={self.leaves_to_search}/{self.tree_size},AH2,reorder={self.reorder}'
