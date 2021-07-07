# Running the Faiss GPU baseline

The script here is based on the T1 baseline, so please take a look at [the Track 1 baseline](../track1_baseline_faiss/README.md) first. 

## Installing software 

See [this doc](../track1_baseline_faiss/README.md#installing-software) but instead of installing faiss-cpu, use: 

```
conda install -c pytorch faiss-gpu cudatoolkit=10.2
```

## How to use the GPU

This script focuses on exploiting the GPU for coarse quantization. 
Therefore, it is suitable for large codebooks. 

The GPU can be used in the following phases: 

- training: `--train_with_gpu` will move the training of the coarse quantizer to GPU

- vector adding to the index: `--quantizer_on_gpu_add --` will do the adding on GPU

- search: `--parallel_mode 3  --quantizer_on_gpu_search` will do coarse quantization on GPU at search time. 

## Building the index and searching 

The following command runs the index constuction and evaluates the search performance: 

```bash
python track3_baseline_faiss/gpu_baseline_faiss.py --dataset deep-100M \
         --indexkey IVF65536,SQ8 
         --train_on_gpu \
         --build --quantizer_on_gpu_add --add_splits 30 \
         --search \
         --searchparams nprobe={1,4,16,64,256}   \
         --parallel_mode 3  --quantizer_on_gpu_search
```

Example logs [without GPU](https://gist.github.com/mdouze/9e000be47c499f79aaec0166365ef654) and [with GPU](https://gist.github.com/mdouze/cd14c802b924299aa2a92db6e05df857) at search time.


