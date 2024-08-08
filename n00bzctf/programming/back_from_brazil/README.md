# Back From Brazil

I might have dropped a couple of eggs on my way to Brazil. Help me find the most optimal path back home. 

Author: Connor Chang

## Challenge

For this challenge we are again given a netcat connection and a python file:

```python
import random, time

def solve(eggs):
    redactedscript = """
    █ █ █████████
    ██ █ ██

    ███ █ ██ █████████
        ██████████████ █ ██

    ████████ █ ██████████

    ███ █ ██ █████████
        ███ █ ██ █████████
            ██ █ ██ █ ███ █ ██ ██
                ████████

            ██ █ ██ ██
                ████████ █ ████ █ █████
            ██ █ ██ ██
                ████████ █ █████████████ ███████ █ ███

            ████████ ██ ██████████

    ██████ ██████████
    """

    return sum([ord(c) for c in redactedscript])

n = 1000

start = time.time()

for _ in range(10):
    eggs = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.randint(0, 696969))
            print(row[j], end=' ')
        eggs.append(row)
        print()

    solution = solve(eggs)
    print("optimal: " + str(solution) + " 🥚")
    inputPath = input()
    inputAns = eggs[0][0]
    x = 0
    y = 0

    for direction in inputPath:
        match direction:
            case 'd':
                x += 1
            case 'r':
                y += 1
            case _:
                print("🤔")
                exit()

        if x == n or y == n:
            print("out of bounds")
            exit()

        inputAns += eggs[x][y]



    if inputAns < solution:
        print(inputAns)
        print("you didn't find enough 🥚")
        exit()
    elif len(inputPath) < 2 * n - 2:
        print("noooooooooooooooo, I'm still in Brazil")
        exit()

    if int(time.time()) - start > 60:
        print("you ran out of time")
        exit()

print("tnxs for finding all my 🥚")
f = open("/flag.txt", "r")
print(f.read())

```

So I know that looks like alot but lets pick it apart.

At the top we have this weird little `redacted` script:
```python
def solve(eggs):
    redactedscript = """
    █ █ █████████
    ██ █ ██

    ███ █ ██ █████████
        ██████████████ █ ██

    ████████ █ ██████████

    ███ █ ██ █████████
        ███ █ ██ █████████
            ██ █ ██ █ ███ █ ██ ██
                ████████

            ██ █ ██ ██
                ████████ █ ████ █ █████
            ██ █ ██ ██
                ████████ █ █████████████ ███████ █ ███

            ████████ ██ ██████████

    ██████ ██████████
    """

    return sum([ord(c) for c in redactedscript])
```

Which is named "solve". So I guess this was the script that was used to calculate a sum of something:
```python
solution = solve(eggs)
print("optimal: " + str(solution) + " 🥚")
```
We can see that here as this is what calculates the solution for us. We will later learn that this is the maximum amount of eggs that we can achieve given the starting point and constraints.

```python
n = 1000

start = time.time()

for _ in range(10):
    eggs = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.randint(0, 696969))
            print(row[j], end=' ')
        eggs.append(row)
        print()
```
In this code segment, we can see that the program is generating a matrix of 1000x1000 10 times and spitting each out to us, row by row. We will need this later so we can find the path needed to obtain the most eggs.

```python
inputPath = input()
    inputAns = eggs[0][0]
    x = 0
    y = 0

    for direction in inputPath:
        match direction:
            case 'd':
                x += 1
            case 'r':
                y += 1
            case _:
                print("🤔")
                exit()

        if x == n or y == n:
            print("out of bounds")
            exit()

        inputAns += eggs[x][y]
```
Then, here we are asking to input the path traversal starting from (0,0). And while we traverse it adds up the values along the way. If we have successfully given the correct path that maximize the value, we get our flag. We can see that code here:
```python
    if inputAns < solution:
        print(inputAns)
        print("you didn't find enough 🥚")
        exit()
    elif len(inputPath) < 2 * n - 2:
        print("noooooooooooooooo, I'm still in Brazil")
        exit()

    if int(time.time()) - start > 60:
        print("you ran out of time")
        exit()

print("tnxs for finding all my 🥚")
f = open("/flag.txt", "r")
print(f.read())
```
We also see that we have some constraints that we need to get past.

## Script

Alright, lets start to solve this problem. First order of business is going to be receiving the matrix.

```python
matrix = []

#Receiving our matrix
for i in range(1000):
    row_1 = p.recvline()
    string_list = row_1.decode().split()
    integer_list = [int(num) for num in string_list]
    matrix.append(integer_list)
```

