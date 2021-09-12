import h5py
import numpy as np
import sys

f = h5py.File('/tmp/foo.hdf5','w')
dt = h5py.vlen_dtype(np.dtype('int32'))
dset = f.create_dataset('vlen_int', (100,), dtype=dt)
dset[0] = np.ones( (3,1) )
dset[1] = [1,2,3,4,5]
print( dset[0:] )

sys.exit(0)

arr = np.empty(1, dtype=object)
print(type(arr), arr.shape, arr.dtype)

a = np.ones( (2,2 ))
print(type(a), a.shape, a.dtype)
arr[0] = a

h5f = h5py.File("/tmp/test", 'w')

print("Adding cluster_list")
#h5f.create_dataset('cluster_list', data=arr)

def add_ndarray_with_type_object( h5f, name, arr ):
    print(type(arr), type(arr[0]), arr)
    dt = arr[0].dtype
    print("add", dt, arr.shape)
    v = h5py.vlen_dtype(dt)
    dset = h5f.create_dataset(name, arr.shape, dtype=dt)
    for i in range( arr.shape[0] ):
        dset[i] = arr[i]
    print( type(dset) )
    print( dset )
    print( dset[0:] )

add_ndarray_with_type_object( h5f, "cluster_list", arr )

h5f.close()
