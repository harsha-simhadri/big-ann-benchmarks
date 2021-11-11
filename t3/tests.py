import numpy as np
import sys
from benchmark.plotting.metrics import get_recall_values

ASSERT= True # Stop unit tests on first failure

if __name__ == "__main__":

    #
    # Unit tests to test recall computation
    #

    def test_recall( true_ids, true_dists, run_ids, count, expected_no_ties, expected_with_ties ):
        '''This function will test the two forms of recall (with and without considering ties.)'''

        # compute recall, don't consider ties
        recall = get_recall_values( (true_ids, true_dists), run_ids, count, False)
        print("test: compute recall don't consider ties=",recall[0], "expected=", expected_no_ties)
        if ASSERT:
            assert recall[0]==expected_no_ties
            print("test passed\n")
       
        #  compute recall, consider tieds
        recall = get_recall_values( (true_ids, true_dists), run_ids, count, True)
        print("test: compute recall consider ties=",recall[0], "expected=", expected_with_ties)
        if ASSERT:
            assert recall[0]==expected_with_ties
            print("test passed\n")

    # create a fake query response with no distance ties, 1 query and k=3
    true_ids    = np.array([ [ 0,   1,   2 ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2 ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    # create a fake query response with no ties, 2 queries and k=3
    true_ids    = np.array([ [ 0,   1,   2   ], [ 2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ], [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2   ], [ 2,   1,   0   ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )
   
    # create a fake query response with no distance ties, 1 query, k=3, GT array is larger than run array
    true_ids    = np.array([ [ 0,   1,   2,   3   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 3.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2        ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    # create a fake query response with an out-of-bounds distance ties, 1 query, k=3, GT array is larger than run array
    true_ids    = np.array([ [ 0,   1,   2,   3   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2        ] ])
    count=3
    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    # this is from bigann GT and query set.  The GT arrays are  size=11 but run array is 10 and there are no ties.
    true_ids    = np.array([ [937541801, 221456167, 336118969, 971823307, 267986685, 544978851, 815975675, 615142927, 640142873, 994367459,  504814] ] )
    true_dists  = np.array([ [55214.,    58224.,    58379.,    58806.,    59251.,    59256.,    60302.,    60573.,    60843.,    60950.,     61125.] ] )
    run_ids     = np.array([ [221456167, 336118969, 971823307, 640142873, 994367459, 504814,    87356234,  628179290, 928121617, 397551598         ] ] )
    count=10
    test_recall( true_ids, true_dists, run_ids, count, 0.5, 0.5 )

    sys.exit(0)

