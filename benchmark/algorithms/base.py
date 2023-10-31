from __future__ import absolute_import
import psutil

class BaseANN(object):
    def done(self):
        """
        This is called after results have been processed.
        Use it for cleaning up if necessary.
        """
        pass

    def track(self):
        """
        return "T1" if submitting an entry for track 1
        return "T2" if submitting an entry for track 2
        return "T3" if submitting an entry for track 3
        """
        raise NotImplementedError()

    def fit(self, dataset):
        """
        Build the index for the data points given in dataset name.
        Assumes that after fitting index is loaded in memory.
        """
        raise NotImplementedError()

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        raise NotImplementedError()

    def index_files_to_store(self, dataset):
        """
        Specify a triplet with the local directory path of index files,
        the common prefix name of index component(s) and a list of
        index components that need to be uploaded to (after build)
        or downloaded from (for search) cloud storage.

        For local directory path under docker environment, please use
        a directory under
        data/indices/track(T1 or T2)/algo.__str__()/DATASETS[dataset]().short_name()
        """
        raise NotImplementedError()

    def query(self, X, k):
        """Carry out a batch query for k-NN of query set X."""
        raise NotImplementedError()

    def range_query(self, X, radius):
        """
        Carry out a batch query for range search with
        radius.
        """
        raise NotImplementedError()


    def get_results(self):
        """
        Helper method to convert query results of k-NN search.
        If there are nq queries, returns a (nq, k) array of integers
        representing the indices of the k-NN for each query.
        """
        return self.res

    def get_range_results(self):
        """
        Helper method to convert query results of range search.
        If there are nq queries, returns a triple lims, D, I.
        lims is a (nq) array, such that

            I[lims[q]:lims[q + 1]] in int

        are the indices of the indices of the range results of query q, and

            D[lims[q]:lims[q + 1]] in float

        are the distances.
        """
        return self.res

    def get_additional(self):
        """
        Retrieve additional results.
        Return a dictionary with metrics
        and corresponding measured values.

        The following additional metrics are supported:

        `mean_latency` in microseconds, if this applies to your algorithm.
        Skip if your algorithm batches query processing.

        `latency_999` is the 99.9pc latency in microseconds, if this applies
        to your algorithm. Skip if your algorithm batches query processing.

        `dist_comps` is the total number of points in the base set
        to which a query was compared.

        `mean_ssd_ios` is the average number of SSD I/Os per query for T2 algorithms.
        """
        return {}

    def __str__(self):
        return self.name

    def get_memory_usage(self):
        """Return the current memory usage of this algorithm instance
        (in kilobytes), or None if this information is not available."""
        # return in kB for backwards compatibility
        return psutil.Process().memory_info().rss / 1024
