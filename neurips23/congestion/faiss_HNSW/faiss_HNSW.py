import numpy as np
from numpy import typing as npt

from neurips23.congestion.base import BaseCongestionDropANN
from neurips23.streaming.faiss_HNSW.faiss_HNSW import faiss_HNSW as faiss_HNSW_streaming
import torch

class faiss_HNSW(BaseCongestionDropANN):
    def __init__(self, metric, index_params):
        super().__init__([faiss_HNSW_streaming(metric, index_params)], metric, index_params)
        self.indexkey="HNSW32"
        self.name = "candy_HNSW_congestion"


