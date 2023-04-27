FROM ubuntu:jammy

RUN apt-get update && apt-get install -y python3-numpy python3-scipy python3-pip build-essential git axel wget
RUN wget https://aka.ms/downloadazcopy-v10-linux && mv downloadazcopy-v10-linux azcopy.tgz && tar xzf azcopy.tgz --transform 's!^[^/]\+\($\|/\)!azcopy_folder\1!' 
RUN cp azcopy_folder/azcopy /usr/bin

RUN pip3 install -U pip

WORKDIR /home/app
COPY requirements_py3.10.txt run_algorithm.py ./
RUN pip3 install -r requirements_py3.10.txt

ENTRYPOINT ["python3", "-u", "run_algorithm.py"]