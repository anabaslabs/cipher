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


def decrypt_digrams(table, ciphertext: str) -> str:
    chars = [ch for ch in ciphertext.upper() if ch in CHARS]
    if len(chars) % 2 != 0:
        raise ValueError("Ciphertext has odd number of valid characters.")
    result = []
    for i in range(0, len(chars), 2):
        a, b = chars[i], chars[i + 1]
        ra, ca = get_position(table, a)
        rb, cb = get_position(table, b)
        if ra == rb:
            result.append(table[ra][(ca - 1) % 6])
            result.append(table[rb][(cb - 1) % 6])
        elif ca == cb:
            result.append(table[(ra - 1) % 6][ca])
            result.append(table[(rb - 1) % 6][cb])
        else:
            result.append(table[ra][cb])
            result.append(table[rb][ca])
    return ''.join(result)


def remove_fillers(decrypted_chars: list[str], filler_positions: list[int]) -> list[str]:
    result = []
    filler_set = set(filler_positions)
    for i, ch in enumerate(decrypted_chars):
        if i not in filler_set:
            result.append(ch)
    return result


def decrypt(ciphertext: str, key: str, meta: dict) -> str:
    table = generate_key_table(key)

    raw_decrypted = decrypt_digrams(table, ciphertext)
    raw_list = list(raw_decrypted)

    filler_positions = meta["filler_positions"]
    clean_alpha = remove_fillers(raw_list, filler_positions)

    non_alpha = meta["non_alpha"]
    original_length = meta["original_length"]
    alpha_positions = meta["alpha_positions"]

    output = [''] * original_length

    for idx_str, ch in non_alpha.items():
        output[int(idx_str)] = ch

    for i, orig_idx in enumerate(alpha_positions):
        if i < len(clean_alpha):
            output[orig_idx] = clean_alpha[i]
        else:
            output[orig_idx] = '?'

    return {
        "key": key,
        "plaintext": ''.join(output)
    }
