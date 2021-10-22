import faiss
import numpy as np

qd=768
d=512
nlist=5

nb=1000
db = np.empty((nb, d // 8), dtype='uint8')

quantizer = faiss.IndexBinaryFlat( d )
index = faiss.IndexBinaryIVF( quantizer, d, nlist )
index.train(db)
index.add(db)

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
            #GW index.invlists.release_ids(list_sz, ids_ptr)
        ids_list[i] = ids

        codes_ptr = index.invlists.get_codes(i)
        codes = np.array(faiss.rev_swig_ptr(codes_ptr, list_sz * nbits // 8)).reshape(list_sz, nbits//8)
        index.invlists.release_codes(codes_ptr)
        #GW index.invlists.release_codes(list_sz * nbits // 8, codes_ptr)
        cluster_list[i] = codes

    print('zero_count =', zero_count)
    return cluster_list, ids_list

cls, ids = convert_index_to_cluster_and_ids_lists(index,d)
print("cls", cls)
print("ids", ids)

# Querying the index
nq = 10
queries = np.empty((nq, d // 8), dtype='uint8')
print("queries", queries)
k = 1
D, I = index.search(queries, k)
print("di",D,I)


quantizer = faiss.downcast_IndexBinary(index.quantizer)
print("Quantizer", type(quantizer))
centroids = faiss.vector_to_array(quantizer.xb)
print("Centroids", type(centroids), centroids.shape)
centroids = np.reshape(centroids, (quantizer.ntotal, quantizer.d//8))
print("Centroids", type(centroids), centroids.shape)
print('centroids (binary):', centroids.shape, centroids.dtype)
