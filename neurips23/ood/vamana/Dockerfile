FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10


ARG CACHEBUST=1
RUN git clone -b ood_v2 https://github.com/cmuparlay/ParlayANN.git && cd ParlayANN && git submodule update --init --recursive && cd python && pip install pybind11 && bash compile.sh 
# WORKDIR /home/app/ParlayANN
# RUN git submodule update --init --recursive
# WORKDIR /home/app/ParlayANN/python

# RUN pip install pybind11

# RUN bash compile.sh

ENV PYTHONPATH=$PYTHONPATH:/home/app/ParlayANN/python

# ENV PARLAY_NUM_THREADS=8

WORKDIR /home/app