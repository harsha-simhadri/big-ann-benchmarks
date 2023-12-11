FROM neurips23

# install MKL support
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libmkl-full-dev

# copy and install the pys2 python package
RUN git clone --branch filter https://github.com/pinecone-io/bigann.git
RUN pip install ./bigann/*.whl
# verify that the build worked
RUN python3 -c 'import pys2;'

