FROM neurips23

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
