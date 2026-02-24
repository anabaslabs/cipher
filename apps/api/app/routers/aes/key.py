import os
import binascii


def generate_key(bits: int = 128) -> str:
    if bits not in (128, 192, 256):
        raise ValueError("AES key bits must be 128, 192, or 256.")
    
    bytes_len = bits // 8
    binary_key = os.urandom(bytes_len)
    return binascii.hexlify(binary_key).decode("utf-8")