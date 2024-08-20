FROM ubuntu:latest

RUN apt-get update 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash tnofo

WORKDIR /home/tnofo

COPY ./flag.txt .
COPY ./chall .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:tnofo /home/tnofo
RUN chmod -R 750 /home/tnofo && chmod 440 flag.txt 
RUN chown root:tnofo /usr/bin/ynetd
RUN chmod 750 /usr/bin/ynetd

EXPOSE 11102

CMD ["/usr/bin/ynetd", "-p", "11102", "/home/tnofo/chall"]
