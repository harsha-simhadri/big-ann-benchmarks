FROM neurips23

RUN apt-get install -y curl

# install rust + build tools
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN git clone --single-branch --branch main https://github.com/pinecone-io/research-bigann-linscan
WORKDIR research-bigann-linscan/

# install maturin (build tool for rust-python)
RUN pip install maturin

# build a whl file
RUN maturin build -r

# pip install the correct wheel (different architectures will produce .whl files with different names)
RUN pip install ./target/wheels/*.whl

# verify that the build worked
RUN python3 -c 'import pylinscan; print(pylinscan.LinscanIndex());'

WORKDIR ..