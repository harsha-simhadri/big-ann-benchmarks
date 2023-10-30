FROM neurips23

RUN apt-get update; DEBIAN_FRONTEND=noninteractive apt install intel-mkl python3-setuptools  wget python3-matplotlib build-essential checkinstall libssl-dev swig4.0 python3-dev  python3-numpy  python3-numpy-dev   -y
COPY install/requirements_conda.txt ./
# conda doesn't like some of our packages, use pip
RUN python3 -m pip install -r requirements_conda.txt


# CMAKE with good enough version
RUN  mkdir /build && wget  https://github.com/Kitware/CMake/archive/refs/tags/v3.27.1.tar.gz  && mv v3.27.1.tar.gz  /build
RUN cd /build; tar -zxvf v3.27.1.tar.gz
RUN cd /build/CMake-3.27.1 &&   ./bootstrap && make   && make install


RUN cd / &&  git clone https://github.com/alemagnani/faiss.git && cd /faiss && git pull && git checkout wm_filter

RUN cd /faiss && rm -rf ./build
RUN cd /faiss/; cmake -B build /faiss/  -DFAISS_ENABLE_GPU=OFF -DFAISS_ENABLE_PYTHON=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release -DFAISS_OPT_LEVEL=avx2  -DBLA_VENDOR=Intel10_64_dyn -DBUILD_TESTING=ON  -DPython_EXECUTABLE=/usr/bin/python3 -DMKL_LIBRARIES=/usr/lib/x86_64-linux-gnu/libmkl_rt.so
RUN cd /faiss/; make -C build -j faiss faiss_avx2 swigfaiss  swigfaiss_avx2
RUN  (cd /faiss/build/faiss/python && python3 setup.py install)

#RUN pip install tritonclient[all]
ENV PYTHONPATH=/faiss/build/faiss/python/build/lib/

RUN python3 -c 'import faiss; print(faiss.IndexFlatL2); print(faiss.__version__)'



