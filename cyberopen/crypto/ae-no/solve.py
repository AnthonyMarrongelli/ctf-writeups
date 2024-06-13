from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
#from secret import flag

#Obtaining IV
cipher = AES.new(b'SecretKey1234567', AES.MODE_CBC)
decrypted_block = cipher.decrypt(bytes.fromhex("96a0299d6c60cd0f40218b73ab5fc4b7"))
iv = bytes([x ^ y for x, y in zip(decrypted_block, b'Here is the flag')])
#Decryption
cipher = AES.new(b'SecretKey1234567', AES.MODE_CBC, iv)
print(cipher.decrypt(bytes.fromhex("96a0299d6c60cd0f40218b73ab5fc4b710b8951bd0ed8977a1382328454a2ce68106660bb48808c2fa7a141ac863732f66f9032d00cf2c0ecc3a6871683911a6")))
