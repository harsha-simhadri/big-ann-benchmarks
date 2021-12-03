# Benchmarking GraphANN

This file describes the installation and configuration for running `big-ann-benchmarks` for `GraphANN`

## Installation

### Julia
Download and unpack julia.
```
wget --no-proxy  https://julialang-s3.julialang.org/bin/linux/x64/1.6/julia-1.6.3-linux-x86_64.tar.gz
tar -xvzf julia-1.6.3-linux-x86_64.tar.gz 
```

### Pyenv
Install pyenv and related dependencies
```
sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel
sudo curl https://pyenv.run | bash
```

### Path and env variable setup
Update path and define env variables by adding these to `~/.bashrc`
```
tee -a ~/.bashrc << EOF
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv virtualenv-init -)"


alias julia="$HOME/julia-1.6.3/bin/julia"
eval "$(pyenv init -)"

export PATH="$HOME/julia-1.6.3/bin/:$PATH"

export JULIA_EXCLUSIVE=1
export JULIA_NUM_THREADS=$(nproc)

export PYANN_ROOT=$HOME/GraphANN/contrib/PyANN/
EOF

exec $SHELL
```

### Download GraphANN
Clone the GraphANN repo
```
git clone https://github.com/hildebrandmw/GraphANN.jl.git GraphANN
```
Install the required packages by and precompile using `julia` command line
```
cd GraphANN
julia --project
# in julia terminal 
using Pkg; Pkg.instantiate();
using GraphANN
# exit julia terminal
exit() 
cd
```

### Download IPMICAP
Clone the ipmicap repo
```
git clone https://github.com/fractalsproject/ipmicap.git
cd ipmicap/
pip3 install -r requirements.txt
```



### Download big-ann-benchmarks
Clone the big-ann-benchmarks repo and checkout the `OPtANNe` branch
```
git clone https://github.com/harsha-simhadri/big-ann-benchmarks.git
cd big-ann-benchmarks/
git fetch origin pull/63/head:OPtANNe
git checkout OPtANNe
```
Install the python version needed and the requirements
```
pyenv update
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.12
pyenv local 3.8.12
pyenv global 3.8.12
pip3 install -r requirements_py38.txt
pip3 install --user julia
python -c "import julia; julia.install()"
```


## Running benchmarks
All the indexes and vectors files are located in `/mnt/data/competition_indexes/`. The `algos.yaml` file contains all the paths, and will pick the index and vectors files for each dataset from `/mnt/data/`
The files will be copied to the PMem devices `/mnt/pm0/public` and `/mnt/pm1/public`. The vectors will then by loaded into DRAM, and index will be memory mapped in place and accessed using PMem AppDirect mode.

### Power caputure
Run the following command in a separate window or tmux session to set the power measurement server going.
```
sudo /home/tstbigann/.pyenv/shims/python ipmicap.py --dcmi-power --ip 192.168.0.100 --username ADMIN --password YEGAGYXJNM --listen 14118 --sessions
```

### Benchmark runs
The search works using `search_window_size` parameter. The `algos.yaml` file contains the parameter values needed to get 90% recall@10 values for `bigann-1B`, `msspacev-1B`, `deep-1B`, `msturing-1B`, and `text2image-1B`. The machine is preconfigured to use 1GB hugepages for best perforamnce.
Benchmark runs with power canpture can be performed by running the following commands.
```
python run.py --algorithm graphann --t3 --nodocker --dataset bigann-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset msspacev-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset deep-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset msturing-1B --power-capture 192.168.0.121:14118:10
python run.py --algorithm graphann --t3 --nodocker --dataset text2image-1B --power-capture 192.168.0.121:14118:10
```




