from __future__ import absolute_import
import numpy as np
import faiss
import os
import time
import ast
from tqdm import tqdm

from benchmark.algorithms.base import BaseANN
from benchmark.datasets import DATASETS, download_accelerated

# GSL stuff
import gdl_bindings as gdl
import gsl_bindings as gsl
from tmp_api import *
import gsl_utils
import gsld_bindings_rerank as gsld_rerank
import h5py

num_records = 1000000000

def time_diff_to_mins_and_secs(time_diff):
    return int(time_diff / 60), int(time_diff % 60)

def knn_to_range(vals, indices, radius):
    count_st_radius = np.sum(vals < radius, axis=1)
    total_num_res = np.sum(count_st_radius)
    n = len(count_st_radius)
    #debugging
    print('debug: total_num_res =', total_num_res)
    print('debug: average =', total_num_res / n)
    print('debug: count_st_radius[0] =', count_st_radius[0])
    print('debug: count_st_radius[50000] =', count_st_radius[50000])
    print('debug: count_st_radius[90000] =', count_st_radius[90000])
    res_limits = np.empty(n + 1, indices.dtype)
    res_vals = np.empty(total_num_res, vals.dtype)
    res_indices = np.empty(total_num_res, indices.dtype)

    offset = 0
    for i in range(n):
        res_limits[i] = offset
        count = count_st_radius[i]
        next_offset = offset + count
        res_vals[offset:next_offset] = vals[i][:count]
        res_indices[offset:next_offset] = indices[i][:count]
        offset = next_offset
    res_limits[n] = offset

    return res_limits, res_vals, res_indices

def read_clusters_and_indices_from_file_into_arrays(filename):
    num_features = None
    np_num_rows_per_cluster = None
    np_records_raw_data = None
    np_indices_raw_data = None
    with h5py.File(filename, 'r') as fh5:
        num_features = int(fh5.attrs['num_features'])
        num_rows_per_cluster = fh5['num_rows_per_cluster']
        records_raw_data = fh5['records_raw_data']
        indices_raw_data = fh5['indices_raw_data']
        centroids_ds = fh5['centroids_ds']

        np_num_rows_per_cluster = np.empty(num_rows_per_cluster.shape, num_rows_per_cluster.dtype)
        num_rows_per_cluster.read_direct(np_num_rows_per_cluster)

        np_records_raw_data = np.empty(records_raw_data.shape, records_raw_data.dtype)
        records_raw_data.read_direct(np_records_raw_data)

        np_indices_raw_data = np.empty(indices_raw_data.shape, indices_raw_data.dtype)
        indices_raw_data.read_direct(np_indices_raw_data)

        np_centroids = np.empty(centroids_ds.shape, centroids_ds.dtype)
        centroids_ds.read_direct(np_centroids)

    return num_features, np_num_rows_per_cluster, np_records_raw_data, np_indices_raw_data, np_centroids

def create_encoding(encoding_file_name, normalize=False):
    single_np_array = np.load(encoding_file_name, allow_pickle=True)
    # contains 6 arrays in a particular order
    layers = [NHEncoding.NHLayer(single_np_array[0], single_np_array[1].reshape(1, len(single_np_array[1]))),
              NHEncoding.NHLayer(single_np_array[2], single_np_array[3].reshape(1, len(single_np_array[3]))),
              NHEncoding.NHLayer(single_np_array[4], single_np_array[5].reshape(1, len(single_np_array[5])))]
    return NHEncoding(layers, normalize)

