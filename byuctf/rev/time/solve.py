from pwn import *
import time

p = remote('time.chal.cyberjousting.com', 1355)
log.info(int(time.time()))
log.info(p.recvuntil(b'\n').decode())
p.close()