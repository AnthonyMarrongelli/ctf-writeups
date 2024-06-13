# Super Duper Quick Maths

Solve my math test and you'll get my flag!

nc 167.99.118.184 31340

## Challenge

The challenge server is not up anymore but the server spit out some text along the lines of `solve these 50 math problems`.

Using python we can easily automate this and get the flag.

Script:

```python
from pwn import *

p = remote('0.cloud.chals.io', 15072)
#Recv all the garbage
p.recvuntil(b'GO!')

#Solve 50 equations
for i in range(50):
    p.recvuntil(b'\n')
    equation = p.recvuntil(b'\n')[:-1].decode()
    solution = eval(equation)
    #Logging the equations and answer
    log.info("{} = {}".format(equation, solution))
    p.sendline(str(solution).encode())

p.interactive()
```

Running the script it will solve the 50 equations and at the end receive the flag.

## Flag

`SIVBGR{L00kM0m!_ICANDO_m4th}`