FROM neurips23

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:git-core/ppa
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y git make cmake g++ libaio-dev libgoogle-perftools-dev libunwind-dev clang-format libboost-dev libboost-program-options-dev libmkl-full-dev libcpprest-dev python3.10
WORKDIR /home/app
RUN git clone --recursive --branch one_g_opt_diff_d_10 https://github.com/matchyc/mysteryann.git
WORKDIR /home/app/mysteryann/pybindings
RUN pip3 install virtualenv build
RUN pip3 install pybind11[global]
RUN pip3 install .
WORKDIR /home/app