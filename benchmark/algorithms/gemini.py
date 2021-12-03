from __future__ import absolute_import
import numpy as np
import sklearn.preprocessing
import ctypes
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

def convert_index_to_cluster_and_ids_lists(index, nbits):
    cluster_list = np.empty(index.invlists.nlist, dtype=object)
    ids_list = np.empty(index.invlists.nlist, dtype=object)

    zero_count = 0

    for i in range(index.invlists.nlist):
        list_sz = index.invlists.list_size(i)

        if list_sz == 0:
            zero_count = zero_count + 1
            ids = None
        else:
            ids_ptr = index.invlists.get_ids(i)
            ids = np.array(faiss.rev_swig_ptr(ids_ptr, list_sz)).reshape(-1, 1).astype(np.uint32) # GSL requires a 2d arrray for some reason
            index.invlists.release_ids(ids_ptr)
            # index.invlists.release_ids(list_sz, ids_ptr)
        ids_list[i] = ids

        codes_ptr = index.invlists.get_codes(i)
        codes = np.array(faiss.rev_swig_ptr(codes_ptr, list_sz * nbits // 8)).reshape(list_sz, nbits//8)
        index.invlists.release_codes(codes_ptr)
        # index.invlists.release_codes(list_sz * nbits // 8, codes_ptr)
        cluster_list[i] = codes

    print('zero_count =', zero_count)
    return cluster_list, ids_list

def get_cluster_and_ids_lists(index, nbits):
    print('Creating cluster + ids lists...')
    ret = convert_index_to_cluster_and_ids_lists(index, nbits)
    return ret

def create_encoding(encoding_file_name, normalize=False):
    print("FILE LOAD PATH", encoding_file_name)
    single_np_array = np.load(encoding_file_name)
    # contains 6 arrays in a particular order
    layers = [NHEncoding.NHLayer(single_np_array[0], single_np_array[1].reshape(1, len(single_np_array[1]))),
              NHEncoding.NHLayer(single_np_array[2], single_np_array[3].reshape(1, len(single_np_array[3]))),
              NHEncoding.NHLayer(single_np_array[4], single_np_array[5].reshape(1, len(single_np_array[5])))]
    [ print(l.shape) for l in single_np_array ]
    return NHEncoding(layers, normalize)

class GeminiT3(BaseANN):
    def __init__(self, metric, index_params):
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
        self.index_params = ast.literal_eval(index_params)
        num_apuc = self.index_params['num_apuc']
        print("NUM_APUC", num_apuc)
        self.gsl_ctx = Context(gdl_ctx_ids[:num_apuc], max_num_threads=56)
        # GSL init end

        self.max_num_queries = 10000
        self.num_records = 1000000000

        print(f'GSI GeminiT3(BaseANN){self.index_params}')

    def index_name(self, name):
        nlist = self.index_params['nlist']
        qbits = self.index_params['qbits']
        nbits = self.index_params['nbits']
        nt = self.index_params['nt']
        is_f16 = self.index_params['f16']
        key = "nbits=%d,qbits=%d,nlist=%d,nt=%d,f16=%s" % (nbits, qbits, nlist, nt, str(is_f16))
        return f"data/{name}.{key}.geminiindex" 

    def fit(self, dataset):
        assert 0

    def load_index(self, dataset):

        nlist = self.index_params['nlist']
        qbits = self.index_params['qbits']
        nbits = self.index_params['nbits']
        nt = self.index_params['nt']
        is_f16 = self.index_params['f16']

        # number of centroids maps to an index subdir
        centroids_dirs = { 524288: 'centroids_512k/', 2097152: 'centroids_2m/', 4194304: 'centroids_4m/'}
        num_centroids_dir = centroids_dirs[nlist]

        # the index name is the parent folder of the index component files
        prefix = self.index_name( dataset )

        resources_path = ''
        case_dir = '1b/'
        resources_path_case = f'{resources_path}{case_dir}'

        fp_quantizer_file_name = f'{prefix}/{resources_path}{num_centroids_dir}Deep1B.nt{nt}.nlist{nlist}.quantizer'
        records_encoding_file_name = f'{prefix}/{resources_path}records_weights/records_weights.bits{nbits}.npy'
        centroids_encoding_file_name = f'{prefix}/{resources_path}{num_centroids_dir}centroids_weights.nt{nt}.nlist{nlist}.nbits{nbits}.npy'
        index_file_name = f'{prefix}/{resources_path_case}Deep1B.ivfbinnh.nt{nt}.nlist{nlist}.nb{self.num_records}.bits{qbits}.index'
        db_path = f'{prefix}/{resources_path_case}fdb.npy'

        print('********************** Paths ***************************')
        print('fp_quantizer_file_name =', fp_quantizer_file_name)
        if not os.path.isfile(fp_quantizer_file_name):
            raise FileNotFoundError(fp_quantizer_file_name)
        print('records_encoding_file_name =', records_encoding_file_name)
        if not os.path.isfile(records_encoding_file_name):
            raise FileNotFoundError(records_encoding_file_name)
        print('centroids_encoding_file_name =', centroids_encoding_file_name)
        if not os.path.isfile(centroids_encoding_file_name):
            raise FileNotFoundError(centroids_encoding_file_name)
        print('index_file_name =', index_file_name)
        if not os.path.isfile(index_file_name):
            raise FileNotFoundError(index_file_name)
        print('db_path =', db_path)
        if not os.path.isfile(db_path):
            raise FileNotFoundError(db_path)            
        print('********************************************************')

        self.centroids_encoding = create_encoding(centroids_encoding_file_name, False)
        print("centroids", centroids_encoding_file_name, self.centroids_encoding)
        self.records_encoding = create_encoding(records_encoding_file_name, False)
        print("records", records_encoding_file_name, self.records_encoding)

        print('load XF deep-1B')
        num_features = 96
        dtype = gsld_rerank.GSLD_RERANK_DATA_TYPE_FLOAT

        print('init rerank...')
        self.rerank = gsld_rerank.init(self.num_records, num_features, num_features * 4, dtype, gsld_rerank.GSLD_RERANK_ALGO_L2, is_f16, db_path)        
        print('finished init rerank')
        
        print(f'GSI loading index:{index_file_name}')
        self.index = faiss.read_index_binary(index_file_name)

        # cluster_list, ids_list = get_cluster_and_ids_lists(self.index, nbits)
        cluster_list, ids_list = get_cluster_and_ids_lists(self.index, qbits)

        print('creating GSL cluster binary DB...')
        self.clstr_bdb = self.gsl_ctx.create_cluster_bdb(cluster_list, ids_list)
        del cluster_list
        del ids_list

        quantizer = faiss.downcast_IndexBinary(self.index.quantizer)
        centroids = faiss.vector_to_array(quantizer.xb)
        centroids = np.reshape(centroids, (quantizer.ntotal, quantizer.d//8))
        self.centroids_bdb = self.gsl_ctx.create_bdb(centroids)
        del centroids

        l2_quantizer = faiss.read_index(fp_quantizer_file_name)
        l2_centroids = faiss.vector_float_to_array(l2_quantizer.xb)
        l2_centroids = np.reshape(l2_centroids, (nlist, l2_quantizer.d))
        print('centroids (float):', l2_centroids.shape, l2_centroids.dtype)
        print('creating GSL centroids float DB...')
        self.centroids_fdb = self.gsl_ctx.create_fdb(l2_centroids, False)

        self.centroids_encoding = create_encoding(centroids_encoding_file_name, False)
        print("centroids", centroids_encoding_file_name, self.centroids_encoding)
        self.records_encoding = create_encoding(records_encoding_file_name, False)
        print("records", records_encoding_file_name, self.records_encoding)

        return True

    def set_query_arguments(self, query_args):

        #destroy previous runs' seesion
        try:
            print('destroying search session')
            self.session_hdl.destroy()
        except AttributeError:
            print('no session to destroy')

        typical_num_queries = self.max_num_queries

        self.search_params = ast.literal_eval(query_args)
        nprobe = self.search_params['nprobe']
        nprobe_refine = self.search_params['nprobe_refine']
        hamming_k = self.search_params['hamming_k']
        average_clstr_size_factor = self.search_params['average_clstr_size_factor']

        print('--->', 'nprobe =', nprobe, 'nprobe_refine =', nprobe_refine, 'hamming_k =', hamming_k, 
            'average_clstr_size_factor =', average_clstr_size_factor)

        rerank_desc = RerankDesc(self.centroids_fdb, nprobe_refine, gsl.GSL_ALG_KNN_L2_FDB)

        desc = ClusterHammingDesc(self.max_num_queries,
                                  typical_num_queries,
                                  self.centroids_bdb,
                                  nprobe,
                                  hamming_k,
                                  rerank_desc,
                                  self.centroids_encoding,
                                  self.records_encoding,
                                  self.clstr_bdb,
                                  average_clstr_size_factor)
                          
        self.session_hdl = self.gsl_ctx.create_session(desc)
        print('Created GSL session')
        self.gsl_ctx.search_in_focus(self.session_hdl)
        print('Set GSL session in focus')

    def get_additional(self):
        return {"dist_comps": faiss.cvar.indexIVF_stats.ndis}

    def __str__(self):
        return f'GSI:{self.index_params} {self.search_params}'

    def query(self, X, n):

        print('Performing search on GSL')
        out_shape = (X.shape[0], self.search_params['hamming_k'])
        outputs = ClusterFlatOutputs(np.empty(out_shape, dtype=np.uint32), np.empty(out_shape, dtype=np.float32))
        out_indices, out_distances = self.gsl_ctx.search(ClusterInputs(X), outputs)
        print('Finished search on GSL')

        print('run rerank...')
        start = time.time()
        res_idx, res_val = gsld_rerank.rerank(self.rerank, X, out_indices, n, 56)
        end = time.time()
        print('rerank time(milisec): ', (end - start) * 1000)
        self.res = out_distances.astype(np.int32), res_idx.astype(np.int64) 

    def range_query(self, X, radius):
        print('in range query <-----')

    def get_results(self):
        print('in get_results <-----')
        D, I = self.res
        return I

    def get_range_results(self):
        print('in get_range_results <-----')
        return self.res

    def __del__(self):
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
