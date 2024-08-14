from Crypto.Util.number import bytes_to_long
import random
import time

# This app is just for generating random number
# I don't care what's the number anyway :P

try:
    flag = open('flag/flag.txt', 'rb').read()
except:
    print('flag missing')
    exit(1)

random.seed(int(time.time()))
x = random.getrandbits(8 * len(flag))
y =  x ^ bytes_to_long(flag)

print(y)