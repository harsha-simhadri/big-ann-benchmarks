from __future__ import absolute_import
import argparse
import logging
import logging.config

import docker
import multiprocessing.pool
import os
import psutil
import random
import shutil
import sys
import traceback

from benchmark.datasets import DATASETS
from benchmark.random_datasets_utils import parse_dataset, normalize_dataset_name
from benchmark.algorithms.definitions import (get_all_definitions, 
                                              get_definitions,
                                              list_algorithms,
                                              algorithm_status,
                                              InstantiationStatus)
from benchmark.results import get_result_filename
from benchmark.runner import run, run_docker, run_no_docker

from benchmark.sensors.power_capture import power_capture

import neurips23.common


def positive_int(s):
    i = None
    try:
        i = int(s)
    except ValueError:
        pass
    if not i or i < 1:
        raise argparse.ArgumentTypeError("%r is not a positive integer" % s)
    return i


def run_worker(args, queue):
    print("RW", args)
    while not queue.empty():
        definition = queue.get()
        memory_margin = 500e6  # reserve some extra memory for misc stuff
        mem_limit = int((psutil.virtual_memory().available - memory_margin))
        #mem_limit = 128e9 # 128gb for competition
        cpu_limit = "0-%d" % (multiprocessing.cpu_count() - 1)

        if args.nodocker:
            run_no_docker(definition, args.dataset, args.count,
                          args.runs, args.timeout, args.rebuild, cpu_limit, mem_limit,
                          args.t3, args.power_capture,
                          args.upload_index, args.download_index,
                          args.blob_prefix, args.sas_string,
                          args.private_query, args.neurips23track, args.runbook_path)

        else:
            run_docker(definition, args.dataset, args.count,
                       args.runs, args.timeout, args.rebuild, cpu_limit, mem_limit,
                       args.t3, args.power_capture,
                       args.upload_index, args.download_index,
                       args.blob_prefix, args.sas_string,
                       args.private_query, args.neurips23track, args.runbook_path)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--dataset',
        metavar='NAME',
        help='the dataset to load training points from',
        default='sift-1M',
        # choices=DATASETS.keys())
        )
    parser.add_argument(
        "-k", "--count",
        default=-1,
        type=int,
        help="the number of near neighbours to search for")
    parser.add_argument(
        '--definitions',
        metavar='FILE',
        help='load algorithm definitions from FILE',
        default='algos-2021.yaml')
    parser.add_argument(
        '--algorithm',
        metavar='NAME',
        help='run only the named algorithm',
        default=None)
    parser.add_argument(
        '--docker-tag',
        metavar='NAME',
        help='run only algorithms in a particular docker image',
        default=None)
    parser.add_argument(
        '--list-algorithms',
        help='print the names of all known algorithms and exit',
        action='store_true')
    parser.add_argument(
        '--force',
        help='re-run algorithms even if their results already exist',
        action='store_true')
    parser.add_argument(
        '--rebuild',
        help='re-build index even if it exists',
        action='store_true')
    parser.add_argument(
        '--runs',
        metavar='COUNT',
        type=positive_int,
        help='run each algorithm instance %(metavar)s times and use only'
             ' the best result',
        default=5)
    parser.add_argument(
        '--timeout',
        type=int,
        help='Timeout (in seconds) for each individual algorithm run, or -1'
             'if no timeout should be set',
        default=12 * 3600)
    parser.add_argument(
        '--max-n-algorithms',
        type=int,
        help='Max number of algorithms to run (just used for testing)',
        default=-1)
    parser.add_argument(
        '--power-capture',
        help='Power capture parameters for the T3 competition. '
            'Format is "ip:port:capture_time_in seconds" (ie, 127.0.0.1:3000:10).',
        default="")
    parser.add_argument(
        '--t3',
        help='Run as a T3 participant.',
        action='store_true')
    parser.add_argument(
        '--nodocker',
        help='Override default of invoking algorithm in docker container.',
        action='store_true')
    parser.add_argument(
        '--upload-index',
        help='Upload index to Azure blob storage and avoid local queries.',
        action='store_true')
    parser.add_argument(
        '--download-index',
        help='Download index uploaded to Azure blob storage and run local queries.',
        action='store_true')
    parser.add_argument(
        '--blob-prefix',
        help='Azure blob prefix to upload indices to and download indices from.'
    )
    parser.add_argument(
        '--sas-string',
        help='SAS string to authenticate to Azure blob storage.'
    )
    parser.add_argument(
        '--private-query',
        help='Use the new set of private queries that were not released during the competition period.',
        action='store_true'
    )
    parser.add_argument(
        '--neurips23track',
        choices=['filter', 'ood', 'sparse', 'streaming', 'none', 'congestion'],
        default='none'
    )
    parser.add_argument(
        '--runbook_path',
        help='runbook yaml path for neurips23 streaming track',
        default='neurips23/streaming/simple_runbook.yaml'
    )
    parser.add_argument(
        '--eventrate',
        type=int,
        help='Event rate for congestion scenarios'
    )
    parser.add_argument(
        '--batchsize',
        type=int,
        help='Batch size for congestion scenarios'
    )

    args = parser.parse_args()

    # if args.neurips23track == 'congestion':
    #     if args.eventrate is None or args.batchsize is None:
    #         raise ValueError("Both --eventrate and --batchsize must be provided when --neurips23track is 'congestion'.")

    if args.timeout == -1:
        args.timeout = None

    if args.list_algorithms:
        list_algorithms(args.definitions)
        sys.exit(0)

    if args.power_capture:
        # validate power capture environment
        power_capture( args.power_capture )
        power_capture.ping()

    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger("annb")

    # dataset = DATASETS[args.dataset]()
    dataset = parse_dataset(args)
    dataset.prepare(args.neurips23track == 'none') # prepare dataset, but skip potentially huge base vectors
    dimension = dataset.d
    point_type = 'float'
    distance = dataset.distance()
    if args.count == -1:
        args.count = dataset.default_count()
    if args.neurips23track == 'none':
        definitions = get_definitions(
            args.definitions, dimension, normalize_dataset_name(args.dataset), distance, args.count)
    else:
        definitions = get_all_definitions(
            neurips23.common.track_path(args.neurips23track), 
            dimension, normalize_dataset_name(args.dataset), distance, args.count)

    # Filter out, from the loaded definitions, all those query argument groups
    # that correspond to experiments that have already been run. (This might
    # mean removing a definition altogether, so we can't just use a list
    # comprehension.)
    filtered_definitions = []
    for definition in definitions:
        query_argument_groups = definition.query_argument_groups
        if not query_argument_groups:
            query_argument_groups = [[]]
        not_yet_run = []
        for query_arguments in query_argument_groups:
            if type(query_arguments) != list:
                query_arguments = [query_arguments]
            fn = get_result_filename(args.dataset,
                                     args.count, definition,
                                     query_arguments)
            if args.force or not os.path.exists(fn):
                not_yet_run.append(query_arguments)
        if not_yet_run:
            if definition.query_argument_groups:
                definition = definition._replace(
                    query_argument_groups=not_yet_run)
            filtered_definitions.append(definition)
    definitions = filtered_definitions

    random.shuffle(definitions)

    if args.algorithm:
        logger.info(f'running only {args.algorithm}')
        definitions = [d for d in definitions if d.algorithm == args.algorithm]

    if not args.nodocker:
        # See which Docker images we have available
        docker_client = docker.from_env()
        docker_tags = set()
        for image in docker_client.images.list():
            for tag in image.tags:
                tag = tag.split(':')[0]
                docker_tags.add(tag)

        if args.docker_tag:
            logger.info(f'running only {args.docker_tag}')
            definitions = [
                d for d in definitions if d.docker_tag == args.docker_tag]

        if set(d.docker_tag for d in definitions).difference(docker_tags):
            logger.info(f'not all docker images available, only: {set(docker_tags)}')
            logger.info(f'missing docker images: '
                        f'{str(set(d.docker_tag for d in definitions).difference(docker_tags))}')
            definitions = [
                d for d in definitions if d.docker_tag in docker_tags]

    if args.max_n_algorithms >= 0:
        definitions = definitions[:args.max_n_algorithms]

    if len(definitions) == 0:
        raise Exception('Nothing to run')
    else:
        logger.info(f'Order: {definitions}')

    queue = multiprocessing.Queue()
    for definition in definitions:
        queue.put(definition)
    #run_worker(args, queue)
    workers = [multiprocessing.Process(target=run_worker, args=(args, queue))
               for i in range(1)]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]
