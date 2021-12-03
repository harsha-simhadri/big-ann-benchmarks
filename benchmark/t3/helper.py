import os
import docker

from benchmark.datasets import DATASETS, BigANNDataset

def print_cuda_versions():
    info = subprocess.check_output(['nvidia-smi', '--query-gpu=driver_version','--format=csv'])
    print(info)
    info = subprocess.check_output(['nvcc', '--version'])
    print(info)


def t3_create_container( definition, cmd, cpu_limit, mem_limit):

    if definition.algorithm in [ 'faiss-t3' ]:

        print("Launching GPU container")
        container = create_container_with_gpu_support(
            docker.from_env(),
            definition.docker_tag,
            cmd,
            volumes={
                os.path.abspath('benchmark'):
                    {'bind': '/home/app/benchmark', 'mode': 'ro'},
                os.path.abspath('data'):
                    {'bind': '/home/app/data', 'mode': 'rw'},
                os.path.abspath('results'):
                    {'bind': '/home/app/results', 'mode': 'rw'},
            },
            cpuset_cpus=cpu_limit,
            mem_limit=mem_limit,
            detach=True)
        container.start()
        return container

    elif definition.algorithm in [ 'cuanns_ivfpq' ]:

        print("Launching GPU container")
        volumes = {
            os.path.abspath('benchmark'): {'bind': '/home/app/benchmark', 'mode': 'ro'},
            os.path.abspath('data'): {'bind': '/home/app/data', 'mode': 'rw'},
            os.path.abspath('results'): {'bind': '/home/app/results', 'mode': 'rw'},
        }
        for path in definition.docker_volumes:
            if os.path.exists(path):
                volumes[path] = {'bind': path, 'mode': 'rw'}
        # print('# volumes: {}'.format(volumes))
        container = create_container_with_gpu_support(
            docker.from_env(),
            definition.docker_tag,
            cmd,
            volumes=volumes,
            cpuset_cpus=cpu_limit,
            mem_limit=mem_limit,
            detach=True)
        container.start()
        return container

    else:
        raise Exception("Docker invoke not supported for this algorithm.")

def create_container_with_gpu_support(client, image, command, volumes, **kwargs):


    from docker.models.images import Image
    from docker.models.containers import _create_container_args

    if isinstance(image, Image):
        image = image.id

    os.environ['NVIDIA_VISIBLE_DEVICES']='all'

    kwargs['image'] = image
    kwargs['command'] = command
    kwargs['version'] = client.containers.client.api._version
    kwargs['volumes'] = volumes
    create_kwargs = _create_container_args(kwargs)

    device_request = {
        'Driver': 'nvidia',
        'Capabilities': [['gpu'], ['nvidia']],
        'Count': -1,  # enable all gpus
    }

    if device_request is not None:
        create_kwargs['host_config']['DeviceRequests'] = [device_request]

    resp = client.api.create_container(**create_kwargs)
    return client.containers.get(resp['Id'])

def create_container_with_network_host_support(client, image, command, volumes, **kwargs):

    kwargs['image'] = image
    kwargs['command'] = command
    kwargs['version'] = client.containers.client.api._version
    kwargs['volumes'] = volumes
    kwargs['network'] = "host"
    create_kwargs = _create_container_args(kwargs)

    resp = client.api.create_container(**create_kwargs)
    return client.containers.get(resp['Id'])


class BigANNDatasetAngular(BigANNDataset):

    def __init__(self, *args, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if self.gt_fn:
            print("You must compute and replace the ground truth file here:", self.gt_fn )
        else:
            gt_fn = self._form_gt_fn()
            if os.path.exists( os.path.join( self.basedir, gt_fn)):
                #print("file %s already exists" % gt_fn )
                self.gt_fn = gt_fn
            else:
                print("You must compute the ground and create the file in here:",
                    os.path.join( self.basedir, gt_fn ) )
        return ret

    def _form_gt_fn(self):
        gt_fn = "gt_angular.ibin"
        print("ds", self.ds_fn, self.nb, 10**9)
        if self.nb < 10**9:
            gt_fn += ".crop_nb_%d" % ( self.nb )
        return gt_fn

    def get_groundtruth(self, *args, **kwargs):
        self.gt_fn = self.gt_fn
        return super().get_groundtruth(*args, **kwargs)

    def distance(self):
        return "angular"


