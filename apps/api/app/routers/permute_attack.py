import re
import random
from collections import Counter

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
EF = {
    "E": 12.70, "T": 9.06, "A": 8.17, "O": 7.51, "I": 6.97, "N": 6.75,
    "S": 6.33, "H": 6.09, "R": 5.99, "D": 4.25, "L": 4.03, "C": 2.78,
    "U": 2.76, "M": 2.41, "W": 2.36, "F": 2.23, "G": 2.02, "Y": 1.97,
    "P": 1.93, "B": 1.29, "V": 0.98, "K": 0.77, "J": 0.15, "X": 0.15,
    "Q": 0.10, "Z": 0.07,
}
BG = {
    "TH", "HE", "IN", "ER", "AN", "RE", "ON", "EN", "AT", "OU",
    "ND", "ST", "ES", "TE", "ET", "OR", "OF", "IT", "IS", "HI",
}
TG = {
    "THE", "AND", "ING", "HER", "HAT", "HIS", "THA", "ERE", "FOR", "ENT",
    "ION", "TER", "WAS", "YOU", "ITH", "VER", "ALL",
}
CW = {
    1: ["A", "I"],
    2: ["OF", "TO", "IN", "IS", "IT", "BE", "AS", "AT", "SO", "WE", "HE", "BY", "OR", "ON", "DO", "IF", "ME", "MY", "AN"],
    3: ["THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "WAS", "ONE", "OUT", "HIS", "HER", "HOW", "ITS"],
    4: ["THAT", "WITH", "HAVE", "THIS", "WILL", "YOUR", "FROM", "THEY", "BEEN", "GOOD", "SOME", "TIME", "WHEN", "WERE", "THEY"],
}
CW_SETS = {k: set(v) for k, v in CW.items()}

PDB = {}
for wl in CW.values():
    for w in wl:
        p = ""
        m = {}
        i = 0
        for c in w:
            if c not in m:
                m[c] = str(i)
                i += 1
            p += m[c]
        PDB.setdefault(p, []).append(w)


def precompute(ct):
    alpha_upper = [c.upper() for c in ct if c.isascii() and c.isalpha()]
    total = len(alpha_upper)
    unigrams = Counter(alpha_upper)
    bigrams = Counter(alpha_upper[i] + alpha_upper[i + 1] for i in range(total - 1))
    trigrams = Counter(alpha_upper[i] + alpha_upper[i + 1] + alpha_upper[i + 2] for i in range(total - 2))
    cipher_words = [w.upper() for w in re.findall(r"[A-Za-z]+", ct)]
    word_counts = Counter(cipher_words)
    return total, unigrams, bigrams, trigrams, word_counts


def score(km, total, unigrams, bigrams, trigrams, word_counts):
    if not total:
        return -1e9

    f = Counter()
    for c, count in unigrams.items():
        f[km.get(c, "?")] += count
    chi = sum((f.get(c, 0) - EF[c] / 100 * total) ** 2 / (EF[c] / 100 * total) for c in ALPHA)
    s = -chi

    for bg, count in bigrams.items():
        if km.get(bg[0], "?") + km.get(bg[1], "?") in BG:
            s += 2 * count

    for tg, count in trigrams.items():
        if km.get(tg[0], "?") + km.get(tg[1], "?") + km.get(tg[2], "?") in TG:
            s += 3 * count

    for cw, count in word_counts.items():
        wlen = len(cw)
        if wlen in CW_SETS:
            w = "".join(km.get(c, "?") for c in cw)
            if w in CW_SETS[wlen]:
                s += 4 * (wlen ** 1.5) * count

    return s


def apply_key(ct, km):
    return "".join(
        km.get(c.upper(), "?") if c.isascii() and c.isupper()
        else km.get(c.upper(), "?").lower() if c.isascii() and c.isalpha()
        else c
        for c in ct
    )


def init_key(ct):
    cleaned = re.sub(r"[^A-Z]", "", ct.upper())
    cs = [c for c, _ in Counter(cleaned).most_common()]
    es = [c for c, _ in sorted(EF.items(), key=lambda x: -x[1])]
    km = {c: es[i] for i, c in enumerate(cs) if i < 26}
    used = set(km.values())
    unused = [c for c in ALPHA if c not in used]
    j = 0
    for c in ALPHA:
        if c not in km:
            km[c] = unused[j]
            j += 1
    return km


def pat(w):
    m = {}
    p = []
    i = 0
    for c in w:
        if c not in m:
            m[c] = str(i)
            i += 1
        p.append(m[c])
    return "".join(p)


def hint_seed(ct, km):
    km = km.copy()
    for cw in re.findall(r"[A-Z]+", ct.upper()):
        cands = PDB.get(pat(cw), [])
        if len(cands) != 1:
            continue
        pw = cands[0]
        lh = {}
        ok = True
        for cc, pc in zip(cw, pw):
            if (cc in lh and lh[cc] != pc) or (pc in lh.values() and lh.get(cc) != pc):
                ok = False
                break
            lh[cc] = pc
        if ok:
            for cc, pc in lh.items():
                if pc not in set(km.values()) or km.get(cc) == pc:
                    old = [k for k, v in km.items() if v == pc]
                    for h in old:
                        km[h] = km[cc]
                    km[cc] = pc
    return km


def hill_climb(ct, km, precomputed_data, iters=10000, restarts=8):
    total, unigrams, bigrams, trigrams, word_counts = precomputed_data
    best = km.copy()
    bs = score(best, total, unigrams, bigrams, trigrams, word_counts)

    for _ in range(restarts):
        cur = best.copy()
        ks = list(ALPHA)

        for _ in range(3):
            a, b = random.sample(ks, 2)
            cur[a], cur[b] = cur[b], cur[a]

        cs = score(cur, total, unigrams, bigrams, trigrams, word_counts)
        improved = True
        it = 0

        while improved and it < iters:
            improved = False
            it += 1

            for i in range(26):
                for j in range(i + 1, 26):
                    k1, k2 = ks[i], ks[j]
                    cur[k1], cur[k2] = cur[k2], cur[k1]
                    ns = score(cur, total, unigrams, bigrams, trigrams, word_counts)

                    if ns > cs:
                        cs = ns
                        improved = True
                    else:
                        cur[k1], cur[k2] = cur[k2], cur[k1]

        if cs > bs:
            bs = cs
            best = cur.copy()

    return best, bs


def frequency_attack(ct: str, restarts: int = 10) -> dict:
    precomputed_data = precompute(ct)
    km = hint_seed(ct, init_key(ct))
    km, best_score = hill_climb(ct, km, precomputed_data, iters=10000, restarts=restarts)
    km = hint_seed(ct, km)
    plaintext = apply_key(ct, km)

    inv = {plain: cipher for cipher, plain in km.items()}
    key_str = "".join(inv.get(c, "?") for c in ALPHA)

    return {
        "guessed_key": key_str,
        "guessed_plaintext": plaintext,
    }