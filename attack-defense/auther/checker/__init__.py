from typing import List, TypedDict, Dict, Tuple, Any
import datetime
import requests
import uuid
import base64
import json
import hashlib
import io

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

def check_regular_user(base_url):
    username = str(uuid.uuid4())
    password = str(uuid.uuid4())
    data = str(uuid.uuid4())

    body = {}
    try:
        res = requests.post(base_url + "/register", json={
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
        res = requests.post(base_url + "/login", json={
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
        res = requests.post(base_url + "/data", json={
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

def check_admin(base_url, flag):
    username = 'admin'
    hasher = hashlib.sha256()
    hasher.update(flag.encode())
    password = hasher.hexdigest()
    data = flag

    body = {}
    try:
        res = requests.post(base_url + "/register", json={
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
        res = requests.post(base_url + "/login", json={
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
        res = requests.post(base_url + "/data", json={
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

def check_upload_file_endpoint(base_url):
    try:
        a = str(uuid.uuid4())
        b = str(uuid.uuid4())

        fake_file = io.BytesIO(a.encode())
        fake_file_bytes = io.BytesIO(fake_file.getvalue())
        files = {"file": (str(uuid.uuid4()), fake_file_bytes, "text/plain")}

        url = base_url + f"/upload?filename={b}"
        res = requests.post(url, files=files)
        body = res.json()
        assert body['filename'] == b
        assert body['content'] == a
    except:
        return (
            False,
            {
                "message": "failed to get desired response from upload file endpoint"
            }
        )
    try:
        url = base_url + f"/upload?filename=ping"
        res = requests.post(url)
        body = res.json()
        assert body['filename'] == "ping"
        assert body['content'] == "pong"
    except:
        return (
            False,
            {
                "message": "failed to get initial file from upload file endpoint"
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
    flag = flags[0]["value"]
    
    base_url = f'http://{ip}:8000'
    result_check_regular_user = check_regular_user(base_url)
    if not result_check_regular_user[0]:
        return result_check_regular_user
    
    result_check_admin = check_admin(base_url, flag)
    if not result_check_admin[0]:
        return result_check_admin

    result_check_upload_file_endpoint = check_upload_file_endpoint(base_url)
    if not result_check_upload_file_endpoint[0]:
        return result_check_upload_file_endpoint

    return (
        True,
        {
            "message": "OK"
        }
    )

#print(check_regular_user('localhost'))
#print(check_admin('localhost', 'LKSN{PLACEHOLDER}'))
#print(check_upload_file_endpoint('localhost'))
#print(main(
#    [{'detail': {
#        'checker': {
#            'ip': 'localhost',
#            'username': '',
#            'private_key': '',
#            'instance_id': '',
#        },
#        'stack_name': ''
#    }}],
#    [{'value': 'LKSN{PLACEHOLDER}'}],
#    None
#))