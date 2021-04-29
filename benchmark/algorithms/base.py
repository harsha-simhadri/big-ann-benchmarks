from __future__ import absolute_import
import psutil

class BaseANN(object):
    def done(self):
        pass

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        Assumes that after fitting index is loaded in memory.
        """
        pass

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
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

    def get_memory_usage(self):
        """Return the current memory usage of this algorithm instance
        (in kilobytes), or None if this information is not available."""
        # return in kB for backwards compatibility
        return psutil.Process().memory_info().rss / 1024

