from pwn import *
import gmpy2
from Crypto.Util.number import inverse

conn = remote('10.0.32.56', 10003)
conn.sendlineafter(b'>> ', b'aaa')
n = int(conn.recvuntil(b'\n')[len('The public key: '):-1].decode())

while not gmpy2.iroot(n, 2)[1]:
    conn.sendlineafter(b'>> ', b'2')
    n = int(conn.recvuntil(b'\n')[len('The public key: '):-1].decode())

    res = conn.recvuntil(b'\n').strip()
    if res == b'out of primes':
        conn.close()
        conn = remote('10.0.32.56', 10003)
        conn.sendlineafter(b'>> ', b'aaa')
        n = int(conn.recvuntil(b'\n')[len('The public key: '):-1].decode())
        n = 2

def get_private_key(e, p, q):
    if p == q:
        return inverse(e, p * (p - 1))
    return inverse(e, (p - 1) * (q - 1))

p = gmpy2.iroot(n, 2)[0]
d = get_private_key(0x10001, p, p)

conn.sendlineafter(b'>> ', b'3')
conn.recvuntil(b'\n')
captcha = int(conn.recvuntil(b'\n').strip(), 16)
res = pow(captcha, d, n)
conn.sendlineafter(b'Enter the signature: ', str(res).encode())
conn.interactive()