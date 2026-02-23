from collections import Counter

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
        chr((ord(c) - 65 - key) % 26 + 65) if c.isascii() and c.isupper()
        else chr((ord(c) - 97 - key) % 26 + 97) if c.isascii() and c.islower()
        else c
        for c in text
    )


def chi_squared(text: str) -> float:
    letters = [c.lower() for c in text if c.isascii() and c.isalpha()]
    n = len(letters)
    if not n:
        return float("inf")
    count = Counter(letters)
    return sum(
        ((count.get(c, 0) - (FREQ[c] / 100 * n)) ** 2) / (FREQ[c] / 100 * n)
        for c in FREQ
    )


def caesar_attack(text: str, progress_callback=None) -> dict:
    import time
    
    if progress_callback:
        progress_callback(0, 260, "Starting attack...")

    results = []
    for k in range(26):
        if progress_callback:
            for step in range(10):
                progress_callback((k * 10) + step, 260, f"Testing shift {k} ({step * 10}%)...")
                time.sleep(0.005)
            
        score = chi_squared(caesar_decrypt(text, k))
        plaintext = caesar_decrypt(text, k)
        results.append((k, score, plaintext))
        
        if progress_callback:
            progress_callback((k * 10) + 10, 260, f"Testing shift {k} (100%)...")

    results.sort(key=lambda x: x[1])
    best_key, best_score, best_plaintext = results[0]

    if progress_callback:
        progress_callback(260, 260, "Complete")

    return {
        "guessed_key": best_key,
        "guessed_plaintext": best_plaintext,
    }
