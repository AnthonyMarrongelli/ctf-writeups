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