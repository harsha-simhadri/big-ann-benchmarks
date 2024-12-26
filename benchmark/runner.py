import argparse
import json
import logging
import os
import threading
import time
import traceback
import yaml

import colors
import docker
import numpy
import psutil

from benchmark.algorithms.definitions import (Definition,
                                               instantiate_algorithm)
from benchmark.algorithms.base_runner import BaseRunner

from benchmark.datasets import DATASETS
from benchmark.dataset_io import upload_accelerated, download_accelerated
from benchmark.results import store_results

from benchmark.sensors.power_capture import power_capture
from benchmark.t3.helper import t3_create_container

from neurips23.common import RUNNERS
from benchmark.streaming.load_runbook import load_runbook

def run(definition, dataset, count, run_count, rebuild,
        upload_index=False, download_index=False,
        blob_prefix="", sas_string="", private_query=False,
        neurips23track="none", runbook_path="neurips23/streaming/simple_runbook.yaml"):
    algo = instantiate_algorithm(definition)
    assert not definition.query_argument_groups \
           or hasattr(algo, "set_query_arguments") or True, """\
            error: query argument groups have been specified for %s.%s(%s), but the \
            algorithm instantiated from it does not implement the set_query_arguments \
            function""" % (definition.module, definition.constructor, definition.arguments)

    assert not upload_index or not download_index

    ds = DATASETS[dataset]()
    #X_train = numpy.array(D['train'])

    distance = ds.distance()
    search_type = ds.search_type()
    build_time = -1 # default value used to indicate that the index was loaded from file
    print(f"Running {definition.algorithm} on {dataset}")

    custom_runner = RUNNERS.get(neurips23track, BaseRunner)
    if neurips23track == 'streaming':
        max_pts, runbook = load_runbook(dataset, ds.nb, runbook_path)

    try:
        # Try loading the index from the file
        memory_usage_before = algo.get_memory_usage()
        if download_index:
            local_dir, index_prefix, components = algo.index_files_to_store(dataset)
            remote_location = blob_prefix + '/' + algo.track() + '/' + algo.__str__() + '/' + DATASETS[dataset]().short_name() + '/'
            for component in components:
                download_accelerated(remote_location + index_prefix + component,
                                     local_dir + '/' + index_prefix + component,
                                     False, sas_string)
            print("Index files downloaded.")
            if algo.load_index(dataset):
                print("Index loaded.")
            else:
                print("Index load failed.")
        elif rebuild or not algo.load_index(dataset):
            # Build the index if it is not available
            build_time = (custom_runner.build(algo,dataset)
                          if neurips23track != 'streaming' 
                          else custom_runner.build(algo, dataset, max_pts))
            print('Built index in', build_time) 
        else:
            print("Loaded existing index")


        index_size = algo.get_memory_usage() - memory_usage_before
        print('Index memory footprint: ', index_size)

        if upload_index:
            print("Starting index upload...")
            local_dir, index_prefix, components = algo.index_files_to_store(dataset)
            remote_location = blob_prefix + '/' + algo.track() + '/' + algo.__str__() + '/' + DATASETS[dataset]().short_name()
            for component in components:
                upload_accelerated(local_dir, remote_location,
                                   index_prefix + component, sas_string)
        else:
            print("Starting query")
            query_argument_groups = definition.query_argument_groups
            # Make sure that algorithms with no query argument groups still get run
            # once by providing them with a single, empty, harmless group
            if not query_argument_groups:
                query_argument_groups = [[]]

            for pos, query_arguments in enumerate(query_argument_groups, 1):
                print("Running query argument group %d of %d..." %
                      (pos, len(query_argument_groups)))
                # TODO: no need to set argument here
                if query_arguments:
                    algo.set_query_arguments(*query_arguments)
                if neurips23track == 'streaming':
                    descriptor, results = custom_runner.run_task(
                        algo, ds, distance, count, 1, search_type, private_query, runbook)
                else:
                    descriptor, results = custom_runner.run_task(
                        algo, ds, distance, count, run_count, search_type, private_query)

                descriptor["build_time"] = build_time
                descriptor["index_size"] = index_size
                descriptor["algo"] = definition.algorithm
                descriptor["dataset"] = dataset
                if power_capture.enabled():
                    if not private_query:
                        X = ds.get_queries()
                    else:
                        X = ds.get_private_queries()
                    power_stats = power_capture.run(algo, X, distance, count,
                                                    run_count, search_type, descriptor)
                print('start store results')
                store_results(dataset, count, definition,
                              query_arguments, descriptor,
                              results, search_type, neurips23track, runbook_path)
                print('end store results')
    finally:
        algo.done()