class GeminiT3(BaseANN):
    def __init__(self, metric, index_params):

        gsl_metrics = {'euclidean': gsl.GSL_ALG_KNN_L2_FDB, 'ip': gsl.GSL_ALG_KNN_COSIM_FDB, 'angular': gsl.GSL_ALG_KNN_COSIM_FDB}
        rerank_metrics = {'euclidean': gsld_rerank.GSLD_RERANK_ALGO_L2, 'ip': gsld_rerank.GSLD_RERANK_ALGO_COSINE, 'angular': gsld_rerank.GSLD_RERANK_ALGO_COSINE}
        # The difference between 'ip' (inner product) and 'angular' seems to be that 'angular' includes the division by norms. This might impact on whether we need to pass the normalize flag to NHEncodin etc.

        self.gsl_metric = gsl_metrics[metric]
        self.rerank_metric = rerank_metrics[metric]

        # GSL init
        s = gdl.gdl_init()
        if s:
            raise Exception('gdl.gdl_init() failed with {}'.format(s))
        s, n_gdl_ctxs = gdl.gdl_context_count_get()
        if s:
             raise Exception('gdl.gdl_context_count_get() failed with {}'.format(s))

        s, gdl_desc_list = gdl.gdl_context_desc_get(n_gdl_ctxs)
        if s:
            raise Exception('gdl.gdl_context_desc_get() failed with {}'.format(s))

        gdl_ctx_ids = [desc.ctx_id for desc in gdl_desc_list if desc.status == gdl.GDL_CONTEXT_READY]
        if not gdl_ctx_ids:
            raise Exception("No valid context found")

        self._index_params = index_params
        self._metric = metric
        print('index_params =\n', index_params)
        self.index_params = ast.literal_eval(index_params)
        self.num_apuc = self.index_params['num_apuc']
        self.num_threads = self.index_params['num_threads']
        if self.num_threads == 0:
            self.num_threads = os.cpu_count()
        self.gsl_ctx = Context(gdl_ctx_ids[:self.num_apuc], max_num_threads=self.num_threads)
        # GSL init end

        #gw
        self.rerank_time = 0
        #gw

        print(f'GeminiT3(BaseANN){self.index_params}')

    def index_name(self, name):
        assert 0

    def fit(self, dataset):
        assert 0

    def load_index(self, dataset):
        load_index_start = time.time()
        files_directory = self.index_params['files_directory']

        fp_quantizer_file_name = self.index_params['fp_quantizer_file_name']
        fp_quantizer_file_path = f'{files_directory}{fp_quantizer_file_name}'

        records_encoding_file_name = self.index_params['records_encoding_file_name']
        records_encoding_file_path = f'{files_directory}{records_encoding_file_name}'

        centroids_encoding_file_name = self.index_params['centroids_encoding_file_name']
        centroids_encoding_file_path = f'{files_directory}{centroids_encoding_file_name}'

        hd5_file_path = self.index_params['hd5_file_path']

        db_file_name = self.index_params['db_file_name']
        db_file_path = f'{files_directory}{db_file_name}'

        rerank_bf16 = self.index_params['rerank_bf16']
        rerank_types = {'U8': gsld_rerank.GSLD_RERANK_DATA_TYPE_U8, 'S8': gsld_rerank.GSLD_RERANK_DATA_TYPE_S8, 'F32': gsld_rerank.GSLD_RERANK_DATA_TYPE_FLOAT,	'BF16': gsld_rerank.GSLD_RERANK_DATA_TYPE_BFLOAT16 }
        np_rerank_types = {'U8': np.uint8, 'S8': np.int8, 'F32': np.float32, 'BF16': np.float32 }
        rerank_types_sizes = {'U8': 1, 'S8': 1, 'F32': 4,	'BF16': 2}
        rerank_src_type_str = self.index_params['rerank_src_type']
        self.rerank_src_type = rerank_types[rerank_src_type_str]
        rerank_dtype_size = rerank_types_sizes[rerank_src_type_str]
        nbits = self.index_params['nbits']
        nlist = self.index_params['nlist']
        num_features = self.index_params['num_features']
        self.max_num_queries = self.index_params['max_num_queries']

        print('********************** Paths ***************************')
        print('fp_quantizer_file_path =', fp_quantizer_file_path)
        if not os.path.isfile(fp_quantizer_file_path):
            raise FileNotFoundError(fp_quantizer_file_path)
        print('records_encoding_file_path =', records_encoding_file_path)
        if not os.path.isfile(records_encoding_file_path):
            raise FileNotFoundError(records_encoding_file_path)
        print('centroids_encoding_file_path =', centroids_encoding_file_path)
        if not os.path.isfile(centroids_encoding_file_path):
            raise FileNotFoundError(centroids_encoding_file_path)
        print('hd5_file_path =', hd5_file_path)
        if not os.path.isfile(hd5_file_path):
            raise FileNotFoundError(hd5_file_path)
        print('db_file_path =', db_file_path)
        if not os.path.isfile(db_file_path):
            raise FileNotFoundError(db_file_path)            
        print('********************************************************')

        print('init rerank...')
        self.rerank = gsld_rerank.init(num_records, num_features, num_features * rerank_dtype_size, self.rerank_src_type, self.rerank_metric, rerank_bf16, db_file_path)        
        print('finished init rerank')

        #warm up the rerank module with a dummy query
        print('warming up rerank...')
        final_k = 10
        random_hamming_k = 1024
        random_queries = (np.random.random(num_features) * 128).astype(np_rerank_types[rerank_src_type_str]).reshape(1, -1)
        random_indices = (np.random.random(random_hamming_k) * num_records).astype(np.uint32).reshape(1, -1)
        gsld_rerank.rerank(self.rerank, random_queries, random_indices, final_k, self.num_threads)
        print('finished warming up rerank')

        fp_quantizer = faiss.read_index(fp_quantizer_file_path)
        fp_centroids = faiss.vector_float_to_array(fp_quantizer.xb)
        fp_centroids = np.reshape(fp_centroids, (nlist, fp_quantizer.d))
        print('centroids (float):', fp_centroids.shape, fp_centroids.dtype)
        print('creating GSL centroids float DB...')
        self.centroids_fdb = self.gsl_ctx.create_fdb(fp_centroids, False)

        self.centroids_encoding = create_encoding(centroids_encoding_file_path, False)
        self.records_encoding = create_encoding(records_encoding_file_path, False)

        print('loading binary clusters into memory...')
        f, np_num_rows_per_cluster, np_records_raw_data, np_indices_raw_data, np_centroids = read_clusters_and_indices_from_file_into_arrays(hd5_file_path)

        print('centroids (binary):', np_centroids.shape, np_centroids.dtype)
        print('creating GSL centroids binary DB...')
        self.centroids_bdb = self.gsl_ctx.create_bdb(np_centroids)
        print('creating GSL cluster binary DB...')
        self.clstr_bdb = self.gsl_ctx.create_cluster_bdb_simple(8*f, np_num_rows_per_cluster, np_records_raw_data, np_indices_raw_data)
        load_index_end = time.time()

        m, s = time_diff_to_mins_and_secs(load_index_end - load_index_start)

        self.rerank_time = 0

        print(f'Load time = {m} m {s} s')

        return True

    def set_query_arguments(self, query_args):

        #destroy previous runs' session
        try:
            print('attempting to destroy search session...')
            self.session_hdl.destroy()
            print('destroyed search session')
        except AttributeError:
            print('no session to destroy')

        if self.rerank_time != 0:
            print('total rerank time =', self.rerank_time)
            self.rerank_time = 0

        typical_num_queries = self.max_num_queries

        self.search_params = ast.literal_eval(query_args)
        nprobe = self.search_params['nprobe']
        nprobe_refine = self.search_params['nprobe_refine']
        hamming_k = self.search_params['hamming_k']
        average_clstr_size_factor = self.search_params['average_clstr_size_factor']
        print('--->', 'nprobe =', nprobe, 'nprobe_refine =', nprobe_refine, 'hamming_k =', hamming_k, 'average_clstr_size_factor =', average_clstr_size_factor)

        rerank_desc = RerankDesc(self.centroids_fdb, nprobe_refine, self.gsl_metric)
        
        desc = ClusterHammingDesc(self.max_num_queries,
                                  typical_num_queries,
                                  self.centroids_bdb,
                                  nprobe,
                                  hamming_k,
                                  rerank_desc,
                                  self.centroids_encoding,
                                  self.records_encoding,
                                  self.clstr_bdb,
                                  average_clstr_size_factor,
                                  gsl.GSL_CLSTR_HAMMING_CENTROID_FLAT_PARALLEL_SEARCH_FLAG if self.num_apuc == 4 else gsl.GSL_CLSTR_HAMMING_CENTROID_FLAT_DEFAULT_SEARCH_FLAG)
                          
        self.session_hdl = self.gsl_ctx.create_session(desc)
        print('Created GSL session')
        self.gsl_ctx.search_in_focus(self.session_hdl)
        print('Set GSL session in focus')

    # shall we return something interesting here?
    def get_additional(self):
        return {"dist_comps": faiss.cvar.indexIVF_stats.ndis}

    def __str__(self):
        return f'GeminiT3:{self.index_params} {self.search_params}'

    def query(self, X, n):

        print('queries =', X.shape, 'dtype =', X.dtype)
        print('Performing search on GSL')
        out_shape = (X.shape[0], self.search_params['hamming_k'])
        print('out_shape =', out_shape)
        outputs = ClusterFlatOutputs(np.empty(out_shape, dtype=np.uint32), np.empty(out_shape, dtype=np.float32))
        out_indices, out_distances = self.gsl_ctx.search(ClusterInputs(X), outputs)
        print('Finished search on GSL')

        print('run rerank...')
        rerank_start = time.time()
        if self.rerank_src_type == gsld_rerank.GSLD_RERANK_DATA_TYPE_S8:
            X = X.astype(np.int8)
        elif self.rerank_src_type == gsld_rerank.GSLD_RERANK_DATA_TYPE_U8:
            X = X.astype(np.uint8)
        res_idx, res_val = gsld_rerank.rerank(self.rerank, X, out_indices, n, self.num_threads)
        rerank_end = time.time()
        rerank_time = rerank_end - rerank_start
        print('rerank time(s): ', rerank_time)
        self.rerank_time += rerank_time
        self.res = out_distances.astype(np.int32), res_idx.astype(np.int64) #TODO: ask Josh about data-type of distances

    def range_query(self, X, radius):
        print('in range query <-----')
        print('X =', X.dtype, X.shape, 'radius =', radius)
        Y = X - 128

        print('Performing search on GSL')
        out_shape = (Y.shape[0], self.search_params['hamming_k'])
        print('out_shape =', out_shape)
        outputs = ClusterFlatOutputs(np.empty(out_shape, dtype=np.uint32), np.empty(out_shape, dtype=np.float32))
        out_indices, out_distances = self.gsl_ctx.search(ClusterInputs(Y), outputs)
        print('Finished search on GSL')

        print('run rerank...')
        rerank_start = time.time()
        if self.rerank_src_type == gsld_rerank.GSLD_RERANK_DATA_TYPE_S8:
            X = X.astype(np.int8)
        elif self.rerank_src_type == gsld_rerank.GSLD_RERANK_DATA_TYPE_U8:
            X = X.astype(np.uint8)
        res_idx, res_val = gsld_rerank.rerank(self.rerank, X, out_indices, self.search_params['hamming_k']-1, self.num_threads)
        rerank_end = time.time()
        rerank_time = rerank_end - rerank_start
        print('rerank time(s): ', rerank_time)
        self.rerank_time += rerank_time

        self.res = knn_to_range(res_val, res_idx, radius)
        
        lims, D, I = self.res

        np.set_printoptions(threshold=10000)
        print('radius:', radius)
        print('x:', X[0])
        print('res_idx:', res_idx[0])
        print('out_indices:', out_indices[0])

        print('I:', I[:40])
        print('D:', D[:40])
        print('lims:', lims[:40])
        

    def get_results(self):
        print('in get_results <-----')
        D, I = self.res
        return I

    def get_range_results(self):
        print('in get_range_results <-----')
        return self.res

    def __del__(self):
        if self.rerank_time != 0:
            print('total rerank time =', self.rerank_time)
        print('exit rerank...')
        gsld_rerank.exit(self.rerank)
        print('destroying search session')
        self.session_hdl.destroy()
        print('destroying centroids float DB')
        self.centroids_fdb.destroy()    
        print('destroying centroids binary DB')
        self.centroids_bdb.destroy()
        print('destroying cluster binary DB')
        self.clstr_bdb.destroy()
        del self.gsl_ctx
        s = gdl.gdl_exit()
        if s:
            raise Exception('gdl.gdl_exit failed with {}'.format(s))
