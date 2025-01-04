import numpy as np
from neurips23.congestion.base import *
def test_congestion_drop_worker():
    # Test parameters
    initial_size = 1000
    insert_size = 3000
    ndims = 16
    max_pts = 5000

    # Generate sample data
    total_size = initial_size + insert_size
    X = np.random.rand(total_size, ndims).astype(np.float32)
    ids = np.arange(total_size)

    # Split data for initial load and insertion
    X_initial = X[:initial_size]
    ids_initial = ids[:initial_size]
    X_insert = X[initial_size:]
    ids_insert = ids[initial_size:]

    # Create and configure a CongestionDropWorker instance
    worker = CongestionDropWorker()
    worker.setup(dtype="float32", max_pts=max_pts, ndim=ndims)
    worker.set_id(1)

    # Perform initial load
    print("Testing initial load operation...")
    worker.initial_load(X_initial, ids_initial)
    print("Initial load completed.")

    # Test insert operation
    print("Testing insert operation...")
    worker.insert(X_insert, ids_insert)
    assert not worker.insert_queue.empty(), "Insert queue should not be empty after inserts."

    # Test delete operation
    print("Testing delete operation...")
    for i in range(10):
        worker.delete(ids_initial[i])
    assert not worker.delete_queue.empty(), "Delete queue should not be empty after delete."

    # Start the thread and process operations
    print("Starting worker thread...")
    worker.startHPC()

    # Wait for a short while to ensure worker processes operations
    import time
    time.sleep(2)

    # Wait for pending operations to complete
    worker.waitPendingOperations()

    # Verify insert operation processed
    print("Verifying insert operation processed...")
    assert worker.ingested_vectors == insert_size, f"Expected {insert_size} ingested vectors, got {worker.ingested_vectors}."

    # Terminate the worker
    print("Terminating worker...")
    worker.endHPC()
    worker.join_thread()

    print("Test passed.")

# Run the test
test_congestion_drop_worker()