def run_from_cmdline(args=None):
    parser = argparse.ArgumentParser('''

            NOTICE: You probably want to run.py rather than this script.

    ''')
    parser.add_argument(
        '--dataset',
        choices=DATASETS.keys(),
        help=f'Dataset to benchmark on.',
        required=True)
    parser.add_argument(
        '--algorithm',
        help='Name of algorithm for saving the results.',
        required=True)
    parser.add_argument(
        '--module',
        help='Python module containing algorithm. E.g. "ann_benchmarks.algorithms.annoy"',
        required=True)
    parser.add_argument(
        '--constructor',
        help='Constructer to load from module. E.g. "Annoy"',
        required=True)
    parser.add_argument(
        '--count',
        help='k: Number of nearest neighbours for the algorithm to return.',
        required=True,
        type=int)
    parser.add_argument(
        '--rebuild',
        help='re-build index even if it exists',
        action='store_true')
    parser.add_argument(
        '--runs',
        help='Number of times to run the algorihm. Will use the fastest run-time over the bunch.',
        required=True,
        type=int)
    parser.add_argument(
        'build',
        help='JSON of arguments to pass to the constructor. E.g. ["angular", 100]'
        )
    parser.add_argument(
        'queries',
        help='JSON of arguments to pass to the queries. E.g. [100]',
        nargs='*',
        default=[])
    parser.add_argument(
        '--power-capture',
        help='Power capture parameters for the T3 competition. '
            'Format is "ip:port:capture_time_in_seconds (ie, 127.0.0.1:3000:10).',
        default="")
    parser.add_argument(
        '--upload-index',
        help='Upload index to cloud storage.',
        action='store_true')
    parser.add_argument(
        '--download-index',
        help='Download index from cloud storage.',
        action='store_true')
    parser.add_argument(
        '--blob-prefix',
        help='Azure blob prefix to upload index to or download index from.')
    parser.add_argument(
        '--sas-string',
        help='SAS string to authenticate to Azure blob storage.')
    parser.add_argument(
        '--private-query',
        help='Use the new set of private queries that were not released during the competition period.',
        action="store_true")
    parser.add_argument(
        '--neurips23track',
        choices=['filter', 'ood', 'sparse', 'streaming', 'none'],
        default='none'
    )
    parser.add_argument(
        '--runbook_path',
        help='runbook yaml path for neurips23 streaming track',
        default='neurips23/streaming/simple_runbook.yaml'
    )

    args = parser.parse_args(args)
    algo_args = json.loads(args.build)
    print(algo_args)
    query_args = [json.loads(q) for q in args.queries]

    if args.power_capture:
        power_capture( args.power_capture )
        power_capture.ping()

    definition = Definition(
        algorithm=args.algorithm,
        docker_tag=None,  # not needed
        docker_volumes=[],
        module=args.module,
        constructor=args.constructor,
        arguments=algo_args,
        query_argument_groups=query_args,
        disabled=False
    )
    run(definition, args.dataset, args.count, args.runs, args.rebuild,
        args.upload_index, args.download_index, args.blob_prefix, args.sas_string,
        args.private_query, args.neurips23track, args.runbook_path)


