# Caselaw Dataset

This file describes a new public vector benchmark based on the [Collaborative Open Legal Data (COLD) Cases dataset](https://huggingface.co/datasets/harvard-lil/cold-cases), based on CourtListener's [bulk data](https://www.courtlistener.com/help/api/bulk-data). The data consists of 8.3 million legal cases, with rich metadata including fields such as the date filed, the court type, name, and jurisdiction, the name of the judge, etc., along with a written opinion for each decision. Due to the long length of some opinions, cases are embedded using OpenAI's [text-embedding-3-small](https://platform.openai.com/docs/models/text-embedding-3-small) model as multi-vectors, where multiple vectors may correspond to one document. 

## License

The original dataset is licensed under a [CC0 1.0 Universal license](https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/cc0-1.0.md). The license of all embedding and auxiliary files in this release is [CDLA-2.0](https://cdla.dev/permissive-2-0/).  

## Files and Format

The embeddings are released using a new multi-vector binary format. It begins with a header containing the number of points, the dimension, and the total number of vectors, followed by the vector counts for each document, in little-endian 32-bit integers. Then the float32 vector data follows in a flat array. For the reader's convenience we also provide a short Python function for parsing this data at the end of the document.

The total number of documents is 8,362,175. We split these vectors into a base set of 8,262,175 multi-vectors and a query set with 100,000 multi-vectors. The base and query embeddings can be downloaded using the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_base_embeddings.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_query_embeddings.bin
```

We calculated ground truth (the top-100 nearest neighbors) for the query set with respect to the full base set, as well as the first 100,000 and 1,000,000 prefixes of the base set. Ground truth is calculated with respect to the Chamfer aggregation metric, where given two collections of vectors $A$ and $B$, the distance from $A$ to $B$ is calculated by:

$$
\sum_{i=1}^n \min_{b_j \in B} ||a_i, b_j||
$$

Where the distance used in this case is Euclidean distance.

Ground truth follows the standard format of a header containing the number of points and the number of top-k results as 32-bit integers, then the groundtruth ids as 32-bit integers, then the float32 distance values for use in tie-breaking. They can be downloaded using the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_gt_100.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_gt_1M_100.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_gt_100K_100.bin
```

The metadata is released in jsonl format, with one line per document, and the following metadata fields:

1. "doc_id": the document id based on the document's numeric order in the base file.
2. "case_id": a unique identifier drawn from the original parquet files; can be used to match a case back to its complete metadata and opinion text.
3. "date_filed": the date the case was filed in YYY-MM-DD format.
4. "court_jurisdiction": the place of jurisdiction of the court. Typically either a US state or the entire United States.
5. "court_type": the court type as a one- or two-letter abbreviation (appeals, criminal, circuit, and so on).
6. "court_full_name": the full name of the court.

Filters for the base and query sets can be downloaded using the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_base_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_query_filters.jsonl
```


## Development

This section contains details on the development of the dataset which may be useful for interpreting any results from the dataset.

### Embedding Generation

Each legal case was formatted as a JSON string encoding all its fields, with the "opinion" field at the end. If the total number of tokens was larger than the 8192-token context window, the string was chunked into multiple text strings with 512-token overlap between chunks. Strings were embedded using OpenAI's [text-embedding-3-small](https://platform.openai.com/docs/models/text-embedding-3-small), with 1532 floating-point dimensions.

### Notes

The case with "case_id" 4292693 was omitted from the embeddings as its opinion seemed to consist of thousands of pages of degenerate text. Otherwise, each file from the [COLD Cases release on HuggingFace](https://huggingface.co/datasets/harvard-lil/cold-cases) was embedded and released. 

## Python Parsing Code

```python
def read_multivec_embedding_file(file_path):
    with open(file_path, 'rb') as f:
        num_points = int.from_bytes(f.read(4), 'little')
        dimension = int.from_bytes(f.read(4), 'little')
        total_chunks = int.from_bytes(f.read(4), 'little')
        print(f"Number of points: {num_points}, dimension: {dimension}, total chunks: {total_chunks}")
         # Read chunk_counts as a numpy array
        chunk_counts = np.frombuffer(f.read(4 * num_points), dtype=np.uint32)

        # Read embeddings as a flat numpy array and reshape
        embeddings = np.frombuffer(f.read(4 * total_chunks * dimension), dtype=np.float32)
        embeddings = embeddings.reshape((total_chunks, dimension))


    # convert embeddings to a list of 2d numpy arrays, one per document
    chunked_embeddings = []
    index = 0
    for count in chunk_counts:
        chunked_embeddings.append(np.array(embeddings[index:index+count], dtype=np.float32))
        index += count
    return chunked_embeddings, chunk_counts, dimension
```