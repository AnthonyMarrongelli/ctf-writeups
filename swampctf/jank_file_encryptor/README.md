# Jank File Encryptor

## Overview:

Category: Cryptography

## Description

They say you shouldn't roll your own encryption code, but I think all those naysayers are just gatekeeping!

## Approach

Let's take a look at the encryption code:

```c
if choice == "encrypt":
    # Generate random numbers for the LCG
    seed = random.randint(1, 256)
    a = random.randint(1, 256)
    c = random.randint(1, 256)
    modulus = random.randint(1, 256)

    print(f"Seed: {seed}")
    print(f"A: {a}")
    print(f"C: {c}")
    print(f"Modulus: {modulus}")

    # Pad the file out with some filler bytes to obscure its size
    arr = bytearray(data)
    arr += bytearray([0x41] * 1000)

    save = bytearray()

    # Encrypt the files contents with the LCG
    for i in arr:
        seed = (a * seed + c) % modulus
        save.append(i ^ seed)

    f.close()

    # Write the encrypted file back to the disk
    with open(f"{file_name}.enc", "wb") as binary_file:
        binary_file.write(save)
```

We can see here that an LCG is being used. A random value between 1-256 is used for the increment, the modulus, and the multiplier. We can also see that the tail end of the data to be encrypted is the byte `0x41`. Looking at this, there are two methods that come to mind right away.

1. We can leak the keystream since it is only 256 bytes and we have 1000 `0x41` bytes at the end.
2. We can crack the LCG and retrieve the increment, modulus, and multiplier values.

I chose to go with attack vector 2.
## Attack 2

First order of business would be to get some seeds so we can calculate the increment, modulus, and multiplier values.

```c
ith open("flag.txt.enc", "rb") as binary_file:
    encrypted_flag = binary_file.read()

seeds = []
for i in range(15, 0, -1):
    seeds.append(encrypted_flag[-i] ^ 0x41)
```

We know the last 15 (Actually 1000) values of the encrypted flag are `seed ^ 0x41`. So we can reliable grab some to play with, I chose 15 just for fun but I believe a minimum of around six is needed.

```c
ith open("flag.txt.enc", "rb") as binary_file:
    encrypted_flag = binary_file.read()

seeds = []
for i in range(15, 0, -1):
    seeds.append(encrypted_flag[-i] ^ 0x41)
```

Now we will use some modular arithmetic to find the modulus.

```c
t_n = []
for i in range(len(seeds) - 1):
    t_n.append(seeds[i+1] - seeds[i])

u_n = []
for i in range(len(t_n) - 2):
    u_n.append(abs( t_n[i+2]*t_n[i] - pow(t_n[i+1], 2) ))

modulus = reduce(math.gcd, u_n)
```

I will not go in depth on how these equations are derived but you can try and manipulate the seeds and set up linear equations to come to this conclusion. I will link references in the bottom for those who want to get a better understanding.

```c
multiplier = (seeds[2] - seeds[1]) * inverse(seeds[1] - seeds[0], modulus) % modulus
increment = (seeds[1] - seeds[0]*multiplier) % modulus
```

After correctly identifying the modulus, grabbing the multiplier and increment is trivial.

So now we have successfully grabbed the multipler, increment, and modulus values.
We can now emulate the LCG and decrypt for our flag.

`Full Solve Script`

```c
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
```

Lets run the script:
```
└─$ python solve.py
bytearray(b"It is super important that this flag be kept secret! I wouldn\'t want anyone to find it!!!\r\nThankfully my encryption scheme is simply IMPENETRABLE!!! MUHAHAHAHAHAHAHA\r\n\r\nswampCTF{d0nt_l3ak_ur_k3ystr3am5}")
```

## Flag

swampCTF{d0nt_l3ak_ur_k3ystr3am5}

# References
1. https://tailcall.net/posts/cracking-rngs-lcgs/
2. https://en.wikipedia.org/wiki/Linear_congruential_generator