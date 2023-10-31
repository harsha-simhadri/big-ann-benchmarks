set -e

export PYTHONPATH=.




function run_on () {
    local sbatch_opt="$1"
    shift
    local name=$1
    shift
    local torun=" $@ "

    if [ -e slurm_scripts/$name.sh ]; then
        echo "script" slurm_scripts/$name.sh exists
        exit 1
    fi

    echo -n $name "  "

    echo $@ > slurm_scripts/$name.sh

    sbatch $sbatch_opt \
           -J $name -o logs/$name.log \
           --wrap "bash slurm_scripts/$name.sh"

}


function run_on_1gpu () {
    run_on "--gres=gpu:1 --ntasks=1 --time=30:00:00 --cpus-per-task=20
           --partition=devlab --mem=64g --nodes=1 " "$@"
}

function run_on_1gpu_learnlab () {
    run_on "--gres=gpu:1 --ntasks=1 --time=30:00:00 --cpus-per-task=20
           --partition=learnlab --mem=64g --nodes=1 " "$@"
}
function run_on_half_machine () {
    run_on "--gres=gpu:1 --ntasks=1 --time=30:00:00 --cpus-per-task=40
           --partition=learnlab --mem=256g --nodes=1 " "$@"
}

function run_on_2gpu_ram256 () {
    run_on "--gres=gpu:2 --ntasks=1 --time=30:00:00 --cpus-per-task=20
           --partition=learnlab --mem=256g --nodes=1 " "$@"
}



##############################################################
# Small scale experiments to evaluate effect of 2-level clustering
##############################################################

# compare 2-level 65k clustering index and regular one

basedir=data/track1_baseline_faiss


if false; then

dsname=bigann-10M


run_on_1gpu $dsname.IVF65k_HNSW.a \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.faissindex \
        --indexkey PCAR64,IVF65536_HNSW32,Flat --maxtrain $((65536 * 50)) \
        --search --train_on_gpu


run_on_1gpu $dsname.IVF65k_2level_HNSW.b \
     python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.IVF65k_2level_HNSW.faissindex \
        --indexkey PCAR64,IVF65536_HNSW32,Flat --maxtrain $((65536 * 50)) \
        --two_level_clustering \
        --search




# for efC in 50 100 200; do

for efC in 400 800; do

run_on_1gpu $dsname.IVF65k_HNSW_efC$efC.b \
     python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.IVF65k_HNSW_efC$efC.faissindex \
        --indexkey PCAR64,IVF65536_HNSW32,Flat --maxtrain $((65536 * 50)) \
        --quantizer_efConstruction $efC \
        --build --search --train_on_gpu

done



# for efS in 20 40 80; do
for efS in 160 320; do

name=$dsname.IVF65k_2level_HNSW_efC200_efS$efS

run_on_1gpu $name.a \
     python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$name.faissindex \
        --indexkey PCAR64,IVF65536_HNSW32,Flat --maxtrain $((65536 * 50)) \
        --quantizer_efConstruction 200 \
        --quantizer_add_efSearch $efS \
        --two_level_clustering \
        --build --search

done




##############################################################
# Experiments on scale 100M
##############################################################

# .a: build
# .c: eval w 32 threads

# start with least problematic datasets  (no IP search, no range search)
# msspace-1B may need to redo experiments because of ties in distance computations
for dsname in bigann-100M deep-100M msturing-100M msspacev-100M; do

    for nc in 256k 1M; do

        case $nc in
        1M) ncn=$((1<<20)) ;;
        256k) ncn=$((1<<18)) ;;
        esac

        name=$dsname.IVF${nc}_2level_PQ32

        run_on_half_machine $name.c \
            python -u track1_baseline_faiss/baseline_faiss.py \
                --dataset $dsname --indexfile $basedir/$name.faissindex \
                --indexkey OPQ32_128,IVF${ncn}_HNSW32,PQ32 \
                --maxtrain 100000000 \
                --quantizer_efConstruction 200 \
                --quantizer_add_efSearch 80 \
                --two_level_clustering \
                --search --searchthreads 32 \
                --maxRAM 256

        name=$dsname.IVF${nc}_2level_PQ64x4fsr

        run_on_half_machine $name.c \
            python -u track1_baseline_faiss/baseline_faiss.py \
                --dataset $dsname --indexfile $basedir/$name.faissindex \
                --indexkey OPQ64_128,IVF${ncn}_HNSW32,PQ64x4fsr \
                --maxtrain 100000000 \
                --quantizer_efConstruction 200 \
                --quantizer_add_efSearch 80 \
                --two_level_clustering \
                --search --searchthreads 32 \
                --maxRAM 256

    done

done


##############################################################
# Experiments on scale 1B
##############################################################

# .a: build
# .b: eval w 32 threads
# .c: redo bigann eval
# .d: with ssnpp, forgot to build...
# .f: redo t2i 64x4 (eval only)

