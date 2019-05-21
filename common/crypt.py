from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex

def pad(text):
    while len(text) < 16:
        text += " "
    return text

def encrypt(key,text):
    aes = AES.new(key.encode(),AES.MODE_ECB)
    encrypt_str = aes.encrypt(pad(text).encode())
    return b2a_hex(encrypt_str).decode('utf-8')

def decrypt(key,text):
    aes = AES.new(key.encode(),AES.MODE_ECB)
    return aes.decrypt(a2b_hex(text)).decode('utf-8').strip()
