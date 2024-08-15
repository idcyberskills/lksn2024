FROM python:3

RUN apt-get update 
RUN apt-get install -y socat 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash rootskids

WORKDIR /home/rootskids

COPY ./chall.py .
COPY ./run.py .

RUN chown -R root:rootskids /home/rootskids
RUN chmod -R 750 /home/rootskids

CMD $
CMD [ "python", "./run.py" ]