import numpy as np
import time
import yaml
import pandas as pd
from benchmark.algorithms.base_runner import BaseRunner
from benchmark.datasets import DATASETS
from benchmark.results import get_result_filename

def generateTimestamps(rows, eventRate=4000):
    """
    generates uniformly increasing event timestamps and processing timestamps for each row of the input batch vectors
    :param rows: int -
    :param eventRate: float
    :return: tuple - (eventTimestamps, processingTimestamps)
    """
    # Calculate time gap in ms
    staticDataSet = False
    intervalMicros = int(1e6 / eventRate)

    numRows = rows
    eventTimestamps = None
    if (staticDataSet):
        # generate processing timestampes and initialize as all 0s
        eventTimestamps = np.zeros(numRows, dtype=int)
    else:
        # generate uniformly increasing event arrival times
        eventTimestamps = np.arange(0, numRows * intervalMicros, intervalMicros, dtype=int)
    return eventTimestamps


def getLatencyPercentile(fraction: float, event_time: np.ndarray, processed_time: np.ndarray) -> int:
    """
    Calculate the latency percentile from event and processed time tensors.

    :param fraction: float - Percentile in the range 0 ~ 1
    :param event_time: torch.Tensor - int64 tensor of event arrival timestamps
    :param processed_time: torch.Tensor - int64 tensor of processed timestamps
    :return: int - The latency value at the specified percentile
    """
    valid_latency = (processed_time - event_time)[(processed_time >= event_time) & (processed_time != 0)]

    # If no valid latency, return 0 as in the C++ code
    if valid_latency.size == 0:
        print("No valid latency found")
        valid_latency = 0

    # Sort the valid latency values
    valid_latency_sorted = np.sort(valid_latency)

    # Calculate the index for the percentile
    t = len(valid_latency_sorted) * fraction
    idx = int(t) if int(t) < len(valid_latency_sorted) else len(valid_latency_sorted) - 1

    # Return the latency at the desired percentile
    return valid_latency_sorted[idx].item()


def store_timestamps_to_csv(filename, ids, eventTimeStamps, arrivalTimeStamps, processedTimeStamps, counts):
    """
    Store the timestamps and IDs into a CSV file.

    Args:
        ids: numpy array of IDs.
        eventTimeStamps: numpy array of event timestamps.
        arrivalTimeStamps: numpy array of arrival timestamps.
        processedTimeStamps: numpy array of processed timestamps.
    """
    # Create a DataFrame with the timestamps and ids
    df = pd.DataFrame({
        'id': ids,
        'eventTime': eventTimeStamps,
        'arrivalTime': arrivalTimeStamps,
        'processedTime': processedTimeStamps
    })
    import os
    head, tail = os.path.split(filename)
    if not os.path.isdir(head):
        os.makedirs(head)
    filename = filename +f"_{counts}_timestamps.csv"
    df.to_csv(filename, index=False)

    print(f"Timestamps saved to {filename}")


