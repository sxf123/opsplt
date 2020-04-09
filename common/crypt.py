from Crypto.Cipher import AES
from binascii import b2a_hex,a2b_hex

def pad(text):
    text = text.encode()
    while len(text) % 16 != 0:
        text += b"\x00"
    return text

def encrypt(key,text):
    aes = AES.new(key.encode(),AES.MODE_ECB)
    encrypt_str = aes.encrypt(pad(text))
    return b2a_hex(encrypt_str).decode('utf-8')

def decrypt(key,text):
    aes = AES.new(key.encode(),AES.MODE_ECB)
    return aes.decrypt(a2b_hex(text)).decode('utf-8').strip('\x00')
