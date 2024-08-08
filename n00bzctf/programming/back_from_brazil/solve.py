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