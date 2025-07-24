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


def can_spell(wc, wild, word):
    need = sum(max(cnt - wc.get(ch, 0), 0) for ch, cnt in Counter(word).items())
    return need <= wild


def top_multiples(wc, wild, words, parts, k=5):
    results = []

    def recurse(avail, wld, combo, total):
        if len(combo) == parts:
            results.append((total, combo))
            return
        for w in words:
            if can_spell(avail, wld, w):
                cnt = Counter(w)
                need = 0
                new_avail = avail.copy()
                for ch, c in cnt.items():
                    have = new_avail.get(ch, 0)
                    used = min(have, c)
                    new_avail[ch] = have - used
                    need += c - used
                recurse(new_avail, wld - need, combo + [w], total + len(w))

    recurse(wc, wild, [], 0)
    top = sorted(results, key=lambda x: x[0], reverse=True)[:k]
    return [combo for _, combo in top]


def main():
    pending = ""  # leftover input for new search
    while True:
        if not pending:
            s = input("Letters (? wildcard, + for extra words): ").lower().strip()
            if not s:
                break
        else:
            s = pending
            pending = ""

        parts = s.count("+") + 1
        letters = s.replace("+", "")
        cnt = Counter(letters)
        wild = cnt.pop("?", 0) + cnt.pop("*", 0)
        total = sum(cnt.values()) + wild
        cand = [w for w in WORDS if len(w) <= total]

        if parts == 1:
            # paginate single-word suggestions
            suggestions = sorted(
                (w for w in cand if can_spell(cnt, wild, w)), key=len, reverse=True
            )
            idx = 0
            page = 0
            while idx < len(suggestions):
                size = 5 if page == 0 else 10
                for w in suggestions[idx : idx + size]:
                    print(w)
                idx += size
                page += 1
                if idx >= len(suggestions):
                    break
                nxt = (
                    input("Press Enter for more, or type new letters: ").lower().strip()
                )
                if nxt:
                    pending = nxt
                    break
            # after paging, loop back for next search
        else:
            # multi-word top 5
            for combo in top_multiples(cnt, wild, cand, parts, k=5):
                print("+".join(combo))
            # after printing, prompt next search


if __name__ == "__main__":
    main()
