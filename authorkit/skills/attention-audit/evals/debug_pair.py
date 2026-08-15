#!/usr/bin/env python3
"""Dump one pair's full shared-term evidence with per-term df, ignoring thresholds."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import collide  # noqa: E402

root, a_pat, b_pat = sys.argv[1], sys.argv[2], sys.argv[3]
entries = collide.gather(root)
docs = {n: d for n, d in entries}
a = next(n for n in docs if a_pat in n)
b = next(n for n in docs if b_pat in n)
n_docs = len(entries)
df, bdf = {}, {}
for _, d in entries:
    for t in collide.tokens(d):
        df[t] = df.get(t, 0) + 1
    for g in collide.bigrams(d):
        bdf[g] = bdf.get(g, 0) + 1
print(f"{a}  <->  {b}   (corpus {n_docs} docs)")
shared_u = sorted(collide.tokens(docs[a]) & collide.tokens(docs[b]), key=lambda t: df[t])
shared_b = sorted(collide.bigrams(docs[a]) & collide.bigrams(docs[b]), key=lambda g: bdf[g])
for t in shared_u:
    print(f"  uni  df={df[t]:3d}  idf={math.log(n_docs/df[t]):.2f}  {t}")
for g in shared_b:
    print(f"  bi   df={bdf[g]:3d}  idf={math.log(n_docs/bdf[g]):.2f}  {g}")
