
# Explanation of NVidia CUANNS_MULTIGPU Anomalies

From yongw@nvidia.com:

We don't have any caching mechanism in our software implementation, for both cuanns_ivfpq and cuanns_multigpu.

The observation is that the first run is slower.

There are 2 reasons:

(1) We use CUDA for GPU programming. The first time a CUDA related function gets called, driver will do some initialization work. This is a one-time overhead.

(2) When there is no workload, GPU is running at low clock rate. Then when the workload occurs, GPU needs some warm-up time to reach normal running clock rate. For the first run, it's very likely that GPU has not reached practical clock rate since the status is just changed from no workload to having workload.

We suggest using some random queries for warm-up before the first run, so both of these can be avoided.
