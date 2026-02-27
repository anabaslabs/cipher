import os
import binascii


def generate_key(b: int = 16) -> str:
    if not (0 <= b <= 255):
        raise ValueError("Key size must be between 0 and 255 bytes.")
    binary_key = os.urandom(b)
    return binascii.hexlify(binary_key).decode("utf-8")