#Finding the bytes used to xor
flag = bytes.fromhex("134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9")

# Byte representing 'H', 'T', 'B', '{' since the key is 4 bytes
byte1 = ord("H") ^ flag[0]
byte2 = ord('T') ^ flag[1]
byte3 = ord('B') ^ flag[2]
byte4 = ord('{') ^ flag[3]
xorkey = bytes([byte1, byte2, byte3, byte4])
print(f"Xor Key: {xorkey}")

#Using same encryption process to flip bytes again
def encrypt(key, data: bytes) -> bytes:
        xored = b''
        for i in range(len(data)):
            xored += bytes([data[i] ^ key[i % len(key)]])
        return xored
        
        
plaintext = encrypt(xorkey, flag)
print(plaintext)
