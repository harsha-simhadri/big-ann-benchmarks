import pdb
import pickle
import numpy as np
import os

from multiprocessing.pool import ThreadPool
from threading import current_thread

import faiss


from faiss.contrib.inspect_tools import get_invlist
from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
from math import log10, pow


def csr_get_row_indices(m, i):
    """ get the non-0 column indices for row i in matrix m """
    return m.indices[m.indptr[i] : m.indptr[i + 1]]

def make_id_selector_ivf_two(docs_per_word):
    sp = faiss.swig_ptr
    return faiss.IDSelectorIVFTwo(sp(docs_per_word.indices), sp(docs_per_word.indptr))

def make_id_selector_cluster_aware(indices, limits, clusters, cluster_limits):
    sp = faiss.swig_ptr
    return faiss.IDSelectorIVFClusterAware(sp(indices), sp(limits), sp(clusters), sp(cluster_limits))

def make_id_selector_cluster_aware_intersect(indices, limits, clusters, cluster_limits, tmp_size):
    sp = faiss.swig_ptr
    return faiss.IDSelectorIVFClusterAwareIntersect(sp(indices), sp(limits), sp(clusters), sp(cluster_limits), int(tmp_size))

def make_id_selector_cluster_aware_direct(id_position_in_cluster, limits, clusters,  cluster_limits, tmp_size):
    sp = faiss.swig_ptr
    return faiss.IDSelectorIVFClusterAwareIntersectDirect(sp(id_position_in_cluster), sp(limits), sp(clusters), sp(cluster_limits), int(tmp_size))

def make_id_selector_cluster_aware_direct_exp(id_position_in_cluster, limits, nprobes, tmp_size):
    sp = faiss.swig_ptr
    return faiss.IDSelectorIVFClusterAwareIntersectDirectExp(sp(id_position_in_cluster), sp(limits), int(nprobes), int(tmp_size))


def find_invlists(index):
    try:
        inverted_lists = index.invlists
    except:
        base_index = faiss.downcast_index(index.base_index)
        print('cannot find the inverted list trying one level down')
        print('type of index', type(base_index))
        inverted_lists = base_index.invlists
    return inverted_lists

def print_stats():
    m = 1000000.
    intersection = faiss.cvar.IDSelectorMy_Stats.intersection/m
    find_cluster = faiss.cvar.IDSelectorMy_Stats.find_cluster/m
    set_list_time = faiss.cvar.IDSelectorMy_Stats.set_list_time/m
    scan_codes =  faiss.cvar.IDSelectorMy_Stats.scan_codes/m
    one_list = faiss.cvar.IDSelectorMy_Stats.one_list/m
    extra = faiss.cvar.IDSelectorMy_Stats.extra / m
    inter_plus_find = intersection + find_cluster
    print('intersection: {}, find_cluster: {}, intersection+ find cluster: {},  set list time: {}, scan_codes: {}, one list: {}, extra: {}'.format(intersection, find_cluster, inter_plus_find, set_list_time, scan_codes, one_list, extra))


def spot_check_filter(docs_per_word, index, indices, limits, clusters, cluster_limits):
    print('running spot check')


    inverted_lists = find_invlists(index)

    from_id_to_map = dict()
    for i in range(inverted_lists.nlist):
        list_ids, _ = get_invlist(inverted_lists, i)
        for id in list_ids:
            from_id_to_map[id] = i

    indptr = docs_per_word.indptr

    ## lets' run some spot check
    for word in [0, 5, 7]:
    #for word in range(docs_per_word.shape[0]):
    #for word in [docs_per_word.shape[0]-1 ]:
        c_start = cluster_limits[word]
        c_end = cluster_limits[word + 1]
        assert c_end >= c_start

        start = indptr[word]
        end = indptr[word + 1]
        ids_in_word = {id for id in docs_per_word.indices[start:end]}

        cluster_base = -1
        for pos, cluster in enumerate(clusters[c_start: c_end]):
            if cluster_base == -1:
                cluster_base = cluster
            else:
                assert cluster != cluster_base
                cluster_base = cluster
            for id in indices[limits[c_start + pos]: limits[c_start + pos + 1]]:
                assert from_id_to_map[id] == cluster
                assert id in ids_in_word
                ids_in_word.remove(id)
        assert len(ids_in_word) == 0  # we should have covered all the ids in the word with the clusters


