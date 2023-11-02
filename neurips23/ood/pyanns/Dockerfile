FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10

RUN git clone https://github.com/veaaaab/DiskANN.git --branch  bigann23_ood
WORKDIR /home/app/DiskANN
RUN pip3 install virtualenv build
RUN python3 -m build
RUN pip install dist/diskannpy-0.5.0rc3.post1-cp310-cp310-linux_x86_64.whl
WORKDIR /home/app

RUN apt update
RUN apt install python-is-python3
RUN git clone https://github.com/veaaaab/pyanns --branch master --depth 1
WORKDIR /home/app/pyanns
RUN pip install -r requirements.txt
RUN bash build.sh
WORKDIR /home/app

RUN python3 -c 'import pyanns'

WORKDIR /home/app

