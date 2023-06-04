from benchmark.algorithms.base import BaseANN

class BaseOODANN(BaseANN):
    def track(self):
        return "ood"