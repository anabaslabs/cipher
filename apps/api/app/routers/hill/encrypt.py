def multiply_matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        (matrix[0][0] * vector[0] + matrix[0][1] * vector[1]) % 26,
        (matrix[1][0] * vector[0] + matrix[1][1] * vector[1]) % 26,
    ]


def encrypt(text: str, key: dict) -> str:
    matrix = key["matrix"]

    alpha_chars = [ch for ch in text if ch.isascii() and ch.isalpha()]
    clean_nums = [ord(ch.upper()) - 65 for ch in alpha_chars]

    if len(clean_nums) % 2 != 0:
        clean_nums.append(23)

    encrypted_alpha = []
    for i in range(0, len(clean_nums), 2):
        block = clean_nums[i : i + 2]
        encrypted_block = multiply_matrix_vector(matrix, block)
        encrypted_alpha.extend(chr(num + 65) for num in encrypted_block)

    result = []
    alpha_idx = 0
    for ch in text:
        if ch.isascii() and ch.isalpha():
            if alpha_idx < len(encrypted_alpha):
                result.append(encrypted_alpha[alpha_idx])
                alpha_idx += 1
            else:
                result.append(ch)
        else:
            result.append(ch)

    while alpha_idx < len(encrypted_alpha):
        result.append(encrypted_alpha[alpha_idx])
        alpha_idx += 1

    return {
        "key": key,
        "ciphertext": "".join(result)
    }