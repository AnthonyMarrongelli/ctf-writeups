import math
from functools import reduce
from Crypto.Util.number import inverse
import re

with open("flag.txt.enc", "rb") as binary_file:
    encrypted_flag = binary_file.read()

seeds = []
for i in range(15, 0, -1):
    seeds.append(encrypted_flag[-i] ^ 0x41)

t_n = []
for i in range(len(seeds) - 1):
    t_n.append(seeds[i+1] - seeds[i])

u_n = []
for i in range(len(t_n) - 2):
    u_n.append(abs( t_n[i+2]*t_n[i] - pow(t_n[i+1], 2) ))

modulus = reduce(math.gcd, u_n)
multiplier = (seeds[2] - seeds[1]) * inverse(seeds[1] - seeds[0], modulus) % modulus
increment = (seeds[1] - seeds[0]*multiplier) % modulus

for i in range(256):
    seed = i
    a = multiplier
    c = increment

    # Remove the padding bytes
    arr = bytearray(encrypted_flag)
    save = bytearray()

    # Decrypt the files contents with the LCG
    for i in arr:
        seed = (a * seed + c) % modulus
        save.append(i ^ seed)
        if re.search(br"swampCTF{.*?}", save):
            print(save)
            break
            