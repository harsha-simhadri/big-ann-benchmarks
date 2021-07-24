#!/bin/bash

# Choose a database
DBASE="msturing" # msturing msspacev deep bigann(sift) text2image

# Choose a size
SIZE="1B"

# Choose an index strategy
KEY="IVF1048576,SQ8"
#KEY="IVF65536,SQ8" - Use this one for smaller test sets

# What to do
BUILD=0
SEARCH=1

if [ "$BUILD" -eq "1" ]; then

    echo "Building index for $DBASE-$SIZE"
    PYTHONPATH="." python -u  t3/gpu_baseline_faiss.py \
        --dataset "$DBASE-$SIZE" \
        --build \
        --train_on_gpu \
        --quantizer_on_gpu_add --train_on_gpu --indexkey "$KEY" --buildthreads 1 \
        --indexfile "../data/$DBASE-$SIZE.$KEY.faissindex" 
fi

if [ "$SEARCH" -eq "1" ]; then

    echo "Searching on $DBASE-$SIZE"
    PYTHONPATH="." python -u  t3/gpu_baseline_faiss.py \
        --dataset "$DBASE-$SIZE" \
        --indexfile "data/$DBASE-$SIZE.$KEY.faissindex" \
        --search \
        --searchparams nprobe={32,37,42,47,52,57,62,64} \
        --parallel_mode 3 \
        --min_test_duration 10 \
        --quantizer_on_gpu_search 

fi

# The following search parameters were useful locating the 2K QPS recall@10 threshold
#        --searchparams nprobe={1,2,4,16,32,64,128,256} \
#        --searchparams nprobe={64,70,80,90,100,110,120,128} \
#        --searchparams nprobe={128,140,160,180,200,220,240,256} \
#        --searchparams nprobe={32,37,42,47,52,57,62,64} \

echo "Done."
