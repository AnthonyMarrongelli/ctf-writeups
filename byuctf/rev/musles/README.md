# Musles

Here's another binary to test your rev musles!! Let's see how you do :)

## Challenge

When running the binary I got some issues so I just jumped straight into disassembly.

The main function extracted:
```c
undefined8 main(void)

{
  int iVar1;
  code *__dest;
  ulong local_10;
  
  alarm(10);
  __dest = (code *)mmap((void *)0x0,0xf1,7,0x22,-1,0);
  if (__dest == (code *)0xffffffffffffffff) {
    perror("Error mapping memory");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  iVar1 = system("pidof gdb > /dev/null");
  if (iVar1 == 0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  memcpy(__dest,&DAT_00104060,0xf1);
  for (local_10 = 0; local_10 < 0xf1; local_10 = local_10 + 1) {
    __dest[local_10] = (code)((byte)__dest[local_10] ^ 0x20);
  }
  (*__dest)();
  iVar1 = munmap(__dest,0xf1);
  if (iVar1 == -1) {
    perror("Error unmapping memory");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  return 0;
}
```

So looking at it, it looks like it just makes room for some code and then brings some code in from `DAT_00104060` and xors each byte by 0x20. Looking back at it now it also looks like the program attempts to keep gdb from running.

First thing I did was grab all of the code out of `DAT_00104060`, slap it in cyberchef and xor each byte by 0x20.

Result:
```
48 c7 c0 00 00 00 00 48 c7 c7 00 00 00 00 48 89 e6 48 c7 c2 26 00 00 00 0f 05 48 b8 81 3a f2 18 e9 59 b4 86 48 b9 e3 43 87 7b 9d 3f cf f3 48 31 0c 24 48 39 04 24 0f 85 a5 00 00 00 5b 48 b8 8a 39 fd 12 9e b7 7e ee 48 b9 f8 66 ba 56 dc e8 0d 85 48 31 0c 24 48 39 04 24 0f 85 82 00 00 00 5b 48 b8 a3 6a 58 d7 d2 77 6a d2 48 b9 ca 06 34 a4 8d 16 18 b7 48 31 0c 24 48 39 04 24 75 63 5b 48 b8 46 dc c7 42 06 15 67 84 48 b9 19 ae a2 23 6a 79 1e db 48 31 c8 48 39 04 24 75 45 5b 48 b8 c6 7c e3 c7 fc 14 00 00 48 b9 b5 0b 8c ab 90 69 00 00 48 31 0c 24 48 39 04 24 75 26 5b 48 c7 c0 01 00 00 00 48 c7 c7 01 00 00 00 48 be 43 6f 72 72 65 63 74 21 56 48 89 e6 48 c7 c2 08 00 00 00 0f 05 48 c7 c0 3c 00 00 00 48 c7 c7 00 00 00 00 0f 05
```

So I figured if the program was trying to call this code, I'll just compile it like shellcode and we can debug it.

```c
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>

unsigned char shellcode[] = "\x48\xc7\xc0\x00\x00\x00\x00\x48\xc7\xc7\x00\x00\x00\x00\x48\x89\xe6\x48\xc7\xc2\x26\x00\x00\x00\x0f\x05\x48\xb8\x81\x3a\xf2\x18\xe9\x59\xb4\x86\x48\xb9\xe3\x43\x87\x7b\x9d\x3f\xcf\xf3\x48\x31\x0c\x24\x48\x39\x04\x24\x0f\x85\xa5\x00\x00\x00\x5b\x48\xb8\x8a\x39\xfd\x12\x9e\xb7\x7e\xee\x48\xb9\xf8\x66\xba\x56\xdc\xe8\x0d\x85\x48\x31\x0c\x24\x48\x39\x04\x24\x0f\x85\x82\x00\x00\x00\x5b\x48\xb8\xa3\x6a\x58\xd7\xd2\x77\x6a\xd2\x48\xb9\xca\x06\x34\xa4\x8d\x16\x18\xb7\x48\x31\x0c\x24\x48\x39\x04\x24\x75\x63\x5b\x48\xb8\x46\xdc\xc7\x42\x06\x15\x67\x84\x48\xb9\x19\xae\xa2\x23\x6a\x79\x1e\xdb\x48\x31\xc8\x48\x39\x04\x24\x75\x45\x5b\x48\xb8\xc6\x7c\xe3\xc7\xfc\x14\x00\x00\x48\xb9\xb5\x0b\x8c\xab\x90\x69\x00\x00\x48\x31\x0c\x24\x48\x39\x04\x24\x75\x26\x5b\x48\xc7\xc0\x01\x00\x00\x00\x48\xc7\xc7\x01\x00\x00\x00\x48\xbe\x43\x6f\x72\x72\x65\x63\x74\x21\x56\x48\x89\xe6\x48\xc7\xc2\x08\x00\x00\x00\x0f\x05\x48\xc7\xc0\x3c\x00\x00\x00\x48\xc7\xc7\x00\x00\x00\x00\x0f\x05";

int main() {
    (*(void(*)()) shellcode)();
    return 0;
}
```

