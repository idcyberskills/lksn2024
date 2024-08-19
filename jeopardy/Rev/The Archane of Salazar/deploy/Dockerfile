FROM ubuntu:latest

RUN apt-get update 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash dedebugbug

WORKDIR /home/dedebugbug

COPY ./flag.txt .
COPY ./chall .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:dedebugbug /home/dedebugbug
RUN chmod -R 750 /home/dedebugbug && chmod 440 flag.txt 
RUN chown root:dedebugbug /usr/bin/ynetd
RUN chmod 750 /usr/bin/ynetd

EXPOSE 37868

CMD ["/usr/bin/ynetd", "-p", "37868", "/home/dedebugbug/chall"]