from Crypto.Util.number import *

def is_perfect_cube(n):
    """
    Check if a given number n is a perfect cube, no matter how big, using binary search.
    
    Returns True if n is a perfect cube, False otherwise.
    """
    # Handle negative numbers
    if n < 0:
        n = -n
    low, high = 0, n
    while low <= high:
        mid = (low + high) // 2
        mid_cubed = mid ** 3
        if mid_cubed < n:
            low = mid + 1
        elif mid_cubed > n:
            high = mid - 1
        else:
            return True
    return False
def cube_root(n):
    """
    Finds the cube root of n using binary search.
    :param n: The number to find the cube root of.
    :return: The cube root of n as an integer.
    """
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

n = 119604938096697044316047691964929805828918626075093639662825464535827900362132954794317391864822750976662931603966282850021396173045319251883406363073183189808699680701857953334587328906486229075428157995555693476599232724728486400143213284483622313607354815609215059406863340823255111036033446109329593686949
e = 3
c = 91149569482452486003218449809382430813144791805261257903556643652008332135606236690176360090659938752235745771493858775509562950906764411011689366104109528195425590415243479424000644174707030408431768079041029193109110970032733391052611637831168097556118005523386390422929265528589660737843901941464809893959

for i in range(120):

    inv = inverse(256**(500-i), n) 
    real_ciphertext = c * pow(inv, e) % n

    for j in range(50):
        if(is_perfect_cube(j*n + real_ciphertext)):
            print(long_to_bytes(int(cube_root(real_ciphertext))))
            exit()