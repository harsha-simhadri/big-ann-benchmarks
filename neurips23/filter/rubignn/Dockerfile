FROM ubuntu:jammy

RUN apt-get update && apt-get install -y python3-numpy python3-scipy python3-pip build-essential git axel wget
RUN wget https://aka.ms/downloadazcopy-v10-linux && mv downloadazcopy-v10-linux azcopy.tgz && tar xzf azcopy.tgz --transform 's!^[^/]\+\($\|/\)!azcopy_folder\1!' 
RUN cp azcopy_folder/azcopy /usr/bin

RUN pip3 install -U pip

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10

WORKDIR /home/app
RUN git clone https://github.com/rutgers-db/ru-bignn-23.git --branch main
WORKDIR /home/app/ru-bignn-23
RUN mkdir build
RUN cmake -S . -B build  -DCMAKE_BUILD_TYPE=Release
RUN cmake --build build -- -j
WORKDIR /home/app
