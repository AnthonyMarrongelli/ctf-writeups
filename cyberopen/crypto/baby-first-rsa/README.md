# Baby's First RSA

I learned just learned about RSA and I am pretty sure that I implemented it right. It should be impossible to get my flag.

## Challenge

We are given two files here:

`main.py`
```python
from Crypto.Util.number import bytes_to_long, getPrime
from secret import FLAG

def genRSA():
  e = 3
  while True:
    p = getPrime(512)
    q = getPrime(512)
    phi = (p-1)*(q-1)
    if phi % e:break
  n = p*q
  d = pow(e,-1,phi)
  return (e,n,d)
  
def main():
  e,n,d = genRSA()
  enc_flag = pow(bytes_to_long(FLAG),e,n)
  print("Here is your encrypted flag: " + str(enc_flag))
  print("Here is your public key:")
  print("n: " + str(n))
  print("e: " + str(e))

if __name__ == '__main__': main()
```

`out.txt`
```
Here is your encrypted flag: 11320887921865707970417131707489304941213737344372772560296232001708703523599042195968223212365109776754039820465372975539526543057079098227551678593290445701559045011482149948708333749562432591623529530280037
Here is your public key:
n: 54635592099855565238567429816156089377033822002759547411082764468188951140701492941799814994802894116863539008046955775901349438057474600774506026999322449088884781059206427090047834145264757894872328436141156254487939678497662258017309980269148722038770041654103035346970408674206071958598445348607191506511
e: 3
```

Inspecting the source code we can notice that its standard RSA encryption. We can see that the rsa keys are being generated here:
```python
def genRSA():
  e = 3
  while True:
    p = getPrime(512)
    q = getPrime(512)
    phi = (p-1)*(q-1)
    if phi % e:break
  n = p*q
  d = pow(e,-1,phi)
  return (e,n,d)
```

Now we can notice that e is being set to 3. This gives us the opportunity to execute a low public exponent attack.

Given that the plaintext is expected to be small as its just a one line flag, we can almost certainly take the cube root of the ciphertext to retrieve our plaintext. This is because when we take a small enough plaintext to the power of 3, it most likely will not be large enough to exceed the n value, therefore keeping us from using modulus and reducing the math complexity.

Here's a script that does exactly that and retrieves the flag, note that I like to use my own cube root functions to escape potential headaches:
```python
from Crypto.Util.number import *

def cube_root(n):
    if n < 0:
        return -cube_root(-n)
    low = 0
    high = n
    while low < high:
        mid = (low + high) // 2
        if mid**3 < n:
            low = mid + 1
        else:
            high = mid
    return low if low**3 == n else low - 1

n = 54635592099855565238567429816156089377033822002759547411082764468188951140701492941799814994802894116863539008046955775901349438057474600774506026999322449088884781059206427090047834145264757894872328436141156254487939678497662258017309980269148722038770041654103035346970408674206071958598445348607191506511
e = 3
c = 11320887921865707970417131707489304941213737344372772560296232001708703523599042195968223212365109776754039820465372975539526543057079098227551678593290445701559045011482149948708333749562432591623529530280037
print(long_to_bytes(int(cube_root(c))))
```

## Flag

`SIVBGR{D0nt_F0rg37_T0_P4D!!!}`