from neurips23.filter.base import BaseFilterANN
from benchmark.datasets import DATASETS
from benchmark.dataset_io import download_accelerated
import subprocess
import os
import pathlib
import numpy as np

class rubignn(BaseFilterANN):
    def __init__(self, metric, index_params):
        self._index_params=index_params
        self._metric = metric
        self.method_name="rubignn"
        print(index_params)
    
    def load_bin_result(self,path,k):
        results = np.fromfile(path,dtype=np.uint32)
        results = results[2:]
        results = results.reshape((-1,k))
        return results
    
    def get_results(self):
        return self.load_bin_result(self.result_path,self.k)

    def filtered_query(self, X, filter, k):
        """
        This is intergrated for CI test, it has overhead to load the index every search time.
        So please use our custom setup for the real test for yfcc-10M
        """
        self.k=k
        print("We have custom setup")
        print(X.shape,k)
        qs_file_name=str(os.path.join(self.ds.basedir, self.ds.qs_fn))
        print(qs_file_name)
        qs_metadata_name = str(os.path.join(self.ds.basedir, self.ds.qs_metadata_fn))
        print(qs_metadata_name)
        result_path_prefix=str(os.path.join("/home/app/results/neurips23/filter",self.dataset,str(k),self.method_name))
        print(result_path_prefix)
        cmd = ['./ru-bignn-23/build/apps/search_contest','--data_type',self.data_dtype,'--index_path_prefix',self.index_path,'--query_file',qs_file_name,'--query_filters_file',qs_metadata_name,'-L',str(self.L_search),"--runs","1","--dataset",self.dataset,"--result_path_prefix",result_path_prefix+"/rubignn"]
        subprocess.run(cmd)
        self.result_path=result_path_prefix+"/rubignn_L"+str(self.L_search)+"_idx_uint32.bin"




    def get_index_prefix(self):
        res = ""
        for i,j in enumerate(self._index_params):
            res=res+str(j)+str(self._index_params[j])+"-"
        res=res+"stiched_index"
        return res

    def fit(self, dataset):
        ds = DATASETS[dataset]()
        print("params:",self._index_params)
        data_path = ds.get_dataset_fn()
        metadata_path = '/home/app/'+ str(os.path.join(ds.basedir, ds.ds_metadata_fn))
        index_file_prefix='/home/app/data/index_file/'
        pathlib.Path(index_file_prefix).mkdir(parents=True, exist_ok=True) 
        label_file_path = index_file_prefix+'label_file_base_'+dataset+'_filter.txt'
        subprocess.run(['./ru-bignn-23/build/apps/base_label_to_label_file',metadata_path,label_file_path])
        index_prefix = index_file_prefix+dataset+"-"+self.get_index_prefix()
        print(index_prefix)
        self.data_dtype='uint8'
        self.ds=ds
        self.dataset=dataset
        if(ds.dtype=="float32"):
            self.data_dtype='float'

        cmd = ['./ru-bignn-23/build/apps/build_stitched_index','--data_type',self.data_dtype,'--data_path','/home/app/'+data_path,'--index_path_prefix',index_prefix,'-R',str(self._index_params['R']),'-L',str(self._index_params['L']),'--stitched_R',str(self._index_params['stitched_R']),'--alpha','1.2','--label_file',label_file_path,'--universal_label','0']
        print(' '.join(cmd))
        subprocess.run(cmd)
        self.index_path=index_prefix
        print("index_path:",self.index_path)
        if os.path.isfile(self.index_path):
            print('Build Index Success!')
        else:
            print("fail,",self.index_path)
            assert(False)


    def set_query_arguments(self, query_args):
        # faiss.cvar.indexIVF_stats.reset()
        # if "nprobe" in query_args:
        #     self.nprobe = query_args['nprobe']
        #     self.ps.set_index_parameters(self.index, f"nprobe={query_args['nprobe']}")
        #     self.qas = query_args
        # else:
        #     self.nprobe = 1
        # if "mt_threshold" in query_args:
        #     self.metadata_threshold = query_args['mt_threshold']
        # else:
        #     self.metadata_threshold = 1e-3

        # TODO: fix
        print("setting query args: ",query_args)
        if "L" in query_args:
            self.L_search = query_args["L"]
        else:
             sefl.L_search=100
        self.qas=query_args

    def load_index(self, dataset):
        """
        Load the index for dataset. Returns False if index
        is not available, True otherwise.

        Checking the index usually involves the dataset name
        and the index build paramters passed during construction.
        """

        return False        
    
    def __str__(self):
        return f'rubignn({self._index_params, self.qas})'

