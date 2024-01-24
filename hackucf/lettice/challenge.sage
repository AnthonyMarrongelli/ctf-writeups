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