# start with least problematic datasets  (no IP search, no range search)
# msspace-1B may need to redo experiments because of ties in distance computations

# for dsname in bigann-1B deep-1B msturing-1B msspacev-1B; do
# for dsname in bigann-1B; do
# for dsname in ssnpp-1B; do
#     for nc in 1M 4M; do

fi

for dsname in text2image-1B; do

    for nc in 1M; do

        case $nc in
        1M) ncn=$((1<<20)) ;;
        4M) ncn=$((1<<22)) ;;
        esac

        if false ;then

        name=$dsname.IVF${nc}_2level_PQ32

        run_on_half_machine $name.e \
            python -u track1_baseline_faiss/baseline_faiss.py \
                --dataset $dsname --indexfile $basedir/$name.faissindex \
                --indexkey OPQ32_128,IVF${ncn}_HNSW32,PQ32 \
                --maxtrain 100000000 \
                --quantizer_efConstruction 200 \
                --quantizer_add_efSearch 80 \
                --two_level_clustering \
                --build --search --searchthreads 32 \
                --maxRAM 256

        fi
        name=$dsname.IVF${nc}_2level_PQ64x4fsr

        run_on_half_machine $name.g \
            python -u track1_baseline_faiss/baseline_faiss.py \
                --dataset $dsname --indexfile $basedir/$name.faissindex \
                --indexkey OPQ64_128,IVF${ncn}_HNSW32,PQ64x4fsr \
                --maxtrain 100000000 \
                --quantizer_efConstruction 200 \
                --quantizer_add_efSearch 80 \
                --two_level_clustering \
                --search --searchthreads 32 \
                --maxRAM 256 --autotune_max nprobe:513


    done

done

if false; then

# speed up construction

dsname=ssnpp-1B
nc=1M
ncn=$((1<<20))

name=$dsname.IVF${nc}_2level_aefS40_PQ32

un_on_half_machine $name.d \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$name.faissindex \
        --indexkey OPQ32_128,IVF${ncn}_HNSW32,PQ32 \
        --maxtrain 100000000 \
        --quantizer_efConstruction 200 \
        --quantizer_add_efSearch 40 \
        --add_splits 30 \
        --two_level_clustering \
        --build --search --searchthreads 32 \
        --maxRAM 256


# find a way to not OOM during autotune

function ssnpp_no_OOM () {
    local key=$1
    shift
    dsname=ssnpp-1B
    nc=1M
    ncn=$((1<<20))

    name=$dsname.IVF${nc}_2level_PQ32.search.$key

    run_on_half_machine $name.a \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$dsname.IVF${nc}_2level_PQ32.faissindex \
            --search --searchthreads 32 \
            --maxRAM 256 "$@"
}

ssnpp_no_OOM radius75000 --radius 75000
ssnpp_no_OOM radius80000 --radius 80000
ssnpp_no_OOM radius60000 --radius 60000
ssnpp_no_OOM maxNP1024  --autotune_max nprobe:1025
ssnpp_no_OOM maxEFS256  --autotune_max quantizer_efSearch:257



##############################################################
# Experiments with 64 bytes per vector
##############################################################

# .a: initial run and build
# .b: re-run to get more detailed search stats


for dsname in bigann-1B deep-1B msturing-1B msspacev-1B; do
    nc=1M
    ncn=$((1<<20))

    name=$dsname.IVF${nc}_2level_PQ64

    run_on_half_machine $name.b \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$name.faissindex \
            --indexkey OPQ64_128,IVF${ncn}_HNSW32,PQ64 \
            --maxtrain 100000000 \
            --quantizer_efConstruction 200 \
            --quantizer_add_efSearch 80 \
            --two_level_clustering \
            --search --searchthreads 32 \
            --maxRAM 256

    name=$dsname.IVF${nc}_2level_PQ128x4fsr

    run_on_half_machine $name.b \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$name.faissindex \
            --indexkey OPQ128_128,IVF${ncn}_HNSW32,PQ128x4fsr \
            --maxtrain 100000000 \
            --quantizer_efConstruction 200 \
            --quantizer_add_efSearch 80 \
            --two_level_clustering \
            --search --searchthreads 32 \
            --maxRAM 256

done



##############################################################
# 10M scale exeperiment for text2image
##############################################################

dsname=text2image-10M


