from collections import Counter


def compare(original: str, recovered: str) -> str:
    n = min(len(original), len(recovered))
    matches = sum(original[i] == recovered[i] for i in range(n))

    alpha = [(x, y) for x, y in zip(original[:n], recovered[:n]) if x.isalpha()]
    alpha_match = sum(x == y for x, y in alpha)

    non_alpha = [(x, y) for x, y in zip(original[:n], recovered[:n]) if not x.isalpha()]
    non_alpha_match = sum(x == y for x, y in non_alpha)

    word_a, word_b = original.split(), recovered.split()
    line_a, line_b = original.splitlines(), recovered.splitlines()

    report = []
    report.append("DECRYPTION ACCURACY REPORT\n")
    report.append(f"Length match: {'YES' if len(original) == len(recovered) else 'NO'}")
    report.append(f"Overall accuracy: {matches / n * 100:.2f}%")
    report.append(
        f"Alphabet accuracy: {alpha_match / len(alpha) * 100:.2f}%" if alpha
        else "Alphabet accuracy: N/A"
    )
    report.append(
        f"Non-alpha accuracy: {non_alpha_match / len(non_alpha) * 100:.2f}%" if non_alpha
        else "Non-alpha accuracy: N/A"
    )

    word_match = sum(x == y for x, y in zip(word_a, word_b))
    line_match = sum(x == y for x, y in zip(line_a, line_b))

    if word_a and word_b:
        report.append(f"\nWord accuracy: {word_match / min(len(word_a), len(word_b)) * 100:.2f}%")
    if line_a and line_b:
        report.append(f"Line accuracy: {line_match / min(len(line_a), len(line_b)) * 100:.2f}%")

    freq_a = Counter(c.lower() for c in original if c.isalpha())
    freq_b = Counter(c.lower() for c in recovered if c.isalpha())
    total_a, total_b = sum(freq_a.values()), sum(freq_b.values())

    report.append("\nLetter frequency diff:")
    for c in "abcdefghijklmnopqrstuvwxyz":
        pa = freq_a.get(c, 0) / total_a * 100 if total_a else 0
        pb = freq_b.get(c, 0) / total_b * 100 if total_b else 0
        report.append(f"{c}: {pb - pa:+.2f}%")

    report.append("\nVERDICT: " + (
        "PERFECT" if matches == n and len(original) == len(recovered)
        else "NEAR MATCH" if matches / n >= 0.95
        else "PARTIAL MATCH" if matches / n >= 0.5
        else "FAILED"
    ))

    return "\n".join(report)