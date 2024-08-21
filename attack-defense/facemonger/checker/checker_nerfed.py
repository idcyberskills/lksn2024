from typing import List, TypedDict, Dict, Tuple, Any
import datetime
import random
import time
import requests
import json


# BASE_URL = "http://54.169.22.114:7744"

def run_testcase(BASE_URL):
    res = requests.get(BASE_URL)
    start_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rand_val = random.randint(5, 15)

    end_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return (
        res.status_code == 200,
        {
            "start_time": start_time,
            "end_time": end_time,
            "duration": rand_val,
            "message": f"Connection: {res.status_code}"
        }
    )

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

def main(services: List[ServiceType], flags: List[FlagType], checker_agent_report: CheckerAgentReport) -> Tuple[bool, Dict]:
    service_detail = services[0]["detail"]

    credentials = service_detail["checker"]
    aws_stack_name = service_detail["stack_name"]
    ip = credentials["ip"]
    username = credentials["username"]
    privkey = credentials["private_key"]
    instance_id = credentials["instance_id"]
    flag = flags[0]["value"]

    base_url = f'http://{ip}:7744'
    return run_testcase(base_url)

#print(run_testcase())
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