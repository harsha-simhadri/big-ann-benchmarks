python install.py --neurips23track sparse    --algorithm nle
for algorithm in NLE-10 NLE
do
    for dataset in sparse-small sparse-1M sparse-full
    do
        python run.py --neurips23track sparse    --algorithm $algorithm --dataset $dataset
    done
done
