#!/bin/bash

cd /usr/local/share/prime-generator/
python3 -m venv env
source env/bin/activate
pip install pycryptodome
socat TCP-L:10003,fork EXEC:"python3 ./server.py",reuseaddr,stderr 2>&1