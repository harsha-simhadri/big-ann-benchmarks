FROM neurips23

RUN apt-get update && apt-get install -y curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip3 install maturin

RUN git clone https://github.com/yp3y5akh0v/prism.git /home/app/prism
RUN cd /home/app/prism/crates/prism-python && maturin build --release && pip3 install /home/app/prism/target/wheels/*.whl
WORKDIR /home/app
