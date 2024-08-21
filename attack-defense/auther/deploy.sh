#!/bin/bash

sudo useradd -m auther

# assume the files are already exist in this directory
sudo -u auther mkdir /home/auther/service
sudo -u auther mkdir /home/auther/service/flag
sudo chown auther:auther start.sh
sudo chown auther:auther main.py
sudo -u auther mv start.sh /home/auther/service
sudo -u auther mv main.py /home/auther/service
sudo -u auther echo LKSN{PLACEHOLDER} > /home/auther/service/flag/flag.txt
sudo chmod +x /home/auther/service/start.sh

# run server
sudo /home/auther/service/start.sh
