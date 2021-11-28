import numpy as np
import sys

from benchmark.plotting.metrics import get_recall_values
from benchmark.datasets import DATASETS

ASSERT= True # Stop unit tests on first failure

GT_MIN_SIZE = 20 # Require ground truth with at least this length for each query

def main_tests():
    #
    # test recall computation on fake responses
    #

    def test_recall( true_ids, true_dists, run_ids, count, expected_no_ties, expected_with_ties ):
        '''This function will test the two forms of recall (with and without considering ties.)'''

        # compute recall, don't consider ties
        recall = get_recall_values( (true_ids, true_dists), run_ids, count, False)
        expected = 1.0  
        print("compute recall(don't consider ties)=%f" % recall[0], "expected recall=%f" % expected_no_ties)
        if ASSERT:
            assert recall[0]==expected_no_ties
            print("passed")
       
        #  compute recall, consider ties
        recall = get_recall_values( (true_ids, true_dists), run_ids, count, True)
        expected = 1.0
        print("compute recall(consider ties)=%f num_queries_with_ties=%d" % (recall[0], recall[3]), "expected recall=%f" % expected_with_ties)
        if ASSERT:
            assert recall[0]==expected_with_ties
            print("passed")

        print()

    print("TEST: fake query response with no distance ties, 1 query and k=3")
    true_ids    = np.array([ [ 0,   1,   2 ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2 ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )
    
    print("TEST: fake query response with no distance ties but not 1.0 recall, 1 query and k=3")
    true_ids    = np.array([ [ 0,   1,   2 ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   3 ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 2.0/3.0, 2.0/3.0 )

    print("TEST: fake query response with no ties, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2   ], [ 2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ], [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2   ], [ 2,   1,   0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )
   
    print("TEST: fake query response with no distance ties, 1 query, k=3, GT array is larger than run array")
    true_ids    = np.array([ [ 0,   1,   2,   3   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 3.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2        ] ])
    count=3
    print("yuk true_ids=", true_ids.shape, "run_ids=", run_ids.shape)
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    print("TEST: fake query response with an out-of-bounds distance ties, 1 query, k=3, GT array is larger than run array.")
    true_ids    = np.array([ [ 0,   1,   2,   3   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2        ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    # this is from bigann GT and query set.  The GT arrays are  size=11 but run array is 10 and there are no ties to consider
    print("TEST: from bigann-1B...")
    true_ids    = np.array([ [937541801, 221456167, 336118969, 971823307, 267986685, 544978851, 815975675, 615142927, 640142873, 994367459,  504814] ] )
    true_dists  = np.array([ [55214.,    58224.,    58379.,    58806.,    59251.,    59256.,    60302.,    60573.,    60843.,    60950.,     61125.] ] )
    run_ids     = np.array([ [221456167, 336118969, 971823307, 640142873, 994367459, 504814,    87356234,  628179290, 928121617, 397551598         ] ] )
    count=10
    test_recall( true_ids, true_dists, run_ids, count, 0.5, 0.5 )
    
    print("TEST: fake query response with ties at beginning, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2,   3   ], [ 3,   2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 0.0, 1.0, 2.0 ], [ 0.0, 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,        3   ], [ 3,   2,        0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0,2.0])/count, np.mean([2.0,2.0])/count)
    
    print("TEST: fake query response with ties at beginning and ties have small diff, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,             2,   3   ], [ 3,   2,             1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 0.0+1e-6-1e-7, 1.0, 2.0 ], [ 0.0, 0.0+1e-6-1e-7, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,                  3   ], [ 3,   2,                  0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0,2.0])/count, np.mean([2.0,2.0])/count)
    
    print("TEST: fake query response with possible ties at beginning but diff is just beyond the 1e-6 threshold, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,        2,   3   ], [ 3,   2,        1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 0.0+1e-6, 1.0, 2.0 ], [ 0.0, 0.0+1e-6, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,             3   ], [ 3,   2,             0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0,2.0])/count, np.mean([2.0,2.0])/count )
    
    print("TEST: fake query response with ties in middle, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2,   3   ], [ 3,   2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 1.0, 2.0 ], [ 0.0, 1.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,        3   ], [ 3,   2,        0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0,2.0])/count, np.mean([2.0,2.0])/count)
    
    print("TEST: fake query response with ties at count-1 and 1 tie after, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2,   3   ], [ 3,   2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 2.0 ], [ 0.0, 1.0, 2.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,        3   ], [ 3,   2,        0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0, 2.0])/float(count), np.mean([3.0, 3.0])/float(count) )
    
    print("TEST: fake query response with ties at count-1 and 1 tie after and 1 after that that is cloe, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2,   3   ], [ 3,   2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 2.0 ], [ 0.0, 1.0, 2.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,        3   ], [ 3,   2,        0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0, 2.0])/float(count), np.mean([3.0, 3.0])/float(count) )
    
    print("TEST: fake query response with ties at count-1 and several close ties after, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2,   3,   4,             5        ], [ 5,   4,   3,   2,   1,             0            ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 2.0, 2.0+1e-6-1e-7, 2.0+1e-6 ], [ 0.0, 1.0, 2.0, 2.0, 2.0+1e-6-1e-7, 2.0+1e-6     ] ])
    run_ids     = np.array([ [ 0,   1,             4                       ], [ 5,   4,                            0            ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0,2.0])/count, np.mean([3.0, 2.0])/float(count) )
    
    print("TEST: fake query response with two independent tie groups, 2 queries and k=3")
    true_ids    = np.array([ [ 0,   1,   2,   3,   4,   5   ], [ 5,   4,   3,   2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 0.0, 2.0, 3.0, 3.0, 4.0 ], [ 0.0, 0.0, 2.0, 3.0, 3.0, 4.0 ] ])
    run_ids     = np.array([ [ 0,   1,                  5   ], [ 5,   4,             1        ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0, 2.0])/float(count), np.mean([2.0, 2.0])/float(count) )
    
    print("TEST: fake query response with two independent tie groups, 2 queries and k=4")
    true_ids    = np.array([ [ 0,   1,   2,   3,   4,   5,   6   ], [ 6,   5,   4,   3,   2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 0.0, 2.0, 3.0, 3.0, 4.0, 5.0 ], [ 0.0, 0.0, 2.0, 3.0, 3.0, 4.0, 5.0 ] ])
    run_ids     = np.array([ [ 0,   1,                  5,   7   ], [ 5,   4,             1,        7   ] ])
    count=4
    test_recall( true_ids, true_dists, run_ids, count, np.mean([2.0, 2.0])/float(count), np.mean([2.0, 2.0])/float(count) )

    #
    # dataset tests
    #
    def test_GT_monotonicity( dset, increasing=True ):
        print("TEST: %s, checking GT distances monotonicity" % dset)
        dataset = DATASETS[dset]()
        gt = dataset.get_groundtruth()
        if ASSERT: assert len(gt)==2
        true_ids    = gt[0]
        true_dists  = gt[1]
        if ASSERT:
            assert true_ids.shape[1]==true_dists.shape[1]
            assert true_ids.shape[1]>=GT_MIN_SIZE 
            assert true_dists.shape[1]>=GT_MIN_SIZE
        func = monotone_increasing if increasing else monotone_decreasing 
        for i in range(true_dists.shape[0]):
            mtest = func(true_dists[i])
            if ASSERT: assert mtest==True
        print()
    
    print("TEST: sanity check the monotone functions")
    mtest = monotone_increasing([0,1,2,3,4,5])
    if ASSERT: assert mtest==True
    mtest = monotone_increasing([0,0,0,3,4,5])
    if ASSERT: assert mtest==True
    mtest = monotone_increasing([3,4,5,4,3,4,5])
    if ASSERT: assert mtest==False
    mtest = monotone_increasing([5,4,4,3,2,1])
    if ASSERT: assert mtest==False
    print()

    # check GT dist increasing monotonicity for each knn dataset
    test_GT_monotonicity( "bigann-1B" )
    test_GT_monotonicity( "deep-1B" )
    test_GT_monotonicity( "msturing-1B" )
    test_GT_monotonicity( "msspacev-1B" )
    test_GT_monotonicity( "text2image-1B", increasing=False)

    #
    # test recall on actual datasets
    #
    def extract_GT_monotonicity( dset, row, c1, c2):
        print("TEST: %s, extraction" % dset, row, c1, c2)
        dataset = DATASETS[dset]()
        gt = dataset.get_groundtruth()
        true_dists  = gt[1]
        lst = true_dists[row,c1:c2]
        print(lst)
        mtest = monotone_increasing(lst)
        print(mtest)
        print()

    def test_GT_as_query( dset, count ):
        print("TEST: %s, using GT as query, k=10" % dset)
        dataset = DATASETS[dset]()
        gt = dataset.get_groundtruth()
        if ASSERT: assert len(gt)==2
        true_ids    = gt[0]
        true_dists  = gt[1]
        if ASSERT:
            assert true_ids.shape[1]==true_dists.shape[1]
            assert true_ids.shape[1]>=GT_MIN_SIZE 
            assert true_dists.shape[1]>=GT_MIN_SIZE 
        run_ids = np.copy( gt[0] )[:,0:count] # create a query set from GT truncated at k
        test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    # test GT as query for each dataset
    test_GT_as_query( "bigann-1B", 10 )
    test_GT_as_query( "deep-1B", 10 )
    test_GT_as_query( "text2image-1B", 10 )
    test_GT_as_query( "msturing-1B", 10 )
    test_GT_as_query( "msspacev-1B", 10 )

    sys.exit(0)



#
# useful functions
#
import itertools
import operator

def monotone_increasing(lst):
    pairs = zip(lst, lst[1:])
    bools = list(itertools.starmap(operator.le, pairs))
    #print(type(bools), len(bools), bools)
    return all( bools )

def monotone_decreasing(lst):
    pairs = zip(lst, lst[1:])
    bools = list(itertools.starmap(operator.ge, pairs))
    #print(type(lst), lst)
    return all( bools )

def monotone(lst):
    return monotone_increasing(lst) or monotone_decreasing(lst)

if __name__ == "__main__":
    main_tests()
