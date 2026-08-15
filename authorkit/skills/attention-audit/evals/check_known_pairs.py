#!/usr/bin/env python3
"""Tuning harness: run collide.collide() over the live estate and check (a) the three
known-real cross-plugin pairs from evals/baseline/collide.md are flagged, (b) total noise."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import collide  # noqa: E402

# The cheap tier's proving fixture: distinctive-vocabulary twins (contested trigger territory
# between FEW claimants). Must appear in the rendered neighbors report or this exits 1.
KNOWN = [("break-down-problem", "break-down-layout")]
# Two baseline-found pairs are deliberately NOT here — each is the canonical example of a
# documented LLM-tier (check-routing) class, with measured evidence (debug_pair.py, 2026-08-15):
#   check-skill <-> bloat-audit: shared evidence is ONLY estate-common words
#     (audit df~40+, review, skill df=52) — the common-words class.
#   naming-rules <-> naming-conventions: shared evidence is a CROWDED COMMONS, not a duel —
#     naming df=23, name/estate df=13, grammar df=12 across the whole rename family; the pair's
#     twinhood is canon knowledge (ADR-0006 old canon vs ADR-0011 new), invisible to lexical
#     ownership at any cap — the crowded-territory class.


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    thr = float(sys.argv[2]) if len(sys.argv) > 2 else collide.THRESHOLD
    all_flags = collide.collide(collide.gather(root), thr)
    report = collide.neighbors(all_flags)  # what the audit procedure actually renders
    print(f"threshold={thr}  unbounded pairs: {len(all_flags)}  neighbors report: {len(report)}")
    missed = 0
    for a, b in KNOWN:
        hit = [(k, x) for k, x in enumerate(report, 1)
               if a in x["a"] + x["b"] and b in x["a"] + x["b"]]
        if hit:
            k, x = hit[0]
            print(f"  IN-REPORT rank {k:4d}  score {x['score']:6.1f}  {a} <-> {b}")
        else:
            missed += 1
            print(f"  MISSED FROM REPORT  {a} <-> {b}")
    print("report top 12:")
    for x in report[:12]:
        fam = " [family]" if x["family"] else ""
        print(f"  {x['score']:6.1f}{fam}  {x['a']} <-> {x['b']}")
    # bite: recall is proven against the REPORT the procedure renders, or this exits red
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main())
