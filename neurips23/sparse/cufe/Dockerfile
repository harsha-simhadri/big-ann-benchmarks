FROM neurips23

RUN apt-get update
RUN apt-get install -y sudo build-essential git axel wget curl


# for python 3.10
RUN sudo apt install software-properties-common -y
RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN sudo apt-get -y install python3.10
RUN apt-get -y install python3-numpy python3-scipy python3-pip

# Get Rust; NOTE: using sh for better compatibility with other base images
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# git clone a single branch
RUN git clone --single-branch --branch main https://github.com/MichaelIbrahim-GaTech/research-bigann-linscan.git
WORKDIR research-bigann-linscan/

# fix python3 link (required for pyo3)
RUN ln -fs /usr/bin/python3.10 /usr/bin/python3

# fix pip3
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

RUN pip3 install maturin

# build a whl file
RUN maturin build -r

# pip install the resulting whl file (regardless of the architecture)
RUN for whl in target/wheels/*.whl; do pip3 install $whl; done

RUN pip3 install -r requirements.txt

# verify that the build worked
RUN python3 -c 'import pylinscancufe; print(pylinscancufe.LinscanIndex());'

WORKDIR ..
