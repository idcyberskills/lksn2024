from typing import List, TypedDict, Dict, Tuple, Any
import datetime
from pwn import *

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

def regis_participant(io, name,age,category):
    io.sendlineafter(b": ",b"1")
    io.sendlineafter(b": ",str(name).encode())
    io.sendlineafter(b": ",str(age).encode())
    io.sendlineafter(b": ",str(category).encode())

def view_participant(io, id):
    io.sendlineafter(b": ",b"2")
    io.sendlineafter(b": ",str(id).encode())

def delete_participant(io, id):
    io.sendlineafter(b": ",b"3")
    io.sendlineafter(b": ",str(id).encode())

def edit_participant(io, id,name,age,category):
    io.sendlineafter(b": ",b"4")
    io.sendlineafter(b": ",str(id).encode())
    io.sendlineafter(b": ",str(name).encode())
    io.sendlineafter(b": ",str(age).encode())
    io.sendlineafter(b": ",str(category).encode())

# true if not error

def check_1(io):
	# io = process("./chall")
	regis_participant(io, "Name Parti for 1",96,"Category Parti for 1")
	view_participant(io, 1)
	data = io.recvuntil(b"--- Competition").decode("utf-8")
	check_data = ["Name: Name Parti for 1","Age: 96","Category: Category Parti for 1"]
	error = 1
	for i in check_data:
		if i not in data:
			return False
	return True

def check_2(io):
	# io = process("./chall")
	regis_participant(io, "Name Parti for 1",96,"Category Parti for 1")
	regis_participant(io, "Name Parti for 2",22,"Category Parti for 2")
	regis_participant(io, "Name Parti for 3",33,"Category Parti for 3")
	delete_participant(io, 1)
	view_participant(io, 1)
	data = io.recvuntil(b"--- Competition").decode("utf-8")
	check_data = ["Name: Name Parti for 2","Age: 22","Category: Category Parti for 2"]
	error = 1
	for i in check_data:
		if i not in data:
			return False
	return True

def check_3(io):
	# io = process("./chall")
	regis_participant(io, "Name Parti for 1",96,"Category Parti for 1")
	edit_participant(io, 1,"Name Parti for 2",22,"Category Parti for 2")
	view_participant(io, 1)
	data = io.recvuntil(b"--- Competition").decode("utf-8")
	check_data = ["Name: Name Parti for 2","Age: 22","Category: Category Parti for 2"]
	error = 1
	for i in check_data:
		if i not in data:
			return False
	return True

def main(services: List[ServiceType], flags: List[FlagType], checker_agent_report: CheckerAgentReport) -> Tuple[bool, Dict]:
    service_detail = services[0]["detail"]

    credentials = service_detail["checker"]
    aws_stack_name = service_detail["stack_name"]
    ip = credentials["ip"]
    username = credentials["username"]
    privkey = credentials["private_key"]
    instance_id = credentials["instance_id"]
    flag = flags[0]["value"]
    port = 11100

    proc = None
    try:
        proc = remote(ip, port)
    except:
        return (
            False,
            {
                "message": "failed to connect to service"
            }
        )
    result_check_1 = check_1(proc)
    proc.close()
    if not result_check_1:
        return (
            False,
            {
                "message": "failed on check 1"
            }
        )
    
    proc = None
    try:
        proc = remote(ip, port)
    except:
        return (
            False,
            {
                "message": "failed to connect to service"
            }
        )
    result_check_2 = check_2(proc)
    proc.close()
    if not result_check_2:
        return (
            False,
            {
                "message": "failed on check 2"
            }
        )
    
    proc = None
    try:
        proc = remote(ip, port)
    except:
        return (
            False,
            {
                "message": "failed to connect to service"
            }
        )
    result_check_3 = check_3(proc)
    proc.close()
    if not result_check_3:
        return (
            False,
            {
                "message": "failed on check 3"
            }
        )

    return (
        True,
        {
            "message": "OK"
        }
    )

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