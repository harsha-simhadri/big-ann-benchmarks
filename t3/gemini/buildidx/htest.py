import h5py
import numpy as np
import sys

if True:
    arr = np.empty( (2,), dtype=object)    
    a = np.random.rand( 3,4 ) 
    b = np.random.rand( 2,4 ) 
    arr[0] = a
    arr[1] = b
    print("arr", arr)

    f = h5py.File('/tmp/foo.hdf5','w')
    dt = h5py.vlen_dtype(a.dtype)
    dset = f.create_dataset('vlen_int', arr.shape, dtype=dt)

    a = a.reshape( -1 )
    dset[0] = a
    
    b = b.reshape( -1 )
    dset[1] = b
   
    farr = dset[0:]
    print(farr.shape, farr.dtype)

    narr = np.empty( (2, ), dtype=object)
    for i in range(2):
        narr[i] = dset[i].reshape( -1, 4 )

    print("narr", narr) 
    sys.exit(0)

if True:
    f = h5py.File('/tmp/foo.hdf5','w')
    dt = h5py.vlen_dtype(np.dtype('int32'))
    dset = f.create_dataset('vlen_int', (2,), dtype=dt)
    dset[0] = [1,2,3,4]
    dset[1] = [1,2,3,4,5]
    print(type(dset[0]),dset[0].dtype,dset[0].shape)
    arr = dset[0]
    a = arr.reshape( (2,2) )
    print("a",a, a.shape) 
    print(dset[0:2])
    print(np.reshape(dset[0],(None,2)))
    print(dset[1])
    sys.exit(0)

if False:
    f = h5py.File('/tmp/foo.hdf5','w')
    float32_t = h5py.special_dtype(vlen=np.dtype('float32'))
    evolutionary_ = f.create_dataset('evolutionary', shape=(1, 3,), maxshape=(None, 3,), dtype=float32_t)
    a = np.random.randn(1, 3, 4)
    b = np.random.randn(1, 3, 6)

    evolutionary_[0] = a
    print('evo[0] is \n', evolutionary_.value)

    evolutionary_.resize(3, axis=0)
    evolutionary_[1] = b
    print('evo[0,1,2] is\n', evolutionary_.value)

    sys.exit(0)

if True:
    f = h5py.File('/tmp/foo.hdf5','w')
    dt = h5py.special_dtype(vlen=np.dtype('float32'))
    dset = f.create_dataset('vlen_int', shape=(1,3,), maxshape=(None,3,), dtype=dt)
    dset[0] = np.random.randn( 1, 3, 3 )
    dset.resize(3, axis=0)
    dset[1] = np.random.randn( 1, 3, 1 )
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
