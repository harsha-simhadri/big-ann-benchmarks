FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libcpprest-dev python3.10
# mkl
RUN DEBIAN_FRONTEND=noninteractive apt install -y intel-mkl
RUN update-alternatives --set libblas.so-x86_64-linux-gnu /usr/lib/x86_64-linux-gnu/libmkl_rt.so 
RUN update-alternatives --set liblapack.so-x86_64-linux-gnu /usr/lib/x86_64-linux-gnu/libmkl_rt.so
ENV MKLROOT=/usr/lib/x86_64-linux-gnu
ENV LD_PRELOAD=/lib/x86_64-linux-gnu/libmkl_def.so:/lib/x86_64-linux-gnu/libmkl_avx2.so:/lib/x86_64-linux-gnu/libmkl_core.so:/lib/x86_64-linux-gnu/libmkl_intel_lp64.so:/lib/x86_64-linux-gnu/libmkl_intel_thread.so:/lib/x86_64-linux-gnu/libiomp5.so
# swig
RUN apt update && apt install -y wget swig
# cmake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.26.5/cmake-3.26.5-linux-x86_64.sh
RUN bash cmake-3.26.5-linux-x86_64.sh --skip-license --prefix=/usr/local

WORKDIR /opt
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3 && \
    rm -r Miniconda3-latest-Linux-x86_64.sh

# conda
WORKDIR /home/app
ENV PATH /opt/miniconda3/bin:$PATH
RUN pip install --upgrade pip && \
    conda update -n base -c defaults conda && \
    conda create -n utokyo python=3.10 && \
    conda init && \
    echo "conda activate utokyo" >> ~/.bashrc
SHELL [ "conda", "run", "-n", "utokyo", "/bin/bash", "-c" ]
ENV CONDA_DEFAULT_ENV utokyo && \
    PATH /opt/miniconda3/envs/utokyo/bin:$PATH

# Py3.10
WORKDIR /home/app
# RUN pip install -r requirements_py3.10.txt
COPY install/requirements_conda.txt ./
# conda doesn't like some of our packages, use pip 
RUN python3 -m pip install -r requirements_conda.txt

# Faiss
RUN conda install -y -c pytorch faiss-cpu=1.7.4 mkl=2021 blas=1.0=mkl

# DiskANN
WORKDIR /home/app
RUN git clone https://github.com/maronuu/DiskANN.git --branch feature/ep-0.5.0.rc3.post1
WORKDIR /home/app/DiskANN
RUN mkdir build
RUN cmake -S . -B build  -DCMAKE_BUILD_TYPE=Release
RUN cd build && make -j
RUN pip install --no-cache-dir virtualenv build
RUN python3 -m build
RUN pip install --no-cache-dir dist/diskannpy-0.5.0rc3.post1-cp310-cp310-linux_x86_64.whl

# hnswlib
RUN pip install hnswlib

WORKDIR /home/app

ENV OMP_MAX_ACTIVE_LEVELS=32
ENV OMP_DYNAMIC=FALSE
ENV MKL_DYNAMIC=FALSE
ENV MKL_NUM_THREADS=8
ENV OMP_NUM_THREADS=8

# ENV MKL_ENABLE_INSTRUCTIONS=AVX2

ENTRYPOINT [ "conda", "run", "--no-capture-output", "-n", "utokyo", "python3", "-u", "run_algorithm.py" ]
