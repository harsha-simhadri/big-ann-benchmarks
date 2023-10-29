import os
import subprocess
import time

from neurips23.ood.base import BaseOODANN
from benchmark.datasets import DATASETS, download_accelerated

import ngtpy

class NGT(BaseOODANN):
    def __init__(self, metric, params):
        metrics = {"euclidean": "2", "angular": "E", "ip": "i"}
        self._params = params
        self._edge_size = int(params["edge"])
        self._outdegree = int(params["outdegree"])
        self._indegree = int(params["indegree"])
        self._metric = metrics[metric]
        self._edge_size_for_search = int(params["search_edge"]) if "search_edge" in params.keys() else 0
        self._build_time_limit = float(params["timeout"]) if "timeout" in params.keys() else 12
        self._epsilon = float(params["epsilon"]) if "epsilon" in params.keys() else 0.1
        self._reduction_range = float(params["reduction"]) if "reduction" in params.keys() else 1.8
        print("ONNG: edge_size:", self._edge_size)
        print("ONNG: outdegree:", self._outdegree)
        print("ONNG: indegree=:", self._indegree)
        print("ONNG: edge_size_for_search:", self._edge_size_for_search)
        print("ONNG: epsilon:", self._epsilon)
        print("ONNG: reduction range:", self._reduction_range)
        print("ONNG: metric:", metric)

    def get_title(self):
        return "index-%s-%s-%s-%.2f-%.2f" % (
            self._edge_size,
            self._outdegree,
            self._indegree,
            self._epsilon,
            self._reduction_range,
        )

    def set_index_path(self, dataset):
        self._index_dir = os.path.join("data", "indices", "ood", "ngt", self.get_title())
        self._index_path = os.path.join(self._index_dir, "onng")
        self._sanng_path = os.path.join(self._index_dir, "sanng")
        self._anng_path = os.path.join(self._index_dir, "anng-" + str(self._edge_size))

    def fit(self, dataset):
        print("ONNG: start indexing...")
        ds = DATASETS[dataset]()
        print("ONNG: dataset:", dataset)
        print("ONNG: dataset str:", ds.__str__())
        print("ONNG: distance:", ds.distance())
        print("ONNG: dimension:", ds.d)
        print("ONNG: type:", ds.dtype)
        print("ONNG: nb:", ds.nb)
        print("ONNG: dataset file name:", ds.get_dataset_fn())
        print("ONNG: index path:", self._index_path)
        self.set_index_path(dataset)
        if not os.path.exists(self._index_dir):
            os.makedirs(self._index_dir)
        print("ONNG: index:", self._index_path)
        dim = ds.d
        if (not os.path.exists(self._index_path)) and (not os.path.exists(self._sanng_path)):
            print("ONNG: create a sparse ANNG to optimize the graph.")
            t = time.time()
            args = [
                "ngt",
                "create",
                "-v",
                "-it",
                "-p8",
                "-b500",
                "-ga",
                "-of",
                "-D" + self._metric,
                "-d" + str(dim),
                "-E5",
                "-S-2",
                "-e0.0",
                "-P0",
                "-B30",
                "-T0",
                self._sanng_path,
            ]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            print("ONNG: append for SANNG")
            args = ["ngt", "append", "-mb",
                    "-n" + str(ds.nb),
                    self._sanng_path,
                    ds.get_dataset_fn()]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            print("ONNG: SANNG appending time(sec)=" + str(time.time() - t))
            print("ONNG: build a sparse ANNG index.")
            t = time.time()
            args = ["ngt", "construct-graph", "-v", "-G-", "-E0.0", "-S100",
                    self._sanng_path]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            print("ONNG: SANNG index build time(sec)=", str(time.time() - t))

        if (not os.path.exists(self._index_path)) and (not os.path.exists(self._anng_path)):
            print("ONNG: build ANNG")
            t = time.time()
            args = [
                "ngt",
                "create",
                "-v",
                "-it",
                "-p8",
                "-b20",
                "-ga",
                "-of",
                "-D" + self._metric,
                "-d" + str(dim),
                "-E18",
                "-S" + str(self._edge_size_for_search),
                "-e" + str(self._epsilon),
                "-P0",
                "-B30",
                "-T" + str(self._build_time_limit),
                self._anng_path,
            ]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            print("ONNG: degree adjustment")
            t = time.time()
            args = [
                "ngt",
                "construct-graph",
                "-v",
                "-Go",
                "-T0",
                "-P0",
                "-N" + str(self._edge_size),
                "-O" + str(self._outdegree),
                "-I" + str(self._indegree),
                self._anng_path,
                self._sanng_path,
            ]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            print("ONNG: degree ajustment time(sec)=" + str(time.time() - t))
        if not os.path.exists(self._index_path):
            print("ONNG: shortcut reduction")
            t = time.time()
            args = [
                "ngt",
                "reconstruct-graph",
                "-v",
                "-R" + str(self._reduction_range),
                "-mS",
                "-Ps",
                "-sp",
                "-o0",
                "-i0",
                self._anng_path,
                self._index_path,
            ]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            print("ONNG: shortcut reduction time(sec)=" + str(time.time() - t))
        if os.path.exists(self._index_path):
            print("ONNG: index already exists!", self._index_path)
            t = time.time()
            self.index = ngtpy.Index(self._index_path, read_only=True, tree_disabled=False)
            self.indexName = self._index_path
            print("ONNG: open time(sec)=" + str(time.time() - t))
        else:
            print("ONNG: something wrong...")
        print("ONNG: end of fit")

    def load_index(self, dataset):
        self.set_index_path(dataset)
        if not os.path.exists(self._index_path + "/grp"):
            if "url" not in self._params:
                return False
            if not os.path.exists(self._index_dir):
                os.makedirs(self._index_dir)
            tar_file = self._index_path + ".tgz";
            if not os.path.exists(tar_file):
                print("ONNG: downloading the index... index={} => {}".format(self._params["url"], self._index_path))
                download_accelerated(self._params["url"], tar_file, quiet=True)
            args = ["tar", "zxf", tar_file, "-C", self._index_dir]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            args = ["rm", "-r", tar_file]
            print("ONNG: '{}'".format(" ".join(args)))
            subprocess.run(args, check=True)
            os.makedirs(self._sanng_path)
            os.makedirs(self._anng_path)

    def set_query_arguments(self, query_args):
        epsilon = query_args.get("epsilon", 1.0)
        edge_size = query_args.get("edge", 0)
        print("ONNG: edge_size:", edge_size)
        print("ONNG: epsilon:", epsilon)
        self.name = "ngt-onng(%s, %s, %s, %s, %s)" % (
            self._edge_size,
            self._outdegree,
            self._indegree,
            self._reduction_range,
            epsilon,
        )
        epsilon = epsilon - 1.0
        self.index.set(epsilon=epsilon, edge_size=edge_size)

    def query(self, X, n):
        self._results = ngtpy.BatchResults()
        return self.index.batch_search(X, self._results, n, with_distance=False)

    def get_results(self):
        return self._results.get_ids()
    
