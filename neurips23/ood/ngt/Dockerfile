FROM neurips23

RUN apt-get update
RUN apt-get install -y git cmake liblapack-dev bc
RUN pip3 install wheel pybind11
RUN git clone https://github.com/masajiro/NGT-neurips23.git NGT
RUN cd NGT && git log -n 1
RUN cd NGT && mkdir build && cd build && cmake .. 
RUN cd NGT/build && make -j 8 && make install
RUN ldconfig
RUN cd NGT/python && python3 setup.py bdist_wheel
RUN pip3 install NGT/python/dist/ngt-*-linux_x86_64.whl
