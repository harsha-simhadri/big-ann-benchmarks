from __future__ import absolute_import

class BaseANN(object):
    def done(self):
        pass

    def fit(self, X, name):
        """
        Build the index for the data points given as X.
        Pass name as well to store index.
        """
        pass

    def load_index(self, name):
        """Load the index from name."""
        pass

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        pass

    def range_query(self, X, r):
        """
        Carry out a batch query for range search with
        radius r of query set X.
        """
        pass

    def get_results(self):
        """
        Helper method to convert query results to the expected format.
        """
        return self.res

    def get_additional(self):
        """
        Allows to retrieve additional results.
        """
        return {}

    def __str__(self):
        return self.name
