# Hanns
Our OOD track solution consists of a vamana index, a mutil-scale spatial clustering index, and a layout-optimized quantization acceleration index.
The entire retrieval process is from coarse to fine. First, the vamana index is used to quick find the nearst clusters. Then, within these clusters, the quantization-accelerated index is uesed for fast distance comparisons to identify the coarsely ranked candidates. Finally, SIMD instructions are used to re-rank these candidates, and the final results are returned.
# Performance
![ood-track](https://github.com/AndrewHYu/Hanns/blob/main/pic/text2image-10M.png)
