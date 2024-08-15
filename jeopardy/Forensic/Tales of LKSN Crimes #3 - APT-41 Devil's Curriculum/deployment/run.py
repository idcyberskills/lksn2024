#!/usr/bin/env python3

import os
port = 23897
command = 'socat -d -d tcp-l:' + str(port) + ',reuseaddr,fork EXEC:"python3 -u chall.py" '
os.system(command)