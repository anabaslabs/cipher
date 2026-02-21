def caesar_encrypt(text: str, key: int) -> dict:
    ciphertext = "".join(
        chr((ord(c) - 65 + key) % 26 + 65) if c.isascii() and c.isupper()
        else chr((ord(c) - 97 + key) % 26 + 97) if c.isascii() and c.islower()
        else c
        for c in text
    )
    return {
        "key": key,
        "ciphertext": ciphertext
    }
