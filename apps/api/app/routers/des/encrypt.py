from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import binascii
import base64


def encrypt(plaintext: str, hex_key: str) -> str:
    key_bytes = binascii.unhexlify(hex_key)
    if len(key_bytes) != 8:
        raise ValueError("Key must be exactly 16 hex characters (8 bytes).")

    cipher = DES.new(key_bytes, DES.MODE_ECB)
    padded_data = pad(plaintext.encode("utf-8"), DES.block_size)
    ciphertext = cipher.encrypt(padded_data)

    return {
        "key": hex_key,
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8")
    }