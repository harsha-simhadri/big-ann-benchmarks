# HMS streaming checks on current main

Engine commit: `12c80decb094d57ee13ba187a01bf1de8788ca2f`. Harness commit: `89a3abaafa63dda46b94b308bdf039e699841b3b`. The engine's hosted CI run `40070371238` passed. Both configured attempts used the official public queries, runbooks, one replay per configuration, eight schedulable CPUs, and an 8 GiB Modal memory setting. Modal's requested eight physical cores (two AWS/GCP vCPU equivalents per core) and storage differ from the official Azure D8lds v5 evaluation VM, so these timings are diagnostic and are not compared with published competitors.

| Dataset and runbook | Parameters | Average recall@10 | Replay wall | Peak process RSS | Outcome |
| --- | --- | ---: | ---: | ---: | --- |
| `msturing-10M-clustered`, `delete_runbook.yaml` | R32 L64 alpha1 T8; merge; deleted_ratio .3; rebuild_after 3; ef/rerank 512 | 0.937585 | 17:31.72 | 4,932,440 KiB | All 33 search checkpoints and 330,000 public queries completed |
| `msturing-30M-clustered`, `final_runbook.yaml` | R32 L64 alpha1 T8; merge; deleted_ratio .3; rebuild_after 1; ef/rerank 256 | — | 3600 s limit | 8,087,056,384 bytes sampled summed RSS | Timed out after step 1032 of 1280; no qualifying full-run recall |

The 10M run processed 10,000,000 inserts at 18,242/s, 5,400,000 deletes at 14,653/s, and 330,000 searches at 2,457 queries/s. Runbook timings include durable writes and consolidation. Queries for tuning were public; no heldout queries were used.

Raw artifact checksums (SHA-256):

| Run | File | SHA-256 |
| --- | --- | --- |
| 10M | `results.csv` | `c51e88be992b3bd801b9f694ec1b891956daa115908f09b6b9b65be5c7a12674` |
| 10M | `run.log` | `93868078309a29df22c15fad5479e3f1f3bb0df9809f1efa92343e0bdbd854d7` |
| 10M | `receipt.json` | `ed8a37464d48434fde552e0c1d9aad782cfd1d83ee418447f489b460b62cd3d8` |
| 30M | `run.log` | `28ce7a727c85e13cc74dca5a5ce52591e391d015c6ced621df38d2c5a00eb066` |
| 30M | `receipt.json` | `d276455b7d9f3f638533914dcb21d89b834c1b309ca30b9ca1d5926cc0358316` |

Modal app receipts: [10M delete](https://modal.com/apps/dcondrey/main/ap-4DDbAdIJPOGg7hELx0rqHy), [30M final](https://modal.com/apps/dcondrey/main/ap-wDnEcKdpMjegUy67SyOe1a). The 10M input base SHA-256 is `da1d48c34205964131b9c206bf7636a079562930c6a9ffb70d39dbd7adee5c3a`; the 30M input base SHA-256 is `05d699b8b973fb1da53752d406d8e7a8204e3f35007e22a060eb93ba76a1cd22`.

The reproduction launcher is `neurips23/streaming/hms/modal_stream.py` in the HMS benchmark worktree, with source and adapter snapshots retained in the run artifact. The third party Dockerfile pins the exact engine commit above. No competition result or standing was submitted.

## Completed public 30M candidate, 2026-10-24 UTC

A separately labeled candidate completed all 1,280 operations and 640 search checkpoints of the unchanged official `final_runbook.yaml` (SHA-256 `92347aff3bdc378b3bead517df33311bec615be2a9c8af0f5b5e0a14e51865f2`). It used the same engine commit, R24/L48/alpha1/T8, merge enabled, delta_ratio 1, deleted_ratio 0.6, min_delta 100000, rebuild_after 3, and ef/rerank256. **These are candidate parameters; the adapter's default R32/L64 configuration remains unchanged.**

The official exporter measured mean recall@10 **0.810018125** over 6,400,000 public queries, with a replay wall time of **36:29.91** (2,189.91s), exit 0. This is lower than the README's historical DiskANN 0.883 recall; it establishes no win, and hardware differences preclude a competitive comparison. All 64,000,000 returned IDs were locally revalidated as live and unique. The recorded inserts/deletes/searches processed 29,998,834/27,630,980/6,400,000 items at 35,187/40,709/9,813 per second respectively, including durable writes and consolidation in replay timing.

The container exposed eight schedulable CPUs and an eight-Modal-physical-core request (not eight AWS vCPUs), AMD CPUID family 26/model 2 (marketing model hidden), and a nominal 8 GiB limit. Process peak RSS was 7,995,784 KiB; peak quarter-second sampled summed RSS was 8,407,363,584 B below 8,589,934,592 B. The process-RSS guard was active, but strict Modal cgroup enforcement is not proven. This host differs from both the official Azure Xeon8370C and earlier runs; differences in outcome cannot be attributed solely to the changed parameters. The base was copied to container-local storage before replay. Preparation/export are excluded from the replay wall time; total container time was 2,389.38 s. Requested-resource cost estimate $0.880885 uses conservative rounded runner rates and excludes image builds, actual-use uplift, startup/idle tails, storage and network. [Current Modal units and billing](https://modal.com/pricing) were verified on 2026-10-24; no app invoice is available.

[CSV, receipt, complete operation log, hardware and validation/hash manifest](evidence/20261024-30m-public-candidate/) are committed with this draft. Raw HDF5 and RSS trace remain on private volume `hms-bigann:/streaming-recall/final-12c80decb094-c725fa3fe2f3419385a67469fb736f2a`; the validation manifest records their SHA-256. [Modal app](https://modal.com/apps/dcondrey/main/ap-BTHkkmhWY8nnDGlv2sux4r), call `fc-01M5PFWQEY583YYREYHXW6JX0C`.

An earlier attempt of this same candidate was externally cancelled at 590/1280 with `InputCancellation`; its issuer was not recorded. That partial run remains a failure. This was one bounded unchanged-configuration retry through a private deployed function. The original R32/L64 timeout and matched DiskANN memory failures above remain unchanged; no heldout queries were used, no standings were submitted, and the PR remains draft.
