from __future__ import absolute_import

import itertools
import numpy
import os
import yaml
import traceback
import sys

from benchmark.plotting.metrics import all_metrics as metrics, get_recall_values
from benchmark.sensors.power_capture import power_capture
from benchmark.dataset_io import knn_result_read
import benchmark.streaming.compute_gt
import benchmark.congestion.compute_gt
from benchmark.streaming.load_runbook import load_runbook_streaming
from benchmark.congestion.load_runbook import load_runbook_congestion

def get_or_create_metrics(run):
    if 'metrics' not in run:
        run.create_group('metrics')
    return run['metrics']


def create_pointset(data, xn, yn):
    xm, ym = (metrics[xn], metrics[yn])
    rev_y = -1 if ym["worst"] < 0 else 1
    rev_x = -1 if xm["worst"] < 0 else 1
    data.sort(key=lambda t: (rev_y * t[-1], rev_x * t[-2]))

    axs, ays, als = [], [], []
    # Generate Pareto frontier
    xs, ys, ls = [], [], []
    last_x = xm["worst"]
    comparator = ((lambda xv, lx: xv > lx)
                  if last_x < 0 else (lambda xv, lx: xv < lx))
    for algo, algo_name, xv, yv in data:
        if not xv or not yv:
            continue
        axs.append(xv)
        ays.append(yv)
        als.append(algo_name)
        if comparator(xv, last_x):
            last_x = xv
            xs.append(xv)
            ys.append(yv)
            ls.append(algo_name)
    return xs, ys, ls, axs, ays, als


def compute_metrics(true_nn, res, metric_1, metric_2,
                    recompute=False):
    all_results = {}
    for i, (properties, run) in enumerate(res):
        algo = properties['algo']
        algo_name = properties['name']
        # cache indices to avoid access to hdf5 file
        if metric_1 == "ap"  or metric_2 == "ap":
            run_nn = (numpy.array(run['lims']),
                    numpy.array(run['neighbors']),
                    numpy.array(run['distances']))
        else:
            run_nn = numpy.array(run['neighbors'])
        if recompute and 'metrics' in run:
            del run['metrics']
        metrics_cache = get_or_create_metrics(run)

        metric_1_value = metrics[metric_1]['function'](
            true_nn, run_nn, metrics_cache, properties)
        metric_2_value = metrics[metric_2]['function'](
            true_nn, run_nn, metrics_cache, properties)

        print('%3d: %80s %12.3f %12.3f' %
              (i, algo_name, metric_1_value, metric_2_value))

        all_results.setdefault(algo, []).append(
            (algo, algo_name, metric_1_value, metric_2_value))

    return all_results

