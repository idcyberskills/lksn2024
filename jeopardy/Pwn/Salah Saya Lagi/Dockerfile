FROM ubuntu:20.04

RUN apt-get update 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /etc/xinetd.d/*

RUN useradd -U -m -s /bin/bash aos

WORKDIR /home/aos

COPY ./flag.txt .
COPY ./chall .
COPY ./ynetd /usr/bin/ynetd

RUN chown -R root:aos /home/aos
RUN chmod -R 750 /home/aos && chmod 440 flag.txt 
RUN mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt
RUN chown root:aos /usr/bin/ynetd
RUN chmod 750 /usr/bin/ynetd

EXPOSE 11103

CMD ["/usr/bin/ynetd", "-p", "11103", "/home/aos/chall"]
