# NeurIPS 2023 Streaming Challenge and Beyond

This README will discuss ongoing changes to the streaming benchmark challenge. See the NeurIPS23 README for instructions on how to execute runbooks and compute groundtruth for them. All changes here are backwards-compatible with those instructions. 

## Semantics
 
The streaming runbooks support four operations: `search`, `insert`, `delete`, and a recent addition `replace`. The addition of replace, where a vector's data is modified in-place, prompts us to define the semantics of vector *tags* versus vector *ids*. 

Each vector is assumed to have a unique *id* which never changes throughout the course of a runbook. In the case of replaces, each vector is also assigned a numeric *tag*. The underlying vector id corresponding to a tag may change throughout the runbook when a vector is replaced. In the runbooks here, the tag of a vector is assumed to correspond to the vector id when a vector is first inserted, and then remains constant when the vector is replaced. For example, a vector with id #245 is first inserted with tag #245. If the vector is later replaced with vector id #1067, tag #245 now corresponds to vector id #1067. Upon another replace, tag #245 might next correspond to vector id #2428. This distinction leads us to define the semantics of each operation in terms of ids and tags:

1. `search` provides a set of query vectors, and returns an array of tags corresponding to the nearest index vectors to each query vector. In this repository, each call to `search` in one runbook refers to the same set of query vectors.
2. `insert` provides a range of vector ids, whose tags are identical to their vector ids, to insert into the index.
3. `delete` provides a range of existing tags whose underlying data is to be deleted from the index and no longer returned as answers to queries.
4. `replace` provides a range of existing tags and a range of vector ids, such that each tag should henceforth correspond to the new vector id. 

## Available Runbooks

Now that the number of runbooks has started to increase significantly, here we list the available runbooks (found in the `runbooks` folder within this directory) with a brief description of each. 

1. `simple_runbook.yaml`: A runbook executing a short sequences of insertions, searches, and deletions to aid with debugging and testing.
2. `simple_replace_runbook.yaml`: A runbook executing a short sequence of inserts, searches, and replaces to aid with debugging and testing.
3. `clustered_runbook.yaml`: A runbook taking a clustered dataset (options are `random-xs-clustered` and `msturing-10M-clustered`) and inserting points in clustered order.
4. `delete_runbook.yaml`: A runbook executing all steps in the clustered runbook, but which then deletes a fraction of each cluster.
5. `final_runbook.yaml`: The NeurIPS 2023 streaming challenge final runbook. It takes the `msturing-30M-clustered` dataset and performs several rounds of insertion and deletion in clustered order.
6. `msmarco-100M_expirationtime_runbook.yaml`: A runbook using the `msmarco-100M` dataset which inserts each point with a randomly chosen expiration time: never, in 200 steps, or in 50 steps.
7. `neurips23/streaming/wikipedia-35M_expirationtime_runbook.yaml`: A runbook using the `wikipedia-35M` dataset which inserts each point with a randomly chosen expiration time: never, in 200 steps, or in 50 steps.
8. `neurips23/streaming/msturing-10M_slidingwindow_runbook.yaml`: A runbook using the `msturing-10M` dataset which inserts half the points, then maintains the index at a consistent size using a sliding window. 
9. `clustered_replace_runbook.yaml`: A replace-focused runbook which takes the `msturing-10M-clustered` dataset, inserts a fraction of the points in each cluster, then replaces some of that fraction with vector ids from the same cluster.
10. `random_replace_runbook.yaml`: A replace-focused runbook which takes the `msturing-10M-clustered` dataset, inserts a fraction of the points in each cluster, then replaces some of that fraction with vector ids from a different randomly selected cluster.
