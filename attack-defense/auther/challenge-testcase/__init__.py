from typing import List, TypedDict, Dict, Tuple, Any
import datetime
import requests
import uuid
import base64
import json
import hashlib

class ServiceType(TypedDict):
    id: int
    team_id: int
    challenge_id: int
    order: int
    secret: str
    detail: Dict[str, Any]
    time_created: datetime.datetime

class FlagType(TypedDict):
    id: int
    team_id: int
    challenge_id: int
    round: int
    tick: int
    value: str
    order: int

class CheckerAgentReport(TypedDict):
    id: int
    source_ip: str
    selinux_status: bool
    flag_status: Dict
    challenge_status: Dict
    time_created: datetime.datetime

def check_regular_user(ip):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    data = str(uuid.uuid4())

    body = {}
    try:
        res = requests.post(ip + "/register", json={
            "username": username,
            "password": password,
            "data": data,
        })
        body = res.json()
    except:
        return (
            False,
            {
                "message": "fail to send request to register api"
            }
        )

    try:
        assert body['username'] == username
        assert body['password'] == password
        assert body['data'] == data
    except:
        return (
            False,
            {
                "message": "response from register api is incorrect"
            }
        )
    
    body = {}
    try:
        res = requests.post(ip + "/login", json={
            "username": username,
            "password": password,
            "data": data,
        })
        body = res.json()
    except:
        return (
            False,
            {
                "message": "fail to send request to login api"
            }
        )

    token = ""
    try:
        token = body['token']
        s = token.split('.')[1]
        s += '=' * (-len(s) % 4)
        token_segment_2 = json.loads(base64.b64decode(s).decode())
        assert token_segment_2['username'] == username
    except:
        return (
            False,
            {
                "message": "response from login api is incorrect"
            }
        )

    body = {}
    try:
        res = requests.post(ip + "/data", json={
            "username": username,
            "password": password,
            "data": data,
        }, headers={
            "Authorization": token,
        })
        body = res.json()
    except:
        return (
            False,
            {
                "message": "fail to send request to get data api"
            }
        )

    try:
        assert body['data'] == data
    except:
        return (
            False,
            {
                "message": "response from get data api is incorrect"
            }
        )
    
    return (
        True,
        {
            "message": "OK"
        }
    )

def check_admin(ip, flag):
    username = 'admin'
    hasher = hashlib.sha256()
    hasher.update(flag.encode())
    password = hasher.hexdigest()
    data = flag

    body = {}
    try:
        res = requests.post(ip + "/register", json={
            "username": username,
            "password": password,
            "data": data,
        })
        body = res.json()
    except:
        return (
            False,
            {
                "message": "fail to send request to register api"
            }
        )

    try:
        assert body['detail'] == "username already registered"
    except:
        return (
            False,
            {
                "message": "response from register api is incorrect"
            }
        )
    
    body = {}
    try:
        res = requests.post(ip + "/login", json={
            "username": username,
            "password": password,
            "data": data,
        })
        body = res.json()
    except:
        return (
            False,
            {
                "message": "fail to send request to login api"
            }
        )

    token = ""
    try:
        token = body['token']
        s = token.split('.')[1]
        s += '=' * (-len(s) % 4)
        token_segment_2 = json.loads(base64.b64decode(s).decode())
        assert token_segment_2['username'] == username
    except:
        return (
            False,
            {
                "message": "response from login api is incorrect"
            }
        )

    body = {}
    try:
        res = requests.post(ip + "/data", json={
            "username": username,
            "password": password,
            "data": data,
        }, headers={
            "Authorization": token,
        })
        body = res.json()
    except:
        return (
            False,
            {
                "message": "fail to send request to get data api"
            }
        )

    try:
        assert body['data'] == data
    except:
        return (
            False,
            {
                "message": "missing flag"
            }
        )
    
    return (
        True,
        {
            "message": "OK"
        }
    )

def main(services: List[ServiceType], flags: List[FlagType], checker_agent_report: CheckerAgentReport) -> Tuple[bool, Dict]:
    service_detail = services[0]["detail"]

    credentials = service_detail["checker"]
    aws_stack_name = service_detail["stack_name"]
    ip = credentials["ip"]
    username = credentials["username"]
    privkey = credentials["private_key"]
    instance_id = credentials["instance_id"]
    
    result_check_regular_user = check_regular_user(ip)
    if not result_check_regular_user[0]:
        return result_check_regular_user

    return result_check_regular_user

#print(check_regular_user('http://localhost:8000'))
#print(check_admin('http://localhost:8000', 'LKSN{PLACEHOLDER}'))