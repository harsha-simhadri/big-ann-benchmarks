import json
import shlex
import sys
import time
from dataclasses import dataclass
from subprocess import Popen, PIPE
from typing import TextIO, Union

from benchmark.algorithms.base import BaseANN


class Protocol:
    prefix: str = "bannb"

    @dataclass(init=False, frozen=True)
    class Message:
        pass

    @dataclass(frozen=True)
    class InitModel(Message):
        metric: str
        dataset: str
        dimension: int
        index_params: Union[dict, list]
        cmd: str = "init_model"

    @dataclass(frozen=True)
    class StatusOK(Message):
        status: str = "OK"


class ProtocolHandler(object):

    def __init__(self, read_buf: TextIO, write_buf: TextIO):
        self.read_buf = read_buf
        self.write_buf = write_buf

    def read(self) -> dict:
        while True:
            line = self.read_buf.readline().strip()
            if line.startswith(Protocol.prefix):
                rest = line[len(Protocol.prefix) + 1:]
                return json.loads(rest)

    def write(self, msg: Protocol.Message) -> None:
        s = f"{Protocol.prefix} {json.dumps(msg.__dict__)}\n"
        self.write_buf.write(s)


class LanguageAgnostic(BaseANN):
    """
    Language-Agnostic model (wrapper).
    Starts a subprocess which implements the actual model.
    Executes the model by sending and receiving JSON-formatted messages to/from the subprocess over stdin and stdout.

    Command protocol:

    1. Initialize the model.

    send    bannbcmd { "cmd": "init_model",
                       "metric": <metric name, e.g., "euclidean">,
                       "dataset": <dataset name, e.g., "bigann-10M">,
                       "dimension": <integer vector dimension, e.g., 128>,
                       "index_params" <JSON dictionary of indexing parameters> }
    receive bannbcmd { "status": "OK" }

    2. Fit the model.

    send     {
               "cmd": "fit",
               "path": <absolute path to dataset file, e.g., "/home/app/data/bigann/base.1B.u8bin">,
               "count": <integer number of vectors to index from the front of the file, e.g., 10000000
             }
    receive  { "status": "OK" }

    3. Initialize the queries.

    4. Execute the queries.

    5. Shutdown.

    send     {
               "cmd": "shutdown"
             }
    receive  Nothing

    """

    def __init__(self, metric: str, dimension: int, index_params: dict, cmd: str):
        self.metric = metric
        self.dimension = dimension
        self.index_params = index_params
        self.proc = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, bufsize=1, universal_newlines=True)
        self.h = ProtocolHandler(self.proc.stdout, self.proc.stdin)

    def fit(self, dataset):
        init_msg = Protocol.InitModel(self.metric, dataset, self.dimension, self.index_params)
        print(self.proc.poll())
        self.h.write(init_msg)
        time.sleep(1)
        print(self.proc.poll())

        # print(f"Waiting on response")
        # ds = DATASETS[dataset]()
        # print(dataset, ds.basedir, ds.ds_fn)
        # pass

    def load_index(self, dataset):
        pass

    def query(self, X, k):
        pass

    def range_query(self, X, radius):
        pass

    def get_range_results(self):
        pass

    def get_additional(self):
        pass

    def set_query_arguments(self, query_args):
        pass

    def __str__(self):
        return "DiskANN"


class SklearnRunner(LanguageAgnostic):

    def __init__(self, metric: str, dimension: int, use_dims: float):
        cmd = "python3 -m benchmark.algorithms.language_agnostic example"
        super().__init__(metric, dimension, dict(use_dims=use_dims), cmd)


class SklearnExample(object):
    """
    Relatively simple example that just uses scikit-learn nearest neighbors on a dimensionality-reduced dataset.
    """

    def __init__(self, metric: str, dimension: int, index_params: dict):
        pass


# Run the SklearnExample in a python sub-process.
if __name__ == "__main__" and sys.argv[-1] == "example":

    h = ProtocolHandler(sys.stdin, sys.stdout)

    # Handle the init command.
    init_dict = h.read()
    init_msg = Protocol.InitModel(**init_dict)
    model = SklearnExample(init_msg.metric, init_msg.dimension, init_msg.index_params)
    h.write(Protocol.StatusOK())
