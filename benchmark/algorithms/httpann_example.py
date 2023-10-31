import numpy as np
from flask import Flask, request, jsonify
from sklearn.neighbors import NearestNeighbors

from benchmark.datasets import DATASETS
from .httpann import HttpANN, HttpANNSubprocess


class HttpANNExampleAlgorithm(HttpANN, HttpANNSubprocess):
    """
    ANN algorithm that serves as a standard "algorithm" (callable from runner.py) and manages an HTTP server that
    implements the actual indexing and query processing algorithms.

    By implementing HttpANNSubprocess, it starts a local server (which is implemented further below in the same file).
    By implementing HttpANN, it can be used by runner.py to make ANN requests from Python to the local server.

    Obviously this is a contrived setup, as the actual algorithm is also implemented in Python.
    It's purely as an example of how one might run an algorithm from another language by using an HTTP server to
    implement the server API expected by HttpANN.
    """

    def __init__(self, metric: str, dimension: int, use_dims: float):
        HttpANNSubprocess.__init__(self, "python3 -m benchmark.algorithms.httpann_example example")
        HttpANN.__init__(self, server_url="http://localhost:8080", start_seconds=3,
                         name=f"http-ann-example-{metric}-{use_dims}", metric=metric, dimension=dimension,
                         use_dims=use_dims)


# Starts a local flask server that adheres to the HttpANN API and delegates the work to a local ANN algorithm.
def main():
    class SimpleANNAlgo(object):
        """
        Very simple ANN algorithm intended only to demonstrate the HttpANN functionality.
        This algorithm is instantiated and called from the example server below.
        The algorithm is approximate in the sense that it uses exact KNN constrained to a configurable subset of the
        highest variance dimensions. For example, if dimensions=100 and use_dims=0.22, the algorithm picks the 22
        dimensions with the highest variance and use them for exact KNN.
        """

        def __init__(self, metric: str, dimension: int, use_dims: float = 0.1):
            self.metric = metric
            self.dimension = dimension
            self.use_dims = use_dims
            self.knn = None
            self.high_variance_dims = None
            self.res = None

        def fit(self, dataset):
            ds = DATASETS[dataset]()
            arr = ds.get_dataset()
            var = arr.var(axis=0)
            num_dims = int(self.use_dims * arr.shape[1])
            self.high_variance_dims = np.argsort(var)[-num_dims:]
            self.knn = NearestNeighbors(algorithm='brute', metric=self.metric)
            self.knn.fit(arr[:, self.high_variance_dims])

        def load_index(self, dataset):
            # Always returns false because the index is not stored.
            return False

        def query(self, X, k):
            self.res = self.knn.kneighbors(X[:, self.high_variance_dims], n_neighbors=k, return_distance=False)

        def range_query(self, X, radius):
            nbrs, dsts = self.knn.radius_neighbors(X[:, self.high_variance_dims], radius=radius, return_distance=True)
            total = sum(map(len, nbrs))
            lims = np.zeros(len(X) + 1, 'int32')
            I = np.zeros(total, 'int32')
            D = np.zeros(total, 'float32')
            for i in range(len(X)):
                lims[i + 1] = lims[i] + len(nbrs[i])
                I[lims[i]:lims[i + 1]] = nbrs[i]
                D[lims[i]:lims[i + 1]] = dsts[i]
            self.res = (lims, I, D)

        def get_results(self):
            return self.res

        def get_range_results(self):
            return self.res

        def get_additional(self):
            return {}

    app = Flask(__name__)

    # Algorithm is instantiated later but needs to be attached to an object.
    app.algo = None

    @app.route("/status", methods=['GET'])
    def status():
        return jsonify(dict()), 200

    @app.route("/init", methods=['POST'])
    def init():
        app.algo = SimpleANNAlgo(**request.json)
        return jsonify(dict()), 200

    @app.route("/load_index", methods=['POST'])
    def load_index():
        b = app.algo.load_index(**request.json)
        return jsonify(dict(load_index=b)), 200

    @app.route("/fit", methods=['POST'])
    def fit():
        app.algo.fit(**request.json)
        return jsonify(dict()), 200

    @app.route("/set_query_arguments", methods=['POST'])
    def set_query_arguments():
        app.algo.set_query_arguments(**request.json)
        return jsonify(dict()), 200

    @app.route("/query", methods=['POST'])
    def query():
        j = request.json
        app.algo.query(np.array(j['X']), j['k'])
        return jsonify(dict()), 200

    @app.route("/range_query", methods=['POST'])
    def range_query():
        j = request.json
        app.algo.range_query(np.array(j['X']), j['radius'])
        return jsonify(dict()), 200

    @app.route("/get_results", methods=['POST'])
    def get_results():
        neighbors = [arr.tolist() for arr in app.algo.res]
        return jsonify(dict(get_results=neighbors)), 200

    @app.route("/get_range_results", methods=['POST'])
    def get_range_results():
        lims, I, D = app.algo.get_range_results()
        res = [
            lims.tolist(),
            [arr.tolist() for arr in I],
            [arr.tolist() for arr in D]
        ]
        return jsonify(dict(get_range_results=res)), 200

    @app.route("/get_additional", methods=['POST'])
    def get_additional():
        return jsonify(dict(get_additional=app.algo.get_additional())), 200

    app.run('0.0.0.0', 8080, debug=False)
    # We could also use gevent/wsgi for a more professional setup.
    # https://flask.palletsprojects.com/en/2.0.x/deploying/wsgi-standalone/#gevent
    # from gevent.pywsgi import WSGIServer
    # http_server = WSGIServer(('0.0.0.0', 8080), app)
    # http_server.serve_forever()


if __name__ == "__main__":
    main()