Boom, now we have a matrix to work with. Next order of business is finding a algorithm that we can utilize to generate this maximum path.

After a bit of searching I came across a `dynamic programming` solution that finds the maximum sum path. The solution finds the path with the highest sum from the top-left to the bottom-right of a matrix. It keeps track of the best sums for each cell using a separate grid. By always choosing the best option from the left or above, it builds up the best possible path. Then, it traces back the path from the end to the start to show the route taken.

So lets break down this solution:
```python
rows = len(matrix)
cols = len(matrix[0])

# Create a dp array with the same dimensions as matrix
dp = [[0 for _ in range(cols)] for _ in range(rows)]

# Initialize the first cell with the value of the first cell of the matrix
dp[0][0] = matrix[0][0]

# Fill the first row
for j in range(1, cols):
    dp[0][j] = dp[0][j-1] + matrix[0][j]

# Fill the first column
for i in range(1, rows):
    dp[i][0] = dp[i-1][0] + matrix[i][0]

# Fill the rest of the dp array
for i in range(1, rows):
    for j in range(1, cols):
        dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + matrix[i][j]

# The maximum sum path value will be in the bottom-right corner
max_sum = dp[rows-1][cols-1]
```
This part of the code initializes and fills a table (dp) to keep track of the maximum sums for paths through the matrix. First, it creates the dp table with the same dimensions as the matrix and sets the starting cell's value. It then fills the first row and first column of the dp table by adding the values from the matrix to the cumulative sums from the left (for rows) or above (for columns). Finally, for each remaining cell, it calculates the maximum sum by considering the best path coming either from the left or above, adding the current cell's value. The maximum sum path value is found in the bottom-right corner of the dp table.

Now given the max sum, we can backtrack and find the path that was used to get there.
```python
# Reconstruct the path
path_string = ""
i, j = rows - 1, cols - 1
while i > 0 and j > 0:
    if dp[i-1][j] > dp[i][j-1]:
        path_string = "d" + path_string
        i -= 1
    else:
        path_string = "r" + path_string
        j -= 1
while i > 0:
    path_string = "d" + path_string
    i -= 1
while j > 0:
    path_string = "r" + path_string
    j -= 1
```
This part of the code reconstructs the path that results in the maximum sum by backtracking from the bottom-right corner of the matrix to the top-left corner. Starting at the bottom-right corner, it checks whether the best previous step was from above or from the left. 

Putting all these pieces together we can construct the `optimal` path that the program is asking for. I added a marker to keep track of the time that it took for each solve to make sure we didn't meet the time constraint. When I initially solved this challenge, the timer was for 30 seconds and not 60.

Full script:
```python
from pwn import *
import time

p = remote('24.199.110.35', 43298)

def max_value_path(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Create a dp array with the same dimensions as matrix
    dp = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Initialize the first cell with the value of the first cell of the matrix
    dp[0][0] = matrix[0][0]
    
    # Fill the first row
    for j in range(1, cols):
        dp[0][j] = dp[0][j-1] + matrix[0][j]
    
    # Fill the first column
    for i in range(1, rows):
        dp[i][0] = dp[i-1][0] + matrix[i][0]
    
    # Fill the rest of the dp array
    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]) + matrix[i][j]
    
    # The maximum sum path value will be in the bottom-right corner
    max_sum = dp[rows-1][cols-1]
    
    # Reconstruct the path
    path_string = ""
    i, j = rows - 1, cols - 1
    while i > 0 and j > 0:
        if dp[i-1][j] > dp[i][j-1]:
            path_string = "d" + path_string
            i -= 1
        else:
            path_string = "r" + path_string
            j -= 1
    while i > 0:
        path_string = "d" + path_string
        i -= 1
    while j > 0:
        path_string = "r" + path_string
        j -= 1
    
    return max_sum, path_string

#To keep track of time
start = time.time()

#10 iterations
for i in range(10):
    
    matrix = []
    
    #Receiving our matrix
    for i in range(1000):
        row_1 = p.recvline()
        string_list = row_1.decode().split()

        integer_list = [int(num) for num in string_list]

        matrix.append(integer_list)

    #Retrieving the maximum sum and path to get it
    solution, path = max_value_path(matrix)
    log.info(f"Time taken: {time.time() - start}")
    p.sendlineafter(b'optimal:' , path.encode())
    
    #Junk
    p.recvline()

#Receiving flag
p.recvuntil(b'\n')
log.info(f"Flag: {p.recvline().decode()}")
p.close()
```

## Flag

`n00bz{1_g0t_b4ck_h0m3!!!}`