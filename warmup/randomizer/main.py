from Crypto.Util.number import getPrime, bytes_to_long

try:
    flag = open('flag/flag.txt', 'rb').read()
except:
    print('flag missing')
    exit(1)

x = int(input('> ').strip())
y = x ^ bytes_to_long(flag)

# should just have return a random number :v
print(y)