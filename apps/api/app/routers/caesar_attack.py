from collections import Counter

# English letter frequency (%)
FREQ = {
    "a": 8.167, "b": 1.492, "c": 2.782, "d": 4.253, "e": 12.702,
    "f": 2.228, "g": 2.015, "h": 6.094, "i": 6.966, "j": 0.153,
    "k": 0.772, "l": 4.025, "m": 2.406, "n": 6.749, "o": 7.507,
    "p": 1.929, "q": 0.095, "r": 5.987, "s": 6.327, "t": 9.056,
    "u": 2.758, "v": 0.978, "w": 2.360, "x": 0.150, "y": 1.974,
    "z": 0.074,
}


def caesar_decrypt(text: str, key: int) -> str:
    return "".join(
        chr((ord(c) - 65 - key) % 26 + 65) if c.isupper()
        else chr((ord(c) - 97 - key) % 26 + 97) if c.islower()
        else c
        for c in text
    )


def chi_squared(text: str) -> float:
    letters = [c.lower() for c in text if c.isalpha()]
    n = len(letters)
    if not n:
        return float("inf")
    count = Counter(letters)
    return sum(
        ((count.get(c, 0) - (FREQ[c] / 100 * n)) ** 2) / (FREQ[c] / 100 * n)
        for c in FREQ
    )


def caesar_attack(text: str) -> dict:
    results = sorted(
        [(k, chi_squared(caesar_decrypt(text, k)), caesar_decrypt(text, k)) for k in range(26)],
        key=lambda x: x[1],
    )

    best_key, best_score, plaintext = results[0]

    return {
        "best_key": best_key,
        "best_score": round(best_score, 2),
        "plaintext": plaintext,
        "top_5": [
            {"key": k, "score": round(s, 2), "preview": d[:80]}
            for k, s, d in results[:5]
        ],
    }
