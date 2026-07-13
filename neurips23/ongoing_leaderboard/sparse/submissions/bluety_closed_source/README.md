# Bluety closed-source Sparse submission

This directory requests inclusion of Bluety as a closed-source entry for the ongoing Big-ANN / NeurIPS 2023 Sparse leaderboard.

## Submission status

- Track: Sparse
- Dataset: `sparse-full`
- Hardware: Azure Standard D8lds v5 class, 8 vCPU / 16 GiB
- Metric: maximum QPS with `recall@10 >= 0.9`
- Source availability: closed source

The ongoing leaderboard rules state that open source is encouraged but not enforced, and that closed-source entries will be marked as such.

## Result

| dataset | algorithm | recall@10 | QPS |
|---|---:|---:|---:|
| sparse-full | bluety [*] | 0.905244 | 37750.13 |

`[*]` closed source.

The full exported row is included in `res_sparse-full.csv`. VM/environment evidence is included in `vm_evidence.txt`.

## Short algorithm description

Bluety is a sparse maximum inner-product search system for SPLADE/MSMARCO-style sparse vectors. It uses a compressed sparse inverted-index layout with posting-list pruning, block/cluster summarization, and query-time candidate generation followed by exact sparse-score refinement. The submitted configuration targets the high-throughput region around `recall@10 >= 0.9` on the public Sparse benchmark query set.

## Confidentiality note

This PR intentionally does not include implementation source code, Dockerfiles, wrappers, or private implementation details. A private closed-source reproducibility package is available to maintainers as `bluety_sparse_closed_submission_nodoc.tar.gz`. It contains the BigANN wrapper, config, offline installer, verification script, and runtime wheels, and intentionally excludes technical writeups/source notes.
