FROM neurips23

RUN apt update
RUN apt-get update
RUN apt-get install -y wget git cmake g++ libaio-dev libgoogle-perftools-dev clang-format libboost-dev python3 python3-setuptools python3-pip
#swig
RUN apt-get update && apt-get install -y swig cmake
RUN pip3 install pybind11 numpy 
RUN cat /etc/ld.so.conf
RUN ls /etc/ld.so.conf.d/
##cmake
RUN wget https://cmake.org/files/v3.22/cmake-3.22.0-linux-x86_64.sh
RUN mkdir cmake && sh cmake-3.22.0-linux-x86_64.sh --skip-license --prefix=cmake
ENV PATH /home/app/cmake/bin:$PATH

#mkl
RUN wget https://registrationcenter-download.intel.com/akdlm/IRC_NAS/adb8a02c-4ee7-4882-97d6-a524150da358/l_onemkl_p_2023.2.0.49497_offline.sh
RUN sh l_onemkl_p_2023.2.0.49497_offline.sh -a --components intel.oneapi.lin.mkl.devel --action install --eula accept -s

RUN echo "/opt/intel/oneapi/mkl/latest/lib/intel64" > /etc/ld.so.conf.d/mkl.conf
RUN ldconfig
RUN touch /etc/profile.d/intel.sh
RUN echo ".  /opt/intel/oneapi/mkl/latest/env/vars.sh" >> /etc/profile.d/intel.sh
RUN . /etc/profile.d/intel.sh

ENV CMAKE_ARGS "-DMKLROOT=/opt/intel/oneapi/mkl/latest/ -DBLA_VENDOR=Intel10_64lp_seq -DBLA_STATIC=ON"
#RUN  git config --global http.sslVerify false

RUN git clone -b streaming https://github.com/baidu/puck.git
RUN cd puck && . /etc/profile.d/intel.sh  && python3 setup.py install
RUN  python3 -c 'from puck import py_puck_api'
