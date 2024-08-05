from pwn import *

p = remote('24.199.110.35', 41199)

#Minimum and Maximum from server code
high = pow(10, 100)
low = 0

while True:

    guess = (high + low) // 2
    log.info(f"Current Guess: {guess}")

    p.sendline(str(guess).encode())
    response = p.recvline().decode()

    #If our guess was too big, we will remove every number greater than the guess
    if 'large' in response:
        high = guess
    #If our guess was too small, we will remove every number smaller than the guess
    elif 'small' in response:
        low = guess
    #We reach here if we have found the correct number
    else:
        log.info(f"Flag: {p.recvline().decode()}")
        exit()