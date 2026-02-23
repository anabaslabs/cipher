from collections import Counter

ROWS = [
    ["A", "F", "K", "P", "U", "1", "6"],
    ["B", "G", "L", "Q", "V", "2", "7"],
    ["C", "H", "M", "R", "W", "3", "8"],
    ["D", "I", "N", "S", "X", "4", "9"],
    ["E", "J", "O", "T", "Y", "5", "0"],
]

def fast_ratio(seq1, seq2, lookahead=10):
    if not seq1 and not seq2:
        return 1.0
    if not seq1 or not seq2:
        return 0.0

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
                
    return (2.0 * matches) / (n1 + n2)

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

    # 1. Overall Character Match
    overall_pct = fast_ratio(original, recovered, lookahead=10)

    # 2. Alpha / Non-Alpha Match
    alpha_orig = [x for x in original if x.isalpha()]
    alpha_recv = [x for x in recovered if x.isalpha()]
    alpha_pct = fast_ratio(alpha_orig, alpha_recv, lookahead=10)

    non_alpha_orig = [x for x in original if not x.isalpha()]
    non_alpha_recv = [x for x in recovered if not x.isalpha()]
    non_alpha_pct = fast_ratio(non_alpha_orig, non_alpha_recv, lookahead=10)

    # 3. Word / Line Match
    word_a, word_b = original.split(), recovered.split()
    line_a, line_b = original.splitlines(), recovered.splitlines()

    word_match = sum(x == y for x, y in zip(word_a, word_b))
    word_pct = word_match / min(len(word_a), len(word_b)) if word_a and word_b else (1.0 if not word_a and not word_b else 0.0)
    
    line_match = sum(x == y for x, y in zip(line_a, line_b))
    line_pct = line_match / min(len(line_a), len(line_b)) if line_a and line_b else (1.0 if not line_a and not line_b else 0.0)

    # 4. Length Penalty
    length_diff = len(recovered) - len(original)
    max_len = max(len(original), len(recovered), 1)
    length_pct = 1.0 - (abs(length_diff) / max_len)

    # 5. Calculate Final Weighted Score
    score = (
        overall_pct * 0.25
        + alpha_pct * 0.25
        + non_alpha_pct * 0.05
        + word_pct * 0.20
        + line_pct * 0.10
        + length_pct * 0.15
    )

    # 6. Determine Verdict
    if score >= 0.99:
        verdict = "PERFECT"
    elif score >= 0.95:
        verdict = "NEAR PERFECT"
    elif score >= 0.85:
        verdict = "NEAR MATCH"
    elif score >= 0.60:
        verdict = "PARTIAL MATCH"
    elif score >= 0.30:
        verdict = "WEAK MATCH"
    else:
        verdict = "FAILED"

    # 7. Generate Output Report
    report = [
        "======== COMPARISON REPORT ========\n",
        f"VERDICT: {verdict}\n",
        f"Original File Length: {len(original)}",
        f"Decrypted File Length: {len(recovered)}",
        f"Length difference: {'+' + str(length_diff) if length_diff > 0 else str(length_diff)}\n",
        f"Overall accuracy: {overall_pct * 100:.2f}%",
        f"Alphabet accuracy: {alpha_pct * 100:.2f}%" if alpha_orig else "Alphabet accuracy: N/A",
        f"Non-alpha accuracy: {non_alpha_pct * 100:.2f}%" if non_alpha_orig else "Non-alpha accuracy: N/A"
    ]

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

    report.extend([
        "\nCharacter string in descending by count:",
        f"{'Original File:'.ljust(16)}{sorted_a}",
        f"{'Decrypted File:'.ljust(16)}{sorted_b}",

        "\nCharacter frequency diff:",
        _freq_diff_table(freq_a, freq_b, total_a, total_b),

        "\nCharacter Count in Original File:",
        _count_table(freq_a),

        "\nCharacter Count in Decrypted File:",
        _count_table(freq_b)
    ])

    return "\n".join(report)
