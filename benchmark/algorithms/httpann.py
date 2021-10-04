import shlex
import sys
import time
from subprocess import Popen
from threading import Thread

import numpy as np
import requests

from benchmark.algorithms.base import BaseANN


class HttpANN(BaseANN):
    """
    HTTP-based ANN algorithm.
    Designed to enable language-agnostic ANN by delegating indexing and querying to a separate HTTP server.

    The HTTP server must satisfy the following API.

    | Method | Route                | Request Body                                                                                               | Expected Status | Response Body                                                              |
    | ------ | -------------------- | ---------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------------------------------------------------- |
    | POST   | /init                | dictionary of constructor arguments, e.g., {"metric": "euclidean", "dimension": 99 }                       | 200             | { }                                                                        |
    | POST   | /load_index          | { "dataset": <dataset name, e.g. "bigann-10m"> }                                                           | 200             | { "load_index": <Boolean indicating whether the index has been loaded> }   |
    | POST   | /fit                 | { "dataset": <dataset name, e.g. "bigann-10m"> }                                                           | 200             | { }                                                                        |
    | POST   | /set_query_arguments | dictionary of query arguments                                                                              | 200             | { }                                                                        |
    | POST   | /query               | { "X": <query vectors as list of lists of floats>, "k": <number of neighbors to find and keep in memory> } | 200             | { }                                                                        |
    | POST   | /range_query         | { "X": <query vectors as list of lists of floats>, “radius”: <distance to neighbors> }                     | 200             | { }                                                                        |
    | POST   | /get_results         | { }                                                                                                        | 200             | { "get_results": <neighbors as list of lists of ints> }                    |
    | POST   | /get_additional      | { }                                                                                                        | 200             | { "get_additional": <dictionary of arbitrary additional result metadata> } |
    | POST   | /get_range_results   | { }                                                                                                        | 200             | { "get_range_results": <list of three 1-dimensional lists (lims, I, D)> }  |

    Note that this is a 1:1 copy of the BaseANN Python Class API implemented as remote procedure calls.
    """

    def __init__(self, server_url: str, start_seconds: int, name: str, **kwargs):
        """
        Base constructor for an HttpANN algorithm.
        @param server_url: base URL for the server including port, e.g., "http:localhost:8080"
        @param start_seconds: how many seconds to wait for the server to start before posting to the /init endpoint.
        @param name: algorithm name
        @param kwargs: any additional keyword arguments that will be passed through to the /init endpoint.
        """
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

    def set_query_arguments(self, *query_args):
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
