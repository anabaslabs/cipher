import os
import binascii


def generate_key() -> str:
    binary_key = os.urandom(16)
    return binascii.hexlify(binary_key).decode("utf-8")