import json
import os
import argparse
import subprocess
from multiprocessing import Pool


def build(library, args, dockerfile):
    print('Building %s...' % library)
    if args is not None and len(args) != 0:
        q = " ".join(["--build-arg " + x.replace(" ", "\\ ") for x in args])
    else:
        q = ""

    try:
        command = 'docker build %s --rm -t big-ann-benchmark-v2-lighweight-%s -f' \
                    % (q, library )
        command += ' neurips-2023/install/Dockerfile.%s .' % (library)  \
                    if not dockerfile else ' %s .' % dockerfile
        subprocess.check_call(command, shell=True)
        return {library: 'success'}
    except subprocess.CalledProcessError:
        return {library: 'fail'}


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
        '--build-arg',
        help='pass given args to all docker builds',
        nargs="+")
    args = parser.parse_args()

    print('Building base image...')
    subprocess.check_call(
        'docker build \
        --rm -t big-ann-benchmark-v2-lighweight -f neurips-2023/install/Dockerfile .', shell=True)

    if args.dockerfile:
        tags = [os.path.basename(os.path.dirname(args.dockerfile))]
    elif args.algorithm:
        tags = [args.algorithm]
    elif os.getenv('LIBRARY'):
        tags = [os.getenv('LIBRARY')]
    else:
        tags = [fn.split('.')[-1] for fn in os.listdir('neurips-2023/install') if fn.startswith('Dockerfile.') and not 'faissgpu' in fn]

    print('Building algorithm images... with (%d) processes' % args.proc)

    if args.proc == 1:
        install_status = [build(tag, args.build_arg, args.dockerfile) for tag in tags ]
    else:
        pool = Pool(processes=args.proc)
        install_status = pool.map(build_multiprocess, [(tag, args.build_arg, args.dockerfile) for tag in tags ])
        pool.close()
        pool.join()

    print('\n\nInstall Status:\n' + '\n'.join(str(algo) for algo in install_status))
