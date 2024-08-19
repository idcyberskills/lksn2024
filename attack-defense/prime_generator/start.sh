#!/bin/bash

pip install pycryptodome
socat TCP-L:10003,fork EXEC:"python3 /home/prime-generator/server.py",reuseaddr,stderr 2>&1