from typing import List, TypedDict, Dict, Tuple, Any
import datetime
from pwn import *
import random
from hashlib import sha256
from Crypto.Util.number import inverse

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

def check_user(proc):
    try:
        proc.sendlineafter(b'>> ', b"nahhhh")
    except:
        return (
            False,
            {
                "message": "service faulty",
                "detail_error": "failed to send admin context"
            }
        )

    n = -1
    p = -1
    q = -1
    e = 0x10001
    try:
        res = proc.recvuntil(b'\n')
        n = int(res[len('The public key: '):-1].decode())
    except:
        return (
            False,
            {
                "message": "service faulty",
                "detail_error": "failed to get public key"
            }
        )
    
    i = 0
    while i < 10:
        #print(f'{n = }, {p == q = }')
        i += 1
        try:
            x = random.randint(2, n)
            proc.sendlineafter(b'>> ', b'1')
            proc.sendlineafter(b'Enter your message: ', str(x).encode())
            res = proc.recvuntil(b'\n')
            enc = int(res[len('Encrypted message: '):-1].decode())
            assert enc == pow(x, e, n)
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to encrypt message"
                }
            )

        try:
            proc.sendlineafter(b'>> ', b'3')
            proc.recvuntil(b'Please sign the following captcha\n')
            captcha = int(proc.recvuntil(b'\n').strip().decode(), 16)
            sig = 41414141
            proc.sendlineafter(b'Enter the signature: ', str(sig).encode())
            res = proc.recvuntil(b'\n').decode().strip()
            assert res == 'Invalid signature'
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to login as user"
                }
            )

        try:
            proc.sendlineafter(b'>> ', b'2')
            res = proc.recvuntil(b'\n')
            n = int(res[len('The public key: '):-1].decode())
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to get public key"
                }
            )
        
        try:
            res = proc.recvuntil(b'\n').strip()
            if res == b'out of primes':
                break
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to get menu"
                }
            )
    
    if i < 1:
        return (
            False,
            {
                "message": "service faulty",
                "detail_error": "prime count too few"
            }
        )
    return (
        True,
        {
            "message": "valid"
        }
    )

def get_private_key(e, p, q):
    if p == q:
        return inverse(e, p * (p - 1))
    return inverse(e, (p - 1) * (q - 1))

def check_admin(proc, flag):
    try:
        proc.sendlineafter(b'>> ', sha256(flag.encode()).hexdigest().encode())
    except:
        return (
            False,
            {
                "message": "service faulty",
                "detail_error": "failed to send admin context"
            }
        )
    
    n = -1
    p = -1
    q = -1
    e = 0x10001
    try:
        res = proc.recvuntil(b'\n')
        n = int(res[len('The public key: '):-1].decode())
        res = proc.recvuntil(b'\n')
        p = int(res[len('p = '):-1].decode())
        res = proc.recvuntil(b'\n')
        q = int(res[len('q = '):-1].decode())
    except:
        return (
            False,
            {
                "message": "service faulty",
                "detail_error": "failed to get public key"
            }
        )
    
    i = 0
    while i < 10:
        #print(f'{n = }, {p == q = }')
        i += 1
        try:
            x = random.randint(2, n)
            proc.sendlineafter(b'>> ', b'1')
            proc.sendlineafter(b'Enter your message: ', str(x).encode())
            res = proc.recvuntil(b'\n')
            enc = int(res[len('Encrypted message: '):-1].decode())
            assert enc == pow(x, e, n)
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to encrypt message"
                }
            )

        try:
            proc.sendlineafter(b'>> ', b'3')
            proc.recvuntil(b'Please sign the following captcha\n')
            captcha = int(proc.recvuntil(b'\n').strip().decode(), 16)
            sig = pow(captcha, get_private_key(e, p, q), n)
            proc.sendlineafter(b'Enter the signature: ', str(sig).encode())
            proc.sendline(b'date +%s')
            res = int(proc.recvuntil(b'\n').strip().decode())
            assert res - int(time.time()) <= 1
            proc.sendline(b'exit')
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to login as admin"
                }
            )

        try:
            proc.sendlineafter(b'>> ', b'2')
            res = proc.recvuntil(b'\n')
            n = int(res[len('The public key: '):-1].decode())
            res = proc.recvuntil(b'\n')
            p = int(res[len('p = '):-1].decode())
            res = proc.recvuntil(b'\n')
            q = int(res[len('q = '):-1].decode())
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to get public key"
                }
            )
        
        try:
            res = proc.recvuntil(b'\n').strip()
            if res == b'out of primes':
                break
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to get menu"
                }
            )
        
    if i < 1:
        return (
            False,
            {
                "message": "service faulty",
                "detail_error": "prime count too few"
            }
        )
    return (
        True,
        {
            "message": "valid"
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
    port = 10003
    
    try:
        proc = None
        try:
            proc = remote(ip, port)
        except:
            return (
                False,
                {
                    "message": "service faulty",
                    "detail_error": "failed to connect to service"
                }
            )
        result_check_user = check_user(proc)
        proc.close()
        if not result_check_user[0]:
            return result_check_user

        proc = None
        try:
            proc = remote(ip, port)
        except:
            return (
                False,
                {
                    "message": "not reachable",
                    "detail_error": "failed to connect to service"
                }
            )
        result_check_admin = check_admin(proc, flag)
        if not result_check_admin[0]:
            return result_check_admin

        return (
            True,
            {
                "message": "valid"
            }
        )
    except:
        pass
    return (
        False,
        {
            "message": "service faulty",
            "detail_error": "unexpected error happened"
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