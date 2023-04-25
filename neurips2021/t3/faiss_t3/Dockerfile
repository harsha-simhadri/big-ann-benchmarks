 
FROM nvidia/cuda:11.0-devel-ubuntu18.04

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

# CONDA

RUN apt-get update  && apt-get install -y wget build-essential git 

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && conda --version \
    && conda install -c pytorch python=3.6.9 faiss-gpu cudatoolkit=11.0

RUN conda --version && which conda && which python && which pip3

# BIGANN

RUN pip3 install -U pip

WORKDIR /home/app
COPY t3/faiss_t3/faiss-gpu_requirements.txt run_algorithm.py ./
RUN pip3 install -r faiss-gpu_requirements.txt

ENTRYPOINT ["python3", "run_algorithm.py"]

## For the following RUN command to work, we need to initiate docker build
## with a gpu device request much like what's done with docker eval run.
# RUN python3 -c 'import faiss; print("gpus=", faiss.get_num_gpus())' 

RUN python3 -c 'import faiss; print(faiss.IndexFlatL2)'
