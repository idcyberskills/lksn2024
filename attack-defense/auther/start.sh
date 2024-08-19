#!/bin/bash

cd /home/auther/service/
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn pydantic jwt python-multipart
uvicorn main:app --reload