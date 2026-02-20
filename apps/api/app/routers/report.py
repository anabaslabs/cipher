from collections import Counter


ROWS = [
    ["A", "F", "K", "P", "U", "1", "6"],
    ["B", "G", "L", "Q", "V", "2", "7"],
    ["C", "H", "M", "R", "W", "3", "8"],
    ["D", "I", "N", "S", "X", "4", "9"],
    ["E", "J", "O", "T", "Y", "5", "0"],
]


def _freq_diff_table(freq_a, freq_b, total_a, total_b):
    def fmt(c):
        pa = freq_a.get(c, 0) / total_a * 100 if total_a else 0
        pb = freq_b.get(c, 0) / total_b * 100 if total_b else 0
        return f"{c}: {pb - pa:+.2f}%"

    lines = []
    for row in ROWS:
        parts = []
        for c in row:
            parts.append(fmt(c).ljust(16))
        lines.append("".join(parts))
    z_val = fmt("Z")
    lines.append(" " * (16 * 4) + z_val)
    return "\n".join(lines)


def _count_table(freq):
    lines = []
    for row in ROWS:
        parts = []
        for c in row:
            cell = f"{c}: {freq.get(c, 0)}"
            parts.append(cell.ljust(12))
        lines.append("".join(parts))
    z_val = f"Z: {freq.get('Z', 0)}"
    lines.append(" " * (12 * 4) + z_val)
    return "\n".join(lines)


def compare(original: str, recovered: str) -> str:
    original = original.upper()
    recovered = recovered.upper()

    n = min(len(original), len(recovered))
    matches = sum(original[i] == recovered[i] for i in range(n))

    alpha = [(x, y) for x, y in zip(original[:n], recovered[:n]) if x.isascii() and x.isalpha()]
    alpha_match = sum(x == y for x, y in alpha)

    non_alpha = [(x, y) for x, y in zip(original[:n], recovered[:n]) if not (x.isascii() and x.isalpha())]
    non_alpha_match = sum(x == y for x, y in non_alpha)

    word_a, word_b = original.split(), recovered.split()
    line_a, line_b = original.splitlines(), recovered.splitlines()

    verdict = (
        "PERFECT" if matches == n and len(original) == len(recovered)
        else "NEAR MATCH" if matches / n >= 0.95
        else "PARTIAL MATCH" if matches / n >= 0.5
        else "FAILED"
    )

    report = []
    report.append("======== COMPARISON REPORT ========\n")
    report.append(f"VERDICT: {verdict}\n")

    report.append(f"Original File Length: {len(original)}")
    report.append(f"Decrypted File Length: {len(recovered)}")
    report.append(f"Length match: {'YES' if len(original) == len(recovered) else 'NO'}\n")

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

    freq_a = Counter(c for c in original if c.isascii() and c.isalnum())
    freq_b = Counter(c for c in recovered if c.isascii() and c.isalnum())
    total_a = sum(freq_a.values())
    total_b = sum(freq_b.values())

    sorted_a = ''.join(c for c, _ in freq_a.most_common())
    sorted_b = ''.join(c for c, _ in freq_b.most_common())

    report.append("\nCharacter string in descending by count:")
    report.append(f"{'Original File:'.ljust(16)}{sorted_a}")
    report.append(f"{'Decrypted File:'.ljust(16)}{sorted_b}")

    report.append("\nCharacter frequency diff:")
    report.append(_freq_diff_table(freq_a, freq_b, total_a, total_b))

    report.append("\nCharacter Count in Original File:")
    report.append(_count_table(freq_a))

    report.append("\nCharacter Count in Decrypted File:")
    report.append(_count_table(freq_b))

    return "\n".join(report)