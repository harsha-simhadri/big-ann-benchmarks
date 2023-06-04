from benchmark.algorithms.base import BaseANN

class BaseStreamingANN(BaseANN):
    def track(self):
        return "ood"