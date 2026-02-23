from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import base64


def decrypt(b64_ciphertext: str, hex_key: str) -> dict:
    key_bytes = binascii.unhexlify(hex_key)
    if len(key_bytes) != 16:
        raise ValueError("Key must be exactly 32 hex characters (16 bytes).")

    combined_data = base64.b64decode(b64_ciphertext)

    iv = combined_data[:16]
    ciphertext = combined_data[16:]

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext_bytes = unpad(decrypted_padded, AES.block_size)

    return {
        "key": hex_key,
        "plaintext": plaintext_bytes.decode("utf-8")
    }