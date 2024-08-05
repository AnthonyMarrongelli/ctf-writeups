# Numbers 2

Let's see if you can do more than just counting... Part 1 was in n00bzCTF 2023. There are no attachments. Note: There are only 3 different types of questions.

Author: NoobMaster

## Challenge

Only thing we are given for this challenge is the ability to start an instance. Let's start one and see what interaction we get.

```
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10264
Welcome to Numbers 2! Time to step up the game...
Current round: 1 of 100
Give me the least common multiple of 11 and 51: 2
Wrong!
```
So just like that we can already see that the program is just asking us a question and looking for the correct answer. We just need to know how many and what questions are being asked. 

Luckily for us the description tells us that `There are only 3 different types of questions`.

We'll we just found one, lets find the others.

```
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10264
Welcome to Numbers 2! Time to step up the game...
Current round: 1 of 100
Give me the greatest prime factor of 197:
```
```
anthony@pwny:~$ nc challs.n00bzunit3d.xyz 10264
Welcome to Numbers 2! Time to step up the game...
Current round: 1 of 100
Give me the greatest common divisor of 169 and 34:
```

Cool, now we know that we just need to script the calculation and answering of GCD, LCM, and greatest prime factor.

## Script

Here is the script I put together to solve this challenge:
```python
from pwn import *
import math
import sympy

p = remote('challs.n00bzunit3d.xyz', 10264)

#Junk
p.recvline()

for i in range(100):
    
    #Junk
    p.recvline()
    
    #Retrieving prompt    
    p.recvuntil(b'Give me the')
    prompt = p.recvuntil(b'of')
    
    if b'greatest common divisor' in prompt:
        
        #Retrieving operands
        x = int(p.recvuntil(b' and')[:-4])
        y = int(p.recvuntil(b':')[:-1])
        
        #Calculating and sending solution
        solution = math.gcd(x, y)
        log.info(f"GCD({x}, {y}) = {solution}")
        p.sendline(str(solution).encode())
        
    elif b'greatest prime factor' in prompt:
        
        #Retrieving operand
        x = int(p.recvuntil(b':')[:-1].strip())
        
        #Calculating and sending solution
        solution = max(sympy.primefactors(x))
        log.info(f"GPF({x}) = {solution}")
        p.sendline(str(solution).encode())
        
    elif b'least common multiple' in prompt:
        
        #Retrieving operands
        x = int(p.recvuntil(b' and')[:-4])
        y = int(p.recvuntil(b':')[:-1])
        
        #Calculating and sending solution
        solution = abs(x * y) // math.gcd(x, y)
        log.info(f"LCM({x}, {y}) = {solution}")
        p.sendline(str(solution).encode())

p.recvuntil(b': ')
log.info("Flag: {}".format(p.recvuntil(b'\n')[:-1].decode()))
```

## Flag

`n00bz{numb3r5_4r3_fun_7f3d4a_a72f12014c3f}`