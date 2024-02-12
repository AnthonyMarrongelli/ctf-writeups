# xorxorxor

## Overview:

Category: Cryptography

Difficulty: Easy

## What We Have:

```challenge.py```
```c
#!/usr/bin/python3
import os
flag = open('flag.txt', 'r').read().strip().encode()

class XOR:
    def __init__(self):
        self.key = os.urandom(4)
        
    def encrypt(self, data: bytes) -> bytes:
        xored = b''
        for i in range(len(data)):
            xored += bytes([data[i] ^ self.key[i % len(self.key)]])
        return xored
    
    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)

def main():
    global flag
    crypto = XOR()
    print ('Flag:', crypto.encrypt(flag).hex())

if __name__ == '__main__':
    main()

```

We have an encryption program that generates a random 4 byte long key, then uses that key to encrypt the data.

```output.txt```
```c
Flag: 134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9
```


## Approach

So four bytes is relatively small for a key, and we can actually anticipate the first four bytes of our flag: `HTB{`

When we have a xor operation, for example: `a xor b = c`, you can revert this by `c xor b = a`. Which is essentially flipping the bits twice, giving you the original byte. 

So we can use our plaintext to xor with the ciphertext in order to obtain the 4 byte key. Then using that key we can recover the entire flag.


## Attack

Script for decryption:

```solve.py```
```c
#Finding the bytes used to xor
flag = bytes.fromhex("134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9")

# Byte representing 'H', 'T', 'B', '{' since the key is 4 bytes
byte1 = ord("H") ^ flag[0]
byte2 = ord('T') ^ flag[1]
byte3 = ord('B') ^ flag[2]
byte4 = ord('{') ^ flag[3]
xorkey = bytes([byte1, byte2, byte3, byte4])
print(f"Xor Key: {xorkey}")

#Using same encryption process to flip bytes again
def encrypt(key, data: bytes) -> bytes:
        xored = b''
        for i in range(len(data)):
            xored += bytes([data[i] ^ key[i % len(key)]])
        return xored
        
        
plaintext = encrypt(xorkey, flag)
print(plaintext)
```
Running this script we get:

```text
$ python solve.py
  Xor Key: b'[\x1e\xb4\x9a'
  b'HTB{rep34t3d_x0r_n0t_s0_s3cur3}' 
```

## Flag

HTB{rep34t3d_x0r_n0t_s0_s3cur3}
