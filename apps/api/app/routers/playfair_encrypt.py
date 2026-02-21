import string

CHARS = string.ascii_uppercase + string.digits + "@#%&*()_+-={}[]:;\"'<>,.?! \n\t"

def generate_key_data(key: str) -> tuple[list[list[str]], dict[str, tuple[int, int]]]:
    key = key.upper()
    seen_chars = []
    seen_set = set()
    for ch in key + CHARS:
        if ch in CHARS and ch not in seen_set:
            seen_chars.append(ch)
            seen_set.add(ch)
    table = [seen_chars[i * 8:(i + 1) * 8] for i in range(8)]
    lookup = {ch: (r, c) for r, row in enumerate(table) for c, ch in enumerate(row)}
    return table, lookup

def prepare_text(text: str) -> list[str]:
    filtered = [ch for ch in text.upper() if ch in CHARS]
    digrams = []
    i = 0
    while i < len(filtered):
        a = filtered[i]
        if i + 1 < len(filtered):
            b = filtered[i + 1]
            if a == b:
                filler = 'X' if a != 'X' else 'Y'
                digrams.extend([a, filler])
                i += 1
            else:
                digrams.extend([a, b])
                i += 2
        else:
            filler = 'X' if a != 'X' else 'Y'
            digrams.extend([a, filler])
            i += 1
    return digrams

def encrypt_digrams(table: list[list[str]], lookup: dict[str, tuple[int, int]], digrams: list[str]) -> str:
    result = []
    for i in range(0, len(digrams), 2):
        a, b = digrams[i], digrams[i + 1]
        ra, ca = lookup[a]
        rb, cb = lookup[b]
        if ra == rb:
            result.append(table[ra][(ca + 1) % 8])
            result.append(table[rb][(cb + 1) % 8])
        elif ca == cb:
            result.append(table[(ra + 1) % 8][ca])
            result.append(table[(rb + 1) % 8][cb])
        else:
            result.append(table[ra][cb])
            result.append(table[rb][ca])
    return ''.join(result)

def encrypt(plaintext: str, key: str) -> dict:
    table, lookup = generate_key_data(key)
    digrams = prepare_text(plaintext)
    encrypted_body = encrypt_digrams(table, lookup, digrams)
    return {
        "key": key,
        "ciphertext": encrypted_body
    }