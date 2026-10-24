# HMS streaming checks on current main

Engine commit: `12c80decb094d57ee13ba187a01bf1de8788ca2f`. Harness commit: `89a3abaafa63dda46b94b308bdf039e699841b3b`. The engine's hosted CI run `40070371238` passed. Both full runs used the official public queries, runbooks, one replay per configuration, eight schedulable CPUs, and an 8 GiB Modal memory setting. Modal's eight physical CPUs and storage differ from the official Azure D8lds v5 evaluation VM, so these timings are diagnostic and are not compared with published competitors.

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
