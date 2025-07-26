#!/usr/bin/env python3
import sys
from collections import Counter

# load word list
try:
    with open("words.txt", encoding="utf-8", errors="ignore") as f:
        WORDS = [w.strip().lower() for w in f if w.strip().isalpha()]
except FileNotFoundError:
    print("Error: no word list found. Put a word list at 'words.txt'")
    sys.exit(1)

# hardness scoring sets
HARD = set("xjqz")
SECO = set("kwfvhy")


def score_word(w):
    return sum(7 if c in HARD else 3 if c in SECO else 1 for c in w)


def need_wild(wc, w):
    return sum(max(cnt - wc.get(ch, 0), 0) for ch, cnt in Counter(w).items())


def can_spell(wc, wild, w):
    return need_wild(wc, w) <= wild


# efficient single-word ranking: minimize wild usage, then length, then hardness
def all_singles_efficient(wc, wild, words):
    # prioritize 9-letter words first, then shorter lengths
    candidates = [w for w in words if len(w) <= 9 and can_spell(wc, wild, w)]
    # bucket by length
    buckets = {}
    for w in candidates:
        buckets.setdefault(len(w), []).append(w)
    results = []
    # lengths 9 down to 1
    for length in range(9, 0, -1):
        bucket = buckets.get(length, [])
        # sort each by fewest wilds, then by hardness
        bucket.sort(key=lambda w: (need_wild(wc, w), -score_word(w)))
        results.extend(bucket)
    return results


# normal multi-word combinations
def top_multiples_normal(wc, wild, words, parts, k=5):
    results = []

    def recurse(avail, wld, combo, total):
        if len(combo) == parts:
            results.append((total, combo))
            return
        for w in words:
            if can_spell(avail, wld, w):
                cnt = Counter(w)
                need = need_wild(avail, w)
                new_avail = avail.copy()
                for c, req in cnt.items():
                    used = min(new_avail.get(c, 0), req)
                    new_avail[c] = new_avail.get(c, 0) - used
                recurse(new_avail, wld - need, combo + [w], total + len(w))

    recurse(wc, wild, [], 0)
    results.sort(key=lambda x: x[0], reverse=True)
    return [combo for _, combo in results[:k]]


# efficient multi-word combinations: restrict to <=9 letters, then rank by wild use and hardness
def top_multiples_efficient(wc, wild, words, parts, k=5):
    small = [w for w in words if len(w) <= 9]
    combos = top_multiples_normal(wc, wild, small, parts, k * 3)
    scored = []
    for combo in combos:
        need = sum(need_wild(wc, w) for w in combo)
        hard = sum(score_word(w) for w in combo)
        scored.append((need, -hard, combo))
    scored.sort(key=lambda x: (x[0], x[1]))
    return [c for _, _, c in scored[:k]]


def main():
    print("Modes: normal / efficient — switch with 'mode normal' or 'mode efficient'")
    mode = "efficient"
    pending = ""
    while True:
        s = pending or input(f"[{mode}] Letters: ").lower().strip()
        pending = ""
        if not s:
            break
        if s.startswith("mode "):
            m = s.split(None, 1)[1]
            if m in ("normal", "efficient"):
                mode = m
                print(f"→ Switched to {mode}")
            else:
                print("Unknown mode; use 'mode normal' or 'mode efficient'")
            continue

        parts = s.count("+") + 1
        letters = s.replace("+", "")
        cnt = Counter(letters)
        wild = cnt.pop("?", 0) + cnt.pop("*", 0)
        total_letters = sum(cnt.values()) + wild
        # Considers that if fewer than 16 letters are provided, the rest are wildcards up to 16
        if total_letters < 16:
            wild += 16 - total_letters
        total = sum(cnt.values()) + wild
        cand = [w for w in WORDS if len(w) <= total]

        if parts == 1:
            if mode == "normal":
                suggestions = sorted(
                    (w for w in cand if can_spell(cnt, wild, w)), key=len, reverse=True
                )
            else:
                suggestions = all_singles_efficient(cnt, wild, cand)
            idx = 0
            size = 5
            while idx < len(suggestions):
                for w in suggestions[idx : idx + size]:
                    wilds = need_wild(cnt, w)
                    if wilds > 0:
                        print(f"{w}  ({wilds})")
                    else:
                        print(f"{w}")
                idx += size
                size = 10
                if idx >= len(suggestions):
                    break
                nxt = input("--- Enter, or new Letters: ").lower().strip()
                if nxt:
                    pending = nxt
                    break
        else:
            if mode == "normal":
                combos = top_multiples_normal(cnt, wild, cand, parts, k=5)
            else:
                combos = top_multiples_efficient(cnt, wild, cand, parts, k=5)
            for combo in combos:
                print("+".join(combo))


if __name__ == "__main__":
    main()