def spot_check_filter_exp(docs_per_word, index, indices, limits):
    print('running spot check')


    inverted_lists = find_invlists(index)

    from_id_to_map = dict()
    for i in range(inverted_lists.nlist):
        list_ids, _ = get_invlist(inverted_lists, i)
        for id in list_ids:
            from_id_to_map[id] = i

    indptr = docs_per_word.indptr

    nprobes = inverted_lists.nlist

    ## lets' run some spot check
    for word in [0, 5000, 12124, 151123, 198000]:
    #for word in range(docs_per_word.shape[0]):
    #for word in [docs_per_word.shape[0]-1 ]:
        local_ids_to_cluster = dict()
        #print(limits[nprobes * word: nprobes * word + nprobes])
        for cluster in range(nprobes):
            c_start = limits[word * nprobes + cluster]
            c_end = limits[word * nprobes + cluster+1]

            if c_end >=0 and c_start >=0  and c_end > c_start:
                for id in indices[c_start: c_end]:
                    local_ids_to_cluster[id] = cluster



        start = indptr[word]
        end = indptr[word + 1]
        ids_in_word = {id for id in docs_per_word.indices[start:end]}
        print(len(ids_in_word), len(local_ids_to_cluster))
        assert len(ids_in_word) == len(local_ids_to_cluster)
        for id in ids_in_word:
            cluster_found = from_id_to_map[id]
            assert cluster_found == local_ids_to_cluster[id]
        print('done checking word ', word)

    print('done spot check')


def find_max_interval(limits):

    out = -1
    for i in range(len(limits)-1):
        delta = limits[i+1] - limits[i]
        if delta > out:
            out = delta
    return out


def prepare_filter_by_cluster(docs_per_word, index):
    print('creating filter cluster')
    inverted_lists = find_invlists(index)
    from_id_to_map = dict()
    from_id_to_pos = dict()
    for i in range(inverted_lists.nlist):
        list_ids, _ = get_invlist(inverted_lists, i)
        for pos, id in enumerate(list_ids):
            #print('list: ', i, "id: ", id, "pos: ",pos)
            from_id_to_map[id] = i
            from_id_to_pos[id] = pos
    print('loaded the mapping with {} entries'.format(len(from_id_to_map)))

    ## reorganize the docs per word
    #
    cluster_limits = [0]
    clusters = list()
    limits = list()
    id_position_in_cluster = list()

    indices = np.array(docs_per_word.indices)
    indptr = docs_per_word.indptr
    for word in range(docs_per_word.shape[0]):
        start = indptr[word]
        end = indptr[word + 1]
        if word % 10000 == 0:
            print('processed {} words'.format(word))
        array_ind_cluster = [(id, from_id_to_map[id]) for id in indices[start:end]]
        array_ind_cluster.sort(key=lambda x: x[1])

        if len(array_ind_cluster) == 0:
            pass
        local_clusters = []
        local_limits = []
        current_cluster = -1
        for pos, arr in enumerate(array_ind_cluster):
            id, cluster = arr
            if current_cluster == -1 or cluster != current_cluster:
                current_cluster = cluster
                local_clusters.append(cluster)
                local_limits.append(start + pos)
            indices[start + pos] = id
            id_position_in_cluster.append(from_id_to_pos[id])

        clusters.extend(local_clusters)
        limits.extend(local_limits)
        new_cluster_limit = len(local_clusters) + cluster_limits[-1]
        cluster_limits.append( new_cluster_limit)
    limits.append(len(indices))

    clusters = np.array(clusters, dtype=np.int16)
    limits = np.array(limits, dtype=np.int32)
    cluster_limits = np.array(cluster_limits, dtype=np.int32)
    id_position_in_cluster = np.array(id_position_in_cluster, dtype=np.int32)

    return indices, limits, clusters, cluster_limits, id_position_in_cluster


