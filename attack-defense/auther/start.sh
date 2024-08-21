#!/bin/bash

cd /home/auther/service/
python3 -m venv env
source env/bin/activate
pip install fastapi uvicorn pydantic pyjwt python-multipart
runcon user_u:user_r:user_t:s0 uvicorn --host 8000 main:app --reload