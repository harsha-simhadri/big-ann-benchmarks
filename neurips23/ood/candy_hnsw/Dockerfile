FROM neurips23

RUN apt update && apt install -y wget swig
RUN wget https://repo.anaconda.com/archive/Anaconda3-2023.03-0-Linux-x86_64.sh
RUN bash Anaconda3-2023.03-0-Linux-x86_64.sh -b

ENV PATH /root/anaconda3/bin:$PATH
ENV CONDA_PREFIX /root/anaconda3/

RUN conda install -c pytorch faiss-cpu
COPY install/requirements_conda.txt ./
# conda doesn't like some of our packages, use pip 
RUN python3 -m pip install -r requirements_conda.txt 

COPY neurips23/filter/faiss/bow_id_selector.swig ./

RUN swig -c++ -python -I$CONDA_PREFIX/include -Ifaiss bow_id_selector.swig 
RUN g++ -shared -O3 -g -fPIC bow_id_selector_wrap.cxx -o _bow_id_selector.so  \
      -I $( python -c "import distutils.sysconfig ; print(distutils.sysconfig.get_python_inc())" )   \
      -I $CONDA_PREFIX/include $CONDA_PREFIX/lib/libfaiss_avx2.so -Ifaiss

RUN python3 -c 'import faiss; print(faiss.IndexFlatL2); print(faiss.__version__)'



