import numpy as np
from numpy import typing as npt

from neurips23.congestion.base import BaseCongestionDropANN
from neurips23.streaming.candy_lvq.candy_lvq import candy_lvq as candy_lvq_streaming
import torch

class candy_lvq(BaseCongestionDropANN):
    def __init__(self, metric, index_params):
        super().__init__([candy_lvq_streaming(metric, index_params)], metric, index_params)
        self.metric = metric
        self.indexkey=self.workers[0].my_index_algo.indexkey
        self.name = self.workers[0].my_index_algo.name

    def set_query_arguments(self, query_args):
        self.workers[0].my_index_algo.set_query_arguments(query_args)


