import shlex
import sys
import time
from dataclasses import dataclass
from subprocess import Popen
from threading import Thread
from typing import Union, List

import numpy as np
from flask import jsonify
from requests import get, post

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS


class Contract:

    @dataclass(frozen=True, init=False)
    class Base:
        pass

    @dataclass(frozen=True)
    class Init(Base):
        metric: str
        dataset: str
        dimension: int
        index_params: Union[dict, list]

    @dataclass(frozen=True)
    class Fit(Base):
        count: int

    @dataclass(frozen=True)
    class SetQueryArgs(Base):
        query_args: Union[dict, list]

    @dataclass(frozen=True)
    class Query(Base):
        X: List[List[Union[float, int]]]
        k: int

        def __str__(self):
            if len(self.X) == 0:
                return f"Query(X=empty, k={self.k})"
            else:
                return f"Query(X={len(self.X)}x{len(self.X[0])}, k={self.k})"


class LanguageAgnosticError(RuntimeError):
    pass


class LanguageAgnostic(BaseANN):
    """
    Language-Agnostic model proxy.
    Executes a model by sending HTTP requests to localhost:8080.
    Starts and manages the HTTP server as a subprocess.
    """

    def __init__(self, metric: str, dimension: int, index_params: dict, server_command: str, server_url: str, start_seconds: int):
        self.metric = metric
        self.dimension = dimension
        self.index_params = index_params
        self.server_url = server_url

        # Used by get_results method, defined in query method.
        self.res = []

        # Start the server subprocess.
        proc = Popen(shlex.split(server_command), stdout=sys.stdout, stderr=sys.stderr)

        # Server health check function.
        def check():
            poll = proc.poll()
            if poll is not None:
                raise LanguageAgnosticError(f"HTTP server process prematurely returned status code {poll}.")
            url = f"{server_url}/status"
            res = get(url)
            if res.status_code != 200:
                raise LanguageAgnosticError(f"Endpoint {url} returned status code {int(res.status_code)}.")
            print(f"HTTP server process is healthy")

        # Let the server start and then run an initial check.
        time.sleep(start_seconds)
        check()

        # Start a background thread to repeatedly check the server.
        def monitor():
            while True:
                time.sleep(10)
                check()
        t = Thread(target=monitor, args=(), daemon=True)
        t.start()

    def post(self, path: str, contract: Contract.Base, expected_status: int = 201) -> dict:
        body = contract.__dict__
        url = f"{self.server_url}/{path}"
        res = post(url, json=body)
        res.raise_for_status()
        if res.status_code != expected_status:
            raise LanguageAgnosticError(
                f"Endpoint {url} returned status code {int(res.status_code)}. Expected {expected_status}.")
        return res.json()

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        init_contract = Contract.Init(
            metric=self.metric,
            dimension=self.dimension,
            index_params=self.index_params,
            dataset=dataset
        )
        fit_contract = Contract.Fit(count=int(ds.nb))
        self.post("init", init_contract)
        self.post("fit", fit_contract)

    def load_index(self, dataset):
        return True

    def query(self, X, k):
        query_contract = Contract.Query([x.tolist() for x in X], k)
        self.res = self.post("query", query_contract, 200)

    def range_query(self, X, radius):
        print(f"Called range_query with {X}, {radius}")
        pass

    def get_range_results(self):
        return None

    def get_additional(self):
        return {}

    def set_query_arguments(self, query_args):
        set_query_arguments_contract = Contract.SetQueryArgs(query_args=query_args)
        self.post("set_query_arguments", set_query_arguments_contract)

    def __str__(self):
        return f"LanguageAgnostic model running on local server at {self.server_url}"


class SklearnRunner(LanguageAgnostic):

    def __init__(self, metric: str, dimension: int, use_dims: float):
        cmd = "python3 -m benchmark.algorithms.language_agnostic example"
        super().__init__(metric, dimension, dict(use_dims=use_dims), cmd, "http://localhost:8080", 3)


def example():

    from flask import Flask, request
    from sklearn.neighbors import NearestNeighbors

    app = Flask(__name__)

    # State is instantiated later but needs to be attached to an object to make Python happy.
    class State(object):
        pass
    state = State()
    state.algo = None
    state.dataset = None
    state.index_params = None
    state.high_variance_dims = None

    @app.route("/status", methods=['GET'])
    def status_handler():
        return jsonify(dict()), 200

    @app.route("/init", methods=['POST'])
    def init_handler():
        body = Contract.Init(**request.json)
        app.logger.info(body)
        state.algo = NearestNeighbors(algorithm='brute', metric=body.metric)
        state.dataset = DATASETS[body.dataset]()
        state.index_params = body.index_params
        return jsonify(dict()), 201

    @app.route("/fit", methods=['POST'])
    def fit_handler():
        body = Contract.Fit(**request.json)
        app.logger.info(str(body))
        arr = state.dataset.get_dataset()
        var = arr.var(axis=0)[:body.count]
        num_dims = int(state.index_params['use_dims'] * arr.shape[1])
        state.high_variance_dims = np.argsort(var)[-num_dims:]
        app.logger.info(f"Fitting KNN on the {num_dims} highest-variance dimensions out of {arr.shape[1]} dimensions.")
        state.algo.fit(arr[state.high_variance_dims])
        return jsonify(dict()), 201

    @app.route("/set_query_arguments", methods=['POST'])
    def set_query_arguments_handler():
        body = Contract.SetQueryArgs(**request.json)
        app.logger.info(str(body))
        return jsonify(dict()), 201

    @app.route("/query", methods=['POST'])
    def query_handler():
        body = Contract.Query(**request.json)
        app.logger.info(str(body))
        res = state.algo.kneighbors(body.X, n_neighbors=body.k, return_distance=False)
        res_lst = [arr.tolist() for arr in res]
        return jsonify(res_lst), 200


    # https://flask.palletsprojects.com/en/2.0.x/deploying/wsgi-standalone/#gevent
    app.run('0.0.0.0', 8080, debug=True)
    # http_server = WSGIServer(('0.0.0.0', 8080), app)
    # http_server.serve_forever()


# Run the SklearnExample in a Flask server.
if __name__ == "__main__" and sys.argv[-1] == "example":
    example()
