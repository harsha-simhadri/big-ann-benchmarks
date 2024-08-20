FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10

# copy and install the pys2 python package
RUN git clone --branch ood https://github.com/pinecone-io/bigann.git
RUN pip install ./bigann/*.whl
# verify that the build worked
RUN python3 -c 'import diskannpy;'
RUN python3 -c 'import pys2;'
