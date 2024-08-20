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

f = 0
for i, z in enumerate(flag[::-1]):
    f += (256**i) * z

x = random.getrandbits(8 * len(flag))
y =  x ^ f

print(y)