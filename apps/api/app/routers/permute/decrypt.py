PLAIN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decrypt(text: str, key: str) -> str:
    key = key.upper()
    dec = {key[i]: PLAIN[i] for i in range(26)}
    result = ""
    for ch in text:
        if ch.isascii() and ch.isalpha():
            if ch.isupper():
                result += dec[ch]
            else:
                result += dec[ch.upper()].lower()
        else:
            result += ch
    return {
        "key": key,
        "plaintext": result
    }
