from threading import Thread,Lock
from typing import Optional
from PyCANDYAlgo.utils import *
from neurips23.streaming.faiss_HNSW.faiss_HNSW import faiss_HNSW
from neurips23.congestion.congestion_utils import *
import numpy as np

class AbstractThread:
    """
    The base class and abstraction of a thread.
    """
    def __init__(self):
        self.thread: Optional[Thread] = None

    def inline_main(self):
        pass

    def start_thread(self):
        self.thread = Thread(target=self.inline_main)
        self.thread.start()

    def join_thread(self):
        if self.thread:
            self.thread.join()


class ParallelIndexWorker(AbstractThread):

    """
    The parallel index worker processes one row at a time for insert, query, and delete
    """
    def __init__(self):
        super().__init__()

        self.insert_queue = NumpyIdxQueue(10)
        self.initial_load_queue = NumpyIdxQueue(10)
        self.delete_queue = IdxQueue(10)
        self.query_queue = NumpyIdxQueue(10)
        self.cmd_queue = IdxQueue(10)

        self.my_id = 0
        self.vec_dim = 0
        self.congestion_drop = True
        self.ingested_vectors = 0
        self.single_worker_opt = True
        self.m_mut = Lock()
        self.my_index_algo = None


    def setup(self, dtype, max_pts, ndim):
        self.vec_dim=ndim
        my_index_algo = faiss_HNSW("",None)
        my_index_algo.setup(dtype, max_pts, ndim)
        self.my_index_algo=my_index_algo

    def inline_main(self):
        print(f"Worker {self.my_id}: Starting main thread logic.")
        shouldLoop = True
        querySeq = 0
        bind_to_core(self.my_id)

        while(shouldLoop):
            # 1. initial load stage
            while not self.m_mut.acquire(blocking=False):
                pass

            initial_vectors = []
            initial_ids = []
            while(not self.initial_load_queue.empty()):
                pair = self.initial_load_queue.front()
                self.initial_load_queue.pop()
                initial_vectors.append(pair.vectors)
                initial_ids.append(pair.idx)
            initial_vectors = np.vstack(initial_vectors)
            initial_ids = np.vstack(initial_ids)
            self.my_index_algo.insert(initial_vectors, initial_ids)

            self.m_mut.release()

            # 2. insert phase
            while not self.m_mut.acquire(blocking=False):
                pass

            while(not self.insert_queue.empty()):
                pair = self.insert_queue.front()
                self.insert_queue.pop()
                self.my_index_algo.insert(pair.vectors, [pair.idx])

                self.ingested_vectors += 1

            self.m_mut.release()

            # 3. delete phase
            while not self.m_mut.acquire(blocking=False):
                pass

            while(not self.delete_queue.empty()):
                idx = self.delete_queue.front()
                self.delete_queue.pop()
                self.my_index_algo.delete([idx])

            self.m_mut.release()

            # 4. terminate
            while(not self.cmd_queue.empty()):
                cmd = self.cmd_queue.front()
                self.cmd_queue.pop()
                if(cmd==-1):
                    shouldLoop=False
                    print(f"parallel worker {self.my_id} terminates")
                    return







    def startHPC(self):
        self.start_thread()
        return True
    def endHPC(self):
        self.cmd_queue.push(-1)
        return False

    def set_id(self,id):
        self.my_id = id
        return

    def waitPendingOperations(self):
        while not self.m_mut.acquire(blocking=False):
            pass
        self.m_mut.release()
        return True

    def initial_load(self,X,ids):
        """
        here index should be loaded several rows at a time before streaming
        """
        if(self.single_worker_opt):
            print("Optimized for single worker!")
            while not self.m_mut.acquire(blocking=False):
                pass
            self.my_index_algo.insert(X,ids)
            self.m_mut.release()
            return
        else:
            for x, id in zip(X,ids):
                self.initial_load_queue.push(NumpyIdxPair(x,id))
            return


    def insert(self,X,id):
        # here is inserted one row by one row
        # X is one row and id is only 1
        if(self.insert_queue.empty() or (not self.congestion_drop)):
            self.insert_queue.push(NumpyIdxPair(X,id))
        else:
            print("DROPPING DATA!")

        return

    def delete(self, id):
        self.delete_queue.push(id)
        return

    def query(self, X, k):
        self.my_index_algo.query(X,k)
        self.res = self.my_index_algo.res
        return

