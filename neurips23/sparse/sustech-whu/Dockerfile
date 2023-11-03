FROM neurips23

RUN apt update
RUN apt install -y libssl-dev cmake

WORKDIR /home/app
RUN git clone https://github.com/lizzy-0323/SUSTech-WHU-Sparse.git --recursive
WORKDIR /home/app/SUSTech-WHU-Sparse
RUN cmake -DCMAKE_BUILD_TYPE=Release . && make -j4
WORKDIR /home/app