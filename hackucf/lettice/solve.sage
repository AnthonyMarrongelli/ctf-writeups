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

        #We know first ord will be 104 ("h")
        r = result - (vector([104, x, y]) * pubkey)
        #Now these two are the next two points which should yield ("a") and ("c") which when using ord yields 97 and 99
        original_vector = (result2 - r) * inverse
        original_vector2 = (result3 - r) * inverse

        #Checking if it is "hac" - beginning of hackucf{}, if so decrypt whole file
        if(original_vector[0] == 97 and original_vector2[0] == 99): 

            with open('encrypted.txt', 'r') as file:
                
                for line in file:
                    
                    #Formatting encrypted output
                    point = line.strip("()\n").split(",")
                    result_file = vector([int(point[0]), int(point[1]), int(point[2])])
                    
                    #Printing our flag piece by piece
                    original_char = (result_file - r) * inverse
                    print(chr(original_char[0]), end="")
                    
            exit()
