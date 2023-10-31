 
#FROM nvidia/cuda:11.0-devel-ubuntu18.04
FROM nvidia/cuda:11.0.3-cudnn8-devel-ubuntu18.04

# CONDA

ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"

RUN apt-get update  
RUN apt-get install -y wget 
RUN apt-get install -y build-essential 
RUN apt-get install -y git 
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.1.0-1-Linux-x86_64.sh
RUN bash Miniconda3-py38_23.1.0-1-Linux-x86_64.sh -b
RUN rm -f Miniconda3-py38_23.1.0-1-Linux-x86_64.sh
RUN conda --version 
RUN conda create -n py38 python=3.8 -y
RUN echo "source activate env" > ~/.bashrc
RUN ls /opt/
ENV PATH /opt/conda/envs/py38/bin:$PATH
RUN conda config --set remote_read_timeout_secs 300
RUN conda install -c pytorch faiss-gpu 
#RUN conda install cudatoolkit=11.0
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
