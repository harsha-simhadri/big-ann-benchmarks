FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10 python3-numpy python3-scipy python3-pip build-essential git libblas-dev liblapack-dev wget libaio-dev libgoogle-perftools-dev clang-format libboost-all-dev libopenblas-dev liblapacke-dev



RUN apt-get update; DEBIAN_FRONTEND=noninteractive apt install intel-mkl python3-setuptools  wget python3-matplotlib build-essential checkinstall libssl-dev swig4.0 python3-dev  python3-numpy  python3-numpy-dev   -y
COPY install/requirements_conda.txt ./
# conda doesn't like some of our packages, use pip
RUN python3 -m pip install -r requirements_conda.txt

RUN pip3 install -U pip numpy pybind11 tqdm
RUN git clone https://github.com/SDU-L/DHQ.git
RUN chmod -R +777 DHQ/
RUN cp /home/app/DHQ/faiss/build/faiss/python/libfaiss_python_callbacks.so /lib
RUN cp /home/app/DHQ/faiss/build/faiss/libfaiss.so /lib
RUN cp /home/app/DHQ/faiss/build/faiss/libfaiss_avx2.so /lib
RUN cp /home/app/DHQ/faiss/build/faiss/python/_swigfaiss_avx2.so /lib
RUN cp /home/app/DHQ/faiss/build/faiss/python/_swigfaiss.so /lib
#RUN
RUN cd /home/app/DHQ/faiss/build/faiss/python/ && python3 setup.py install

RUN cd /home/app

ENV PYTHONPATH=DHQ/faiss/build/faiss/python/build/lib/
RUN python3 -c 'import faiss; print(faiss.IDSelectorFilterWise); print(faiss.__version__)'
RUN pip3 install DHQ/DHQ-1.0.3-cp310-cp310-linux_x86_64.whl
RUN python3 -c 'import DHQ'





