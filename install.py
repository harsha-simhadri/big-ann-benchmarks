import json
import os
import argparse
import subprocess
from multiprocessing import Pool
import neurips23.common


def build(tag, args, dockerfile):
    print('Building %s...' % tag)
    if args is not None and len(args) != 0:
        q = " ".join(["--build-arg " + x.replace(" ", "\\ ") for x in args])
    else:
        q = ""

    try:
        command = 'docker build %s --rm -t %s -f' \
                   % (q, tag)
        command += ' %s .' % dockerfile
        print(command)
        subprocess.check_call(command, shell=True)
        return {tag: 'success'}
    except subprocess.CalledProcessError:
        return {tag: 'fail'}

def build_multiprocess(args):
    return build(*args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--proc",
        default=1,
        type=int,
        help="the number of process to build docker images")
    parser.add_argument(
        '--algorithm',
        metavar='NAME',
        help='build only the named algorithm image',
        default=None)
    parser.add_argument(
        '--dockerfile',
        metavar='PATH',
        help='build only the image from a Dockerfile path',
        default=None)
    parser.add_argument(
        '--neurips23track',
        choices=['filter','ood','streaming','sparse','none'],
        default='none'
    )
    parser.add_argument(
        '--build-arg',
        help='pass given args to all docker builds',
        nargs="+")
    args = parser.parse_args()

    print('Building base image...')
    if args.neurips23track != 'none':
        subprocess.check_call(
            'docker build \
            --rm -t %s -f %s .' % (neurips23.common.docker_tag_base(), neurips23.common.dockerfile_path_base()), shell=True)
        track = args.neurips23track

        build_postgres_base = False

        if args.algorithm: # build a specific algorithm
            algos = [args.algorithm]
            build_postgres_base = args.algorithm.startswith('postgres-')
        else: # build all algorithms in the track with Dockerfiles.
            algos = list(filter(lambda entry : os.path.exists(neurips23.common.dockerfile_path(track, entry)),
                            os.listdir(neurips23.common.track_path(track))))
            build_postgres_base = True

        if build_postgres_base:
            print('Building Postgres base image...')
            subprocess.check_call(
                'docker build \
                --rm -t %s -f %s .' % (neurips23.common.docker_tag_postgres_base(), neurips23.common.dockerfile_path_postgres_base()), shell=True)

        tags = [neurips23.common.docker_tag(track, algo) for algo in algos]
        dockerfiles = [neurips23.common.dockerfile_path(track, algo) for algo in algos]
    else: # NeurIPS'21
        track_prefix = 'billion-scale-benchmark'
        subprocess.check_call(
            'docker build \
            --rm -t %s -f install/Dockerfile .' % track_prefix, shell=True)
        if args.dockerfile:
            tags = [track_prefix + '-' + os.path.basename(os.path.dirname(args.dockerfile))]
            dockerfiles = args.dockerfile
        else:
            if args.algorithm:
                algos = [args.algorithm]
            elif os.getenv('LIBRARY'):
                algos = [os.getenv('LIBRARY')]
            else:
                algos = [fn.split('.')[-1] for fn in os.listdir('install') if fn.startswith('Dockerfile.') and not 'faissgpu' in fn]
            dockerfiles = ['install/Dockerfile.' +  algo for algo in algos]
            tags = [track_prefix + '-' + algo for algo in algos]

    print('Building algorithm images... with (%d) processes' % args.proc)

    if args.proc == 1:
        install_status = [build(tag, args.build_arg, dockerfile) for (tag, dockerfile) in zip(tags, dockerfiles)]
    else:
        pool = Pool(processes=args.proc)
        install_status = pool.map(build_multiprocess, 
                                  [(tag, args.build_arg, dockerfile) for (tag, dockerfile) in zip(tags, dockerfiles)])
        pool.close()
        pool.join()

    print('\n\nInstall Status:\n' + '\n'.join(str(algo) for algo in install_status))
