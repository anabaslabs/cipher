PLAIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt(text: str, key: str) -> str:
    key = key.upper()
    enc = {PLAIN[i]: key[i] for i in range(26)}
    result = ""
    for ch in text:
        if ch.isascii() and ch.isalpha():
            if ch.isupper():
                result += enc[ch]
            else:
                result += enc[ch.upper()].lower()
        else:
            result += ch
    return {
        "key": key,
        "ciphertext": result
    }
