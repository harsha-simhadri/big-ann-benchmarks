import shlex
import sys
import time
from subprocess import Popen
from threading import Thread

import numpy as np
import requests
from flask import jsonify
from sklearn.neighbors import NearestNeighbors

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS


class HttpANN(BaseANN):
    """
    HTTP-based ANN algorithm.
    Designed to enable language-agnostic ANN by delegating indexing and querying to a separate HTTP server.

    The HTTP server must satisfy the following API.

    | Method | Route                | Request Body                                                                                               | Expected Status | Response Body                                                              |
    | ------ | -------------------- | ---------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------------- |
    | POST   | /init                | dictionary of constructor arguments, e.g., {"metric": "euclidean", "dimension": 99 }                       | 200             | { }                                                                        |
    | POST   | /load_index          | { "dataset": <dataset name, e.g. "bigann-10m"> }                                                           | 200             | { "load_index": <Boolean indicating whether the index can be loaded> }     |
    | POST   | /set_query_arguments | dictionary of query arguments                                                                              | 200             | { }                                                                        |
    | POST   | /query               | { "X": <query vectors as list of lists of floats>, "k": <number of neighbors to find and keep in memory> } | 200             | { }                                                                        |
    | POST   | /range_query         | { "X": <query vectors as list of lists of floats>, “radius”: <distance to neighbors> }                     | 200             | { }                                                                        |
    | POST   | /get_results         | { }                                                                                                        | 200             | { "get_results": <neighbors as list of lists of ints> }                    |
    | POST   | /get_additional      | { }                                                                                                        | 200             | { "get_additional": <dictionary of arbitrary additional result metadata> } |
    | POST   | /get_range_results   | { }                                                                                                        | 200             | { "get_range_results": <list of three 1-dimensional lists (lims, I, D)> }  |

    Note that this is a 1:1 copy of the BaseANN Python Class API implemented as remote procedure calls.
    """

    def __init__(self, server_url: str, start_seconds: int, name: str, **kwargs):
        self.server_url = server_url
        self.name = name

        # Used by get_results method, defined in query method.
        self.res = []

        # Let the server start and post to init.
        time.sleep(start_seconds)
        self.post("init", kwargs, 200)

    def post(self, path: str, body: dict, expected_status: int) -> dict:
        url = f"{self.server_url}/{path}"
        res = requests.post(url, json=body)
        if res.status_code != expected_status:
            raise HttpANNResponseError(url, expected_status, res.status_code)
        return res.json()

    def fit(self, dataset):
        body = dict(dataset=dataset)
        self.post("fit", body, 200)

    def load_index(self, dataset):
        body = dict(dataset=dataset)
        json = self.post("load_index", body, 200)
        return json["load_index"]

    def query(self, X, k):
        body = dict(X=[arr.tolist() for arr in X], k=k)
        self.post("query", body, 200)

    def range_query(self, X, radius):
        body = dict(X=[arr.tolist() for arr in X], radius=radius)
        self.post("range_query", body, 200)

    def get_results(self):
        json = self.post("get_results", dict(), 200)
        return np.array(json["get_results"])

    def get_range_results(self):
        json = self.post("get_range_results", dict(), 200)
        [lims, I, D] = json["get_range_results"]
        return np.array(lims, 'int32'), np.array(I, 'int32'), np.array(D, 'float32')

    def get_additional(self):
        json = self.post("get_additional", dict(), 200)
        return json["get_additional"]

    def set_query_arguments(self, query_args):
        body = dict(query_args=query_args)
        self.post("set_query_arguments", body, 200)


class HttpANNError(RuntimeError):
    """Custom error type"""
    pass


class HttpANNResponseError(HttpANNError):
    """Custom error type"""
    def __init__(self, endpoint: str, expected_status: int, actual_status: int):
        super(HttpANNError, self).__init__(f"Endpoint {endpoint} expected {expected_status} but got {actual_status}")


class HttpANNSubprocess(object):
    """
    Helper class to start the HTTP server as a local subprocess.
    Starts a background thread to monitor the subprocess by checking for an exit code once per second.
    If the background thread finds an exit code, it will raise an HttpANNError.
    """
    def __init__(self, server_subprocess_command: str):
        proc = Popen(shlex.split(server_subprocess_command), stdout=sys.stdout, stderr=sys.stderr)

        def monitor():
            while True:
                time.sleep(1)
                poll = proc.poll()
                if poll is not None:
                    raise HttpANNError(f"HTTP server subprocess prematurely returned status code {poll}.")

        t = Thread(target=monitor, args=(), daemon=True)
        t.start()


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
        HttpANNSubprocess.__init__(self, "python3 -m benchmark.algorithms.httpann example")
        HttpANN.__init__(self, server_url="http://localhost:8080", start_seconds=3,
                         name=f"http-ann-example-{metric}-{use_dims}", metric=metric, dimension=dimension,
                         use_dims=use_dims)


# Starts a local flask server that adheres to the HttpANN API and delegates the work to a local ANN algorithm.
if __name__ == "__main__" and sys.argv[-1] == "example":

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


    from flask import Flask, request

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
