from Crypto.Util.number import bytes_to_long, getPrime
import random
flag = bytes_to_long(open("flag.txt", "rb").read())
p,q = getPrime(512), getPrime(512)
n = p*q
e = 3

c = pow(2**24 * flag + random.randint(1, 2**21), e, n)
c2 = pow(2**24 * flag + random.randint(1, 2**21), e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
print(f"c2 = {c2}")
