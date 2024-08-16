#!/bin/bash

sudo apt-get install gunicorn ffmpeg libsm6 libxext6 supervisor python3-virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo mkdir /var/log/facemonger
sudo touch /var/log/facemonger/facemonger.out.log
sudo touch /var/log/facemonger/facemonger.err.log

# ./venv/bin/gunicorn main:main -b localhost:7744
# sudo service supervisor restart
# sudo supervisorctl status
