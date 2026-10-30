# NeurIPS Big ANN: VIBE-aligned zero-step HingeZero run

Author: David Duffy / HingeZero. Prepared 30 October 2026.

## Why this is a separate run

The recorded VIBE result (98.617% recall@100 at 5,010.826592 QPS on its fastest shared runner) came from **VIBE `yi-128-ip`**, using a `fit_ood`-learned **32,768-vector** support pool, FAISS `IndexFlatIP`, and a native HingeZero witness/ranking kernel with **zero refinement steps**. That score does **not** belong to NeurIPS Big ANN `openai-100K`. Neither the training-label support selection nor the score should be copied without verifying the target benchmark permits and supplies the same learning interface.

The current [Big ANN pull request #352](https://github.com/harsha-simhadri/big-ann-benchmarks/pull/352) has a different measured baseline: C++ v3, four threads, eight refinement steps, IVF/PQ with expansion, recall@10 0.914250 and 165.889364 QPS on `openai-100K`.

## Alignment experiment: zero-step / single core / complete corpus

The existing native C++ v3 code supports zero refinement steps without changing its source. With `--steps 0 --rounds 0`, HingeZero still verifies the original stored states and original-query metric ranking; it does **not** run a recurrent refinement or extra candidate-expansion pass. A single CPU core is selected by `--threads 1`. The existing IVF/PQ candidate index covers **all 100,000 source vectors**. This is the nearest *permitted full-corpus analogue* to VIBE's zero-step decision flow, **not** an exact transplant of VIBE's learned-support method.

From the root of this fork, after installing the requirements and obtaining the official dataset files through the benchmark's documented setup:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python run_hingezero_cpp_v3.py --dataset openai-100K \
  --steps 0 --rounds 0 --threads 1 --batch-size 32 \
  --nprobe 32 --candidates 512 --expansion-candidates 0
```

This invokes the existing official runner via `run_hingezero_cpp_v3.py`, queries **every public query**, records provenance and HDF5 results, and scores recall@10 against `openai-100K` ground truth only **after** retrieval. Check `hz_steps=0`, `hz_rounds=0`, `native_threads=1`, `failed_checks=0`, and the run's actual recall/QPS before registering a new official method configuration.

The default existing v3 submission and its historical measured result remain untouched. The alternate `hingezero_cpp_zero_steps_v3` configuration is now registered under `openai-100K` in `algos-2021.yaml` so the existing pull request exposes it for organizer evaluation. **No NeurIPS score is claimed for this unrun configuration.** Maintainer acceptance and an official reference-hardware rerun remain pending.

## Methodological limitations

- VIBE searched 32,768 training-label-selected vectors; this experiment searches an IVF/PQ index built from the full `openai-100K` corpus and reranks its candidates. Search speed and recall can be very different.
- NeurIPS recorded recall@10; VIBE reported recall@100. Compare like with like, not raw percentages.
- Zero refinement does not disable witness identity checks; it avoids recurrent query reconstruction.
- Candidate retrieval is provided by FAISS. HingeZero here performs deterministic state/identity verification and original-metric reranking. The isolated benefit of HingeZero versus FAISS must be established separately in controlled ablations.
