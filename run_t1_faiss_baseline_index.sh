python -u track1_baseline_faiss/baseline_faiss.py --dataset bigann-dim-reduced-100M \
    --indexkey OPQ64_128,IVF1048576_HNSW32,PQ64x4fsr \
    --maxtrain 10000000 \
    --two_level_clustering \
    --build \
    --add_splits 30 \
    --indexfile data/track1_baseline_faiss_dim_reduction/bigann-100M.IVF1M_2level_PQ64x4fsr.faissindex \
    --quantizer_efConstruction 200 \
    --quantizer_add_efSearch 80


