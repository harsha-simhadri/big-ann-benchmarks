params="
nprobe=1,quantizer_efSearch=4
nprobe=2,quantizer_efSearch=4
nprobe=4,quantizer_efSearch=4
nprobe=4,quantizer_efSearch=8
nprobe=8,quantizer_efSearch=4
nprobe=8,quantizer_efSearch=8
nprobe=8,quantizer_efSearch=16
nprobe=8,quantizer_efSearch=32
nprobe=16,quantizer_efSearch=16
nprobe=16,quantizer_efSearch=32
nprobe=16,quantizer_efSearch=64
nprobe=32,quantizer_efSearch=8
nprobe=32,quantizer_efSearch=32
nprobe=32,quantizer_efSearch=64
nprobe=32,quantizer_efSearch=128
nprobe=64,quantizer_efSearch=16
nprobe=64,quantizer_efSearch=32
nprobe=64,quantizer_efSearch=64
nprobe=64,quantizer_efSearch=128
nprobe=64,quantizer_efSearch=256
nprobe=128,quantizer_efSearch=32
nprobe=128,quantizer_efSearch=64
nprobe=128,quantizer_efSearch=128
nprobe=128,quantizer_efSearch=256
nprobe=128,quantizer_efSearch=512
nprobe=256,quantizer_efSearch=64
nprobe=256,quantizer_efSearch=128
nprobe=256,quantizer_efSearch=512
nprobe=512,quantizer_efSearch=256
nprobe=512,quantizer_efSearch=512
nprobe=1024,quantizer_efSearch=256
"

python  track1_baseline_faiss/baseline_faiss.py \
   --dataset bigann-dim-reduced-100M --indexfile data/track1_baseline_faiss/bigann-100M.IVF1M_2level_PQ64x4fsr.faissindex \
   --search --searchparams $params
