from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
from pwn import xor

FLAG = open("flag.txt", "rb").read()
FLAG = pad(FLAG, 16)
key = os.urandom(16)

def aes_bcebccbcbecbeb(iv, data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return xor(cipher.encrypt(data), iv)

def encrypt(data, iv=None):
    if iv is None:
        iv = os.urandom(16)
    print(f"IV: {iv.hex()}")
    ct = b""
    for i in range(0, len(data), 16):
        ct += aes_bcebccbcbecbeb(data[i:i+16], iv, key)
        iv = ct[-16:]
    print(f"CT: {ct.hex()}")

while True:
    print("1. Encrypt")
    print("2. Get Flag")
    print("3. Exit")
    choice = int(input(">> "))
    if choice == 1:
        iv = bytes.fromhex(input("IV: "))
        if len(iv) != 16:
            iv = None
        data = bytes.fromhex(input("Msg: "))
        data = pad(data, 16)
        encrypt(data, iv)
    elif choice == 2:
        encrypt(FLAG)
    elif choice == 3:
        break