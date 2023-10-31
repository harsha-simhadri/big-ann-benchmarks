import os
import yaml

from neurips23.filter.run import FilterRunner
from neurips23.sparse.run import SparseRunner
from neurips23.ood.run import OODRunner
from neurips23.streaming.run import StreamingRunner

def docker_tag_base():
    return 'neurips23'

def basedir():
    return 'neurips23'

def docker_tag(track, algo):
    return docker_tag_base() + '-' + track + '-' + algo

def dockerfile_path_base():
    return os.path.join('neurips23', 'Dockerfile')

def track_path(track):
    return os.path.join('neurips23', track)

def dockerfile_path(track, algo):
    return os.path.join(track_path(track), algo, 'Dockerfile')

def yaml_path(track, algo):
    return os.path.join(track_path(track), algo, 'config.yaml')

def get_definitions(track, algo):
    return yaml.load(yaml_path(track, algo))

RUNNERS = {
    "filter": FilterRunner,
    "sparse": SparseRunner,
    "ood": OODRunner,
    "streaming": StreamingRunner
}


