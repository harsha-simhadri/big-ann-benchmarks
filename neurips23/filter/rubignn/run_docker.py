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
import sys
sys.path.append(".")
sys.path.append("../../../")

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


def run_docker(dataset, count, runs,
               cpu_limit, mem_limit=None,
               t3=None, power_capture=None,
               upload_index=False, download_index=False,
               blob_prefix="", sas_string="", private_query=False,
               neurips23track='filter'):
    cmd = ['--dataset', dataset,
           '--algorithm', 'rubignn',
           '--runs', str(runs),
           '--count', str(count)]

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

    cmd += ["--neurips23track", "filter"]

    client = docker.from_env()
    if mem_limit is None:
        mem_limit = psutil.virtual_memory().available if neurips23track != 'streaming' else (8*1024*1024*1024)

    # ready the container object invoked later in this function
    container = None

    container = client.containers.run(
        "neurips23-filter-rubignn",
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

run_docker("yfcc-10M",10,1,8)