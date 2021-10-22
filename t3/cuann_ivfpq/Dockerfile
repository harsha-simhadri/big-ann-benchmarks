FROM nvidia/cuda:11.4.2-devel-ubuntu20.04

RUN apt-get update
RUN apt-get install --no-install-recommends -y build-essential wget git python3-dev python3-pip
RUN pip3 install -U pip

RUN mkdir /home/soft
RUN cd /home/soft && wget -nv "https://drive.google.com/uc?export=download&id=1IybRBhZPQzMqQ2HRX9KSL7woftO8WZdV" -O pkg-libcuann-0.0.7.tgz && tar xfz pkg-libcuann-0.0.7.tgz
RUN pip3 install /home/soft/libcuann/python/dist/cuann-0.0.7-cp38-cp38-linux_x86_64.whl
RUN rm /home/soft/pkg-libcuann-0.0.7.tgz
RUN rm -rf /home/soft/libcuann/python

WORKDIR /home/app
COPY requirements_py38.txt run_algorithm.py ./
RUN pip3 install -r requirements_py38.txt
RUN pip3 install 'Cython>=0.29.*' 'numpy>=1.19.*' cupy-cuda114

ENV LD_LIBRARY_PATH="/home/soft/libcuann/lib:${LD_LIBRARY_PATH}"

ENTRYPOINT ["python3", "run_algorithm.py"]