def prepare_filter_by_cluster_exp(docs_per_word, index):
    print('creating filter cluster expanded')
    inverted_lists = find_invlists(index)
    from_id_to_map = dict()
    from_id_to_pos = dict()

    nprobes = inverted_lists.nlist
    for i in range(inverted_lists.nlist):
        list_ids, _ = get_invlist(inverted_lists, i)
        for pos, id in enumerate(list_ids):
            #print('list: ', i, "id: ", id, "pos: ",pos)
            from_id_to_map[id] = i
            from_id_to_pos[id] = pos
    print('loaded the mapping with {} entries'.format(len(from_id_to_map)))

    ## reorganize the docs per word
    #

    limits = -np.ones( (docs_per_word.shape[0] * nprobes + 1,), dtype=np.int32)
    id_position_in_cluster = list()

    indices = np.array(docs_per_word.indices)
    indptr = docs_per_word.indptr
    for word in range(docs_per_word.shape[0]):
        start = indptr[word]
        end = indptr[word + 1]
        if word % 10000 == 0:
            print('processed {} words'.format(word))
        array_ind_cluster = [(id, from_id_to_map[id]) for id in indices[start:end]]
        array_ind_cluster.sort(key=lambda x: x[1])



        local_limits = []
        current_cluster = -1

        for pos, arr in enumerate(array_ind_cluster):
            id, cluster = arr
            if current_cluster == -1 or cluster != current_cluster:

                if current_cluster != -1:
                    limits[word * nprobes + current_cluster + 1] = start + pos


                current_cluster = cluster
                local_limits.append(start + pos)

                limits[word * nprobes + current_cluster] = start + pos

            indices[start + pos] = id
            id_position_in_cluster.append(from_id_to_pos[id])

        limits[word * nprobes + current_cluster + 1] = start + len(array_ind_cluster)


    limits = np.array(limits, dtype=np.int32)

    id_position_in_cluster = np.array(id_position_in_cluster, dtype=np.int32)

    return indices, limits, id_position_in_cluster, nprobes


