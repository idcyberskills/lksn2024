#!/bin/bash

mkdir -p /home/auther/service
mkdir /home/auther/service/flag
mv main.py start.sh /home/auther/service

chown auther:auther /home/auther/service/flag
chown auther:auther /home/auther/service/main.py
chown auther:auther /home/auther/service/start.sh

mv auther.service /etc/systemd/system/auther.service
systemctl start auther.service
systemctl enable auther.service