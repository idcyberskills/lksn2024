from fastapi import FastAPI, HTTPException, Header
from dataclasses import dataclass
import hashlib
import jwt

app = FastAPI()
flag_path = './flag/flag.txt'
secret = "VERY_SECURE"

@dataclass
class User:
    username: str
    password: str
    data: str

users = {}

def update_admin_password():
    f = open(flag_path, "rb")
    hasher = hashlib.sha256()
    hasher.update(f.read())
    users["admin"].password = hasher.hexdigest()
    f.close()

@app.post("/register")
def register(user: User):
    update_admin_password()
    if user.username in users:
        raise HTTPException(status_code=400, detail="username already registered")
    users[user.username] = user
    return user

@app.post("/login")
def login(user: User):
    update_admin_password()
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
    update_admin_password()
    try:
        jwt.decode(authorization, secret, algorithms=['HS256'])
    except:
        raise HTTPException(status_code=401, detail="wrong token")
    if user.username not in users:
        raise HTTPException(status_code=401, detail="username invalid")
    return users[user.username]

f = open(flag_path)
users["admin"] = User("admin", "", f.read())
update_admin_password()
f.close()