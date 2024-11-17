from random import getrandbits
from math import gcd

def generate_keys(bit_size=1024):
    # Generate public and private keys using RSA
    p, q = generate_prime(bit_size // 2), generate_prime(bit_size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for e
    while gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key

def encrypt(message, key):
    e, n = key
    return ''.join([str(pow(ord(char), e, n)).zfill(8) for char in message])

def decrypt(ciphertext, key):
    d, n = key
    blocks = [ciphertext[i:i + 8] for i in range(0, len(ciphertext), 8)]
    return ''.join([chr(pow(int(block), d, n)) for block in blocks])

def generate_prime(bit_size):
    # Generate a large prime number
    while True:
        prime = getrandbits(bit_size) | 1  # Ensure it's odd
        if is_prime(prime):
            return prime

def is_prime(num, tests=5):
    # Miller-Rabin primality test
    if num < 2:
        return False
    for _ in range(tests):
        a = getrandbits(len(bin(num)[2:])) % (num - 1) + 1
        if pow(a, num - 1, num) != 1:
            return False
    return True