def compute_metrics_all_runs(dataset, dataset_name, res, recompute=False, 
        sensor_metrics=False, search_times=False,
        private_query=False, neurips23track=None, runbook_path=None):

    if neurips23track == 'congestion' and runbook_path:
        dataset_params = get_dataset_params_from_runbook(runbook_path, dataset_name)

    try:
        if neurips23track not in ['streaming', 'congestion']:
            true_nn = dataset.get_private_groundtruth() if private_query else dataset.get_groundtruth()
        elif neurips23track == 'streaming':
            true_nn_across_steps = []
            gt_dir = benchmark.streaming.compute_gt.gt_dir(dataset, runbook_path)
            max_pts, runbook = load_runbook_streaming(dataset_name, dataset.nb, runbook_path)
            for step, entry in enumerate(runbook):
                if entry['operation'] == 'search':
                    step_gt_path = os.path.join(gt_dir, 'step' + str(step+1) + '.gt100')
                    true_nn = knn_result_read(step_gt_path)
                    true_nn_across_steps.append(true_nn)
        elif neurips23track == "congestion":
            true_nn_across_steps = []
            gt_dir = benchmark.congestion.compute_gt.gt_dir(dataset, runbook_path)
            max_pts, runbook = load_runbook_congestion(dataset_name, dataset.nb, runbook_path)
            true_nn_across_batches = []
            num_batch_insert = 0
            for step, entry in enumerate(runbook):
                if entry['operation'] == 'search':
                    if neurips23track == 'congestion':
                        step_gt_path = os.path.join(gt_dir, 'step' + str(step) + '.gt100')
                    else:
                        step_gt_path = os.path.join(gt_dir, 'step' + str(step+1) + '.gt100')
                    true_nn = knn_result_read(step_gt_path)
                    true_nn_across_steps.append(true_nn)

                if entry['operation'] == 'batch_insert':
                    batchSize = entry['batchSize']
                    temp_gt_dir = gt_dir
                    if batchSize==2500 and runbook_path!='neurips23/runbooks/congestion/test_experiment.yaml':
                        temp_gt_dir = benchmark.congestion.compute_gt.gt_dir(dataset, 'neurips23/runbooks/congestion/general_experiment/general_experiment.yaml')

                    true_nn_across_batches.append([])
                    end = entry['end']
                    start = entry['start']
                    batchSize = entry['batchSize']
                    batch_step = (end - start) // batchSize
                    continuous_counter = 0
                    for i in range(batch_step):
                        continuous_counter += batchSize
                        if(continuous_counter >= (end-start)/100):
                            step_gt_path = os.path.join(temp_gt_dir, 'batch' +str(num_batch_insert) +"_"+str(i) + '.gt100')
                            true_nn = knn_result_read(step_gt_path)
                            true_nn_across_batches[-1].append(true_nn)
                            continuous_counter = 0
                    if (start + batch_step * batchSize < end and start + (batch_step + 1) * batchSize > end):
                        continuous_counter += batchSize
                        if(continuous_counter>=(end-start)/100):
                            step_gt_path = os.path.join(temp_gt_dir, 'batch' + str(num_batch_insert) + "_" + str(batch_step) + '.gt100')

                            true_nn = knn_result_read(step_gt_path)
                            true_nn_across_batches[-1].append(true_nn)
                    num_batch_insert += 1


    except:
        print(f"Groundtruth for {dataset} not found.")
        #traceback.print_exc()
        return

    search_type = dataset.search_type()
    for i, (properties, run) in enumerate(res):
        algo = properties['algo']
        algo_name = properties['name']
        # cache distances to avoid access to hdf5 file
        if search_type == "knn" or search_type == "knn_filtered":
            if neurips23track in ['streaming','congestion']:
                run_nn_across_steps = []
                run_nn_across_batches = []
                for i in range(0,properties['num_searches']):
                   step_suffix = str(properties['step_' + str(i)])
                   run_nn_across_steps.append(numpy.array(run['neighbors_step' +  step_suffix]))
                   #true_nn_across_steps.append()
                for i in range(len(properties['continuousQueryResults'])):
                    run_nn_across_batches.append([])
                    for j in range(len(properties['continuousQueryResults'][i])):
                        temp = numpy.array(properties['continuousQueryResults'][i][j])
                        run_nn_across_batches[i].append(temp)



            else:
                run_nn = numpy.array(run['neighbors'])
        elif search_type == "range":
            if neurips23track in ['streaming', 'congestion']:
                run_nn_across_steps = []
                for i in range(1,run['num_searches']):
                    step_suffix = str(properties['step_' + str(i)])
                    run_nn_across_steps.append(
                        (
                        numpy.array(run['neighbors_step' + step_suffix]),
                        numpy.array(run['neighbors_step' + step_suffix]),
                        numpy.array(run['distances_step' + step_suffix])
                        )
                    )
            else:
                run_nn = (numpy.array(run['lims']),
                        numpy.array(run['neighbors']),
                        numpy.array(run['distances']))
        if recompute and 'metrics' in run:
            print('Recomputing metrics, clearing cache')
            del run['metrics']
        metrics_cache = get_or_create_metrics(run)

        dataset = properties['dataset']
        try:
            dataset = dataset.decode()
            algo = algo.decode()
            algo_name = algo_name.decode()
        except:
            pass


        dataset_info = dataset
        if neurips23track == 'congestion' and dataset_params:
            batchsize = dataset_params.get('batchSize', None)
            eventrate = dataset_params.get('eventRate', None)
            if batchsize and eventrate:
                dataset_info = f"{dataset}(BatchSize: {batchsize}, EventRate: {eventrate})"

        run_result = {
            'algorithm': algo,
            'parameters': algo_name,
            'dataset': dataset_info if neurips23track not in ['streaming', 'congestion'] else dataset_info + '(' + os.path.split(runbook_path)[-1] + ')',
            'count': properties['count'],
        }
        for name, metric in metrics.items():
            if search_type == "knn" and name == "ap" or\
                search_type == "range" and name == "k-nn" or\
                search_type == "knn_filtered" and name == "ap" or\
                neurips23track in ["streaming", 'congestion'] and name == "qps" or\
                neurips23track in ["streaming", 'congestion'] and name == "queriessize":
                continue
            if not sensor_metrics and name=="wspq": #don't process power sensor_metrics by default
                continue
            if not search_times and name=="search_times": #don't process search_times by default
                continue
            if neurips23track in ['streaming', 'congestion']:
                v = []
                bv=[]
                assert len(true_nn_across_steps) == len(run_nn_across_steps)
                for (true_nn, run_nn) in zip(true_nn_across_steps, run_nn_across_steps):
                  clear_cache = True

                  if clear_cache and 'knn' in metrics_cache:
                    del metrics_cache['knn']
                  val = metric["function"](true_nn, run_nn, metrics_cache, properties)
                  v.append(val)
                if name == 'k-nn':
                  print('Recall: ', v)
                #v = numpy.mean(v)
                assert len(true_nn_across_batches) == len(run_nn_across_batches)
                for(true_nn, run_nn) in zip(true_nn_across_batches, run_nn_across_batches):
                    bv.append([])
                    assert(len(true_nn)==len(run_nn))
                    for(t,r) in zip(true_nn, run_nn):
                        mean, std, recalls, queries_with_ties = get_recall_values(t, r, properties['count'])
                        val = mean
                        bv[-1].append(val)



            else:
                v = metric["function"](true_nn, run_nn, metrics_cache, properties)

            if(name=="k-nn"):
                for i in range(len(v)):
                    run_result['knn_'+str(i)] = v[i]

                for i in range(len(bv)):
                    recall_sum = 0
                    latency_sum = 0
                    for j in range(len(bv[i])):
                        recall_sum+=bv[i][j]
                        latency_sum+=properties['continuousQueryLatencies'][i][j]
                    run_result['continuousRecall_'+str(i)] = recall_sum/len(bv[i])
                    run_result['continuousLatency_'+str(i)] = latency_sum/len(bv[i])
                    run_result['continuousThroughput_'+str(i)] = properties['querySize']/((run_result['continuousLatency_'+str(i)])/1e6)

                for i in range(len(properties['latencyInsert'])):
                    run_result['latencyInsert_'+str(i)] = properties['latencyInsert'][i]
                    run_result['insertThroughput' + str(i)] = properties['insertThroughput'][i]
                for i in range(len(properties['latencyQuery'])):
                    run_result['latencyQuery_'+str(i)] = properties['latencyQuery'][i]
                    run_result['queryThroughput'+str(i)] = properties['querySize']/(properties['latencyQuery'][i]/1e6)


                run_result['updateMemFPRT'] = properties['updateMemoryFootPrint']
                run_result['searchMemFPRT'] = properties['searchMemoryFootPrint']
                run_result['querySize'] = properties['querySize']




            run_result[name] = numpy.nanmean(v)
        yield run_result

