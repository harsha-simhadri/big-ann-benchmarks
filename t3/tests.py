
from benchmark.plotting.metrics import compute_recall_with_distance_ties, compute_recall_without_distance_ties, get_recall_values

# unit tests
if __name__ == "__main__":

    print("compute recall unit tests...")

    # Recall without ties 
    true_ids   = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids   =  [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    count = 10
    recall = get_recall_values( (true_ids, true_dists), run_ids, count, False)
    print("compute without ties, recall=",recall)
    assert recall==10
    
    # Recall without ties - note that 'count' does not seem to be 
    # used in the implementation so we truncate using count.
    # In this test, we have 1 invalid neighbor within k=10
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8,  9,   10, 11, 12 ]
    true_dists = [ 0, 1, 2, 3, 4, 5, 6, 7, 8,  9,   10, 11, 12 ]
    run_ids =    [ 0, 1, 2, 3, 4, 5, 6, 7, 10, 8,    9, 12, 11 ]
    count = 10
    recall = compute_recall_without_distance_ties(true_ids[:count], run_ids[:count], count)
    print("compute without ties, recall=",recall)
    assert recall==9
    
    # Recall with ties - using monitonically increasing distance,
    # we expect the same recall as without ties
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids =    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    recall = compute_recall_with_distance_ties(true_ids, true_dists, run_ids, count)
    print("compute with ties, recall=",recall)
    assert recall==10
    
    # Recall with ties - with 1 distance tie within k=10
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 2, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids =    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    recall = compute_recall_with_distance_ties(true_ids, true_dists, run_ids, count)
    print("compute with ties, recall=",recall)
    assert recall==10
    
    # Recall with ties - with 1 distance tie but 2 indices reversed at the tie within k=10
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 2, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids =    [ 0, 2, 1, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    recall = compute_recall_with_distance_ties(true_ids, true_dists, run_ids, count)
    print("compute with ties, recall=",recall)
    assert recall==10
    
    # Recall with ties - with 1 distance tie but 3 indices mismatched at the tie within k=10
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 2, 2, 2, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids =    [ 0, 3, 2, 1, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    recall = compute_recall_with_distance_ties(true_ids, true_dists, run_ids, count)
    print("compute with ties, recall=",recall)
    assert recall==10
    
    # Recall with ties - with 1 distance tie but 3 indices mismatched at the tie
    # with 1 pair switch outside of k=10
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 2, 2, 2, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids =    [ 0, 3, 2, 1, 4, 5, 6, 7, 8, 9,    10, 12, 11 ]
    recall = compute_recall_with_distance_ties(true_ids, true_dists, run_ids, count)
    print("compute with ties, recall=",recall)
    assert recall==10
    
    # Recall with ties - with 1 distance tie but 3 indices mismatched at the tie
    # with 1 pair switch at the boundary of k=10
    true_ids =   [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    true_dists = [ 0, 2, 2, 2, 4, 5, 6, 7, 8, 9,    10, 11, 12 ]
    run_ids =    [ 0, 3, 2, 1, 4, 5, 6, 7, 12,9,    10, 11, 8 ]
    recall = compute_recall_with_distance_ties(true_ids, true_dists, run_ids, count)
    print("compute with ties, recall=",recall)
    assert recall==9
