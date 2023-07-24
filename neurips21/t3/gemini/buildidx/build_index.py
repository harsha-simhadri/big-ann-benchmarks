import os
import numpy as np
import h5py
import faiss
import sys

#
# Get parameters
#
dbase = "deep-1B"
nlist = 2097152
qbits = 768
nbits = 512
nt = 83886080
is_f16 = True
num_records = 1000000000
output_dir = "/mnt/localdisk2/George/Projects/BigANN/gemini/indexes"

#
# Form the path to the source files
#
resources_path = '../../t3/gsi/'
case_dir = '1b/'
resources_path_case = f'{resources_path}{case_dir}'
centroids_dirs = { 524288: 'centroids_512k/', 2097152: 'centroids_2m/', 4194304: 'centroids_4m/'}
num_centroids_dir = centroids_dirs[nlist]
fp_quantizer_file_name = f'{resources_path}{num_centroids_dir}Deep1B.nt{nt}.nlist{nlist}.quantizer'
records_encoding_file_name = f'{resources_path}records_weights/records_weights.bits{nbits}.npy'
centroids_encoding_file_name = f'{resources_path}{num_centroids_dir}centroids_weights.nt{nt}.nlist{nlist}.nbits{nbits}.npy'
index_file_name = f'{resources_path_case}Deep1B.ivfbinnh.nt{nt}.nlist{nlist}.nb{num_records}.bits{qbits}.index'
db_path = f'{resources_path_case}fdb.npy'

#
# Validate all the source files exists
#
print('********************** Paths ***************************')
print('fp_quantizer_file_name =', fp_quantizer_file_name)
if not os.path.isfile(fp_quantizer_file_name):
    raise FileNotFoundError(fp_quantizer_file_name)
print('records_encoding_file_name =', records_encoding_file_name)
if not os.path.isfile(records_encoding_file_name):
    raise FileNotFoundError(records_encoding_file_name)
print('centroids_encoding_file_name =', centroids_encoding_file_name)
if not os.path.isfile(centroids_encoding_file_name):
    raise FileNotFoundError(centroids_encoding_file_name)
print('index_file_name =', index_file_name)
if not os.path.isfile(index_file_name):
    raise FileNotFoundError(index_file_name)
print('db_path =', db_path)
if not os.path.isfile(db_path):
    raise FileNotFoundError(db_path)
print('********************************************************')

#
# Form the path to the output index file
#
output_file = "%s.nbits=%d,qbits=%d,nlist=%d,nt=%d,nb=%d,fp16=%s.geminiindex" % ( dbase, nbits, qbits, nlist, nt, num_records, str(is_f16))
full_path = os.path.join( output_dir, output_file )
print("Checking if index file already exists (%s)" % full_path)
if os.path.exists(full_path):
    raise Exception("gemini index file already exists (%s)" % full_path )

#
# Load the source files
#
def convert_index_to_cluster_and_ids_lists(index, nbits):
    cluster_list = np.empty(index.invlists.nlist, dtype=object)
    ids_list = np.empty(index.invlists.nlist, dtype=object)

    zero_count = 0

    for i in range(index.invlists.nlist):
        list_sz = index.invlists.list_size(i)

        if list_sz == 0:
            zero_count = zero_count + 1
            ids = None
        else:
            ids_ptr = index.invlists.get_ids(i)
            ids = np.array(faiss.rev_swig_ptr(ids_ptr, list_sz)).reshape(-1, 1).astype(np.uint32) # GSL requires a 2d arrray for some reason
            index.invlists.release_ids(ids_ptr)
            # index.invlists.release_ids(list_sz, ids_ptr)
        ids_list[i] = ids

        codes_ptr = index.invlists.get_codes(i)
        codes = np.array(faiss.rev_swig_ptr(codes_ptr, list_sz * nbits // 8)).reshape(list_sz, nbits//8)
        index.invlists.release_codes(codes_ptr)
        # index.invlists.release_codes(list_sz * nbits // 8, codes_ptr)
        cluster_list[i] = codes

    print('zero_count =', zero_count)
    return cluster_list, ids_list

def get_cluster_and_ids_lists(index, nbits):
    print('Creating cluster + ids lists...')
    ret = convert_index_to_cluster_and_ids_lists(index, nbits)
    return ret

print("Reading binary index %s" % index_file_name)
index = faiss.read_index_binary(index_file_name)

print("Extracting binary cluster list and ids")
# cluster_list, ids_list = get_cluster_and_ids_lists(self.index, nbits)
cluster_list, ids_list = get_cluster_and_ids_lists(index, qbits)
print(type(cluster_list), type(ids_list), cluster_list[0].shape, cluster_list[0].dtype, cluster_list[1].shape, ids_list[0].shape, ids_list[0].dtype)

print("Extracting binary quantizer and centroids")
quantizer = faiss.downcast_IndexBinary(index.quantizer)
centroids = faiss.vector_to_array(quantizer.xb)
centroids = np.reshape(centroids, (quantizer.ntotal, quantizer.d//8))
print('Got centroids (binary):', centroids.shape, centroids.dtype)

print("Extracting float quantizer and centroids")
l2_quantizer = faiss.read_index(fp_quantizer_file_name)
l2_centroids = faiss.vector_float_to_array(l2_quantizer.xb)
l2_centroids = np.reshape(l2_centroids, (nlist, l2_quantizer.d))
print('Got centroids (float):', l2_centroids.shape, l2_centroids.dtype)

print("Reading centroids encoding file")
centroids_encoding_np = np.load(centroids_encoding_file_name)

print("Reading records encoding file")
records_encoding_np = np.load(records_encoding_file_name)

#
# Create the monolithic index and save
#
def add_ndarray_with_type_object( h5f, name, arr ):
    print("arrs", arr[0].shape, arr[0].dtype, arr[1].shape, arr[0].dtype)
    dt = h5py.vlen_dtype(arr[0].dtype)
    dset = h5f.create_dataset(name, arr.shape, dtype=dt)
    print("dt", dt, dset)
    for i in range( arr.shape[0] ):
        item = arr[i]
        #print("item",i, type(item)),
        if item!=None: dset[i] = item.reshape(-1) 
        else: dset[i] = item

print("Creating (h5py) index file at %s" % full_path)
h5f = h5py.File(full_path, 'w')

print("Adding cluster_list")
#h5f.create_dataset('cluster_list', data=cluster_list)
add_ndarray_with_type_object( h5f, "cluster_list", cluster_list )

print("Adding ids_list")
#h5f.create_dataset('ids_list', data=ids_list)
add_ndarray_with_type_object( h5f, "ids_list", ids_list )

print("Adding binary centroids")
h5f.create_dataset('centroids', data=centroids)

print("Adding float centroids")
h5f.create_dataset('l2_centroids', data=l2_centroids)

print("Adding centroids_encoding")
h5f.create_dataset('centroids_encoding_np', data=centroids_encoding_np)

print("Adding records_encoding")
h5f.create_dataset('records_encoding_np', data=records_encoding_np)

print("Adding dataset")
h5f.create_dataset('
print("Finalizing and closing index.")
h5f.close()

printf("Done. Wrote index at %s" % full_path )
