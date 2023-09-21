FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10

RUN git clone https://github.com/microsoft/DiskANN.git --branch  0.5.0.rc3
WORKDIR /home/app/DiskANN
RUN pip3 install virtualenv build
RUN python3 -m build
<<<<<<< HEAD
=======
# RUN echo $(ls /home/app/DiskANN/dist)
>>>>>>> ee9924e54e0a72d152bfa5be074d4eae5d235bab
RUN pip install dist/diskannpy-0.5.0rc2-cp310-cp310-linux_x86_64.whl
WORKDIR /home/app
