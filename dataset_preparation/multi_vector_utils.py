import numpy as np

# read an embedding file in the following format:
# all in binary
# the number of points, followed by the dimension, followed by the total number of chunks, as uint32
# then a num_points length array of chunk counts per document, as uint32
# then a flat array of float32 embedding data of shape (total_number_of_chunks, dimension)
def read_multivec_embedding_file(file_path, dtype):
    with open(file_path, 'rb') as f:
        num_points = int.from_bytes(f.read(4), 'little')
        dimension = int.from_bytes(f.read(4), 'little')
        total_chunks = int.from_bytes(f.read(4), 'little')
        print(f"Number of points: {num_points}, dimension: {dimension}, total chunks: {total_chunks}")
         # Read chunk_counts as a numpy array
        chunk_counts = np.frombuffer(f.read(4 * num_points), dtype=np.uint32)

        # Read embeddings as a flat numpy array and reshape
        embeddings = np.frombuffer(f.read(np.dtype(dtype).itemsize * total_chunks * dimension), dtype=dtype)
        embeddings = embeddings.reshape((total_chunks, dimension))


    # convert embeddings to a list of 2d numpy arrays, one per document
    chunked_embeddings = []
    index = 0
    for count in chunk_counts:
        chunked_embeddings.append(np.array(embeddings[index:index+count], dtype=dtype))
        index += count
    return chunked_embeddings, chunk_counts, dimension

# Takes in a list of 2D numpy arrays (one per entry) and writes to a binary file
# in the multi-vec file format
def write_multivec_embedding_file(file_path, embeddings, dtype):
    num_points = len(embeddings)
    dimension = embeddings[0].shape[1] if num_points > 0 else 0
    chunk_counts = [emb.shape[0] for emb in embeddings]
    total_chunks = sum(chunk_counts)

    print(f"Writing {num_points} points, dimension {dimension}, total chunks {total_chunks} to {file_path}")

    with open(file_path, 'wb') as f:
        f.write(num_points.to_bytes(4, 'little'))
        f.write(dimension.to_bytes(4, 'little'))
        f.write(total_chunks.to_bytes(4, 'little'))
        for count in chunk_counts:
            f.write(count.to_bytes(4, 'little'))
        for emb in embeddings:
            f.write(emb.astype(dtype).tobytes())