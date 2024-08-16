#!/bin/bash

pip install fastapi uvicorn
uvicorn main:app --reload