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
        expected = 1.0  
        print("test: compute recall don't consider ties=",recall[0], "expected=", expected_no_ties)
        if ASSERT:
            assert recall[0]==expected_no_ties
            print("passed\n")
       
        #  compute recall, consider tieds
        recall = get_recall_values( (true_ids, true_dists), run_ids, count, True)
        expected = 1.0
        print("test: compute recall consider ties=",recall[0], "expected=", expected_with_ties)
        if ASSERT:
            assert recall[0]==expected_with_ties
            print("passed\n")

    # create a query response with no ties, 1 query
    true_ids    = np.array([ [ 0,   1,   2 ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2 ] ])
    count=3

    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )

    # create a query response with no ties, 2 queries
    true_ids    = np.array([ [ 0,   1,   2   ], [ 2,   1,   0   ] ])
    true_dists  = np.array([ [ 0.0, 1.0, 2.0 ], [ 0.0, 1.0, 2.0 ] ])
    run_ids     = np.array([ [ 0,   1,   2   ], [ 2,   1,   0   ] ])
    count=3

    test_recall( true_ids, true_dists, run_ids, count, 1.0, 1.0 )


    sys.exit(0)

