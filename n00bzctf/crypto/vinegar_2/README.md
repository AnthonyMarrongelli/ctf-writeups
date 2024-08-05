# Vinegar 2

Never limit yourself to only alphabets!

Author: NoobMaster

## Challenge

For this one we get a enc.txt file and a chall.py file as follows:
```
*fa4Q(}$ryHGswGPYhOC{C{1)&_vOpHpc2r0({
```
```python
alphanumerical = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(){}_?'
matrix = []
for i in alphanumerical:
	matrix.append([i])

idx=0
for i in alphanumerical:
	matrix[idx][0] = (alphanumerical[idx:len(alphanumerical)]+alphanumerical[0:idx])
	idx += 1

flag=open('../src/flag.txt').read().strip()
key='5up3r_s3cr3t_k3y_f0r_1337h4x0rs_r1gh7?'
assert len(key)==len(flag)
flag_arr = []
key_arr = []
enc_arr=[]
for y in flag:
	for i in range(len(alphanumerical)):
		if matrix[i][0][0]==y:
			flag_arr.append(i)

for y in key:
	for i in range(len(alphanumerical)):
		if matrix[i][0][0]==y:
			key_arr.append(i)

for i in range(len(flag)):
	enc_arr.append(matrix[flag_arr[i]][0][key_arr[i]])
encrypted=''.join(enc_arr)
f = open('enc.txt','w')
f.write(encrypted)
```

So after looking through the code and looking at what each thing does, you'll realize that only one or two things need to be inverted in order to retrieve the plaintext.

```python
for y in flag:
	for i in range(len(alphanumerical)):
		if matrix[i][0][0]==y:
			flag_arr.append(i)

for i in range(len(flag)):
	enc_arr.append(matrix[flag_arr[i]][0][key_arr[i]])
encrypted=''.join(enc_arr)
```

These two bits are the main points that we need to revert. Given the enc_arr, we will be reverting it to the flag since the key and matrix stay the same.

Here is the function that inverts the mappings to retrieve the plaintext.
```python
flag_arr = []
for i in range(len(encrypted)):
    encrypted_char = encrypted[i]
    key_index = key_arr[i]
    for row in matrix:
        if row[0][key_index] == encrypted_char:
            flag_arr.append(alphanumerical[matrix.index(row)])
```

Final script:
```python
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
```

## Flag

`n00bz{4lph4num3r1c4l_1s_n0t_4_pr0bl3m}`