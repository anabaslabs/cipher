def get_inverse_matrix(matrix: list[list[int]]) -> list[list[int]]:
    det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
    det_inv = pow(det, -1, 26)
    return [
        [(matrix[1][1] * det_inv) % 26, (-matrix[0][1] * det_inv) % 26],
        [(-matrix[1][0] * det_inv) % 26, (matrix[0][0] * det_inv) % 26],
    ]


def decrypt(text: str, key: dict) -> str:
    matrix = key["matrix"]
    inv_matrix = get_inverse_matrix(matrix)

    alpha_chars = [ch for ch in text if ch.isascii() and ch.isalpha()]
    cipher_nums = [ord(ch.upper()) - 65 for ch in alpha_chars]

    decrypted_alpha = []
    for i in range(0, len(cipher_nums), 2):
        block = cipher_nums[i : i + 2]
        decrypted_block = [
            (inv_matrix[0][0] * block[0] + inv_matrix[0][1] * block[1]) % 26,
            (inv_matrix[1][0] * block[0] + inv_matrix[1][1] * block[1]) % 26,
        ]
        decrypted_alpha.extend(chr(num + 65) for num in decrypted_block)

    result = []
    alpha_idx = 0
    for ch in text:
        if ch.isascii() and ch.isalpha():
            if alpha_idx < len(decrypted_alpha):
                result.append(decrypted_alpha[alpha_idx])
                alpha_idx += 1
            else:
                result.append(ch)
        else:
            result.append(ch)

    return {
        "key": key,
        "plaintext": "".join(result)
    }