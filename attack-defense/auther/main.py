from fastapi import FastAPI, HTTPException, Header
from dataclasses import dataclass
import hashlib
import jwt
import os

app = FastAPI()
flag_path = os.getcwd() + '/flag/flag.txt'
secret = "VERY_SECURE"

@dataclass
class User:
    username: str
    password: str
    data: str

users = {}

def update_admin():
    f = open(flag_path, "rb")
    flag = f.read()
    f.close()
    hasher = hashlib.sha256()
    hasher.update(flag)
    users["admin"].password = hasher.hexdigest()
    users["admin"].data = flag

@app.post("/register")
def register(user: User):
    update_admin()
    if user.username in users:
        raise HTTPException(status_code=400, detail="username already registered")
    users[user.username] = user
    return user

@app.post("/login")
def login(user: User):
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
def get_data(user: User, authorization: str = Header(None)):
    update_admin()
    try:
        data = jwt.decode(authorization, secret, algorithms=['HS256'])
        assert data['username'] in users
    except:
        raise HTTPException(status_code=401, detail="wrong token")
    if user.username not in users:
        raise HTTPException(status_code=401, detail="username invalid")
    return users[user.username]

@app.post("/delete")
def delete(authorization: str = Header(None)):
    try:
        data = jwt.decode(authorization, secret, algorithms=['HS256'])
        assert data['username'] in users
        del users[data['username']]
    except:
        raise HTTPException(status_code=401, detail="wrong token")

f = open(flag_path)
users["admin"] = User("admin", "", f.read())
update_admin()
f.close()