
# Explanation of NVidia CUANNS_MULTIGPU Anomalies

From yongw@nvidia.com:

"We don’t have any caching mechanism in our software implementation, for both cuanns_ivfpq and cuanns_multigpu.

The hardware (A100 GPU) has cache, but we suspect it won’t have much impact since the size of visited data for each run should be larger than the hardware cache size.

...We suggest sending some random queries before the first run.

The reason is that many hardware, including and CPU and GPU, is running at low frequency when there is no workload. They need some warm-up time to run at practical frequency.

And we use CUDA for GPU programming. CUDA context is initialized when first related function gets called. It’s a one-time overhead but it might not be trivial. So, using some random queries before first run will avoid counting this overhead."

