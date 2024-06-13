# What's Diffie

Alice and Bob have been experimenting with a way to send flags back and forth securely. Can you intercept their messages?

nc 0.cloud.chals.io 32820

## Challenge

When connecting to the server with netcat we are greeted with this:
```
└─$ nc 0.cloud.chals.io 32820
g =  12
p =  53
a =  8
b =  67

What is their shared secret?

Enter your input: 
```

We are given some numbers here to start a diffie-hellman key exchange. We have the public base and public modulus as well as the private keys a and b, typically denoted to Alice and Bob.

We are asked to compute the shared secret, which would be `g` to the power of `a` to the power of `b`, or `g` to the power of `b` to the power of `a`. If you are unfamiliar with diffie-hellman key exchange I suggest reading [this](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange).

Doing that calculation and getting the shared secret `S`, sending it back to the server we get this:
```
To find the flag you will need to perform a bitwise XOR operation between each byte of the encrypted message and the corresponding byte of the shared secret key.

7c 66 79 6d 68 7d 54 1b 70 49 43 1b 48 70 49 5d 1f 42 70 1b 43 1e 4c 1c 70 1b 41 4b 70 4d 1f 4d 52
```

So to obtain the flag we can just xor these values with the shared secret.

Solve script:
```python
from pwn import *
io = remote('0.cloud.chals.io', 32820)

io.recvuntil(b'g =  ')
g = int(io.recvuntil(b'\n')[:-1])
io.recvuntil(b'p =  ')
p = int(io.recvuntil(b'\n')[:-1])
io.recvuntil(b'a =  ')
a = int(io.recvuntil(b'\n')[:-1])
io.recvuntil(b'b =  ')
b = int(io.recvuntil(b'\n')[:-1])

A = pow(g, a, p)
B = pow(g, b, p)
s = pow(B, a, p)

io.sendlineafter(b'Enter your input: ', str(s).encode())

#Receiving junk
for i in range(3):
    io.recvline()

flag = io.recvline()[:-1]
flag_bytes = bytes.fromhex(flag.decode().replace(' ', ''))
flag = bytes([byte ^ s for byte in flag_bytes])
log.info(flag.decode())
```

## Flag

`SIVBGR{4_fl4g_fr0m_4l1c3_4nd_b0b}`