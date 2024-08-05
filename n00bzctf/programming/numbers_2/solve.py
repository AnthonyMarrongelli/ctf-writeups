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