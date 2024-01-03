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
RUN python3 -c 'import pys2;'
RUN python3 -c 'import diskannpy;'

#COPY DiskANN-fast-l2 ./DiskANN-fast-l2
#WORKDIR /home/app/DiskANN-fast-l2
#RUN pip3 install virtualenv build
#RUN python3 -m build
#RUN pip install dist/diskannpy-0.7.0rc2-cp310-cp310-linux_x86_64.whl
#WORKDIR /home/app
