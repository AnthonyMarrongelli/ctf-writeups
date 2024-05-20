# Times

It's just multiplication... right?

## Challenge

So we are given:
```python
import hashlib
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from ellipticcurve import * # I'll use my own library for this
from base64 import b64encode
import os
from Crypto.Util.number import getPrime

def encrypt_flag(shared_secret: int, plaintext: str):
    iv = os.urandom(AES.block_size)

    #get AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    #encrypt flag
    plaintext = pad(plaintext.encode('ascii'), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    return { "ciphertext" : b64encode(ciphertext), "iv" : b64encode(iv) }
    
def main():
    the_curve = EllipticCurve(13, 245, getPrime(128))
    start_point = None
    while start_point is None:
        x = getPrime(64)
        start_point = the_curve.point(x)
    print("Curve: ", the_curve)
    print("Point: ", start_point)
    new_point = start_point * 1337

    flag = "byuctf{REDACTED}"
    print(encrypt_flag(new_point.x, flag))

if __name__ == "__main__":
    main()

```
as well as the [output](./times.txt).

Here's an elliptical curve challenge, thankfully its just a simple multiplication trick and not anything that really requires ECC knowledge.

We're given the starting point in our output and we need that multiplied by 1337 in order to decrypt our flag. But the trick here is that its not simple multiplication because we are dealing with a point on the curve. So to get around this confusion we will use an ECC library and perform the multiplication there.

Scripted:
```python
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from ecdsa.ellipticcurve import CurveFp, Point
from ecdsa.numbertheory import inverse_mod

flag = b'SllGMo5gxalFG9g8j4KO0cIbXeub0CM2VAWzXo3nbIxMqy1Hl4f+dGwhM9sm793NikYA0EjxvFyRMcU2tKj54Q=='
iv = b'MWkMvRmhFy2vAO9Be9Depw=='

def decrypt_flag(shared_secret: int, encrypted_data, iv):
    ciphertext = b64decode(encrypted_data)
    iv = b64decode(iv)

    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_plaintext = cipher.decrypt(ciphertext)
    decrypted_plaintext = unpad(decrypted_plaintext, AES.block_size)
    return decrypted_plaintext.decode('ascii')

p = 335135809459196851603485825030548860907

# y^2 = x^3 + 13x + 245
a = 13
b = 245
curve = CurveFp(p, a, b)

# point coordinates
x = 14592775108451646097
y = 237729200841118959448447480561827799984
point = Point(curve, x, y)
scalar = 1337
result_point = point * scalar
print(decrypt_flag(result_point.x(), flag, iv))
```

Using a simple ECC library from python we can retrieve the multiplied point and then by tweaking the encryption function we can easily decrypt for our flag.
```
└─$ python solve.py 
byuctf{mult1pl1c4t10n_just_g0t_s0_much_m0r3_c0mpl1c4t3d}
```

## Flag

`byuctf{mult1pl1c4t10n_just_g0t_s0_much_m0r3_c0mpl1c4t3d}`