import os
import random
from Crypto.Util.number import getPrime
from hashlib import sha256
import time

random.seed(sha256(str(int(time.time())).encode()).digest())
def get_random_bytes(x):
    return random.getrandbits(x*8).to_bytes(x, "big")
primes = [getPrime(512, get_random_bytes) for _ in range(10)]

def gen_pubkey():
    global primes
    p = random.choice(primes)
    q = random.choice(primes)
    n = p*q
    if p in primes: primes.remove(p)
    if q in primes: primes.remove(q)
    return n, p, q

print('Are you an admin?')
admin_context = input('>> ').strip()
is_admin = False
if sha256(open("./flag/flag.txt","rb").read().strip()).hexdigest() == admin_context:
    is_admin = True

e = 0x10001
n, p, q = gen_pubkey()
print("The public key:", n)
if is_admin:
    print(f'{p = }')
    print(f'{q = }')
while len(primes) > 0:
    print("1. Encrypt")
    print("2. Regenerate Public Key")
    print("3. Admin Login")
    print("4. Exit")
    choice = int(input(">> "))
    if choice == 1:
        m = int(input("Enter your message: "))
        if m < n:
            c = pow(m, e, n)
            print(f"Encrypted message: {c}")
        else:
            print("Message too long")
    elif choice == 2:
        n, p, q = gen_pubkey()
        print("The public key:", n)
        if is_admin:
            print(f'{p = }')
            print(f'{q = }')
    elif choice == 3:
        print("Please sign the following captcha")
        captcha = os.urandom(16)
        print(captcha.hex())
        sig = int(input("Enter the signature: "))
        if pow(sig, e, n) == int.from_bytes(captcha, "big"):
            os.system("sh")
        else:
            print("Invalid signature")
    elif choice == 4:
        break
    else:
        print("Invalid choice")

print("out of primes")