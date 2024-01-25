FROM neurips23

RUN apt update
RUN apt install python-is-python3
RUN git clone https://github.com/hhy3/zilliz-bigann.git --branch sparse --depth 1
RUN pip install ./zilliz-bigann/*.whl

RUN python3 -c 'import sparse_searcher'

