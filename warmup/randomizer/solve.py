from pwn import *
from Crypto.Util.number import long_to_bytes
import random

p = process(['python3', 'main.py'])

y = int(p.recvall().strip().decode())
for i in range(100):
    random.seed(int(time.time()))
    flag = long_to_bytes(y ^ random.getrandbits(8 * i))
    if b'LKSN' in flag:
        print(flag.decode())
        break