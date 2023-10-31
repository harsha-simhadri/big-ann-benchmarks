FROM neurips23

RUN apt update
RUN apt install -y libssl-dev cmake
# RUN wget https://cmake.org/files/v3.23/cmake-3.23.1.tar.gz
# RUN tar -zxvf cmake-3.23.1.tar.gz
# WORKDIR /home/app/cmake-3.23.1
# RUN ./bootstrap --parallel=8
# RUN make -j4
# RUN make install
WORKDIR /home/app
RUN git clone https://github.com/lizzy-0323/SUSTech-WHU-Sparse.git --recursive
WORKDIR /home/app/SUSTech-WHU-Sparse
RUN cmake -DCMAKE_BUILD_TYPE=Release . && make -j4
WORKDIR /home/app