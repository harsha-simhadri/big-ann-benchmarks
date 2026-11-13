FROM neurips23

RUN apt-get update && apt-get install -y curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain 1.99.0
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip3 install maturin

# WARM (WritersLogic Adaptive Retention & Memory), pinned to one commit. This ARG is the only
# place the revision is set; change it here and rebuild.
ARG WARM_COMMIT=cc846be0b61c946db3943282daa044333bf604d5
RUN GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/writerslogic/warm.git /home/app/warm \
    && cd /home/app/warm && git checkout ${WARM_COMMIT} \
    && maturin build --release --features python -i python3 -o /home/app/wheels \
    && pip3 install /home/app/wheels/*.whl
WORKDIR /home/app
