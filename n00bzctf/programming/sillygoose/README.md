# Sillygoose

There's no way you can guess my favorite number, you silly goose. 

Author: Connor Chang

## Challenge

So we are given a netcat connection and a challenge file:
```python
from random import randint
import time
ans = randint(0, pow(10, 100))
start_time = int(time.time())
turns = 0
while True:
    turns += 1

    inp = input()

    if int(time.time()) > start_time + 60:
       print("you ran out of time you silly goose") 
       break

    if "q" in inp:
        print("you are no fun you silly goose")
        break

    if not inp.isdigit():
        print("give me a number you silly goose")
        continue

    inp = int(inp)
    if inp > ans:
        print("your answer is too large you silly goose")
    elif inp < ans:
        print("your answer is too small you silly goose")
    else:
        print("congratulations you silly goose")
        f = open("/flag.txt", "r")
        print(f.read())

    if turns > 500:
        print("you have a skill issue you silly goose")
```

Reading through the challenge code we can pick out a few important things:

- There is a randomly generated number that we need to guess
- We have 60 seconds to guess the correct number
- We have 500 guesses

Successfully guessing the number gives us the flag.

Given that bit of knowledge we can utilize a search algorithm named `binary search`.

For those unfamiliar with the algorithm, heres the premise:
```
Binary search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing the search interval in half. If the target value is less than the middle element of the interval, the search continues in the lower half, otherwise in the upper half. This process continues until the target value is found or the interval is empty. The time complexity of binary search is O(log n), making it much faster than linear search for large datasets.
```

This algorithm is directly applicable to this problem as we can use the list of numbers from the minimum value to the maximum value as the sorted set we are searching. From there we can break it in half up until we eventually land on the correct number.

## Script

Here is the script I put together to solve this challenge:
```python
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
```

## Flag

`n00bz{y0u_4r3_4_sm4rt_51l1y_g0053}`