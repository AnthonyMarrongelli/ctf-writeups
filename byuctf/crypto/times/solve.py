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

