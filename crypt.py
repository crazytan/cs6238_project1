# helper module for en/decryption

from Crypto.Cipher import AES


def get_key(key):
    # return a byte string key
    pass


def encrypt(message, key):
    # encrypt a message with a key
    cipher = AES.new(key=get_key(key), mode=AES.MODE_CFB)
    return cipher.encrypt(message)


def decrypt(message, key):
    # decrypt a message with a key
    cipher = AES.new(key=get_key(key), mode=AES.MODE_CFB)
    return cipher.decrypt(message)
