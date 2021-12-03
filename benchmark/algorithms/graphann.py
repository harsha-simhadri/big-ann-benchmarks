import os
import psutil
import shutil

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

# Bootstrap importing GraphANN code
import julia
from julia import Pkg
Pkg.activate(os.getenv("PYANN_ROOT"))
Pkg.instantiate()
from julia import PyANN

class GraphANN(BaseANN):
    def __init__(self, metric, index_params):
        self.name = "GraphANN"
        self._index_params = index_params

        self._vectors_file = index_params.get('vectors_file')
        self._index_file = index_params.get('index_file')
        
        if index_params.get('vectors_location')=='DRAM':
            self._allocator = PyANN.stdallocator
        elif index_params.get('vectors_location')=='HUGE':
            self._allocator = PyANN.hugepage_1gib_allocator
        elif index_params.get('vectors_location')=='PMEM':
            self._allocator = PyANN.direct_mmap
        else:
            self._allocator = PyANN.stdallocator
            
        # unpack params
        #self._search_window_size = index_params.get("search_window_size")

        # Manually instantiate the metric
        if metric == "euclidean":
            self._metric = PyANN.Euclidean()
        elif metric == "angular":
            self._metric = PyANN.InnerProduct()
        else:
            print("Error: unknown metric {}".format(metric))

        # Other helpful parameters
        self.PQ = 0 if index_params.get("PQ") == None else index_params.get("PQ")

    #####
    ##### BaseANN API
    #####

    def track(self):
        return "T3"

    def fit(self, dataset):
        raise NotImplementedError()

    def load_index(self, dataset):
        ds = DATASETS[dataset]()
        # Metric
        if ds.distance() == "euclidean":
            self._metric = PyANN.Euclidean()
            numacopy = True
        elif ds.distance() == "ip":
            self._metric = PyANN.InnerProduct()
            numacopy = False
        else:
            print("Unsuported distance function.")
            return False

        # Data Type
        if ds.dtype == "float32":
            self._dtype = PyANN.Float16
        elif ds.dtype == "int8":
            self._dtype = PyANN.Int8
        elif ds.dtype == "uint8":
            self._dtype = PyANN.UInt8
        else:
            print ("Unsupported data type.")
            return False

        # Dimensionality
        self._dims = ds.d

        # Load the index and query runner
        self._index = PyANN.loadindex(
            self.create_index_dir(ds),
            self._dtype,
            self._dims,
            self._metric,
            allocator = self._allocator,
            diskann_format = True,
            numacopy = numacopy,
            datapath = "/mnt/pm0/public/data.bin"
        )
        self._runner = PyANN.make_runner(
            self._index,
            16
        )
        # TODO: warm up compilation and runner

        return True

    def index_files_to_store(self, dataset):
        raise NotImplementedError()

    def query(self, X, k):
        self.res = PyANN.search(
            self._runner,
            self._index,
            X,
            k,
        )
        return True

    def range_query(self, X, radius):
        raise NotImplementedError()

    def get_results(self):
        return self.res

    def get_range_results(self):
        return self.res

    def get_additional(self):
        return {}

    def __str__(self):
        return self.name

    def get_memory_usage(self):
        """Return the current memory usage of this algorithm instance
        (in kilobytes), or None if this information is not available."""
        # return in kB for backwards compatibility
        return psutil.Process().memory_info().rss / 1024

    #####
    ##### Utilities
    #####

    def index_name(self):
        return "generic_index"

    def create_index_dir(self, dataset):
        index_dir0 = "/mnt/pm0/public"
        index_dir1 = "/mnt/pm1/public"
        os.makedirs(index_dir0, mode=0o777, exist_ok=True)
        os.makedirs(index_dir1, mode=0o777, exist_ok=True)
        graph_file0 = os.path.join(index_dir0,'graph.bin')
        print('Copying index to PMem...')
        if os.path.isfile(graph_file0):
            os.remove(graph_file0)
        shutil.copy(self._index_file, graph_file0)
        
        graph_file1 = os.path.join(index_dir1,'graph.bin')
        if os.path.isfile(graph_file1):
            os.remove(graph_file1)
        shutil.copy(self._index_file, graph_file1)
        print('done')
        
        print('Copying vectors to PMem...')
        vector_file = os.path.join(index_dir0,'data.bin')
        if os.path.isfile(vector_file):
            os.remove(vector_file)
        shutil.copy(self._vectors_file, vector_file)
        print('done')
        return [index_dir0, index_dir1]


    def set_query_arguments(self, query_args):
        self._query_args = query_args
        self._search_window_size = query_args.get("search_window_size")
        PyANN.resize(self._runner,self._search_window_size)

