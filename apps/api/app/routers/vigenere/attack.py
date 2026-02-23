from collections import Counter

ENGLISH_FREQ = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094,
    0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929,
    0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150,
    0.01974, 0.00074,
]

COMMON_BIGRAMS = [
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND",
    "TI", "ES", "OR", "TE", "OF", "ED", "IS", "IT", "AL", "AR",
    "ST", "TO", "NT", "NG", "SE", "HA", "AS", "OU", "IO", "LE",
]


def get_top_key_lengths(cipher_alpha: str, max_key_len: int = 20, top_n: int = 3) -> list[int]:
    ic_scores = {}
    for key_len in range(1, max_key_len + 1):
        ic_total = 0
        for i in range(key_len):
            subseq = cipher_alpha[i::key_len]
            n = len(subseq)
            if n < 2:
                continue
            freq = Counter(subseq)
            ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
            ic_total += ic
        avg_ic = ic_total / key_len
        ic_scores[key_len] = avg_ic
    return sorted(ic_scores, key=ic_scores.get, reverse=True)[:top_n]


def frequency_attack_chi_square(cipher_alpha: str, key_len: int) -> str:
    key = []
    for i in range(key_len):
        subseq = cipher_alpha[i::key_len]
        n = len(subseq)
        counts = [0] * 26
        for c in subseq:
            counts[ord(c) - 65] += 1
        best_shift = 0
        best_chi_sq = float("inf")
        for shift in range(26):
            chi_sq = 0
            for c_val in range(26):
                orig_val = (c_val - shift) % 26
                expected = n * ENGLISH_FREQ[orig_val]
                observed = counts[c_val]
                if expected > 0:
                    chi_sq += ((observed - expected) ** 2) / expected
            if chi_sq < best_chi_sq:
                best_chi_sq = chi_sq
                best_shift = shift
        key.append(chr(best_shift + 65))
    return "".join(key)


def score_plaintext(text: str) -> int:
    text = text.upper()
    return sum(text.count(bg) for bg in COMMON_BIGRAMS)


def decrypt(cipher: str, key: str) -> str:
    result = []
    key_shifts = [ord(k) - 65 for k in key.upper()]
    key_len = len(key)
    key_index = 0
    for ch in cipher:
        if ch.isascii() and ch.isalpha():
            shift = key_shifts[key_index % key_len]
            if ch.isupper():
                result.append(chr((ord(ch) - 65 - shift) % 26 + 65))
            else:
                result.append(chr((ord(ch) - 97 - shift) % 26 + 97))
            key_index += 1
        else:
            result.append(ch)
    return "".join(result)


def reduce_key(key: str) -> str:
    for length in range(1, len(key) + 1):
        if len(key) % length == 0:
            pattern = key[:length]
            if pattern * (len(key) // length) == key:
                return pattern
    return key


def vigenere_attack(ciphertext: str, progress_callback=None) -> dict:
    import time
    cipher_alpha = "".join(c for c in ciphertext.upper() if c.isascii() and c.isalpha())
    if not cipher_alpha:
        return {"guessed_key": "", "guessed_plaintext": ""}

    if progress_callback:
        progress_callback(0, 4, "Finding key lengths...")
    top_lengths = get_top_key_lengths(cipher_alpha)
    best_key = ""
    best_text = ""
    best_score = -1

    total_shifts_to_test = sum(length * 26 for length in top_lengths)
    shifts_tested = 0

    for idx, length in enumerate(top_lengths):
        if progress_callback:
            progress_callback(shifts_tested, total_shifts_to_test, f"Trying key length {length}...")
            time.sleep(0.1)
            
        key = []
        for i in range(length):
            subseq = cipher_alpha[i::length]
            n = len(subseq)
            counts = [0] * 26
            for c in subseq:
                counts[ord(c) - 65] += 1
            best_shift = 0
            best_chi_sq = float("inf")
            for shift in range(26):
                
                shifts_tested += 1
                if progress_callback and shifts_tested % 5 == 0:
                    progress_callback(shifts_tested, total_shifts_to_test, f"Testing key length {length} (Shift {shift + 1}/26)...")
                    time.sleep(0.01)

                chi_sq = 0
                for c_val in range(26):
                    orig_val = (c_val - shift) % 26
                    expected = n * ENGLISH_FREQ[orig_val]
                    observed = counts[c_val]
                    if expected > 0:
                        chi_sq += ((observed - expected) ** 2) / expected
                if chi_sq < best_chi_sq:
                    best_chi_sq = chi_sq
                    best_shift = shift
            key.append(chr(best_shift + 65))
            
        candidate_key = "".join(key)
        candidate_text = decrypt(ciphertext, candidate_key)
        english_score = score_plaintext("".join(c for c in candidate_text if c.isascii() and c.isalpha()))

        if english_score > best_score:
            best_score = english_score
            best_key = candidate_key
            best_text = candidate_text

    if progress_callback:
        progress_callback(len(top_lengths) + 1, len(top_lengths) + 1, "Complete")

    return {
        "guessed_key": reduce_key(best_key),
        "guessed_plaintext": best_text,
    }