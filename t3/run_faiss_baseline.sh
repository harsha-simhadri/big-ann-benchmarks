#!/bin/bash

# Choose a database
DBASE="msspacev" # msturing msspacev deep bigann text2image

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
        --searchparams nprobe={1,2,4,16,32,64,128,256} \
        --parallel_mode 3 \
        --min_test_duration 10 \
        --quantizer_on_gpu_search 

fi

echo "Done."
