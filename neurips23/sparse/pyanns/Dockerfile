FROM neurips23

RUN apt update
RUN apt install python-is-python3
RUN git clone https://github.com/veaaaab/pyanns.git --branch sparse --depth 1
WORKDIR /home/app/pyanns
RUN pip install -r requirements.txt
RUN bash build.sh

RUN python3 -c 'import pyanns'

WORKDIR /home/app
