from fastapi import FastAPI, HTTPException, Header, UploadFile
from pydantic import BaseModel
from typing import Optional
import hashlib
import jwt
import os
import uuid

app = FastAPI()
flag_path = os.getcwd() + '/flag/flag.txt'
secret = "VERY_SECURE"

class User(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    data: Optional[str] = None

users = {}
files = {}

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

def create_initial_file():
    try:
        files['ping'] = 'pong'
        f = open('ping', 'w')
        f.write('pong')
        f.close()
    except:
        pass

@app.post("/register")
async def register(user: User):
    update_admin()
    if user.username in users:
        raise HTTPException(status_code=400, detail="username already registered")
    users[user.username] = user
    return user

@app.post("/login")
async def login(user: User):
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

@app.post("/upload")
async def upload_file(filename: Optional[str], file: Optional[UploadFile] = None):
    try:
        if not filename:
            filename = str(uuid.uuid4())
        if filename in files:
            return {"filename": filename, "content": files[filename]}
        if os.path.isfile(filename):
            return {"filename": filename, "content": open(filename).read()}
        content = await file.read()
        files[filename] = content
        return {"filename": filename, "content": content}
    except:
        return {"error": "upload a file"}

@app.post("/data")
def get_data(user: Optional[User] = None, authorization: str = Header(None)):
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
create_initial_file()