#!/bin/bash

mv main.py start.sh /home/auther/
mkdir /home/auther/flag

chown auther:auther /home/auther/flag
chown auther:auther /home/auther/main.py
chown auther:auther /home/auther/start.sh

mv auther.service /etc/systemd/system/auther.service
systemctl start auther.service
systemctl enable auther.service