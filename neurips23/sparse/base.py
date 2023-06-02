from benchmark.algorithms.base import BaseANN

class BaseSparseANN(BaseANN):
    def track(self):
        return "sparse"