After compiling it, I opened it up with gdb and began looking at the disassembly.

```
   0x0000555555558020 <+0>:     mov    rax,0x0
   0x0000555555558027 <+7>:     mov    rdi,0x0
   0x000055555555802e <+14>:    mov    rsi,rsp
   0x0000555555558031 <+17>:    mov    rdx,0x26
   0x0000555555558038 <+24>:    syscall
   0x000055555555803a <+26>:    movabs rax,0x86b459e918f23a81
   0x0000555555558044 <+36>:    movabs rcx,0xf3cf3f9d7b8743e3
   0x000055555555804e <+46>:    xor    QWORD PTR [rsp],rcx
   0x0000555555558052 <+50>:    cmp    QWORD PTR [rsp],rax
   0x0000555555558056 <+54>:    jne    0x555555558101 <shellcode+225>
   0x000055555555805c <+60>:    pop    rbx
   0x000055555555805d <+61>:    movabs rax,0xee7eb79e12fd398a
   0x0000555555558067 <+71>:    movabs rcx,0x850de8dc56ba66f8
   0x0000555555558071 <+81>:    xor    QWORD PTR [rsp],rcx
   0x0000555555558075 <+85>:    cmp    QWORD PTR [rsp],rax
   0x0000555555558079 <+89>:    jne    0x555555558101 <shellcode+225>
   0x000055555555807f <+95>:    pop    rbx
   0x0000555555558080 <+96>:    movabs rax,0xd26a77d2d7586aa3
   0x000055555555808a <+106>:   movabs rcx,0xb718168da43406ca
   0x0000555555558094 <+116>:   xor    QWORD PTR [rsp],rcx
   0x0000555555558098 <+120>:   cmp    QWORD PTR [rsp],rax
   0x000055555555809c <+124>:   jne    0x555555558101 <shellcode+225>
   0x000055555555809e <+126>:   pop    rbx
   0x000055555555809f <+127>:   movabs rax,0x8467150642c7dc46
   0x00005555555580a9 <+137>:   movabs rcx,0xdb1e796a23a2ae19
   0x00005555555580b3 <+147>:   xor    rax,rcx
   0x00005555555580b6 <+150>:   cmp    QWORD PTR [rsp],rax
   0x00005555555580ba <+154>:   jne    0x555555558101 <shellcode+225>
   0x00005555555580bc <+156>:   pop    rbx
   0x00005555555580bd <+157>:   movabs rax,0x14fcc7e37cc6
   0x00005555555580c7 <+167>:   movabs rcx,0x6990ab8c0bb5
   0x00005555555580d1 <+177>:   xor    QWORD PTR [rsp],rcx
   0x00005555555580d5 <+181>:   cmp    QWORD PTR [rsp],rax
   0x00005555555580d9 <+185>:   jne    0x555555558101 <shellcode+225>
   0x00005555555580db <+187>:   pop    rbx
   0x00005555555580dc <+188>:   mov    rax,0x1
   0x00005555555580e3 <+195>:   mov    rdi,0x1
   0x00005555555580ea <+202>:   movabs rsi,0x2174636572726f43
   0x00005555555580f4 <+212>:   push   rsi
   0x00005555555580f5 <+213>:   mov    rsi,rsp
   0x00005555555580f8 <+216>:   mov    rdx,0x8
   0x00005555555580ff <+223>:   syscall
   0x0000555555558101 <+225>:   mov    rax,0x3c
   0x0000555555558108 <+232>:   mov    rdi,0x0
   0x000055555555810f <+239>:   syscall
   0x0000555555558111 <+241>:   add    BYTE PTR [rax],al
```
Poking around with the values in rcx and rax, I noticed the xor and decided to xor the two values together and what do you know:
```
0x86b459e918f23a81 ^ 0xf3cf3f9d7b8743e3 = u{ftcuyb
```

Continuing to xor each time theres a pair of rcx and rax, as well as fixing the endianess, I ended up with this:
```
byuctf{u
r_GDB_sk
ills_are
_really_
swoll}
```

## Flag

`byuctf{ur_GDB_skills_are_really_swoll}`
