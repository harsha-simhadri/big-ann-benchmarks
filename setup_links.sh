#!/bin/sh

DATASET_HOME=/raid/workspace/dataset
INDEX_HOME=/raid/workspace/anaruse/libcuann/models

mkdir -p data/indices/t3/CuannsIvfpq 2> /dev/null

#
cd data
if [ ! -e bigann ]; then
    ln -s ${DATASET_HOME}/bigann-1B bigann
fi
if [ ! -e deep1b ]; then
    ln -s ${DATASET_HOME}/deep-1B deep1b
fi
if [ ! -e MSSPACEV1B ]; then
    ln -s ${DATASET_HOME}/msspacev-1B MSSPACEV1B
fi
if [ ! -e MSTuringANNS ]; then
    ln -s ${DATASET_HOME}/msturing-1B MSTuringANNS
fi
if [ ! -e text2image1B ]; then
    ln -s ${DATASET_HOME}/text2image-1B text2image1B
fi

#
cd indices/t3/CuannsIvfpq
if [ ! -e bigann-1B.cluster_250000.pq_64.5_bit ]; then
    ln -s ${INDEX_HOME}/BIGANN-1B-uint8-1000000000x128.cluster_250000.pq_64.5_bit bigann-1B.cluster_250000.pq_64.5_bit
fi
if [ ! -e deep-1B.cluster_250000.pq_64.5_bit ]; then
    ln -s ${INDEX_HOME}/DEEP-1B-float32-1000000000x96.cluster_250000.pq_64.5_bit deep-1B.cluster_250000.pq_64.5_bit
fi
if [ ! -e msspacev-1B.cluster_500000.pq_64.5_bit ]; then
    ln -s ${INDEX_HOME}/MS-SPACEV-1B-int8-1000000000x100.cluster_500000.pq_64.5_bit msspacev-1B.cluster_500000.pq_64.5_bit
fi
if [ ! -e msturing-1B.cluster_250000.pq_64.5_bit ]; then
    ln -s ${INDEX_HOME}/MS-Turing-ANNS-1B-float32-1000000000x100.cluster_250000.pq_64.5_bit msturing-1B.cluster_250000.pq_64.5_bit
fi
if [ ! -e text2image-1B.cluster_500000.pq_72.8_bit ]; then
    ln -s ${INDEX_HOME}/T2I-1B-float32-1000000000x200.cluster_500000.pq_72.8_bit text2image-1B.cluster_500000.pq_72.8_bit
fi

