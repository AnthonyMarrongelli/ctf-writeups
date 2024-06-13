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