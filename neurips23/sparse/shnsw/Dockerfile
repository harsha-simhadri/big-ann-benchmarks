FROM neurips23

RUN apt update
RUN apt-get install -y python-setuptools python-pip
RUN pip3 install pybind11 numpy setuptools
RUN git clone https://github.com/Leslie-Chung/SHNSW.git

WORKDIR SHNSW
RUN pip3 install .

RUN python3 -c 'import sparse_hnswlib'
WORKDIR /home/app