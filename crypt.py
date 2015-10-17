# helper module for en/decryption

from Crypto.Cipher import AES
from Crypto import Random
from gmpy2 import mpz


# return a byte string key
def get_key(key):
    key_bit =  key.digits(2)
    key_bit = '0'*(256 - len(key_bit)) + key_bit
    key_byte = ''
    while len(key_bit) > 0:
        key_byte += chr(int(mpz(key_bit[:8], base=2).digits()))
        key_bit = key_bit[8:]
    return key_byte

# encrypt a message with a key
def encrypt(message, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key=get_key(key), mode=AES.MODE_CFB, IV=iv)
    return iv + cipher.encrypt(message)


# decrypt a message with a key
def decrypt(message, key):
    iv = message[:AES.block_size]
    message = message[AES.block_size:]
    cipher = AES.new(key=get_key(key), mode=AES.MODE_CFB, IV=iv)
    return cipher.decrypt(message)


# a keyed pseudorandom function family
def g(x, key):
    pass


# a keyed pseudorandom permutation function family
def p(x, key):
    # TODO
    return x


if __name__ == "__main__":
    message = "This is a message"
    print "Plaintext:"
    print message
    message = encrypt(message, mpz(17))
    print "Encrypted message:"
    print message
    message = decrypt(message, mpz(17))
    print "Decrypted message:"
    print message
