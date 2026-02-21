def decrypt(cipher: str, key: str) -> str:
    result = ""
    key = key.upper()
    key_index = 0

    for ch in cipher:
        if ch.isascii() and ch.isalpha():
            shift = ord(key[key_index % len(key)]) - ord("A")

            if ch.isupper():
                result += chr((ord(ch) - ord("A") - shift) % 26 + ord("A"))
            else:
                result += chr((ord(ch) - ord("a") - shift) % 26 + ord("a"))

            key_index += 1
        else:
            result += ch

    return {
        "key": key,
        "plaintext": result
    }