for nc in 16k 65k; do

    case $nc in
    16k) ncn=$((1<<14)) ;;
    65k) ncn=$((1<<16)) ;;
    esac

    # baseline
    key=IVF$nc
    run_on_1gpu $dsname.$key.d \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
            --indexkey IVF${ncn},Flat --maxtrain $((ncn * 4 * 50)) \
            --build --search --train_on_gpu

    # loss due to 2-level
    key=IVF${nc}_2level
    run_on_1gpu $dsname.$key.d \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
            --indexkey IVF${ncn},Flat --maxtrain $((ncn * 4 * 50)) \
            --build --search --two_level_clustering

    # loss due to HNSW
    key=IVF${nc}_HNSW
    run_on_1gpu $dsname.$key.d \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
            --indexkey IVF${ncn}_HNSW32,Flat --maxtrain $((ncn * 4 * 50)) \
            --quantizer_efConstruction 200 \
            --quantizer_add_efSearch 80 \
            --build --search --train_on_gpu

    # loss due to 2-level + HNSW
    key=IVF${nc}_2level_HNSW
    run_on_1gpu $dsname.$key.d \
        python -u track1_baseline_faiss/baseline_faiss.py \
            --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
            --indexkey IVF${ncn}_HNSW32,Flat --maxtrain $((ncn * 4 * 50)) \
            --quantizer_efConstruction 200 \
            --quantizer_add_efSearch 80 \
            --build --search --two_level_clustering

done

# evaluate various IVF codes

ncn=16384


key=IVF16k,SQ8
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR200,IVF16384,SQ8 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu

key=IVF16k,SQ8_nores
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR200,IVF16384,SQ8 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu --by_residual 0

key=IVF16k,SQ6
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR200,IVF16384,SQ6 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu

key=IVF16k,SQ6_nores
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR200,IVF16384,SQ6 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu --by_residual 0


key=IVF16k,SQ8_PQ32
run_on_1gpu_learnlab $dsname.$key.a \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey OPQ32_128,IVF16384,PQ32 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu

key=IVF16k,SQ8_PQ32_nores
run_on_1gpu_learnlab $dsname.$key.a \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey OPQ32_128,IVF16384,PQ32 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu --by_residual 0


key=IVF16k,SQ4
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR200,IVF16384,SQ4 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu

key=IVF16k,SQ4_PCAR100
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey PCAR100,IVF16384,SQ4 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu

key=IVF16k,RR192_PQ32
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR192,IVF16384,PQ32 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu

key=IVF16k,RR192_PQ32x12
run_on_1gpu_learnlab $dsname.$key.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey RR192,IVF16384,PQ32x12 --maxtrain $((ncn * 4 * 50)) \
        --build --search --train_on_gpu


dsname=text2image-10M

key=IVF16k,PQ48
run_on_1gpu $dsname.$key.c \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey OPQ48_192,IVF16384,PQ48 --maxtrain $((65536 * 50)) \
        --search --train_on_gpu

key=IVF16k,PQ64
run_on_1gpu $dsname.$key.c \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey OPQ64_192,IVF16384,PQ64 --maxtrain $((65536 * 50)) \
        --search --train_on_gpu


dsname=text2image-10M
key=IVF16k,PQ48
run_on_1gpu $dsname.$key.c \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey OPQ48_192,IVF16384,PQ48 --maxtrain $((65536 * 50)) \
        --search --train_on_gpu



## try out additive quants


export PYTHONPATH=/private/home/matthijs/faiss_versions/faiss_add_quant_search/build/faiss/python/build/lib:.
dsname=text2image-10M
for key in IVF16384,RQ32x8_Nfloat  IVF16384,RQ31x8_Nqint8 IVF16384,LSQ32x8_Nfloat IVF16384,LSQ31x8_Nqint8 ; do
run_on_1gpu $dsname.$key.g \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.$key.faissindex \
        --indexkey $key --maxtrain $((65536 * 50))  \
        --search --build # --train_on_gpu

done


##############################################################
# GPU based search  (T3)
##############################################################

basedir=data/track3_baseline_faiss
dsname=deep-1B

#.a: run with a too tight limit in RAM
#.b: increased RAM

key=IVF262k,PQ8
run_on_2gpu_ram256 T3.$dsname.$key.b \
    python -u track3_baseline_faiss/gpu_baseline_faiss.py \
        --maxRAM 256 \
        --dataset  $dsname --indexkey IVF$((1<<18)),SQ8 \
        --build \
        --searchparams nprobe={1,4,16,64,256,1024} \
        --train_on_gpu  --quantizer_on_gpu_add  \
        --indexfile $basedir/$dsname.$key.faissindex \
        --add_splits 30 \
        --search \
        --parallel_mode 3  --quantizer_on_gpu_search


key=IVF1M,PQ8
run_on_2gpu_ram256 T3.$dsname.$key.b \
    python -u track3_baseline_faiss/gpu_baseline_faiss.py \
        --maxRAM 256 \
        --dataset  $dsname --indexkey IVF$((1<<20)),SQ8 \
        --build \
        --searchparams nprobe={1,4,16,64,256,1024} \
        --train_on_gpu  --quantizer_on_gpu_add  \
        --indexfile $basedir/$dsname.$key.faissindex \
        --add_splits 30 \
        --search \
        --parallel_mode 3  --quantizer_on_gpu_search


fi