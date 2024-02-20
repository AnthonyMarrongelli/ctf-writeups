# aplet321

## Overview:

Category: Reverse Engineering

## What We Have:

```aplet321```
```c
$ file aplet321  
aplet321: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b6322155d8e3d5ecbc678a2697ccce38be0e7c10, for GNU/Linux 3.2.0, not stripped
```

```Dockerfile```
```c
FROM pwn.red/jail

COPY --from=debian@sha256:36a9d3bcaaec706e27b973bb303018002633fd3be7c2ac367d174bafce52e84e / /srv
COPY aplet321 /srv/app/run
COPY flag.txt /srv/app/flag.txt
RUN chmod 755 /srv/app/run
```

## Approach

Let's disassemble aplet321 and have a peak at the code.

After throwing the elf into ghidra we can find the main function:
```c
{
  int iVar1;
  size_t sVar2;
  char *pcVar3;
  int iVar4;
  int iVar5;
  char local_238;
  char acStack_237 [519];
  
  setbuf(stdout,(char *)0x0);
  puts("hi, i\'m aplet321. how can i help?");
  fgets(&local_238,512,stdin);
  sVar2 = strlen(&local_238);
  if (5 < sVar2) {
    iVar4 = 0;
    iVar5 = 0;
    pcVar3 = &local_238;
    do {
      iVar1 = strncmp(pcVar3,"pretty",6);
      iVar5 = iVar5 + (uint)(iVar1 == 0);
      iVar1 = strncmp(pcVar3,"please",6);
      iVar4 = iVar4 + (uint)(iVar1 == 0);
      pcVar3 = pcVar3 + 1;
    } while (pcVar3 != acStack_237 + ((int)sVar2 - 6));
    if (iVar4 != 0) {
      pcVar3 = strstr(&local_238,"flag");
      if (pcVar3 == (char *)0x0) {
        puts("sorry, i didn\'t understand what you mean");
        return 0;
      }
      if ((iVar5 + iVar4 == 54) && (iVar5 - iVar4 == -24)) {
        puts("ok here\'s your flag");
        system("cat flag.txt");
        return 0;
      }
      puts("sorry, i\'m not allowed to do that");
      return 0;
    }
  }
  puts("so rude");
  return 0;
}
```

So just by looking at this we can see our win condition:
```c
pcVar3 = strstr(&local_238,"flag");
      if (pcVar3 == (char *)0x0) {
        puts("sorry, i didn\'t understand what you mean");
        return 0;
}
if ((iVar5 + iVar4 == 54) && (iVar5 - iVar4 == -24)) {
        puts("ok here\'s your flag");
        system("cat flag.txt");
        return 0;
      }
```

So a few things need to be true here:
- "flag" needs to be in our input
- var5 + var4 == 54 and var5 - var4 == -24

Okay, well what are var5 and var4?
```c
iVar1 = strncmp(pcVar3,"pretty",6);
iVar5 = iVar5 + (uint)(iVar1 == 0);

iVar1 = strncmp(pcVar3,"please",6);
iVar4 = iVar4 + (uint)(iVar1 == 0);
````

strcmp here is returning the number of times the identified string is occuring. 

Therefore var5 is count of `prettys` and var4 is count of `please`.





## Attack

So doing some math we get:
```
x + y == 54 and x - y = -24
x = 15, y = 39
payload = (15 * "pretty") + (39 * "please") + "flag"
```

Sending that in:


```text
$ nc chall.lac.tf 31321
hi, i'm aplet321. how can i help?
prettyprettyprettyprettyprettyprettyprettyprettyprettyprettyprettyprettyprettyprettyprettypleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleasepleaseflag
ok here's your flag
lactf{next_year_i'll_make_aplet456_hqp3c1a7bip5bmnc} 
```

## Flag

lactf{next_year_i'll_make_aplet456_hqp3c1a7bip5bmnc} 
