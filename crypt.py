# helper module for en/decryption

from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA
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


# return a bit string from byte string
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
    return iv + cipher.encrypt(message)  # append the initial vector with the encrypted message and returns


# decrypt a message with a key
def decrypt(message, key):
    iv = message[:AES.block_size]  # extract the initial vector
    message = message[AES.block_size:]
    cipher = AES.new(key=get_byte_str_from_mpz(key), mode=AES.MODE_CFB, IV=iv)
    return cipher.decrypt(message)


# a keyed pseudorandom function family
def g(x, key):
    if not config.simple:
        mac = HMAC.new(key=get_byte_str_from_mpz(key), msg=get_byte_str_from_mpz(x)).digest()
        return gmpy2.t_mod(mpz(get_bit_str_from_byte(mac), base=2), config.q)
    return mpz()  # if in simple mode, return 0


# a keyed pseudorandom permutation function family
def p(x, key):
    if not config.simple:
        mac = HMAC.new(key=get_byte_str_from_mpz(key), msg=get_byte_str_from_mpz(x), digestmod=SHA).digest()
        return gmpy2.t_mod(mpz(get_bit_str_from_byte(mac), base=2), config.q)
    return x  # if in simple mode, return x


if __name__ == "__main__":
    # test for encrypt and decrypt
    mock_history = "history1;history2;etc."
    config.init_random()
    for i in xrange(100):
        mock_key = mpz(config.generate_rand())
        history_encrypt = encrypt(mock_history, mock_key)
        history_decrypt = decrypt(history_encrypt, mock_key)
        assert mock_history == history_decrypt, "de/encryption failed!"
