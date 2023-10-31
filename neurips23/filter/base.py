from benchmark.algorithms.base import BaseANN

class BaseFilterANN(BaseANN):
    def filtered_query(self, X, filter, k):
        """
        Carry out a batch query for k-NN of query set X with associated filter.
        Query X[i] has asks for k-NN in the index that pass all filters in filter[i].
        """
        raise NotImplementedError()
    
    def track(self):
        return "filter"