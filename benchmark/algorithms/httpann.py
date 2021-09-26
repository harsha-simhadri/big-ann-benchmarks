import requests
import shlex
import sys
import time
from dataclasses import dataclass
from subprocess import Popen
from threading import Thread
from typing import Union, List

import numpy as np
from flask import jsonify

from sklearn.neighbors import NearestNeighbors

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS


class HttpANNError(RuntimeError):
    pass


class HttpANNResponseError(HttpANNError):
    def __init__(self, endpoint: str, expected_status: int, actual_status: int):
        super(HttpANNError, self).__init__(f"Endpoint {endpoint} expected {expected_status} but got {actual_status}")


class HttpANN(BaseANN):

    def __init__(self, server_url: str, start_seconds: int, name: str, **kwargs):
        self.server_url = server_url
        self.name = name

        # Used by get_results method, defined in query method.
        self.res = []

        # Let the server start and post to init.
        time.sleep(start_seconds)
        self.post("init", kwargs, 201)

    def post(self, path: str, body: dict, expected_status: int) -> dict:
        url = f"{self.server_url}/{path}"
        res = requests.post(url, json=body)
        if res.status_code != expected_status:
            raise HttpANNResponseError(url, expected_status, res.status_code)
        return res.json()

    def get(self, path: str, expected_status: int) -> dict:
        url = f"{self.server_url}/{path}"
        res = requests.get(url)
        if res.status_code != expected_status:
            raise HttpANNResponseError(url, expected_status, res.status_code)
        return res.json()

    def fit(self, dataset):
        body = dict(dataset=dataset)
        self.post("fit", body, 201)

    def load_index(self, dataset):
        body = dict(dataset=dataset)
        json = self.post("load_index", body, 201)
        return json["load_index"]

    def query(self, X, k):
        body = dict(X=[arr.tolist() for arr in X], k=k)
        self.post("query", body, 201)

    def range_query(self, X, radius):
        pass

    def get_results(self):
        json = self.get("results", 200)
        return np.array(json)

    def get_range_results(self):
        pass

    def get_additional(self):
        return {}

    def set_query_arguments(self, query_args):
        body = dict(query_args=query_args)
        self.post("set_query_arguments", body, 201)


class HttpANNSubprocess(object):
    def __init__(self, cmd: str):
        proc = Popen(shlex.split(cmd), stdout=sys.stdout, stderr=sys.stderr)

        def check():
            poll = proc.poll()
            if poll is not None:
                raise HttpANNError(f"HTTP server subprocess prematurely returned status code {poll}.")

        def monitor():
            while True:
                time.sleep(1)
                check()

        t = Thread(target=monitor, args=(), daemon=True)
        t.start()


class HttpANNExampleModelImplementation(BaseANN):

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
        self.knn.fit(arr[:150000, self.high_variance_dims])

    def load_index(self, dataset):
        ds = DATASETS[dataset]()
        return ds.nb_M <= 10

    def query(self, X, k):
        arr = np.array(X)[:, self.high_variance_dims]
        self.res = self.knn.kneighbors(arr, n_neighbors=k, return_distance=False)

    def range_query(self, X, radius):
        pass

    def get_results(self):
        return self.res

    def get_range_results(self):
        return self.res

    def get_additional(self):
        return {}


class HttpANNExampleModel(HttpANN, HttpANNSubprocess):
    def __init__(self, metric: str, dimension: int, use_dims: float):
        HttpANNSubprocess.__init__(self, "python3 -m benchmark.algorithms.httpann example")
        HttpANN.__init__(self, server_url="http://localhost:8080", start_seconds=3,
                         name=f"http-ann-example-{metric}-{use_dims}",
                         metric=metric, dimension=dimension, use_dims=use_dims)


def example():
    from flask import Flask, request
    from gevent.pywsgi import WSGIServer

    app = Flask(__name__)

    # Model is instantiated later but needs to be attached to an object.
    app.model = None

    @app.route("/status", methods=['GET'])
    def status():
        return jsonify(dict()), 200

    @app.route("/init", methods=['POST'])
    def init():
        app.model = HttpANNExampleModelImplementation(**request.json)
        return jsonify(dict()), 201

    @app.route("/load_index", methods=['POST'])
    def load_index():
        b = app.model.load_index(**request.json)
        return jsonify(dict(load_index=b)), 201

    @app.route("/fit", methods=['POST'])
    def fit():
        app.model.fit(**request.json)
        return jsonify(dict()), 201

    @app.route("/set_query_arguments", methods=['POST'])
    def set_query_arguments():
        app.model.set_query_arguments(**request.json)
        return jsonify(dict()), 201

    @app.route("/query", methods=['POST'])
    def query():
        j = request.json
        app.model.query(np.array(j['X']), j['k'])
        return jsonify(dict()), 201

    @app.route("/range_query", methods=['POST'])
    def range_query():
        j = request.json
        app.model.query(np.array(j['X']), j['radius'])
        return jsonify(dict()), 201

    @app.route("/results", methods=['GET'])
    def get_results():
        res_lists = [arr.tolist() for arr in app.model.res]
        return jsonify(res_lists), 200

    @app.route("/range_results", methods=['GET'])
    def get_range_results():
        return jsonify(dict(error="Not implemented")), 501

    @app.route("/additional", methods=['GET'])
    def get_additional():
        return jsonify(app.model.get_additional()), 200

    # https://flask.palletsprojects.com/en/2.0.x/deploying/wsgi-standalone/#gevent
    # app.run('0.0.0.0', 8080, debug=True)
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()


# Run the SklearnExample in a Flask server.
if __name__ == "__main__" and sys.argv[-1] == "example":
    example()
