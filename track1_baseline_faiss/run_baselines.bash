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

function run_on_half_machine () {
    run_on "--gres=gpu:1 --ntasks=1 --time=30:00:00 --cpus-per-task=40
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

# start with least problematic datasets  (no IP search, no range search)
# msspace-1B may need to redo experiments because of ties in distance computations

# for dsname in bigann-1B deep-1B msturing-1B msspacev-1B; do
for dsname in bigann-1B; do
    for nc in 1M 4M; do


        case $nc in
        1M) ncn=$((1<<20)) ;;
        4M) ncn=$((1<<22)) ;;
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

        run_on_half_machine $name.a \
            python -u track1_baseline_faiss/baseline_faiss.py \
                --dataset $dsname --indexfile $basedir/$name.faissindex \
                --indexkey OPQ64_128,IVF${ncn}_HNSW32,PQ64x4fsr \
                --maxtrain 100000000 \
                --quantizer_efConstruction 200 \
                --quantizer_add_efSearch 80 \
                --two_level_clustering \
                --build --search --searchthreads 32 \
                --maxRAM 256


    done

done

fi

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




if false; then


##############################################################
# 10M scale exeperiment for max IP search
##############################################################

dsname=text2image-10M



run_on_1gpu $dsname.IVF65k_HNSW.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.faissindex \
        --indexkey PCAR64,IVF65536_HNSW32,Flat --maxtrain $((65536 * 50)) \
        --quantizer_efConstruction 200 \
        --quantizer_add_efSearch 80 \
        --build --search --train_on_gpu


run_on_1gpu $dsname.IVF65k_2level_HNSW.b \
     python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.IVF65k_2level_HNSW.faissindex \
        --indexkey PCAR64,IVF65536_HNSW32,Flat --maxtrain $((65536 * 50)) \
        --quantizer_efConstruction 200 \
        --quantizer_add_efSearch 80 \
        --two_level_clustering \
        --build --search


run_on_1gpu $dsname.IVF65k_HNSW_PQ32.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.faissindex \
        --indexkey OPQ128_32,IVF65536_HNSW32,PQ32 --maxtrain $((65536 * 50)) \
        --quantizer_efConstruction 200 \
        --quantizer_add_efSearch 80 \
        --build --search --train_on_gpu


run_on_1gpu $dsname.IVF65k_HNSW_PQ32_nores.b \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.faissindex \
        --indexkey OPQ128_32,IVF65536_HNSW32,PQ32 --maxtrain $((65536 * 50)) \
        --quantizer_efConstruction 200 \
        --quantizer_add_efSearch 80 \
        --build --search --train_on_gpu --by_residual 0




run_on_1gpu $dsname.IVF16k.a \
    python -u track1_baseline_faiss/baseline_faiss.py \
        --dataset $dsname --indexfile $basedir/$dsname.IVF16k.faissindex \
        --indexkey IVF16384,Flat --maxtrain $((65536 * 50)) \
        --build --search --train_on_gpu
fi
