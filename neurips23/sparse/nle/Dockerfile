FROM neurips23

RUN apt-get update 

RUN apt-get install -y curl git build-essential libpcre3-dev cmake libtool automake libatlas3-base libatlas-base-dev libstdc++-12-dev patchelf ninja-build libtbb2

RUN pip3 install scikit-build

#RUN apt-get install -y curl git openjdk-11-jdk build-essential libpcre3-dev cmake libtool automake libatlas3-base libatlas-base-dev libstdc++-12-dev patchelf ninja-build libtbb2

RUN git clone https://github.com/cadurosar/tttt.git /workspace/tttt && cd /workspace/tttt && bash build.sh

WORKDIR /home/app