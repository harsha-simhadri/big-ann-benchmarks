from threading import Thread,Lock
from typing import Optional,List
from PyCANDYAlgo.utils import *

from benchmark.algorithms.base import BaseANN

from neurips23.congestion.congestion_utils import *
import numpy as np
import time
import random

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


class CongestionDropWorker(AbstractThread):

    """
    The parallel index worker processes one batch at a time for insert, query, and delete
    """
    def __init__(self, my_index_algo):
        super().__init__()

        self.insert_queue = NumpyIdxQueue(10)
        self.initial_load_queue = NumpyIdxQueue(10)
        self.delete_queue = NumpyIdxQueue(10)
        self.query_queue = NumpyIdxQueue(10)
        self.cmd_queue = IdxQueue(10)

        self.my_id = 0
        self.vec_dim = 0
        self.congestion_drop = True
        self.ingested_vectors = 0
        self.single_worker_opt = True
        self.m_mut = Lock()
        self.my_index_algo = my_index_algo

        self.randomContamination = False
        self.randomDrop = False

        self.randomDropProb = 0.0
        self.randomContaminationProb = 0.0

        self.outOfOrder = False





    def setup(self, dtype, max_pts, ndim):
        self.vec_dim=ndim
        self.my_index_algo.setup(dtype, max_pts, ndim)

    def inline_main(self):
        print(f"Worker {self.my_id}: Starting main thread logic.")
        shouldLoop = True
        querySeq = 0
        bind_to_core(self.my_id)

        while(shouldLoop):
            # 1. initial load stage
            while not self.m_mut.acquire(blocking=False):
                pass
            #print("Lock acquire by inline main initial")
            initial_vectors = []
            initial_ids = []
            while(not self.initial_load_queue.empty()):
                pair = self.initial_load_queue.front()
                self.initial_load_queue.pop()
                initial_vectors.append(pair.vectors)
                initial_ids.append(pair.idx)
            if(len(initial_vectors)>0):
                initial_vectors = np.vstack(initial_vectors)
                initial_ids = np.vstack(initial_ids)
                self.my_index_algo.insert(initial_vectors, initial_ids)
            #print("Lock to be released by inline main initial")
            self.m_mut.release()

            # 2. insert phase
            while not self.m_mut.acquire(blocking=False):
                pass
            #print("Lock acquire by inline main insertion & deletion")
            while(not self.insert_queue.empty()):
                pair = self.insert_queue.front()
                self.insert_queue.pop()
                self.my_index_algo.insert(pair.vectors, np.array(pair.idx))

                self.ingested_vectors += pair.vectors.shape[0]
                #print(f"ingested_vectors={self.ingested_vectors}")


            # 3. delete phase
            while(not self.delete_queue.empty()):
                idx = self.delete_queue.front().idx
                self.delete_queue.pop()
                self.my_index_algo.delete(np.array(idx))

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
            while not self.m_mut.acquire(blocking=False):
                pass
            #print("Lock acquire by initial_load")
            self.my_index_algo.insert(X,ids)
            #print("Lock to be released by initial_load")
            self.m_mut.release()
            return


    def insert(self,X,id):
        if(not self.randomDrop):
            if(self.insert_queue.empty() or (not self.congestion_drop)):
                if(not self.randomContamination):
                    self.insert_queue.push(NumpyIdxPair(X,id))
                else:
                    rand = random.random()
                    if(rand<self.randomContaminationProb):
                        rand_X = np.random.random(X.shape)
                        print(f"RANDOM CONTAMINATING DATA {id[0]}:{id[-1]}")
                        # simply replace the current batch with random data
                        self.insert_queue.push(NumpyIdxPair(rand_X, id))
                    else:
                        self.insert_queue.push(NumpyIdxPair(X,id))
            else:
                print(f"DROPPING DATA {id[0]}:{id[-1]}")
                pass
        else:
            rand_drop =random.random()
            if(rand_drop<self.randomDropProb):
                print(f"RANDOM DROPPING DATA {id[0]}:{id[-1]}")
                pass
            if(self.insert_queue.empty() or (not self.congestion_drop)):
                if(not self.randomContamination):
                    self.insert_queue.push(NumpyIdxPair(X,id))
                else:
                    rand = random.random()
                    if(rand<self.randomContaminationProb):
                        print(f"RANDOM CONTAMINATING DATA {id[0]}:{id[-1]}")
                        rand_X = np.random.random(X.shape)
                        # simply replace the current batch with random data
                        self.insert_queue.push(NumpyIdxPair(rand_X, id))
                    else:
                        self.insert_queue.push(NumpyIdxPair(X,id))
            else:
                print(f"DROPPING DATA {id[0]}:{id[-1]}")
                pass

        return

    def delete(self, id):
        if(self.delete_queue.empty() or (not self.congestion_drop)):
            self.delete_queue.push(NumpyIdxPair(np.array([0.0]),id))
        else:
            #TODO: Fix this
            print("Failed to process deletion!")
        return

    def query(self, X, k):
        self.my_index_algo.query(X,k)
        self.res = self.my_index_algo.res
        return

    def enableScenario(self, randomContamination=False, randomContaminationProb=0.0, randomDrop=False,
                       randomDropProb=0.0, outOfOrder=False):
        self.randomDropProb = randomDropProb
        if(randomDropProb):
            print("Enabling random dropping!")
        self.randomDrop = randomDrop

        self.randomContamination = randomContamination
        if(randomContamination):
            print("Enabling random contamination!")
        self.randomContaminationprob = randomContaminationProb

        if(outOfOrder):
            print("Enabling outta order ingestion!")
        self.outOfOrder = outOfOrder

