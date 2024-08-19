from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional
import hashlib
import jwt
import os

app = FastAPI()
flag_path = os.getcwd() + '/flag/flag.txt'
secret = "VERY_SECURE"

class User(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    data: Optional[str] = None

users = {}

def update_admin():
    f = open(flag_path, "rb")
    flag = f.read()
    f.close()
    hasher = hashlib.sha256()
    hasher.update(flag)
    users["admin"] = User()
    users["admin"].username = "admin"
    users["admin"].password = hasher.hexdigest()
    users["admin"].data = flag

@app.post("/register")
def register(user: User):
    # Register user
    update_admin()
    if user.username in users:
        raise HTTPException(status_code=400, detail="username already registered")
    users[user.username] = user
    return user

@app.post("/login")
def login(user: User):
    # Authenticate user
    update_admin()
    if user.username not in users:
        raise HTTPException(status_code=404, detail="user not found")
    usr = users[user.username]
    if user.password != usr.password:
        raise HTTPException(status_code=401, detail="wrong password")

    encoded_jwt = jwt.encode({
        "username": user.username,
    }, secret, algorithm="HS256", headers={  
        "alg": "HS256",  
        "typ": "JWT"  
    })
    return {
        "token": encoded_jwt,
    }

@app.post("/data")
def get_data(user: Optional[User] = None, authorization: str = Header(None)):
    # Get user's data
    update_admin()
    try:
        data = jwt.decode(authorization, secret, algorithms=['HS256'])
        assert data['username'] in users
    except:
        raise HTTPException(status_code=401, detail="wrong token")
    if user.username not in users:
        raise HTTPException(status_code=401, detail="username invalid")
    return users[user.username]

update_admin()