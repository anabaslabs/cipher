from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import base64
import os


def encrypt(plaintext: str, hex_key: str) -> dict:
    key_bytes = binascii.unhexlify(hex_key)
    if len(key_bytes) != 16:
        raise ValueError("Key must be exactly 32 hex characters (16 bytes).")

    iv = os.urandom(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode("utf-8"), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)

    combined_data = iv + ciphertext
    b64_ciphertext = base64.b64encode(combined_data).decode("utf-8")

    return {
        "key": hex_key,
        "ciphertext": b64_ciphertext
    }