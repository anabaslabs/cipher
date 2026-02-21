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

def clean_playfair_artifacts(text: str) -> str:
    cleaned = []
    i = 0
    while i < len(text):
        if text[i] == 'X' and i > 0 and i < len(text) - 1 and text[i-1] == text[i+1] and text[i-1] != 'X':
            i += 1
            continue
        if text[i] == 'Y' and i > 0 and i < len(text) - 1 and text[i-1] == 'X' and text[i+1] == 'X':
            i += 1
            continue
        cleaned.append(text[i])
        i += 1
    result = ''.join(cleaned)
    if len(result) >= 2:
        if result.endswith('X') and result[-2] != 'X':
            result = result[:-1]
        elif result.endswith('Y') and result[-2] == 'X':
            result = result[:-1]
    return result

def decrypt_digrams(table: list[list[str]], lookup: dict[str, tuple[int, int]], ciphertext: str) -> str:
    chars = [ch for ch in ciphertext.upper() if ch in CHARS]
    if len(chars) % 2 != 0:
        chars.append('X')
    result = []
    for i in range(0, len(chars), 2):
        a, b = chars[i], chars[i + 1]
        ra, ca = lookup[a]
        rb, cb = lookup[b]
        if ra == rb:
            result.append(table[ra][(ca - 1) % 8])
            result.append(table[rb][(cb - 1) % 8])
        elif ca == cb:
            result.append(table[(ra - 1) % 8][ca])
            result.append(table[(rb - 1) % 8][cb])
        else:
            result.append(table[ra][cb])
            result.append(table[rb][ca])
    return ''.join(result)

def decrypt(ciphertext: str, key: str, auto_clean: bool = True) -> dict:
    table, lookup = generate_key_data(key)
    raw_plaintext = decrypt_digrams(table, lookup, ciphertext)
    final_plaintext = clean_playfair_artifacts(raw_plaintext) if auto_clean else raw_plaintext
    return {
        "key": key,
        "plaintext": final_plaintext
    }