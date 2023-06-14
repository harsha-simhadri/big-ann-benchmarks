import numpy as np
import numpy.typing as npt
from benchmark.algorithms.base import BaseANN

class BaseStreamingANN(BaseANN):
    def track(self):
        return "stream"
    
    def setup(self, dtype, max_pts, ndims) -> None:
        '''
        Initialize the data structures for your algorithm
        dtype can be 'uint8', 'int8 'or 'float32'
        max_pts is an upper bound on non-deleted points that the index must support
        ndims is the size of the dataset
        '''
        raise NotImplementedError
        
    def insert(self, X: np.array, ids: npt.NDArray[np.uint32]) -> None:
        '''
        Implement this for your algorithm
        X is num_vectos * num_dims matrix 
        ids is num_vectors-sized array which indicates ids for each vector
        '''
        raise NotImplementedError
    
    def delete(self, ids: npt.NDArray[np.uint32]) -> None:
        '''
        Implement this for your algorithm
        delete the vectors labelled with ids.
        '''
        raise NotImplementedError


    def fit(self, dataset):
        '''
        Do not override this method
        '''
        raise NotImplementedError
    
    def load_index(self, dataset):
        """
        Do not override
        """
        return False
    
    def get_index_components(self, dataset):
        """
        Does not apply to streaming indices
        """
        raise NotImplementedError

    def index_files_to_store(self, dataset):
        """
        Does not apply to streaming indices
        """
        raise NotImplementedError
    