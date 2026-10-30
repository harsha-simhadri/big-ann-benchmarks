# HingeZero full v2

Creator: David Duffy. The HingeZero architecture consists of the memory bank, dual-tanh recurrent state refinement, stored-state witness and retaining loop. FAISS supplies the candidate index; ANN integration was prepared with AI assistance.

## HingeZero full architecture: static dense k-NN adapter

This adds David Duffy's HingeZero memory-bank, dual-tanh, witness and retaining-loop architecture to a static dense k-NN adapter. FAISS IVF/PQ retrieves candidates; the unchanged HingeZero core refines the working state, verifies tagged stored states and evaluates retaining checkpoints. Original vectors remain read-only and disk-mapped. Final neighbours are ranked using the original query and dataset metric. No softmax is used.

Every mode retains the same 512 initial candidates. Full mode uses eight recurrent updates and a refined-state/checkpoint blend to route additional candidate lookup. The contribution includes no-HingeZero, zero-step, no-retention and original-query-expansion controls.

### Author-reported OpenAI-100K results

All 20,000 public queries, k=10, nprobe=32, one run per mode through the official runner on the author's local machine. These are local results, not organizer measurements.

| Mode | Recall@10 | Queries/sec | Search seconds | Mean candidates |
|---|---:|---:|---:|---:|
| without_hz | 88.6275% | 232.02 | 86.20 | 512.00000 |
| full | 88.6870% | 63.61 | 314.44 | 512.02530 |
| zero_steps | 88.6650% | 67.49 | 296.32 | 512.01710 |
| no_retention | 88.6675% | 65.50 | 305.34 | 512.01795 |
| query_expansion | 91.5500% | 114.23 | 175.09 | 768.00000 |

Full mode reports 240,000 witness checks, zero failed checks, zero seed-score regressions and zero retention commits. Its 88.6870% recall exceeds the same-index baseline by 0.0595 percentage points. The original-query-expansion control reaches 91.5500%; this result belongs to the non-recurrent control and is not attributed to the HingeZero recurrence. Full mode adds an average of 0.0253 new candidates, while the expansion control adds 256. Modes perform different search work and are not compute-matched.

### Reproducibility and integration

- Code, comparison definitions, report command, Dockerfile and a manually dispatched random-xs container workflow are included.
- OpenAI configuration contains one index build and ten proposed search settings (nprobe 1, 2, 4, 8, 16, 32, 64, 96, 128, 256). Only nprobe=32 has author OpenAI measurements in this contribution; the others are organizer evaluation settings.
- Previously completed development checks: 174 correctness checks passed; all five modes ran across all 1,000 random-xs public queries at 99.78% recall. These are synthetic development measurements, separate from the author's OpenAI results.
- Core SHA256: dd4c7e82c9823ea6c69b972113ef6a3a132d152d6b319551658fe00333e7bfa8. Core and adapter algorithm bytes are preserved from the measured v2 distribution. The Docker entrypoint is corrected to the repository's run_algorithm.py wrapper; this packaging change has not been container-tested.
- No further local benchmarks were run when preparing this submission. The review workflow is manual; the publication commit requests skipping push/pull-request CI. No Docker or organizer CI pass is claimed.

This is submitted as a draft static dense k-NN code contribution for maintainer review, with T2-style disk-backed vector storage. It does not implement streaming insert/delete operations, provide a billion-vector result, or establish eligibility for a current prize competition. Please confirm whether OpenAI-100K and this adapter are suitable for the repository's current evaluation process.

## Reproduce the measured run (reference only)

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 MKL_NUM_THREADS=1 .venv-hingezero-full-v1/bin/python -u run_hingezero_full_v2.py --dataset openai-100K --all-modes --runs 1
```

This command records how the author produced the uploaded reports. It is not run by the submission publisher. Software versions from the author's OpenAI run are not contained in the reports. The author previously described a Pop!_OS laptop, eight CPU cores, 7.7 GiB RAM and a GTX 1050; hardware details were not independently collected. The benchmark adapter is CPU-based, with four FAISS threads. No GPU throughput is claimed.

Build time -1 in these reports means an existing index was loaded, not that building required negative time. Index file size is 10,347,956 bytes; original vector bank size is 614,400,000 bytes. These are distinct from peak RAM. The reported index RAM delta is not a total process-memory measurement.

The existing full-mode expansion asks for 256 routed neighbours after preserving 512 seed neighbours. This creates substantial overlap on OpenAI-100K. That measured behaviour is preserved in this submission. The proposed 768-neighbour routed expansion has not been substituted into code associated with these results.

The provided summary reports are author-produced evidence. HDF5 result files may be copied from the author's existing repository by submit.py, without running queries. No dataset or index is uploaded. Source publication uses the target repository's contribution process; no separate license file is added by this package.

Official protocol: https://github.com/harsha-simhadri/big-ann-benchmarks/blob/main/neurips21/t1_t2/README.md#submitting_your_algorithm
