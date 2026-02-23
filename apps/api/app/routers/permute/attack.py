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


def _build_letter_index(unigrams, bigrams, trigrams, word_counts):
    bg_idx = {c: [] for c in ALPHA}
    for bg, cnt in bigrams.items():
        bg_idx[bg[0]].append((bg, cnt))
        if bg[1] != bg[0]:
            bg_idx[bg[1]].append((bg, cnt))

    tg_idx = {c: [] for c in ALPHA}
    for tg, cnt in trigrams.items():
        seen = set()
        for ch in tg:
            if ch not in seen:
                tg_idx[ch].append((tg, cnt))
                seen.add(ch)

    wd_idx = {c: [] for c in ALPHA}
    for cw, cnt in word_counts.items():
        wlen = len(cw)
        if wlen in CW_SETS:
            seen = set()
            for ch in cw:
                if ch not in seen:
                    wd_idx[ch].append((cw, wlen, cnt))
                    seen.add(ch)

    return bg_idx, tg_idx, wd_idx


def _contrib_uni(km, letter, unigrams, total):
    plain = km.get(letter, "?")
    observed = unigrams.get(letter, 0)
    expected = EF.get(plain, 0.01) / 100 * total
    return -((observed - expected) ** 2 / expected)


def _contrib_bg(km, bg):
    p = km.get(bg[0], "?") + km.get(bg[1], "?")
    return p in BG


def _contrib_tg(km, tg):
    p = km.get(tg[0], "?") + km.get(tg[1], "?") + km.get(tg[2], "?")
    return p in TG


def _contrib_wd(km, cw, wlen):
    w = "".join(km.get(c, "?") for c in cw)
    return w in CW_SETS[wlen]


def hill_climb(ct, km, precomputed_data, iters=10000, restarts=8, progress_callback=None):
    import time
    total, unigrams, bigrams, trigrams, word_counts = precomputed_data
    bg_idx, tg_idx, wd_idx = _build_letter_index(unigrams, bigrams, trigrams, word_counts)

    best = km.copy()
    bs = score(best, total, unigrams, bigrams, trigrams, word_counts)

    ks = list(ALPHA)

    for restart_i in range(restarts):
        if progress_callback:
            progress_callback(float(restart_i), float(restarts), f"Hill climbing (Restart {restart_i + 1}/{restarts})...")
            time.sleep(0.1)
            
        cur = best.copy()

        for _ in range(3):
            a, b = random.sample(ks, 2)
            cur[a], cur[b] = cur[b], cur[a]

        cs = score(cur, total, unigrams, bigrams, trigrams, word_counts)
        improved = True
        it = 0

        while improved and it < iters:
            improved = False
            it += 1
            
            if progress_callback and it % max(iters // 20, 1) == 0:
                # Add the partial progress of the current restart's iterations
                partial_restart = it / iters
                progress_callback(restart_i + partial_restart, restarts, f"Hill climbing (Restart {restart_i + 1}/{restarts}, Iteration {it})...")
                time.sleep(0.001)

            for i in range(26):
                for j in range(i + 1, 26):
                    k1, k2 = ks[i], ks[j]

                    old_uni = _contrib_uni(cur, k1, unigrams, total) + _contrib_uni(cur, k2, unigrams, total)

                    affected_bgs = set()
                    old_bg = 0.0
                    for bg, cnt in bg_idx[k1]:
                        affected_bgs.add(bg)
                        if _contrib_bg(cur, bg):
                            old_bg += 2 * cnt
                    for bg, cnt in bg_idx[k2]:
                        if bg not in affected_bgs:
                            affected_bgs.add(bg)
                            if _contrib_bg(cur, bg):
                                old_bg += 2 * cnt

                    affected_tgs = set()
                    old_tg = 0.0
                    for tg, cnt in tg_idx[k1]:
                        affected_tgs.add(tg)
                        if _contrib_tg(cur, tg):
                            old_tg += 3 * cnt
                    for tg, cnt in tg_idx[k2]:
                        if tg not in affected_tgs:
                            affected_tgs.add(tg)
                            if _contrib_tg(cur, tg):
                                old_tg += 3 * cnt

                    affected_wds = set()
                    old_wd = 0.0
                    for cw, wlen, cnt in wd_idx[k1]:
                        affected_wds.add(cw)
                        if _contrib_wd(cur, cw, wlen):
                            old_wd += 4 * (wlen ** 1.5) * cnt
                    for cw, wlen, cnt in wd_idx[k2]:
                        if cw not in affected_wds:
                            affected_wds.add(cw)
                            if _contrib_wd(cur, cw, wlen):
                                old_wd += 4 * (wlen ** 1.5) * cnt

                    cur[k1], cur[k2] = cur[k2], cur[k1]

                    new_uni = _contrib_uni(cur, k1, unigrams, total) + _contrib_uni(cur, k2, unigrams, total)

                    new_bg = 0.0
                    for bg in affected_bgs:
                        cnt = bigrams[bg]
                        if _contrib_bg(cur, bg):
                            new_bg += 2 * cnt

                    new_tg = 0.0
                    for tg in affected_tgs:
                        cnt = trigrams[tg]
                        if _contrib_tg(cur, tg):
                            new_tg += 3 * cnt

                    new_wd = 0.0
                    for cw in affected_wds:
                        cnt = word_counts[cw]
                        wlen = len(cw)
                        if _contrib_wd(cur, cw, wlen):
                            new_wd += 4 * (wlen ** 1.5) * cnt

                    delta = (new_uni - old_uni) + (new_bg - old_bg) + (new_tg - old_tg) + (new_wd - old_wd)

                    if delta > 0:
                        cs += delta
                        improved = True
                    else:
                        cur[k1], cur[k2] = cur[k2], cur[k1]

        if cs > bs:
            bs = cs
            best = cur.copy()

    return best, bs


def frequency_attack(ct: str, restarts: int = 10, progress_callback=None) -> dict:
    if progress_callback:
        progress_callback(0, restarts + 2, "Precomputing statistics...")
    precomputed_data = precompute(ct)
    if progress_callback:
        progress_callback(1, restarts + 2, "Seeding initial key...")
    km = hint_seed(ct, init_key(ct))
    km, best_score = hill_climb(ct, km, precomputed_data, iters=10000, restarts=restarts,
                                progress_callback=lambda i, t, s: progress_callback(i + 2.0, float(t + 2), s) if progress_callback else None)
    km = hint_seed(ct, km)
    plaintext = apply_key(ct, km)

    inv = {plain: cipher for cipher, plain in km.items()}
    key_str = "".join(inv.get(c, "?") for c in ALPHA)

    if progress_callback:
        progress_callback(restarts + 2, restarts + 2, "Complete")

    return {
        "guessed_key": key_str,
        "guessed_plaintext": plaintext,
    }