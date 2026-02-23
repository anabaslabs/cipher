import math
import itertools
from collections import Counter

ENGLISH_FREQ = {
    "A": 8.167, "B": 1.492, "C": 2.782, "D": 4.253, "E": 12.702,
    "F": 2.228, "G": 2.015, "H": 6.094, "I": 6.966, "J": 0.153,
    "K": 0.772, "L": 4.025, "M": 2.406, "N": 6.749, "O": 7.507,
    "P": 1.929, "Q": 0.095, "R": 5.987, "S": 6.327, "T": 9.056,
    "U": 2.758, "V": 0.978, "W": 2.360, "X": 0.150, "Y": 1.974,
    "Z": 0.074,
}

COMMON_BIGRAMS = {
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "EN", "AT", "ND",
    "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR",
    "ST", "TO", "NT", "NG", "SE", "HA", "AS", "OU", "IO", "LE",
}

COMMON_TRIGRAMS = {
    "THE", "AND", "ING", "HER", "HAT", "HIS", "THA", "ERE", "FOR",
    "ENT", "ION", "TER", "WAS", "YOU", "ITH", "VER", "ALL", "WIT",
}


def chi_squared(text: str) -> float:
    n = len(text)
    if n == 0:
        return float("inf")
    count = Counter(text)
    return sum(
        ((count.get(c, 0) - (ENGLISH_FREQ[c] / 100 * n)) ** 2) / (ENGLISH_FREQ[c] / 100 * n)
        for c in ENGLISH_FREQ
    )


def score_text(text: str) -> float:
    if not text:
        return -1e9

    chi = chi_squared(text)
    s = -chi

    for i in range(len(text) - 1):
        if text[i : i + 2] in COMMON_BIGRAMS:
            s += 3

    for i in range(len(text) - 2):
        if text[i : i + 3] in COMMON_TRIGRAMS:
            s += 5

    return s


def hill_attack(ciphertext: str, progress_callback=None) -> dict:
    import time
    cipher_nums = [ord(ch) - 65 for ch in ciphertext.upper() if ch.isascii() and ch.isalpha()]
    sample_len = min(200, len(cipher_nums))

    best_score = -1e9
    best_key = None
    total_iters = 26 ** 4
    iter_count = 0
    report_interval = max(total_iters // 200, 1)

    for a, b, c, d in itertools.product(range(26), repeat=4):
        iter_count += 1
        if progress_callback and iter_count % report_interval == 0:
            current_matrix = f"[[{a}, {b}], [{c}, {d}]]"
            progress_callback(iter_count, total_iters, f"Testing matrix {current_matrix}...")
            time.sleep(0.0001)
            
        det = (a * d - b * c) % 26
        if math.gcd(det, 26) != 1:
            continue

        det_inv = pow(det, -1, 26)
        inv = [
            [(d * det_inv) % 26, (-b * det_inv) % 26],
            [(-c * det_inv) % 26, (a * det_inv) % 26],
        ]

        test_text = ""
        for i in range(0, sample_len - 1, 2):
            p0 = (inv[0][0] * cipher_nums[i] + inv[0][1] * cipher_nums[i + 1]) % 26
            p1 = (inv[1][0] * cipher_nums[i] + inv[1][1] * cipher_nums[i + 1]) % 26
            test_text += chr(p0 + 65) + chr(p1 + 65)

        score = score_text(test_text)

        if score > best_score:
            best_score = score
            best_key = [[a, b], [c, d]]

    if best_key:
        from app.routers.hill.decrypt import decrypt

        key_data = {"size": 2, "matrix": best_key}
        full_plaintext = decrypt(ciphertext, key_data)

        if progress_callback:
            progress_callback(total_iters, total_iters, "Complete")

        return {
            "guessed_key": key_data,
            "guessed_plaintext": full_plaintext["plaintext"],
        }

    return {
        "guessed_key": None,
        "guessed_plaintext": None,
    }