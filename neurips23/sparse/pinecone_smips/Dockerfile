FROM neurips23

RUN apt-get update && apt-get install -y curl

# download and install the whl file
RUN git clone --branch sparse https://github.com/pinecone-io/bigann.git
RUN pip install ./bigann/*.whl

# verify that the build worked
RUN python3 -c 'import py_pinecone_smips;'
