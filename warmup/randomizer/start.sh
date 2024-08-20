#!/bin/bash

socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"python3 -u main.py"