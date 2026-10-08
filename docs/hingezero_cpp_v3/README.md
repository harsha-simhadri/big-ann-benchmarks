# HingeZero C++ v3

Author: David Duffy / HingeZero.

C++17/OpenMP recurrence, witness and exact original-query scoring, with batched FAISS IVF/PQ lookup and a read-only original-vector bank. Python supplies dataset and official-runner integration. No softmax.

The corrected lookup requests enough results to exclude retained seeds and admit up to 256 additional candidates. The submitted local full run completed 20,000 public queries against all 100,000 OpenAI vectors, using 512 seeds, 256 new candidates per query, eight HingeZero steps, four threads and batches of 32. Recall@10 was 0.91425, throughput 165.889364 queries/second and search time 120.562280 seconds. These are author results on local hardware, not organizer-certified scores or billion-scale measurements.

Zero reported witness failures and seed-score regressions; 260,000 witness checks and 200,000 output-record checks. There were 20,000 retention events and zero retention commits. The port and lookup changed together, so these results do not isolate a recurrence benefit or a language-only speedup.

The source native.cpp SHA-256 is 763c2e9637f11caaa827a094a0c8e666151f1a14bb54ae987c657f918582a10f. The reference Python core SHA-256 is dd4c7e82c9823ea6c69b972113ef6a3a132d152d6b319551658fe00333e7bfa8.

## Reproduction

Build: `docker build -f install/Dockerfile.hingezero_cpp_v3 -t billion-scale-benchmark-hingezero_cpp_v3 .`

Official entry: `python run.py --algorithm hingezero_cpp_full_v3 --dataset openai-100K --count 10 --runs 1`

Convenience runner: `python run_hingezero_cpp_v3.py --dataset openai-100K`

Only the measured full-mode configuration is registered here. Existing v2 comparisons and records are preserved separately. Reports and the completed official HDF5 are copied from the author's existing run; no queries are run during submission. Ground truth is used only after retrieval for scoring.

The native library is compiled for the runtime CPU with -O3, OpenMP and contraction disabled, without fast-math. No precompiled library is committed. NumPy and C++ floating-point reduction orders can differ. This adapter supports static dense k-NN datasets; its in-memory IVF/PQ index has a memory guard.
