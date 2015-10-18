# helper module for en/decryption

from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto import Random
from gmpy2 import mpz
import gmpy2
import config


# return a byte string from mpz
def get_byte_str_from_mpz(key):
    key_bit = key.digits(2)
    key_bit = '0'*(256 - len(key_bit)) + key_bit
    key_byte = ''
    while len(key_bit) > 0:
        key_byte += chr(int(mpz(key_bit[:8], base=2).digits()))
        key_bit = key_bit[8:]
    return key_byte

# return a bit string
def get_bit_str_from_byte(key):
    bits = []
    for ch in key:
        tmp = ord(ch)
        while tmp > 0:
            bits.append(str(tmp & 1))
            tmp >>= 1
    return ''.join(bits)


# encrypt a message with a key
def encrypt(message, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key=get_byte_str_from_mpz(key), mode=AES.MODE_CFB, IV=iv)
    return iv + cipher.encrypt(message)


# decrypt a message with a key
def decrypt(message, key):
    iv = message[:AES.block_size]
    message = message[AES.block_size:]
    cipher = AES.new(key=get_byte_str_from_mpz(key), mode=AES.MODE_CFB, IV=iv)
    return cipher.decrypt(message)


# a keyed pseudorandom function family
def g(x, key):
    if not config.simple:
        mac = HMAC.new(key=get_byte_str_from_mpz(key), msg=get_byte_str_from_mpz(x)).digest()
        return gmpy2.t_mod(mpz(get_bit_str_from_byte(mac), base=2), config.q)
    return 0


# a keyed pseudorandom permutation function family
def p(x, key):
    if not config.simple:
        pass  # TODO
    return x


# if __name__ == "__main__":
#     # test for encrypt and decrypt
#     message = "This is a message"
#     print "Plaintext:"
#     print message
#     message = encrypt(message, mpz(17))
#     print "Encrypted message:"
#     print message
#     message = decrypt(message, mpz(17))
#     print "Decrypted message:"
#     print message
#
#     # test for g
#     config.init_random()
#     config.generate_prime()
#     print 'g(1,97): ', g(mpz(1), mpz(97))
#     print 'g(2,97): ', g(mpz(2), mpz(97))
#     print 'g(1,87): ', g(mpz(1), mpz(87))
