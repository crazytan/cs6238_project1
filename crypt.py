# helper module for en/decryption

from Crypto.Cipher import AES
from gmpy2 import mpz


# return a byte string key
def get_key(key):
    pass


# encrypt a message with a key
def encrypt(message, key):
    # TODO
    cipher = AES.new(key=get_key(key), mode=AES.MODE_CFB)
    return cipher.encrypt(message)


# decrypt a message with a key
def decrypt(message, key):
    # TODO
    cipher = AES.new(key=get_key(key), mode=AES.MODE_CFB)
    return cipher.decrypt(message)


# a keyed pseudorandom function family
def g(x, key):
    pass


# a keyed pseudorandom permutation function family
def p(x, key):
    # TODO
    return x
