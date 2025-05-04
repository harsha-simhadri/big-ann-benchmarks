FROM kemingy/rabbithole:pg17

# https://github.com/tensorchord/rabbithole

RUN apt-get update \
    && apt-get install -y python3-pip build-essential git axel wget
RUN wget https://aka.ms/downloadazcopy-v10-linux && \
    mv downloadazcopy-v10-linux azcopy.tgz && \
    tar xzf azcopy.tgz --transform 's!^[^/]\+\($\|/\)!azcopy_folder\1!' && \
    cp azcopy_folder/azcopy /usr/bin

WORKDIR /home/app
COPY requirements_py3.10.txt .

RUN python3 -m pip install --break-system-packages -r requirements_py3.10.txt
RUN python3 -m pip install --break-system-packages psycopg[binary] pgvector

COPY run_algorithm.py .

ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=postgres

RUN printf '#!/bin/bash\n\
runuser -u postgres -- initdb \n\
runuser -u postgres -- postgres -c shared_preload_libraries=rabbithole.so &\n\
sleep 5\n\
python3 -u run_algorithm.py "$@"' > entrypoint.sh \
 && chmod u+x entrypoint.sh

ENTRYPOINT ["/home/app/entrypoint.sh"]
