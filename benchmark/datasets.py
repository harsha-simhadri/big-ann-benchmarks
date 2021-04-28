import h5py
import numpy
import os
import random
import sys

from benchmark.distances import metrics

from urllib.request import urlopen
from urllib.request import urlretrieve

from faiss.contrib.exhaustive_search import knn_ground_truth, knn, range_ground_truth
from faiss import ResultHeap



def download(src, dst):
    if not os.path.exists(dst):
        # TODO: should be atomic
        print('downloading %s -> %s...' % (src, dst))
        urlretrieve(src, dst)


def get_dataset_fn(dataset):
    if not os.path.exists('data'):
        os.mkdir('data')
    return os.path.join('data', '%s.hdf5' % dataset)


def get_dataset(which):
    hdf5_fn = get_dataset_fn(which)
    try:
        url = 'http://TODO/%s.hdf5' % which
        download(url, hdf5_fn)
    except:
        print("Cannot download %s" % url)
        if which in DATASETS:
            print("Creating dataset locally")
            DATASETS[which](hdf5_fn)
    hdf5_f = h5py.File(hdf5_fn, 'r')
    return hdf5_f


# Everything below this line is related to creating datasets
# TODO: This is supposed to be carried out in a docker container

def bvecs_mmap(fname):
    x = numpy.memmap(fname, dtype='uint8', mode='r')
    d = x[:4].view('int32')[0]
    return x.reshape(-1, d + 4)[:, 4:]

def sanitize(x):
    return numpy.ascontiguousarray(x, dtype='float32')

def sift(out_fn, batchsize):
#    import tarfile
#
#    url = 'ftp://ftp.irisa.fr/local/texmex/corpus/sift.tar.gz'
#    fn = os.path.join('data', 'sift.tar.tz')
#    download(url, fn)
#    with tarfile.open(fn, 'r:gz') as t:
#        train = _get_irisa_matrix(t, 'sift/sift_base.fvecs')
#        test = _get_irisa_matrix(t, 'sift/sift_query.fvecs')
#        write_output(train, test, out_fn, 'euclidean')
    # for now assume vectors exist locally
    f = h5py.File(out_fn, 'w')
    f.attrs['distance'] = 'euclidean'
    f.attrs['type'] = 'knn' # carry out k-nn queries (as opposed to range)

    queries = bvecs_mmap('bigann_query.bvecs')
    f['queries'] = queries

    data = bvecs_mmap('bigann_base.bvecs')
    parts = (data.shape[0] - 1) // batchsize + 1
    #parts = 4
    res = ResultHeap(nq=len(queries), k=100)
    for part in range(parts):
        print(f"Running part {part}/{parts}")
        name = f"data_{part}"
        part_data = data[part * batchsize : (part + 1) * batchsize, :]
        f[name] = part_data
        D, I = knn(sanitize(queries), sanitize(part_data), 100)
        res.add_result(D=D, I=I + part * batchsize)
        f[name + "_D"] = res.D
        f[name + "_I"] = res.I

    f.close()


DATASETS = {
    'random-xs-20-euclidean': lambda out_fn, batchsize: random_float(out_fn, 20, 10000, 100,
                                                    'euclidean'),
    'random-s-100-euclidean': lambda out_fn, batchsize: random_float(out_fn, 100, 100000, 1000,
                                                    'euclidean'),
    'random-xs-20-angular': lambda out_fn, batchsize: random_float(out_fn, 20, 10000, 100,
                                                  'angular'),
    'random-s-100-angular': lambda out_fn, batchsize: random_float(out_fn, 100, 100000, 1000,
                                                  'angular'),
    'sift-128-euclidean': sift,
}
