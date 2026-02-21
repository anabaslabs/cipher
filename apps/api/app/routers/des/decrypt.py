from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import binascii
import base64


def decrypt(b64_ciphertext: str, hex_key: str) -> str:
    key_bytes = binascii.unhexlify(hex_key)
    ciphertext = base64.b64decode(b64_ciphertext)

    cipher = DES.new(key_bytes, DES.MODE_ECB)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext_bytes = unpad(decrypted_padded, DES.block_size)

    return {
        "key": hex_key,
        "plaintext": plaintext_bytes.decode("utf-8")
    }