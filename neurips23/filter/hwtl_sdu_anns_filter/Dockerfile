FROM neurips23

RUN apt update
RUN apt install apt-utils
RUN apt update && apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10 python3-numpy python3-scipy python3-pip build-essential git libblas-dev liblapack-dev wget libaio-dev libgoogle-perftools-dev clang-format libboost-all-dev libopenblas-dev liblapacke-dev



RUN apt update && apt install -y wget swig
RUN wget https://repo.anaconda.com/archive/Anaconda3-2023.03-0-Linux-x86_64.sh
RUN bash Anaconda3-2023.03-0-Linux-x86_64.sh -b

ENV PATH /root/anaconda3/bin:$PATH
ENV CONDA_PREFIX /root/anaconda3/

RUN conda install -c pytorch faiss-cpu
COPY install/requirements_conda.txt ./
# conda doesn't like some of our packages, use pip
RUN python3 -m pip install -r requirements_conda.txt
WORKDIR /home/app/
RUN pip3 install -U pip pybind11 numpy

RUN git clone https://github.com/WPJiang/HWTL_SDU-ANNS-filter.git
RUN cp ./HWTL_SDU-ANNS-filter/bow_id_selector.py  ./
RUN cp ./HWTL_SDU-ANNS-filter/_bow_id_selector.so  ./

ENV LD_PRELOAD /root/anaconda3/lib/libmkl_core.so:/root/anaconda3/lib/libmkl_sequential.so
RUN python3 -c 'import faiss; print(faiss.IndexFlatL2); print(faiss.__version__)'




