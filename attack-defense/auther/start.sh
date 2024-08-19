#!/bin/bash

pip install fastapi uvicorn pydantic
cd /home/auther
uvicorn main:app --reload