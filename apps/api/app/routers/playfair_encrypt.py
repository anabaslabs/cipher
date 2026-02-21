import string

CHARS = string.ascii_uppercase + string.digits


def generate_key_table(key: str) -> list[list[str]]:
    key = key.upper()
    seen = []
    for ch in key:
        if ch in CHARS and ch not in seen:
            seen.append(ch)
    for ch in CHARS:
        if ch not in seen:
            seen.append(ch)
    return [seen[i * 6:(i + 1) * 6] for i in range(6)]


def get_position(table, ch):
    for r, row in enumerate(table):
        if ch in row:
            return r, row.index(ch)
    raise ValueError(f"Character '{ch}' not in table.")


def prepare_alpha(alpha_str: str) -> tuple[list[str], list[int]]:
    filtered = list(alpha_str)
    digrams = []
    filler_positions = []
    i = 0
    while i < len(filtered):
        a = filtered[i]
        if i + 1 < len(filtered):
            b = filtered[i + 1]
            if a == b:
                filler = '9' if a == 'X' else 'X'
                digrams.append(a)
                filler_positions.append(len(digrams))
                digrams.append(filler)
                i += 1
            else:
                digrams.extend([a, b])
                i += 2
        else:
            filler = '9' if a == 'X' else 'X'
            digrams.append(a)
            filler_positions.append(len(digrams))
            digrams.append(filler)
            i += 1
    return digrams, filler_positions


def encrypt_digrams(table, digrams: list[str]) -> str:
    result = []
    for i in range(0, len(digrams), 2):
        a, b = digrams[i], digrams[i + 1]
        ra, ca = get_position(table, a)
        rb, cb = get_position(table, b)
        if ra == rb:
            result.append(table[ra][(ca + 1) % 6])
            result.append(table[rb][(cb + 1) % 6])
        elif ca == cb:
            result.append(table[(ra + 1) % 6][ca])
            result.append(table[(rb + 1) % 6][cb])
        else:
            result.append(table[ra][cb])
            result.append(table[rb][ca])
    return ''.join(result)


def encrypt(plaintext: str, key: str) -> tuple[str, dict]:
    table = generate_key_table(key)
    upper = plaintext.upper()

    non_alpha = {}
    alpha_chars = []
    alpha_positions = []

    for i, ch in enumerate(upper):
        if ch in CHARS:
            alpha_chars.append(ch)
            alpha_positions.append(i)
        else:
            non_alpha[str(i)] = plaintext[i]

    digrams, filler_positions = prepare_alpha(''.join(alpha_chars))
    encrypted_body = encrypt_digrams(table, digrams)

    meta = {
        "non_alpha": non_alpha,
        "alpha_positions": alpha_positions,
        "filler_positions": filler_positions,
        "original_length": len(plaintext)
    }

    return {
        "key": key,
        "ciphertext": encrypted_body,
        "meta": meta
    }
