FROM neurips23

RUN apt update
RUN apt install -y sudo software-properties-common python3.10
RUN git clone https://github.com/AndrewHYu/Hanns.git
RUN pip install ./Hanns/*.whl

WORKDIR /home/app