class BaseCongestionDropANN(BaseANN):
    workers: List[CongestionDropWorker]
    workerMap: List[bool]
    def __init__(self, my_index_algos, metric, index_params, parallel_workers=1,fine_grained=False, single_worker_opt=True, clear_pending_operations=True):
        self.parallel_workers = parallel_workers
        self.insert_idx = 0
        self.fine_grained_parallel_insert = fine_grained
        self.single_worker_opt = single_worker_opt
        self.clear_pending_operations = clear_pending_operations
        self.workers=[]
        self.verbose = False



        for i in range(parallel_workers):
            self.workers.append(CongestionDropWorker(my_index_algo=my_index_algos[i]))



    def setup(self, dtype, max_pts, ndims) -> None:
        for i in range(self.parallel_workers):
            worker = self.workers[i]
            worker.setup(dtype, max_pts, ndims)
            worker.my_id=i
        return

    def startHPC(self):
        for i in range(self.parallel_workers):
            self.workers[i].startHPC()
        return

    def endHPC(self):
        for i in range(self.parallel_workers):
            self.workers[i].endHPC()
        for i in range(self.parallel_workers):
            self.workers[i].join_thread()
        return

    def waitPendingOperations(self):
        if(self.clear_pending_operations):
            if self.verbose:
                print("CLEAR CURRENT OPERATION QUEUE!")
            for i in range(self.parallel_workers):
                while(self.workers[i].insert_queue.size()!=0 and self.workers[i].delete_queue.size()!=0):
                    self.workers[i].waitPendingOperations()
            return
        for i in range(self.parallel_workers):
            self.workers[i].waitPendingOperations()

    def initial_load(self,X,ids):
        if self.parallel_workers==1 and self.single_worker_opt==True:
            if self.verbose:
                print("Initial_Load Optimized for single worker!")
            self.workers[0].initial_load(X,ids)
            time.sleep(2)
            self.workers[0].waitPendingOperations()
            return

        self.partition_initial_load(X,ids)
        for i in range(self.parallel_workers):
            self.waitPendingOperations()
        return

    def insert(self, X, ids):
        if(not self.fine_grained_parallel_insert):
            self.insertInline(X,ids)
        else:
            rows = X.shape[0]
            for i in range(rows):
                rowI = X[i]
                idI = ids[i]
                self.insertInline(rowI, [idI])
        return

    def delete(self, ids):
        if(self.parallel_workers==1 and self.single_worker_opt==True):
            if self.verbose:
                print("Delete Optimized for single worker!")
            self.workers[0].delete(ids)
        else:
            mapping = dict()
            for i in range(self.parallel_workers):
                mapping[i] =[]
            for i in ids:
                mapping[self.workerMap[i]].append(i)
                self.workers[i]=-1

            for i in range(self.parallel_workers):
                self.workers[i].delete(mapping[i])

        return

    def query(self, X, k):
        if(self.parallel_workers==1 and self.single_worker_opt==True):
            self.workers[0].query(X, k)
            self.res = self.workers[0].res
            return


    def partition_initial_load(self, X, ids):
        rows = X.shape[0]
        startPos = [0]*self.parallel_workers
        endPos = [0]*self.parallel_workers

        step = (int)(rows/self.parallel_workers)
        startPos[0] = 0
        endPos[self.parallel_workers-1]=rows
        stepAcc = step
        for i in range(1, self.parallel_workers):
            startPos[i] = stepAcc
            stepAcc += step

        stepAcc=step

        for i in range(self.parallel_workers-1):
            endPos[i]=stepAcc
            stepAcc+=step
        for i in range(self.parallel_workers):
            sub = X[startPos[i]:endPos[i]]
            sub_id=ids[startPos[i]:endPos[i]]
            self.workerMap.extend([i]*(endPos[i]-startPos[i]))
            self.workers[i].initial_load(sub,sub_id)


    def insertInline(self,X,ids):
        self.workers[self.insert_idx].insert(X,ids)
        if(self.single_worker_opt==False or self.parallel_workers>1):
            for i in ids:
                self.workerMap[i]=self.insert_idx
        self.insert_idx+=1
        if(self.insert_idx>=self.parallel_workers):
            self.insert_idx=0

    def set_query_arguments(self, query_args):
        self.workers[0].my_index_algo.set_query_arguments(query_args)

    def index_name(self, name):
        return self.workers[0].my_index_algo.index_name(name)

    def replace(self,X,ids):
        self.delete(X,ids)
        self.insert(X,ids)


    def enableScenario(self, randomContamination=False, randomContaminationProb=0.0, randomDrop=False,
                       randomDropProb=0.0, outOfOrder=False):
        for i in range(self.parallel_workers):
            self.workers[i].enableScenario(self, randomContamination, randomContaminationProb, randomDrop, randomDropProb, outOfOrder)



