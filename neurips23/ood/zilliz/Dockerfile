FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10

RUN apt install python-is-python3
RUN git clone https://github.com/hhy3/zilliz-bigann.git --branch ood --depth 1
RUN pip install ./zilliz-bigann/*.whl

RUN python3 -c 'import ood_searcher'
