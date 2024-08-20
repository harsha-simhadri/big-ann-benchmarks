import os

from benchmark.datasets import DATASETS
from google.protobuf import text_format
from neurips23.streaming.base import BaseStreamingANN
import numpy as np
import numpy.typing as npt
import scann
from scann.proto import scann_pb2


class Scann(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.name = 'scann'
        self.max_brute_force = 4_000_000
        self.k = 10
        self.n_threads = 8
        self.tree_size = index_params.get('tree_size')
        self.leaves_to_search = index_params.get('leaves_to_search')
        self.reorder = index_params.get('reorder')
        self.config = f"""
        num_neighbors: 10
        distance_measure {{
          distance_measure: "DotProductDistance"
        }}
        partitioning {{
          num_children: { self.tree_size }
          max_clustering_iterations: 10
          min_cluster_size: 10
          partitioning_distance {{
            distance_measure: "SquaredL2Distance"
          }}
          query_spilling {{
            spilling_type: FIXED_NUMBER_OF_CENTERS
            max_spill_centers: { self.leaves_to_search }
          }}
          database_spilling {{
            spilling_type: TWO_CENTER_ORTHOGONALITY_AMPLIFIED
          }}
          partitioning_type: GENERIC
          query_tokenization_distance_override {{
            distance_measure: "DotProductDistance"
          }}
          query_tokenization_type: FLOAT
          balancing_type: UNBALANCED_FLOAT32
          expected_sample_size: 1000000
          single_machine_center_initialization: RANDOM_INITIALIZATION
        }}
        hash {{
          asymmetric_hash {{
            projection {{
              projection_type: CHUNK
              num_blocks: 50
              num_dims_per_block: 2
              input_dim: 100
            }}
            num_clusters_per_block: 16
            max_clustering_iterations: 10
            quantization_distance {{
              distance_measure: "SquaredL2Distance"
            }}
            lookup_type: INT8_LUT16
            use_residual_quantization: true
            noise_shaping_threshold: 0.2
            expected_sample_size: 32000
            use_global_topn: true
          }}
        }}
        exact_reordering {{
          approx_num_neighbors: { self.reorder }
        }}"""

    def setup(self, dtype, max_pts, ndims) -> None:
        self.brute_force = True
        self.searcher = (scann.scann_ops_pybind.builder(
            np.zeros([0, ndims]).astype(dtype), self.k, 'dot_product')
            .score_brute_force()
            .build(docids=[]))
        self.searcher.reserve(max_pts)
        self.searcher.set_num_threads(self.n_threads)

    def insert(self, X: np.array, ids: npt.NDArray[np.uint32]) -> None:
        print('Insert: ', ids.shape[0])
        self.searcher.upsert(ids.tolist(), X, batch_size=1024)

        if self.brute_force and self.searcher.size() > self.max_brute_force:
            self.searcher.rebalance(self.config)
            self.searcher.set_num_threads(self.n_threads)
            self.brute_force = False

    def delete(self, ids: npt.NDArray[np.uint32]) -> None:
        print('Delete: ', ids.shape[0])
        self.searcher.delete(ids.tolist())

    def query(self, X, k):
        print('Search: ', X.shape[0])
        self.res = self.searcher.search_batched_parallel(
            X, final_num_neighbors=k,
            leaves_to_search=self.leaves_to_search,
            pre_reorder_num_neighbors=self.reorder,
            batch_size=1250
        )[0]

    def set_query_arguments(self, query_args):
        pass

    def __str__(self):
        return f'ScaNN,tree={self.leaves_to_search}/{self.tree_size},AH2,reorder={self.reorder}'
