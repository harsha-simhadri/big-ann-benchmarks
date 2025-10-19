FROM neurips23

# -----------------------------
# Set up environment variables
# -----------------------------
ENV CONDA_DIR=/opt/miniconda
ENV PATH="${CONDA_DIR}/bin:${PATH}"
ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------
# Install system dependencies
# -----------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      wget \
      curl \
      build-essential \
      ca-certificates \
      swig \
      git \
      libomp5 \
      libomp-dev \
      graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install CMake 3.24.2
RUN wget -qO /tmp/cmake.sh https://github.com/Kitware/CMake/releases/download/v3.24.2/cmake-3.24.2-linux-x86_64.sh && \
    chmod +x /tmp/cmake.sh && \
    /tmp/cmake.sh --skip-license --prefix=/usr/local && \
    rm /tmp/cmake.sh

# -----------------------------
# Clone Quake
# -----------------------------
RUN echo "Cloning the quake repo"
WORKDIR /home/app/
RUN git clone https://github.com/marius-team/quake.git --branch devesh/multi_level_bigann
WORKDIR /home/app/quake
RUN git submodule update --init --recursive

# -----------------------------
# Install Quake
# -----------------------------
RUN python3 -m pip install -r /home/app/quake/requirements.txt
RUN python3 -m pip install --no-use-pep517 .

# -----------------------------
# Verify quake installation
# -----------------------------
WORKDIR /home/app/
RUN python3 -c "import quake; print('✅ Quake imported successfully!')"