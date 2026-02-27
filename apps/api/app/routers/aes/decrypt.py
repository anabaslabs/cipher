from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
import base64


def decrypt(b64_ciphertext: str, hex_key: str) -> dict:
    key_bytes = binascii.unhexlify(hex_key)
    byte_len = len(key_bytes)
    if byte_len not in (16, 24, 32):
        expected_bits = 128 if byte_len < 20 else 192 if byte_len < 28 else 256
        expected_bytes = expected_bits // 8
        raise ValueError(f"Expected {expected_bytes * 2} hex chars")

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