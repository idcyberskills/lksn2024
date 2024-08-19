#!/bin/bash

pip install fastapi uvicorn pydantic
uvicorn main:app --reload