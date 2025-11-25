# Caselaw Dataset

This file describes a new public vector benchmark based on the [Collaborative Open Legal Data (COLD) Cases dataset](https://huggingface.co/datasets/harvard-lil/cold-cases), based on CourtListener's [bulk data](https://www.courtlistener.com/help/api/bulk-data). The data consists of 8.3 million legal cases, with rich metadata including fields such as the date filed, the court type, name, and jurisdiction, the name of the judge, etc., along with a written opinion for each decision. Due to the long length of some opinions, cases are embedded using OpenAI's [text-embedding-3-small](https://platform.openai.com/docs/models/text-embedding-3-small) model as multi-vectors, where multiple vectors may correspond to one document. 

## License

The original dataset is licensed under a [CC0 1.0 Universal license](https://huggingface.co/datasets/choosealicense/licenses/blob/main/markdown/cc0-1.0.md). The license of all embedding and auxiliary files in this release is [CDLA-2.0](https://cdla.dev/permissive-2-0/).  

## Files and Format

The embeddings are released using a new multi-vector binary format. It begins with a header containing the number of points, the dimension, and the total number of vectors, followed by the vector counts for each document, in little-endian 32-bit integers. Then the float32 vector data follows in a flat array. For the reader's convenience we provide a utility for reading and writing files in this format in `multi_vector_utils.py`.

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
3. "date_filed": the date the case was filed. Originally in YYYY-MM-DD format, we converted dates to ordinals using Python's `datetime` library for ease of use for comparative operators. They can be converted back to the original format using `datetime`'s `fromordinal()` function.
4. "court_jurisdiction": the place of jurisdiction of the court. Typically either a US state or the entire United States.
5. "court_type": the court type as a one- or two-letter abbreviation (appeals, criminal, circuit, and so on).
6. "court_full_name": the full name of the court.

Filters for the base and query sets can be downloaded using the following urls:

```bash
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_base_metadata.jsonl
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_query_metadata.jsonl
```

In addition to releasing metadata, we also curated a set of filtered queries from the query metadata and computed ground truth with respect to points satisfying those queries, again using Chamfer distance. The filter queries as well as groundtruth for the full dataset and the first 1M and 100K vectors can be downloaded using the following links:

```bash
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_query_filters.jsonl
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_filtered_gt.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_filtered_gt_1M.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_filtered_gt_100K.bin
```

The filtered groundtruth is calculated for up to the top 100 points, but since some very selective queries may have fewer than 100 points satisfying the filter predicate, we use the range groundtruth format for storing the groundtruth files. It consists of the number of points, followed by the total number of results, the number of results per point, and then the identifiers of the ground truth points. A reader for this format can be found in the function `range_result_read` in `benchmark/dataset_io.py`.

Python functions for reading the jsonl metadata files and checking whether a line satisfies a given filter query are included in `jsonl_filter_utils.py`. Unfortunately they are not currently compatible with the utilities described in `filter_utils.md`. 

### Single Vector Files

For ease of use for those who wish to work with single-vector datasets instead of multi-vector datasets, we also release a utility for splitting the dataset and query set into those documents which were embedded into a single vector (due to being short enough to fit within the embedding context token maximum), versus those which were embedded to multi-vectors. Due to the Pareto-like distribution of the document lengths, this resulted in 7414023 base vectors and 89812 query vectors after withholding multi-vector documents. The utility for this conversion is found in `multi_vector_utils.py`. This utility was used to isolate the base and query documents, metadata, and filters that embedded to single vectors. We then computed both filtered and unfiltered groundtruth for the single-vector base and query sets, as well as 100K and 1M prefixes of the base set. Note that the groundtruth ids are re-indexed, so the id of a vector in the groundtruth below does not correspond to the same vector as in the groundtruth files above.

The groundtruth can be downloaded using the following links:

```bash
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_singlevec_gt.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_singlevec_gt_1M.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_singlevec_gt_100K.bin

wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_singlevec_gt_filtered.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_singlevec_gt_filtered_1M.bin
wget https://comp21storage.z5.web.core.windows.net/caselaw/caselaw_singlevec_gt_filtered_100K.bin
```

## Development

This section contains details on the development of the dataset which may be useful for interpreting any results from the dataset.

### Embedding Generation

Each legal case was formatted as a JSON string encoding all its fields, with the "opinion" field at the end. If the total number of tokens was larger than the 8192-token context window, the string was chunked into multiple text strings with 512-token overlap between chunks. Strings were embedded using OpenAI's [text-embedding-3-small](https://platform.openai.com/docs/models/text-embedding-3-small), with 1532 floating-point dimensions.

### Filter Curation

Here we provide a brief summary of how we selected a filter query for each query. Each of the four nontrivial metadata fields (excluding the document ids from consideration) was converted to a predicate. For fields "court_full_name", "court_jurisdiction", and "court_type", the predicate is in the form of equality to the string value. For "date_filed", a date range around the date of filing was used. For dates prior to 1900, a twenty-year radius around the date filed was used. For dates between 1900-1950, a ten-year radius was used; for dates 1950-present, a four-year radius was used. 

Each query was randomly assigned a single predicate with probability one-third or a logical AND of two predicates with probability two-thirds. For the purposes of this document, a date radius query was counted as a single predicate, even though it is technically encoded as an AND of two predicates (less than a particular date and greater than a particular date). For the single-predicate queries, one of the four fields was randomly chosen with a slight bias towards court name to help keep the average specificity low. For the double-predicate queries, the first field was randomly chosen, but since the name of a court implies its type and jurisdiction, if "court_name" was the first field selected we disallowed type and jurisdiction for the second field, and similarly if type or jurisdiction were selected as the first field, we disallowed name as the second field. 

The average specificity (proportion of base points satisfying a given query) was about 4.5%, with maximum value 38% and minimum 0%. We did not disallow non-satisfiable queries as they are a phenomenon that can validly occur in filter scenarios, but they were empirically very rare.

### Notes

The case with "case_id" 4292693 was omitted from the embeddings as its opinion seemed to consist of thousands of pages of degenerate text. Otherwise, each file from the [COLD Cases release on HuggingFace](https://huggingface.co/datasets/harvard-lil/cold-cases) was embedded and released. 

