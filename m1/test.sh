#!/bin/bash

set -e
set -x

## faiss sparse

# Launch with just bash
#cd .. && docker run --entrypoint /bin/bash --platform linux/amd64 -it -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/benchmark:/home/app/benchmark -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/data:/home/app/data -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/results:/home/app/results -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/neurips23:/home/app/neurips23 neurips23-filter-faiss

## after bash:  python3 -m run_algorithm.py --dataset random-filter-s --algorithm faiss --module neurips23.filter.faiss.faiss --constructor FAISS --runs 1 --count 10 --neurips23track filter '["euclidean", {"indexkey": "IVF1024,SQ8"}]' '[{"nprobe": 1}]' '[{"nprobe": 2}]' '[{"nprobe": 4}]'

# WORKS! - 
cd .. && docker run --platform linux/amd64 -it -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/benchmark:/home/app/benchmark -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/data:/home/app/data -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/results:/home/app/results -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/neurips23:/home/app/neurips23 neurips23-filter-faiss --dataset random-filter-s --algorithm faiss --module neurips23.filter.faiss.faiss --constructor FAISS --runs 1 --count 10 --neurips23track filter '["euclidean", {"indexkey": "IVF1024,SQ8"}]' '[{"nprobe": 1}]' '[{"nprobe": 2}]' '[{"nprobe": 4}]'

# WITH TRACE! - cd .. && docker run -e QEMU_STRACE=1 --platform linux/amd64 -it -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/benchmark:/home/app/benchmark -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/data:/home/app/data -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/results:/home/app/results -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/neurips23:/home/app/neurips23 neurips23-filter-faiss --dataset random-filter-s --algorithm faiss --module neurips23.filter.faiss.faiss --constructor FAISS --runs 1 --count 10 --neurips23track filter '["euclidean", {"indexkey": "IVF1024,SQ8"}]' '[{"nprobe": 1}]' '[{"nprobe": 2}]' '[{"nprobe": 4}]'

## linscan

#args ['--dataset', 'sparse-small', '--algorithm', 'linscan', '--module', 'neurips23.sparse.linscan.linscan', '--constructor', 'Linscan', '--runs', '5', '--count', '10', '--neurips23track', 'sparse', '["ip", {}]', '[{"budget": 1}]', '[{"budget": 0.5}]', '[{"budget": 0.4}]', '[{"budget": 0.3}]', '[{"budget": 0.25}]', '[{"budget": 0.2}]', '[{"budget": 0.15}]', '[{"budget": 0.1}]', '[{"budget": 0.075}]', '[{"budget": 0.05}]']

# platform flag - cd .. && docker run --platform linux/amd64 -it -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/benchmark:/home/app/benchmark -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/data:/home/app/data -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/results:/home/app/results -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/neurips23:/home/app/neurips23  neurips23-sparse-linscan '--dataset' 'sparse-small' '--algorithm' 'linscan' '--module' 'neurips23.sparse.linscan.linscan' '--constructor' 'Linscan' '--runs' '5' '--count' '10' '--neurips23track' 'sparse' '["ip", {}]' '[{"budget": 1}]', '[{"budget": 0.5}]' '[{"budget": 0.4}]' '[{"budget": 0.3}]' '[{"budget": 0.25}]', '[{"budget": 0.2}]' '[{"budget": 0.15}]' '[{"budget": 0.1}]' '[{"budget": 0.075}]' '[{"budget": 0.05}]'

# WORKS! - cd .. && docker run -it -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/benchmark:/home/app/benchmark -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/data:/home/app/data -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/results:/home/app/results -v /Users/cuongwilliams/Projects/BigANN/big-ann-benchmarks/neurips23:/home/app/neurips23  neurips23-sparse-linscan '--dataset' 'sparse-small' '--algorithm' 'linscan' '--module' 'neurips23.sparse.linscan.linscan' '--constructor' 'Linscan' '--runs' '5' '--count' '10' '--neurips23track' 'sparse' '["ip", {}]' '[{"budget": 1}]' '[{"budget": 0.5}]' '[{"budget": 0.4}]' '[{"budget": 0.3}]' '[{"budget": 0.25}]' '[{"budget": 0.2}]' '[{"budget": 0.15}]' '[{"budget": 0.1}]' '[{"budget": 0.075}]' '[{"budget": 0.05}]'
