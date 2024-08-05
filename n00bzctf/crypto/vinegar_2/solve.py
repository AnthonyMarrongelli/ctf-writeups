alphanumerical = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(){}_?'
matrix = []

# Create the matrix
for i in alphanumerical:
    matrix.append([i])

idx = 0
for i in alphanumerical:
    matrix[idx][0] = (alphanumerical[idx:len(alphanumerical)] + alphanumerical[0:idx])
    idx += 1

#Given key and encrypted text
encrypted = "*fa4Q(}$ryHGswGPYhOC{C{1)&_vOpHpc2r0({"
key = '5up3r_s3cr3t_k3y_f0r_1337h4x0rs_r1gh7?'

# Generate key_arr
key_arr = []
for y in key:
    for i in range(len(alphanumerical)):
        if matrix[i][0][0] == y:
            key_arr.append(i)


# Decrypt the text
flag_arr = []
for i in range(len(encrypted)):
    encrypted_char = encrypted[i]
    key_index = key_arr[i]
    for row in matrix:
        if row[0][key_index] == encrypted_char:
            flag_arr.append(alphanumerical[matrix.index(row)])

flag = ''.join(flag_arr)
print(flag)