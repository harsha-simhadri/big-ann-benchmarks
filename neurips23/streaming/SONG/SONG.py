import numpy as np
import torch
import PyCANDYAlgo
from neurips23.streaming.base import BaseStreamingANN


class SONG(BaseStreamingANN):
    def __init__(self, metric, index_params):
        self.indexkey = index_params['indexkey']
        self.metric = metric
        self.name = "SONG"
        self.ef = 16
        self.trained = False

    def setup(self, dtype, max_pts, ndim):
        """ 初始化索引 """
        index = PyCANDYAlgo.createIndex(self.indexkey, ndim)

        cm = PyCANDYAlgo.ConfigMap()
        if self.metric == 'euclidean':
            cm.edit("metricType", "L2")
        else:
            cm.edit("metricType", "IP")

        cm.edit("indexTag", self.indexkey)
        cm.edit("vecDim", ndim)
        index.setConfig(cm)
        self.index = index

    def insert(self, X, ids):
        """ 插入数据，保留 `ids` 未不使用 """
        subA = torch.from_numpy(X.copy())
        if self.trained:
            self.index.insertTensor(subA)  # 直接插入张量
        else:
            self.index.loadInitialTensor(subA)
            self.trained = True

    def query(self, X, k):
        """ 查询数据 """
        queryTensor = torch.from_numpy(X.copy())
        # print(f"Query Tensor Shape: {queryTensor.shape}, k = {k}")  # 打印查询张量的形状
        results = self.index.searchTensor(queryTensor, k)
        # print(f"Search Index Results (indices):\n{results}")  # 打印 searchIndex 返回的索引
        # print(f"Expected shape of results: ({X.shape[0]}, {k})")  # 预期的形状
        # 处理返回结果
        res = np.array([r.numpy() for r in results])  # 转换 PyTorch 张量到 NumPy 数组
        res = res.reshape(X.shape[0], k)
        self.res = res

    def delete(self, ids):
        pass

    def set_query_arguments(self, query_args):
        """ 设置查询参数 """
        if "ef" in query_args:
            self.ef = query_args['ef']
        else:
            self.ef = 16

    def index_name(self, name):
        """ 生成索引文件名 """
        return f"data/{name}.{self.indexkey}.faissindex"
