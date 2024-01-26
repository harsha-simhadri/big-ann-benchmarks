FROM neurips23

# install MKL support
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libmkl-full-dev libaio-dev

RUN git clone https://github.com/hhy3/zilliz-bigann.git --branch filter
RUN pip install ./zilliz-bigann/*.whl


