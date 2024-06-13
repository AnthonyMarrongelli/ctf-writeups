from pwn import *

p = remote('0.cloud.chals.io', 15072)
p.recvuntil(b'GO!')

for i in range(50):
    p.recvuntil(b'\n')
    equation = p.recvuntil(b'\n')[:-1].decode()
    solution = eval(equation)
    log.info("{} = {}".format(equation, solution))
    p.sendline(str(solution).encode())
p.interactive()