class FAISS(BaseFilterANN):

    def __init__(self,  metric, index_params):
        self._index_params = index_params
        self._metric = metric

        self.train_size = index_params.get('train_size', None)
        self.indexkey = index_params.get("indexkey", "IVF32768,SQ8")
        self.metadata_threshold = 1e-3
        self.nt = index_params.get("threads", 1)
        self.type = index_params.get("type", "intersect")

        self.clustet_dist = []


    def fit(self, dataset):
        faiss.omp_set_num_threads(self.nt)
        ds = DATASETS[dataset]()

        print('the size of the index', ds.d)
        index = faiss.index_factory(ds.d, self.indexkey)
        xb = ds.get_dataset()

        print("train")
        print('train_size', self.train_size)
        if self.train_size is not None:
            x_train = xb[:self.train_size]
        else:
            x_train = xb
        index.train(x_train)
        print("populate")

        bs = 1024
        for i0 in range(0, ds.nb, bs):
            index.add(xb[i0: i0 + bs])


        print('ids added')
        self.index = index
        self.nb = ds.nb
        self.xb = xb
        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.index)
        print("store", self.index_name(dataset))
        faiss.write_index(index, self.index_name(dataset))

        if ds.search_type() == "knn_filtered":
            words_per_doc = ds.get_dataset_metadata()
            words_per_doc.sort_indices()
            self.docs_per_word = words_per_doc.T.tocsr()
            self.docs_per_word.sort_indices()
            self.ndoc_per_word = self.docs_per_word.indptr[1:] - self.docs_per_word.indptr[:-1]
            self.freq_per_word = self.ndoc_per_word / self.nb
            del words_per_doc

            if self.type == 'exp':
                self.indices, self.limits, self.id_position_in_cluster, self.total_clusters = prepare_filter_by_cluster_exp(
                    self.docs_per_word, self.index)
                pickle.dump(
                    (self.indices, self.limits, self.id_position_in_cluster, self.total_clusters ),
                    open(self.cluster_sig_name(dataset), "wb"), -1)
                #spot_check_filter_exp(self.docs_per_word, self.index, self.indices, self.limits)
            else:
                self.indices, self.limits, self.clusters, self.cluster_limits, self.id_position_in_cluster = prepare_filter_by_cluster(self.docs_per_word, self.index)
                print('dumping cluster map')
                pickle.dump((self.indices, self.limits, self.clusters, self.cluster_limits, self.id_position_in_cluster), open(self.cluster_sig_name(dataset), "wb"), -1)
                #spot_check_filter(self.docs_per_word, self.index, self.indices, self.limits, self.clusters,
                 #                 self.cluster_limits)

            self.max_range = find_max_interval(self.limits)
            print('the max range is {}'.format(self.max_range))
    
    def index_name(self, name):

        if self.type == 'exp':
            return f"data/{name}.{self.indexkey}_exp_wm.faissindex"
        else:
            return f"data/{name}.{self.indexkey}_wm.faissindex"


    def cluster_sig_name(self, name):
        if self.type == 'exp':
            return f"data/{name}.{self.indexkey}_exp_cluster_wm.pickle"
        return f"data/{name}.{self.indexkey}_cluster_wm.pickle"


    def get_probes(self, freq, a, b, min_prob = 4, max_prob=256):
        #print("b: ", b)
        probes = int( pow(2, - a * log10(freq )+ b))
        probes = max(min_prob, probes)
        probes = min(max_prob, probes)
        return probes

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """
        if not os.path.exists(self.index_name(dataset)):
            if 'url' not in self._index_params:
                return False

            print('Downloading index in background. This can take a while.')
            download_accelerated(self._index_params['url'], self.index_name(dataset), quiet=True)

        print("Loading index")
        ds = DATASETS[dataset]()
        self.nb = ds.nb
        self.xb = ds.get_dataset()

        if ds.search_type() == "knn_filtered":
            words_per_doc = ds.get_dataset_metadata()
            words_per_doc.sort_indices()
            self.docs_per_word = words_per_doc.T.tocsr()
            self.docs_per_word.sort_indices()
            self.ndoc_per_word = self.docs_per_word.indptr[1:] - self.docs_per_word.indptr[:-1]
            self.freq_per_word = self.ndoc_per_word / self.nb
            del words_per_doc

        self.index = faiss.read_index(self.index_name(dataset))

        if ds.search_type() == "knn_filtered":
            if  os.path.isfile( self.cluster_sig_name(dataset)):
                print('loading cluster file')
                if self.type == 'exp':
                    self.indices, self.limits, self.id_position_in_cluster, self.total_clusters  = pickle.load(
                        open(self.cluster_sig_name(dataset), "rb"))
                    #spot_check_filter_exp(self.docs_per_word, self.index, self.indices, self.limits)

                else:
                    self.indices, self.limits, self.clusters, self.cluster_limits, self.id_position_in_cluster = pickle.load(open(self.cluster_sig_name(dataset), "rb"))
            else:
                print('cluster file not found')
                if self.type == 'exp':
                    self.indices, self.limits,  self.id_position_in_cluster, self.total_clusters  = prepare_filter_by_cluster_exp(
                        self.docs_per_word, self.index)
                    pickle.dump(
                        (self.indices, self.limits, self.id_position_in_cluster, self.total_clusters ),
                        open(self.cluster_sig_name(dataset), "wb"), -1)
                    #spot_check_filter_exp(self.docs_per_word, self.index, self.indices, self.limits)

                else:
                    self.indices, self.limits, self.clusters, self.cluster_limits, self.id_position_in_cluster = prepare_filter_by_cluster(self.docs_per_word, self.index)
                    pickle.dump((self.indices, self.limits, self.clusters, self.cluster_limits, self.id_position_in_cluster), open(self.cluster_sig_name(dataset), "wb"), -1)

                    #spot_check_filter(self.docs_per_word, self.index, self.indices, self.limits, self.clusters, self.cluster_limits)

            self.max_range = find_max_interval(self.limits)
            print('the max range is {}'.format(self.max_range))

        self.ps = faiss.ParameterSpace()
        self.ps.initialize(self.index)


        # delete not necessary data
        del self.xb
        del ds
        if self.type == "exp" or self.type == 'direct':
            print(" deleting indices")
            del self.indices
        #del self.docs_per_word
        return True

    def index_files_to_store(self, dataset):
        """
        Specify a triplet with the local directory path of index files,
        the common prefix name of index component(s) and a list of
        index components that need to be uploaded to (after build)
        or downloaded from (for search) cloud storage.

        For local directory path under docker environment, please use
        a directory under
        data/indices/track(T1 or T2)/algo.__str__()/DATASETS[dataset]().short_name()
        """
        raise NotImplementedError()
    
    def query(self, X, k):
        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int32')        
        bs = 1024

        try:
            print('k_factor', self.index.k_factor)
            self.index.k_factor = self.k_factor
        except Exception as e:
            print(e)
            pass
        for i0 in range(0, nq, bs):
            _, self.I[i0:i0+bs] = self.index.search(X[i0:i0+bs], k)



    def filtered_query(self, X, filter, k):

        # try:
        #     self.index.k_factor = self.k_factor
        # except Exception as e:
        #     pass

        nq = X.shape[0]
        self.I = -np.ones((nq, k), dtype='int32')

        meta_q = filter
        selector_by_thread = dict()

        def process_one_row(q):
            faiss.omp_set_num_threads(1)
            thread = current_thread()

            qwords = csr_get_row_indices(meta_q, q)
            w1 = qwords[0]
            if qwords.size == 2:
                w2 = qwords[1]
            else:
                w2 = -1

            if thread not in selector_by_thread:

                sel = make_id_selector_cluster_aware_direct(self.id_position_in_cluster, self.limits, self.clusters,
                                                            self.cluster_limits, self.max_range)
                # # IVF first, filtered search
                # if self.type == 'simple':
                #     sel = make_id_selector_ivf_two(self.docs_per_word)
                # elif self.type == "aware":
                #     sel = make_id_selector_cluster_aware(self.indices, self.limits, self.clusters, self.cluster_limits)
                # elif self.type == 'intersect':
                #     sel = make_id_selector_cluster_aware_intersect(self.indices, self.limits, self.clusters, self.cluster_limits, self.max_range)
                # elif self.type == 'direct':
                #     sel = make_id_selector_cluster_aware_direct(self.id_position_in_cluster, self.limits, self.clusters,
                #                                                    self.cluster_limits, self.max_range)
                # elif self.type == 'exp':
                #     sel = make_id_selector_cluster_aware_direct_exp(self.id_position_in_cluster, self.limits, self.total_clusters, self.max_range)
                # else:
                #     raise Exception('unknown type ', self.type)
                selector_by_thread[thread] = sel
            else:
                sel = selector_by_thread.get(thread)

            sel.set_words(int(w1), int(w2))

            params = faiss.SearchParametersIVF(sel=sel, nprobe=self.nprobe, max_codes=self.max_codes, selector_probe_limit=self.selector_probe_limit)
            _, Ii = self.index.search( X[q:q+1], k, params=params)
            Ii = Ii.ravel()
            self.I[q] = Ii

        if self.nt <= 1:
            for q in range(nq):
                process_one_row(q)
        else:
            faiss.omp_set_num_threads(self.nt)

            pool = ThreadPool(self.nt)
            list(pool.map(process_one_row, range(nq)))

    def get_results(self):
        return self.I

    def set_query_arguments(self, query_args):
        #faiss.cvar.indexIVF_stats.reset()
        #faiss.cvar.IDSelectorMy_Stats.reset()
        if "nprobe" in query_args:
            self.nprobe = query_args['nprobe']
            self.ps.set_index_parameters(self.index, f"nprobe={query_args['nprobe']}")
            self.qas = query_args
        else:
            self.nprobe = 1
        if "max_codes" in query_args:
            self.max_codes = query_args["max_codes"]
            self.ps.set_index_parameters(self.index, f"max_codes={query_args['max_codes']}")
            self.qas = query_args
        else:
            self.max_codes = -1
        if "selector_probe_limit" in query_args:
            self.selector_probe_limit = query_args['selector_probe_limit']
            self.ps.set_index_parameters(self.index, f"selector_probe_limit={query_args['selector_probe_limit']}")
            self.qas = query_args
        else:
            self.selector_probe_limit = 0

        if "k_factor" in query_args:
            self.k_factor = query_args['k_factor']
            self.qas = query_args



    def __str__(self):
        return f'Faiss({self.indexkey,self.type, self.qas})'

   