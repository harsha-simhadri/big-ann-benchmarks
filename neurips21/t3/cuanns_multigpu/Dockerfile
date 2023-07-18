FROM nvidia/cuda:11.4.2-devel-ubuntu20.04

RUN apt-get update
RUN apt-get install --no-install-recommends -y build-essential wget git python3-dev python3-pip libopenblas-dev
RUN pip3 install -U pip

RUN mkdir /home/soft
RUN cd /home/soft && wget -nv https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3-linux-x86_64.tar.gz && tar xzf cmake-3.21.3-linux-x86_64.tar.gz
RUN cd /home/soft && wget -nv https://github.com/facebookresearch/faiss/archive/refs/tags/v1.7.1.tar.gz -O faiss-1.7.1.tar.gz && tar xzf faiss-1.7.1.tar.gz
RUN cd /home/soft/faiss-1.7.1 \
  && ../cmake-3.21.3-linux-x86_64/bin/cmake -B build\
  -DFAISS_ENABLE_GPU=ON \
  -DFAISS_ENABLE_PYTHON=OFF -DBUILD_TESTING=OFF \
  -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_ARCHITECTURES="80" \
  -DCMAKE_INSTALL_PREFIX=/home/soft/faiss . \
  && cd build && make -j 8 && make install



WORKDIR /home/app
COPY requirements_py38.txt run_algorithm.py ./
RUN pip3 install -r requirements_py38.txt

RUN cd /home/soft/ && wget -nv "https://drive.google.com/uc?export=download&id=1jU4aLrihX6cPPzOB9oRQrrSYZkyUGoQ5" -O pycuann.tar.gz && tar xf pycuann.tar.gz pycuann.so

ENV LD_LIBRARY_PATH="/home/soft:${LD_LIBRARY_PATH}"
ENV PATH="/home/soft:${PATH}"
ENTRYPOINT ["python3", "run_algorithm.py"]
