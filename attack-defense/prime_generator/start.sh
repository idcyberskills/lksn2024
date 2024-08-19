#!/bin/bash

pip install pycryptodome
cd /home/prime-generator/
socat TCP-L:10003,fork EXEC:"python3 ./server.py",reuseaddr,stderr 2>&1