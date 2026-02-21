from collections import Counter

ROWS = [
    ["A", "F", "K", "P", "U", "1", "6"],
    ["B", "G", "L", "Q", "V", "2", "7"],
    ["C", "H", "M", "R", "W", "3", "8"],
    ["D", "I", "N", "S", "X", "4", "9"],
    ["E", "J", "O", "T", "Y", "5", "0"],
]

def fast_ratio(seq1, seq2, lookahead=15):
    i = j = matches = 0
    n1, n2 = len(seq1), len(seq2)
    
    while i < n1 and j < n2:
        if seq1[i] == seq2[j]:
            matches += 1
            i += 1
            j += 1
        else:
            found = False
            for k in range(1, lookahead + 1):
                if i + k < n1 and seq1[i + k] == seq2[j]:
                    i += k
                    found = True
                    break
                if j + k < n2 and seq1[i] == seq2[j + k]:
                    j += k
                    found = True
                    break
            if not found:
                i += 1
                j += 1
                
    return (2.0 * matches) / (n1 + n2) if (n1 + n2) > 0 else 0.0

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

    overall_pct = fast_ratio(original, recovered)

    alpha_orig = [x for x in original if x.isascii() and x.isalpha()]
    alpha_recv = [x for x in recovered if x.isascii() and x.isalpha()]
    alpha_pct = fast_ratio(alpha_orig, alpha_recv)

    non_alpha_orig = [x for x in original if not (x.isascii() and x.isalpha())]
    non_alpha_recv = [x for x in recovered if not (x.isascii() and x.isalpha())]
    non_alpha_pct = fast_ratio(non_alpha_orig, non_alpha_recv)

    word_a, word_b = original.split(), recovered.split()
    line_a, line_b = original.splitlines(), recovered.splitlines()

    word_pct = fast_ratio(word_a, word_b) if word_a and word_b else 0
    line_pct = fast_ratio(line_a, line_b) if line_a and line_b else 0
    
    length_diff = len(recovered) - len(original)

    if overall_pct == 1.0:
        verdict = "PERFECT"
    elif overall_pct >= 0.95:
        verdict = "NEAR PERFECT"
    elif overall_pct >= 0.85:
        verdict = "NEAR MATCH"
    elif overall_pct >= 0.60:
        verdict = "PARTIAL MATCH"
    elif overall_pct >= 0.30:
        verdict = "WEAK MATCH"
    else:
        verdict = "FAILED"

    report = []
    report.append("======== COMPARISON REPORT ========\n")
    report.append(f"VERDICT: {verdict}\n")

    report.append(f"Original File Length: {len(original)}")
    report.append(f"Decrypted File Length: {len(recovered)}")
    report.append(f"Length difference: {'+' + str(length_diff) if length_diff > 0 else str(length_diff)}\n")

    report.append(f"Overall accuracy: {overall_pct * 100:.2f}%")
    report.append(
        f"Alphabet accuracy: {alpha_pct * 100:.2f}%" if alpha_orig
        else "Alphabet accuracy: N/A"
    )
    report.append(
        f"Non-alpha accuracy: {non_alpha_pct * 100:.2f}%" if non_alpha_orig
        else "Non-alpha accuracy: N/A"
    )

    if word_a and word_b:
        report.append(f"\nWord accuracy: {word_pct * 100:.2f}%")
    if line_a and line_b:
        report.append(f"Line accuracy: {line_pct * 100:.2f}%")

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