FROM neurips23

RUN apt update
RUN apt install -y libssl-dev
RUN wget https://cmake.org/files/v3.23/cmake-3.23.1.tar.gz
RUN tar -zxvf cmake-3.23.1.tar.gz
WORKDIR /home/app/cmake-3.23.1
RUN ./bootstrap --parallel=8
RUN make -j4
RUN make install
WORKDIR /home/app
RUN git clone -b faiss https://github.com/whateveraname/SUSTech-OOD.git --recursive
WORKDIR /home/app/SUSTech-OOD
RUN cmake -DCMAKE_BUILD_TYPE=Release . && make -j4
WORKDIR /home/app