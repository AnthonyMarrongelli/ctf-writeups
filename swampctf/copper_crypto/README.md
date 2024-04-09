# Copper Crypto

## Overview:

Category: Cryptography

## Description

I've been learning the new pycryptodome library! I don't know much yet though. Here's my first code to encrypt some text:

## Approach

Let's take a look at the encryption code:

```c
#!/bin/python3

from Crypto.Util.number import *

with open('flag.txt', 'rb') as fin:
	flag = fin.read().rstrip()

pad = lambda x: x + b'\x00' * (500 - len(x))

m = bytes_to_long(pad(flag))

p = getStrongPrime(512)
q = getStrongPrime(512)

n = p * q
e = 3
c = pow(m,e,n)

with open('out.txt', 'w') as fout:
	fout.write(f'n = {n}\n')
	fout.write(f'e = {e}\n')
	fout.write(f'c = {c}\n')
```

Just looking at it we can see that its a pretty standard RSA ctf challenge. The cool thing about this one is that there is a small twist, small enough that it could stump some people.

Normally, RSA with a small e like `3` we would just take the cube root of the ciphertext for the plaintext when n is large enough. Here, the padding makes it so that the ciphertext is too large and loops around n, disrupting the cube root attack.

To solve this we can reduce the ciphertext using some inverse modulus.
```c
pad = lambda x: x + b'\x00' * (500 - len(x))
```
This line right here shows the plaintext being padded to have `\x00` bytes at the end to make it length 500. This is essentially the same as this operation:
```c
bytes_to_long(flag) * pow(256, 500-len(x))
```
This is because padding to the right would be like shifting left eight times.

Now this is exploitable as we can just reverse that multiplication using modular inverse:
```c
inv = inverse(256**(500-i), n) 
real_ciphertext = c * pow(inv, e) % n
```
Now it's important to note that this holds true when `i` is the length of the `flag` here.
## Attack 

So the only thing we really don't know here is the length of the flag. But we can just bruteforce and see if we come up with the ciphertext.

```c
for i in range(120):

    inv = inverse(256**(500-i), n) 
    real_ciphertext = c * pow(inv, e) % n

    for j in range(50):
        if(is_perfect_cube(j*n + real_ciphertext)):
            print(long_to_bytes(int(cube_root(real_ciphertext))))
```

Notice I utilize two cube root functions here: the function to take the cube root, and a function to check if there is a perfect cube root.

I normally import my own cube root functions just because sometimes that can be a headache.

`Full Solve Script`
```c
from Crypto.Util.number import *

def is_perfect_cube(n):
    # Handle negative numbers
    if n < 0:
        n = -n
    low, high = 0, n
    while low <= high:
        mid = (low + high) // 2
        mid_cubed = mid ** 3
        if mid_cubed < n:
            low = mid + 1
        elif mid_cubed > n:
            high = mid - 1
        else:
            return True
    return False

def cube_root(n):
    if n < 0:
        return -cube_root(-n)
    
    low = 0
    high = n
    while low < high:
        mid = (low + high) // 2
        if mid**3 < n:
            low = mid + 1
        else:
            high = mid
    return low if low**3 == n else low - 1

n = 119604938096697044316047691964929805828918626075093639662825464535827900362132954794317391864822750976662931603966282850021396173045319251883406363073183189808699680701857953334587328906486229075428157995555693476599232724728486400143213284483622313607354815609215059406863340823255111036033446109329593686949
e = 3
c = 91149569482452486003218449809382430813144791805261257903556643652008332135606236690176360090659938752235745771493858775509562950906764411011689366104109528195425590415243479424000644174707030408431768079041029193109110970032733391052611637831168097556118005523386390422929265528589660737843901941464809893959

for i in range(120):

    inv = inverse(256**(500-i), n) 
    real_ciphertext = c * pow(inv, e) % n

    for j in range(50):
        if(is_perfect_cube(j*n + real_ciphertext)):
            print(long_to_bytes(int(cube_root(real_ciphertext))))
            exit()
```


Lets run the script:
```
└─$ python solve.py
b'swampCTF{pycryp70d0m3_h45_4_p4dd1n6_func}'
```

## Flag

swampCTF{pycryp70d0m3_h45_4_p4dd1n6_func}

# References
1. https://crypto.stackexchange.com/questions/68976/rsa-padding-risk-of-using-constants
- Note that this reference using an improper equation as in their example they have multiplied by 70 as opposed to the power of 70.