# Lettice

## Overview:

Category: Cryptography

Difficulty: Medium

Flag Format: hackucf{flag_goes_here}

## What We Have:

```challenge.sage```
```c
from random import randint

flag = open('flag.txt').read()
r = open('r.txt').read()
r = r.split(",")
vec = vector([int(r[0]), int(r[1]), int(r[2])])

pubkey = Matrix(ZZ, [
    [32, -45, -65],
    [-19, 86, 70],
    [91, -63, 81]
])

for c in flag:
    v = vector([ord(c), randint(0, 100), randint(0, 100)]) * pubkey + vec
    print(v)
```

```encrypted.txt```
```c
(7283, -3366, 1152)
(2691, -27, -2281)
(7736, -1380, 4630)
(9424, -7175, 83)
(5392, -6069, -6179)
(4904, -75, 1327)
(11170, -6157, 4625)
(7444, -4640, -1350)
(9238, -5135, 1403)
(3551, 210, 2524)
(3656, 3024, 6194)
(4355, -1079, -813)
(9921, -6244, 5954)
(4157, -3720, -4966)
(11432, -9885, 693)
(11861, -8588, 3374)
(968, 5572, 4290)
(5734, -3291, 2027)
(8400, -2641, 4265)
(4608, -2821, -2987)
(4573, -2814, -2244)
(4571, 1034, 1880)
(9003, -4880, 6006)
(4492, 1543, 1557)
(8840, -1543, 6595)
(5100, -4359, -269)
(11389, -8941, 1017)
(3531, -1434, -3644)
(8434, -1158, 9404)
(5066, 290, 1312)
(9571, -4459, 6887)
(9406, -4015, 8723)
(9475, -4562, 2096)
```

## Approach

Lets look at the code:

```c
for c in flag:
    v = vector([ord(c), randint(0, 100), randint(0, 100)]) * pubkey + vec
    print(v)
```

So here we can see that for every letter of our flag, it is being inserted into a vector with random integers for the y and z axis. Following that it is being multiplied by a given matrix, and then a constant vector is added.

Now, when you multiple a vector by a matrix, you can retrieve the given vector by multiplying the resulting vector with the inverse of the given matrix. As for vector addition, `<a, b, c> + <d, e, f>` yields the result `<a + d ,b + e ,c + f>`.

So after establishing those ideas. We can look at the order of operations. `vector * matrix + vector`. Here we can pretty easily recognize that the `vector * matrix` is going to occur first, and then `result + vector` will occur.

## Attack

Knowing what we know we can begin to solve for the flag.

Now we were told the format of the flag was `hackucf{flag_goes_here}`. So we can anticipate what the first value of `vector([ord(c), randint(0, 100), randint(0, 100)])` is going to be.

And we know that the next two values will be a number between 0 and 100 (inclusive). Given that, we can calculate the possible values and see if bruteforce is feasable.
`1 x 101 x 101 = 10,201`, this is a very small number and is definitely bruteforce-able.

```text
Lets manipulate this equation real quick:
v = vector([ord(c), randint(0, 100), randint(0, 100)]) * pubkey + vec

  Note: v is the vector given in our encrypted.txt file and vector([ord(c), randint(0, 100), randint(0, 100)]) is the vector we are trying to find.

vec = v - (vector([ord(c), randint(0, 100), randint(0, 100)]) * pubkey)
```
`solve.sage`
```c
pubkey = Matrix(ZZ, [
    [32, -45, -65],
    [-19, 86, 70],
    [91, -63, 81]
])

inverse = pubkey.inverse()

#First Three Vectors
result = vector([7283, -3366, 1152])
result2 = vector([2691, -27, -2281])
result3 = vector([7736, -1380, 4630])

#Looping through all possible values of rand integers
for x in range(101):
    for y in range(101):

        #We know first ord() value of the vector will always be 104 ("h") for the correct answer, but could also be for an incorrect answer.
        vec = result - (vector([104, x, y]) * pubkey)

        #Now these two are the next two points which should yield ("a") and ("c") which when using ord yields 97 and 99. 
        original_vector = (result2 - vec) * inverse
        original_vector2 = (result3 - vec) * inverse

        #Checking if it is "hac" - beginning of hackucf{}, if so decrypt whole file
        if(original_vector[0] == 97 and original_vector2[0] == 99): 

            with open('encrypted.txt', 'r') as file:
                
                for line in file:
                    
                    point = line.strip("()\n").split(",")
                    result_file = vector([int(point[0]), int(point[1]), int(point[2])])
                    
                    original_char = (result_file - vec) * inverse
                    print(chr(original_char[0]), end="")
                    
            exit()
```



```text
$ sage solve.sage
  hackucf{w31c0me_64ck_f0r_3pr1n9!}
```

## Flag

hackucf{w31c0me_64ck_f0r_3pr1n9!}
