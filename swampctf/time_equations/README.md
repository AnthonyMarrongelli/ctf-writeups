# The Time Equations

## Overview:

Category: Miscellaneous

## Description

I have found the secrets of time travel hidden in 5 linear equations! HOWEVER, they need to be solved within 10 seconds or else the quantumn state of the universe changes and the original equations are no longer valid! Can you do it?

`nc chals.swampctf.com 60001`

## Approach

Looking through the source code as well as connecting to the server, we can see that in order to win here we need to correctly get the values of a, b, c, d, and e,

`Source Code Snippet`
```c
// Fail if one of variables is incorrect
    for(int i = 0; i < 5; i++){
        if(solution[i] != submission[i]) {
            printf("AAaaahhh the time jump failed!!! The solution set must have been wrong!!\n");
            exit(1);
        }
    }
```

And here is what we are greeted with when connecting to the server:
```
└─$ nc chals.swampctf.com 60001               
Quick! These set of linear equations describe the secretes to time travel!
But the quantum state of the universe only gives us 10 mere seconds to solve them!!!

4869*a + 1125*b + 4188*c + 600*d + 8814*e = 52285308
6812*a + 1327*b + 8048*c + 6052*d + 71*e = 93120062
5562*a + 9974*b + 6186*c + 5419*d + 2435*e = 135025902
7903*a + 2911*b + 5897*c + 4170*d + 6445*e = 100122936
246*a + 9056*b + 6556*c + 7278*d + 8082*e = 116364476
a = test
b = c = d = e = AAaaahhh the time jump failed!!! The solution set must have been wrong!!
```

We can clearly see that the program is just looking for us to solve for the values within a time frame:
```c
// Fail if it takes longer then 10 seconds to solve the system
    if((time(0) - time_start) >= 10){
        printf("Aaaah we didn't solve the system fast enough!\n");
        exit(1);
    }
```

## Attack

We will use the powerful tool z3 to take in these equations and spit out the answers.

`Solve Script`
```c
from pwn import *
from z3 import *
import re

p = remote('chals.swampctf.com', 60001)

def grabEquation():
    equation = p.recvline()[:-1].decode()
    coefficients = list(map(int, re.findall(r'-?\d+', equation)))
    return coefficients

p.recvuntil(b'!!!\n\n')

solver = Solver()
a, b, c, d, e = Ints('a b c d e')

for i in range(5):
    a_coeff, b_coeff, c_coeff, d_coeff, e_coeff, constant = grabEquation()
    equation = a_coeff*a + b_coeff*b + c_coeff*c + d_coeff*d + e_coeff*e == constant
    solver.add(equation)

if solver.check() == sat:
    model = solver.model()
    p.sendlineafter(b'a = ', f"{model[a]}".encode())
    p.sendlineafter(b'b = ', f"{model[b]}".encode())
    p.sendlineafter(b'c = ', f"{model[c]}".encode())
    p.sendlineafter(b'd = ', f"{model[d]}".encode())
    p.sendlineafter(b'e = ', f"{model[e]}".encode())
    
print(p.recvline())
```
As you can see here we are using pwntools to connect, grab equations, throw them into z3, and then from there have z3 solve them and spit the answers back into the server.

```
└─$ python solve.py
[+] Opening connection to chals.swampctf.com on port 60001: Done
b'We did it! We have traveled through time! Here is the flag: swampCTF{tim3_trav3l_i5nt_r3al}\n'
[*] Closed connection to chals.swampctf.com port 60001
```

## Flag

swampCTF{tim3_trav3l_i5nt_r3al}

# References
1. https://z3prover.github.io/api/html/z3.html