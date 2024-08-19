FROM ubuntu:22.04
env DEBIAN_FRONTEND=noninteractive

RUN apt update --fix-missing && apt install libseccomp-dev xinetd -y
RUN groupadd -r ctf && useradd -r -g ctf ctf

WORKDIR /home/ctf

COPY public/chall .
COPY /flagdottieksti.txt /

RUN echo '#!/bin/bash\nservice xinetd restart && /bin/sleep infinity' > /etc/init.sh
RUN echo 'service ctf\n\ 
{\n\ 
    disable = no\n\ 
    socket_type = stream\n\ 
    protocol = tcp\n\ 
    wait = no\n\ 
    user = ctf\n\ 
    type = UNLISTED\n\ 
    port = 14120\n\ 
    bind = 0.0.0.0\n\ 
    server = /home/ctf/run\n\ 
}' > /etc/xinetd.d/ctf

RUN echo '#!/bin/bash\ncd /home/ctf && ./chall' > /home/ctf/run
RUN chmod 400 /etc/xinetd.d/ctf
RUN chmod 550 /home/ctf/chall /home/ctf/run /etc/init.sh

RUN chown -R root:ctf /home/ctf
RUN service xinetd restart
