from neurips23.streaming.base_postgres import BaseStreamingANNPostgres

class PostgresPgvectorHnsw(BaseStreamingANNPostgres):
    def __init__(self, metric, index_params):
        self.name = "PostgresPgvectorHnsw"
        self.pg_index_method = "hnsw"
        self.guc_prefix = "hnsw"

        super().__init__(metric, index_params)

    # Can add support for other metrics here.
    def determine_index_op_class(self, metric):
        if metric == 'euclidean':
            return "vector_l2_ops"
        else:
            raise Exception('Invalid metric')

    # Can add support for other metrics here.
    def determine_query_op(self, metric):
        if metric == 'euclidean':
            return "<->"
        else:
            raise Exception('Invalid metric')