class CongestionRunner(BaseRunner):
    def build(algo, dataset, max_pts):
        '''
        Return set up time
        '''
        t0 = time.time()
        ds = DATASETS[dataset]()
        ndims = ds.d
        algo.setup(ds.dtype, max_pts, ndims)
        print('Algorithm set up')
        return time.time() - t0
    


    def run_task(algo, ds, distance, count, run_count, search_type, private_query, runbook, definition, query_arguments, runbook_path,dataset):
        best_search_time = float('inf')
        search_times = []
        all_results = []

        # data = ds.get_dataset()
        # ids = np.arange(1, ds.nb+1, dtype=np.uint32)

        Q = ds.get_queries() if not private_query else ds.get_private_queries()
        print(fr"Got {Q.shape[0]} queries")  

        # Load Runbook
        result_map = {}
        num_searches = 0
        counts = {'initial':0,'batch_insert':0,'insert':0,'delete':0,'search':0}

        attrs = {
            "name": str(algo),
            "pendingWrite":0
        }

        for step, entry in enumerate(runbook):
            start_time = time.time()
            match entry['operation']:
                case 'initial':
                    start = entry['start']
                    end = entry['end']
                    ids = np.arange(start,end,dtype=np.uint32)
                    algo.initial_load(ds.get_data_in_range(start,end),ids)
                case 'startHPC':
                    algo.startHPC()
                case 'endHPC':
                    algo.endHPC()
                case 'waitPending':
                    t0 = time.time()
                    algo.waitPendingOperations()
                    attrs['pendingWrite'] += (time.time()-t0)*1e6
                case 'batch_insert':
                    start = entry['start']
                    end = entry['end']
                    batchSize = entry['batchSize']
                    eventRate = entry['eventRate']
                    print(f"Inserting with batch size={batchSize}")
                    step = (end-start)//batchSize
                    ids = np.arange(start, end, dtype=np.uint32)
                    eventTimeStamps = generateTimestamps(rows=end-start,eventRate=eventRate)
                    arrivalTimeStamps = np.zeros(end-start,dtype=int)
                    processedTimeStamps = np.zeros(end-start, dtype=int)

                    # TODO: with time
                    start_time = time.time()
                    for i in range(step):
                        tNow = (time.time()-start_time)*1e6
                        tExpectedArrival = eventTimeStamps[(i+1)*batchSize-1]
                        while tNow<tExpectedArrival:
                            # busy waiting for a batch to arrive
                            tNow = (time.time()-start_time)*1e6
                        arrivalTimeStamps[i*batchSize:(i+1)*batchSize] = tExpectedArrival

                        print(f'step {start+i*batchSize}:{start+(i+1)*batchSize}')
                        algo.insert(ds.get_data_in_range(start+i*batchSize,start+(i+1)*batchSize), ids[i*batchSize:(i+1)*batchSize])
                        processedTimeStamps[i*batchSize:(i+1)*batchSize] = (time.time()-start_time)*1e6


                    # process the rest
                    if(start+step*batchSize<end and start+(step+1)*batchSize>end):
                        tNow = (time.time()-start_time)*1e6
                        tExpectedArrival = eventTimeStamps[end-start-1]
                        while tNow<tExpectedArrival:
                            # busy waiting for a batch to arrive
                            tNow = (time.time()-start_time)*1e6
                        print(f'last {start+step*batchSize}:{end}')
                        algo.insert(ds.get_data_in_range(step*batchSize,end), ids[step*batchSize:])
                        processedTimeStamps[step*batchSize:end] = (time.time() - start_time) * 1e6
                        arrivalTimeStamps[step*batchSize:end] = tExpectedArrival

                    attrs["95%latency(Insert)_" + str(counts['batch_insert'])] = getLatencyPercentile(0.95,
                                                                                                      eventTimeStamps,
                                                                                                      processedTimeStamps)
                    filename = get_result_filename(dataset, count, definition, query_arguments, neurips23track="congestion", runbook_path=runbook_path)
                    store_timestamps_to_csv(filename, ids,eventTimeStamps, arrivalTimeStamps, processedTimeStamps, counts['batch_insert'])
                    counts['batch_insert'] +=1


                case 'insert':
                    start = entry['start']
                    end = entry['end']
                    ids = np.arange(start, end, dtype=np.uint32)
                    algo.insert(ds.get_data_in_range(start, end), ids)

                    counts['insert'] +=1
                case 'delete':
                    ids = np.arange(entry['start'], entry['end'], dtype=np.uint32)
                    algo.delete(ids)

                    counts['delete'] +=1
                case 'replace':
                    tags_to_replace = np.arange(entry['tags_start'], entry['tags_end'], dtype=np.uint32)
                    ids_start = entry['ids_start']
                    ids_end = entry['ids_end']
                    algo.replace(ds.get_data_in_range(ids_start, ids_end), tags_to_replace)
                case 'search':
                    if search_type == 'knn':
                        t0=time.time()
                        algo.query(Q, count)
                        attrs['latencyOfQuery_'+str(counts['search'])]=(time.time()-t0)*1e6
                        results = algo.get_results()

                    elif search_type == 'range':
                        algo.range_query(Q, count)
                        results = algo.get_range_results()
                    else:
                        raise NotImplementedError(f"Search type {search_type} not available.")
                    all_results.append(results)
                    result_map[num_searches] = step + 1
                    num_searches += 1

                    counts['search'] +=1

                case _:
                    raise NotImplementedError('Invalid runbook operation.')
            step_time = (time.time() - start_time)
            print(f"Step {step+1} took {step_time}s.")

        attrs["run_count"]=run_count
        attrs["distance"]=distance
        attrs["type"]= search_type,
        attrs["count"] =int(count)
        attrs["search_times"]= search_times
        attrs["num_searches"]= num_searches
        attrs["private_queries"]=private_query

        # record each search
        for k, v in result_map.items():
            attrs['step_' + str(k)] = v
        print(attrs)
        additional = algo.get_additional()
        for k in additional:
            attrs[k] = additional[k]
        return (attrs, all_results)