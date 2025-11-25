import numpy as np

# read an embedding file in the following format:
# all in binary
# the number of points, followed by the dimension, followed by the total number of chunks, as uint32
# then a num_points length array of chunk counts per document, as uint32
# then a flat array of embedding data of shape (total_number_of_chunks, dimension) 
# with dtype specified by the caller (e.g., np.float32)
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

def read_multivec_embedding_file_header(embedding_file_path):
    """
    Reads the header from the embedding binary file and returns:
    num_documents, dimension, total_number_of_embeddings, chunk_counts (np.array), offset (start of embedding data)
    """
    with open(embedding_file_path, 'rb') as f:
        num_documents = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
        dimension = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
        total_number_of_embeddings = int(np.frombuffer(f.read(4), dtype=np.int32)[0])
        chunk_counts = np.frombuffer(f.read(4 * num_documents), dtype=np.int32)
        offset = 4 + 4 + 4 + 4 * num_documents  # bytes to start of embedding data
    return num_documents, dimension, total_number_of_embeddings, chunk_counts, offset


def withhold_multichunk_docs(
    metadata_jsonl_path,
    embeddings_bin_path,
    output_metadata_jsonl,
    output_embeddings_bin,
    withheld_metadata_jsonl,
    withheld_embeddings_bin,
    filter_jsonl_path = None,
    filter_output_jsonl = None,
    withheld_filter_jsonl = None
):
    """
    Withholds all documents with more than one chunk from the embeddings and metadata fields.
    Writes the remaining and withheld documents to new files in the same format as embed_caselaw_dataset.
    """
    # Read all metadata fields
    with open(metadata_jsonl_path, 'r') as f:
        metadata_lines = f.readlines()
    num_documents = len(metadata_lines)
    print(f"Total documents: {num_documents}")

    # Read header and chunk counts from embedding file
    num_docs_file, dimension, total_number_of_embeddings, chunk_counts, offset = read_multivec_embedding_file_header(embeddings_bin_path)
    assert num_documents == num_docs_file, "Mismatch between metadata fields and embedding file header."

    # Compute start/end indices for each document's embeddings
    chunk_starts = np.cumsum(np.concatenate(([0], chunk_counts[:-1])))
    chunk_ends = chunk_starts + chunk_counts

    # Find indices for single-chunk and multi-chunk documents
    single_chunk_indices = [i for i, c in enumerate(chunk_counts) if c == 1]
    multi_chunk_indices = [i for i, c in enumerate(chunk_counts) if c > 1]
    print(f"Keeping {len(single_chunk_indices)} single-chunk documents.")
    print(f"Withholding {len(multi_chunk_indices)} multi-chunk documents.")

    # Split metadata fields and chunk counts
    kept_metadata_lines = [metadata_lines[i] for i in single_chunk_indices]
    withheld_metadata_lines = [metadata_lines[i] for i in multi_chunk_indices]
    kept_chunk_counts = [chunk_counts[i] for i in single_chunk_indices]
    withheld_chunk_counts = [chunk_counts[i] for i in multi_chunk_indices]

    # Read all embeddings
    with open(embeddings_bin_path, 'rb') as f:
        f.seek(offset)
        embeddings = np.frombuffer(f.read(), dtype=np.float32)
    assert len(embeddings) == total_number_of_embeddings * dimension, "Embedding data size mismatch."
    embeddings = embeddings.reshape(total_number_of_embeddings, dimension)

    # Split embeddings by document
    kept_embeddings = []
    withheld_embeddings = []
    for i in single_chunk_indices:
        start, end = chunk_starts[i], chunk_ends[i]
        kept_embeddings.append(embeddings[start:end])
    for i in multi_chunk_indices:
        start, end = chunk_starts[i], chunk_ends[i]
        withheld_embeddings.append(embeddings[start:end])

    # Flatten for writing
    kept_embeddings_flat = np.vstack(kept_embeddings) if kept_embeddings else np.empty((0, dimension), dtype=np.float32)
    withheld_embeddings_flat = np.vstack(withheld_embeddings) if withheld_embeddings else np.empty((0, dimension), dtype=np.float32)

    # Write kept embeddings in simple format
    with open(output_embeddings_bin, 'wb') as f:
        f.write(np.int32(len(kept_metadata_lines)).tobytes())
        f.write(np.int32(dimension).tobytes())
        f.write(kept_embeddings_flat.tobytes())

    # Write withheld embeddings in the multichunk format
    with open(withheld_embeddings_bin, 'wb') as f:
        f.write(np.int32(len(withheld_metadata_lines)).tobytes())
        f.write(np.int32(dimension).tobytes())
        f.write(np.int32(len(withheld_embeddings_flat)).tobytes())
        f.write(np.array(withheld_chunk_counts, dtype=np.int32).tobytes())
        f.write(withheld_embeddings_flat.tobytes())

    # Write metadata fields
    with open(output_metadata_jsonl, 'w') as f_out:
        # rewrite doc_id fields of metadata lines to be consecutive integers
        for i, line in enumerate(kept_metadata_lines):
            line = json.loads(line)
            line['doc_id'] = i
            f_out.write(json.dumps(line) + "\n")
    with open(withheld_metadata_jsonl, 'w') as f_withheld:
        for i, line in enumerate(withheld_metadata_lines):
            line = json.loads(line)
            line['doc_id'] = i
            f_withheld.write(json.dumps(line) + "\n")

    if filter_jsonl_path:
        # Read all filter fields
        with open(filter_jsonl_path, 'r') as f:
            filter_lines = f.readlines()
        assert len(filter_lines) == num_documents, "Mismatch between filter fields and metadata."
        # Split filter fields
        kept_filter_lines = [filter_lines[i] for i in single_chunk_indices]
        withheld_filter_lines = [filter_lines[i] for i in multi_chunk_indices]
        # Write filter fields
        with open(filter_output_jsonl, 'w') as f_out:
            for i, line in enumerate(kept_filter_lines):
                line = json.loads(line)
                line['query_id'] = i
                f_out.write(json.dumps(line) + "\n")
        with open(withheld_filter_jsonl, 'w') as f_withheld:
            for i, line in enumerate(withheld_filter_lines):
                line = json.loads(line)
                line['query_id'] = i
                f_withheld.write(json.dumps(line) + "\n")
        print(f"Written filter fields to {filter_output_jsonl} and {withheld_filter_jsonl}")


    print(f"Written {len(kept_embeddings_flat)} embeddings to {output_embeddings_bin}")
    print(f"Written {len(withheld_embeddings_flat)} embeddings to {withheld_embeddings_bin}")
    print(f"Written metadata fields to {output_metadata_jsonl} and {withheld_metadata_jsonl}")