def run_docker(definition, dataset, count, runs, timeout, rebuild,
               cpu_limit, mem_limit=None,
               t3=None, power_capture=None,
               upload_index=False, download_index=False,
               blob_prefix="", sas_string="", private_query=False,
               neurips23track='none', runbook_path='neurips23/streaming/simple_runbook.yaml'):
    cmd = ['--dataset', dataset,
           '--algorithm', definition.algorithm,
           '--module', definition.module,
           '--constructor', definition.constructor,
           '--runs', str(runs),
           '--count', str(count)]
    if power_capture:
        cmd += ["--power-capture", power_capture ]
    if rebuild:
        cmd.append("--rebuild")
    if upload_index:
        cmd.append("--upload-index")
        cmd += ["--blob-prefix", blob_prefix]
        cmd += ["--sas-string", sas_string]
    if download_index:
        cmd.append("--download-index")
        cmd += ["--blob-prefix", blob_prefix]
        cmd += ["--sas-string", sas_string]
    if private_query==True:
        cmd.append("--private-query")

    cmd += ["--neurips23track", neurips23track]
    if neurips23track == 'streaming':
        cmd += ["--runbook_path", runbook_path]

    cmd.append(json.dumps(definition.arguments))
    cmd += [json.dumps(qag) for qag in definition.query_argument_groups]

    client = docker.from_env()
    if mem_limit is None:
        mem_limit = psutil.virtual_memory().available if neurips23track != 'streaming' else (8*1024*1024*1024)

    # ready the container object invoked later in this function
    container = None
    if t3: # T3 from NeurIPS'23
        container = t3_create_container(definition, cmd, cpu_limit, mem_limit )

    else: # T1/T2 from NeurIPS'21 or NeurIPS'23
        container = client.containers.run(
            definition.docker_tag,
            cmd,
            volumes={
                os.path.abspath('benchmark'):
                    {'bind': '/home/app/benchmark', 'mode': 'ro'},
                os.path.abspath('data'):
                    {'bind': '/home/app/data', 'mode': 'rw'},
                os.path.abspath('results'):
                    {'bind': '/home/app/results', 'mode': 'rw'},
                os.path.abspath('neurips23'):
                    {'bind': '/home/app/neurips23', 'mode': 'ro'},
            },
            cpuset_cpus=cpu_limit,
            mem_limit=mem_limit,
            detach=True)
 
    # set/override container timeout based on competition flag
    if neurips23track!='none':
        # 1 hour for streaming and 12 hours for other tracks
        timeout = 60 * 60 if neurips23track == 'streaming' else 12 * 60 * 60
        print("Setting container wait timeout to %d seconds" % timeout)       

    elif not timeout: 
        # default to 3 days (includes NeurIPS'21)
        timeout = 3600*24*3 # 3 days
        print("Setting container wait timeout to 3 days")       

    else:
        print("Requested container timeout is %d seconds" % timeout)

    logging.config.fileConfig("logging.conf") 
    logger = logging.getLogger(f"annb.{container.short_id}")

    logger.info('Created container %s: CPU limit %s, mem limit %s, timeout %d, command %s' % \
                (container.short_id, cpu_limit, mem_limit, timeout, cmd))

    def stream_logs():
        for line in container.logs(stream=True):
            logger.info(colors.color(line.decode().rstrip(), fg='blue'))

    t = threading.Thread(target=stream_logs, daemon=True)
    t.start()

    try:
        return_value = container.wait(timeout=timeout)
        _handle_container_return_value(return_value, container, logger)
    except:
        logger.error('Container.wait for container %s failed with exception' % container.short_id)
        logger.error('Invoked with %s' % cmd)
        traceback.print_exc()
    finally:
        container.remove(force=True)


def _handle_container_return_value(return_value, container, logger):
    base_msg = 'Child process for container %s' % (container.short_id)
    if type(return_value) is dict: # The return value from container.wait changes from int to dict in docker 3.0.0
        error_msg = return_value['Error'] if 'Error' in return_value else ""
        exit_code = return_value['StatusCode']
        msg = base_msg + 'returned exit code %d with message %s' %(exit_code, error_msg)
    else:
        exit_code = return_value
        msg = base_msg + 'returned exit code %d' % (exit_code)

    if exit_code not in [0, None]:
        logger.error(colors.color(container.logs().decode(), fg='red'))
        logger.error(msg)


def run_no_docker(definition, dataset, count, runs, timeout, rebuild,
                  cpu_limit, mem_limit=None, t3=False, power_capture=None,
                  upload_index=False, download_index=False,
                  blob_prefix="", sas_string="", private_query=False,
                  neurips23track='none', runbook_path='neurips23/streaming/simple_runbook.yaml'):
    cmd = ['--dataset', dataset,
           '--algorithm', definition.algorithm,
           '--module', definition.module,
           '--constructor', definition.constructor,
           '--runs', str(runs),
           '--count', str(count)]
    if power_capture:
        cmd += ["--power-capture", power_capture ]
    if rebuild:
        cmd.append("--rebuild")
    if upload_index:
        cmd.append("--upload-index")
        cmd += ["--blob-prefix", blob_prefix]
        cmd += ["--sas-string", sas_string]
    if download_index:
        cmd.append("--download-index")
        cmd += ["--blob-prefix", blob_prefix]
        cmd += ["--sas-string", sas_string]
    if private_query==True:
        cmd.append("--private-query")
    
    cmd += ["--neurips23track", neurips23track]
    if neurips23track == 'streaming':
        cmd += ["--runbook_path", runbook_path]

    cmd.append(json.dumps(definition.arguments))
    cmd += [json.dumps(qag) for qag in definition.query_argument_groups]
    run_from_cmdline(cmd)


