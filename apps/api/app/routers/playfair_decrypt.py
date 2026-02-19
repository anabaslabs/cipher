import re


def generate_6x6_matrix(keyword):
    keyword = re.sub(r'[^A-Z0-9]', '', keyword.upper())
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    matrix_chars = []
    used = set()
    for char in keyword + alphabet:
        if char not in used:
            matrix_chars.append(char)
            used.add(char)
    return matrix_chars


def decrypt(text: str, keyword: str) -> str:
    matrix = generate_6x6_matrix(keyword)

    valid_chars = []
    valid_indices = []
    for i, char in enumerate(text):
        if char.isalnum() and char.upper() in matrix:
            valid_chars.append(char.upper())
            valid_indices.append(i)

    decrypted_chars = []
    for i in range(0, len(valid_chars), 2):
        a = valid_chars[i]
        r1, c1 = divmod(matrix.index(a), 6)

        if i + 1 < len(valid_chars):
            b = valid_chars[i+1]
            r2, c2 = divmod(matrix.index(b), 6)

            if r1 == r2 and c1 == c2:
                d_a = matrix[((r1-1)%6)*6 + (c1-1)%6]
                d_b = matrix[((r2-1)%6)*6 + (c2-1)%6]
            elif r1 == r2:
                d_a = matrix[r1*6 + (c1-1)%6]
                d_b = matrix[r2*6 + (c2-1)%6]
            elif c1 == c2:
                d_a = matrix[((r1-1)%6)*6 + c1]
                d_b = matrix[((r2-1)%6)*6 + c2]
            else:
                d_a = matrix[r1*6 + c2]
                d_b = matrix[r2*6 + c1]

            decrypted_chars.extend([d_a, d_b])
        else:
            d_a = matrix[((r1-1)%6)*6 + (c1-1)%6]
            decrypted_chars.append(d_a)

    result = list(text)
    for i, orig_idx in enumerate(valid_indices):
        orig_char = text[orig_idx]
        dec_char = decrypted_chars[i]
        result[orig_idx] = dec_char.lower() if orig_char.islower() else dec_char

    return "".join(result)
