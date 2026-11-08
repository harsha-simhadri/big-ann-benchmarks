FROM neurips23

RUN apt-get update && apt-get install -y curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain 1.99.0
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip3 install maturin

# WARM (WritersLogic Adaptive Retention & Memory), pinned to one commit. This ARG is the only
# place the revision is set; change it here and rebuild.
ARG WARM_COMMIT=459a54031a7293be86227c62755d6b82de81dd2f
RUN GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/writerslogic/warm.git /home/app/warm \
    && cd /home/app/warm && git checkout ${WARM_COMMIT} \
    && maturin build --release --features python,experimental -i python3 -o /home/app/wheels \
    && pip3 install /home/app/wheels/*.whl
WORKDIR /home/app