#def compute_all_metrics(true_nn, run, properties, recompute=False):
#    algo = properties["algo"]
#    algo_name = properties["name"]
#    print('--')
#    print(algo_name)
#    results = {}
#    # cache nn to avoid access to hdf5 file
#    run_nn = numpy.array(run["neighbors"])
#    if recompute and 'metrics' in run:
#        del run['metrics']
#    metrics_cache = get_or_create_metrics(run)
#
#    for name, metric in metrics.items():
#        v = metric["function"](
#            true_nn, run_nn, metrics_cache, properties)
#        results[name] = v
#        if v:
#            print('%s: %g' % (name, v))
#    return (algo, algo_name, results)
#

def generate_n_colors(n):
    vs = numpy.linspace(0.3, 0.9, 7)
    colors = [(.9, .4, .4, 1.)]

    def euclidean(a, b):
        return sum((x - y)**2 for x, y in zip(a, b))
    while len(colors) < n:
        new_color = max(itertools.product(vs, vs, vs),
                        key=lambda a: min(euclidean(a, b) for b in colors))
        colors.append(new_color + (1.,))
    return colors


def create_linestyles(unique_algorithms):
    colors = dict(
        zip(unique_algorithms, generate_n_colors(len(unique_algorithms))))
    linestyles = dict((algo, ['--', '-.', '-', ':'][i % 4])
                      for i, algo in enumerate(unique_algorithms))
    markerstyles = dict((algo, ['+', '<', 'o', '*', 'x'][i % 5])
                        for i, algo in enumerate(unique_algorithms))
    faded = dict((algo, (r, g, b, 0.3))
                 for algo, (r, g, b, a) in colors.items())
    return dict((algo, (colors[algo], faded[algo],
                        linestyles[algo], markerstyles[algo]))
                for algo in unique_algorithms)


def get_up_down(metric):
    if metric["worst"] == float("inf"):
        return "down"
    return "up"


def get_left_right(metric):
    if metric["worst"] == float("inf"):
        return "left"
    return "right"


def get_plot_label(xm, ym):
    template = ("%(xlabel)s-%(ylabel)s tradeoff - %(updown)s and"
                " to the %(leftright)s is better")
    return template % {"xlabel": xm["description"],
                       "ylabel": ym["description"],
                       "updown": get_up_down(ym),
                       "leftright": get_left_right(xm)}


# Add the batchsize and eventrate parameters to the result file
def get_dataset_params_from_runbook(runbook_path, dataset_name):

    with open(runbook_path, 'r') as file:
        runbook = yaml.safe_load(file)

    if dataset_name not in runbook:
        print(f"Dataset {dataset_name} not found in runbook.")
        return None

    dataset_info = runbook[dataset_name]

    batchsize = None
    eventrate = None

    for step, step_details in dataset_info.items():
        if isinstance(step_details, dict):
            batchsize = step_details.get('batchSize', None)
            eventrate = step_details.get('eventRate', None)
            if batchsize and eventrate:
                return {'batchSize': batchsize, 'eventRate': eventrate}

    return None