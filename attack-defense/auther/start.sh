#!/bin/bash

cd /home/auther/service/
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn pydantic pyjwt python-multipart
uvicorn --host 0.0.0.0 --port 8000 main:app --reload