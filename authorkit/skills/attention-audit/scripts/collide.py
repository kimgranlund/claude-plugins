#!/usr/bin/env python3
"""collide.py — deterministic lexical-collision pre-detection between menu descriptions.

Scans every ROUTABLE description (skills without disable-model-invocation:true, plus all
agents) across the whole estate — cross-plugin BY DEFAULT, because that's the proven blind
spot: same-plugin siblings fence reciprocally, cross-plugin pairs don't, and per-plugin eval
runs never see the collision. A pair is flagged when it shares >= THRESHOLD distinctive terms
AND neither description names the other artifact (a NOT-fence naming the sibling defuses it).

This is the cheap deterministic tier UPSTREAM of harness /check-routing's LLM-judged blind
simulation — it pre-filters, it never replaces the judged run.

Usage:
  python3 collide.py --target <estate-root> [--json] [--threshold N]
  python3 collide.py selftest

Exit: 0 no collisions · 1 collisions found · 2 error.
"""
import argparse
import json
import os
import re
import sys

THRESHOLD = 7.0  # pair score floor
OWN_MAX = 10     # only terms owned by <= OWN_MAX descriptions count as evidence: routing twins
                 # share CONTESTED TRIGGER TERRITORY (words few artifacts claim), not bulk
                 # vocabulary — a pair sharing forty medium words is prose kinship, not a twin

STOP = set("""a an and are as at be but by can do for from has have how i in is it its my not
of on one or our so that the their these this those to use used using we what when where which
who will with you your never always only also""".split())

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def parse_desc(text):
    m = FM_RE.match(text)
    if not m:
        return None, None, False
    fm = m.group(1)
    name = None
    nm = re.search(r"^name:\s*(\S+)", fm, re.M)
    if nm:
        name = nm.group(1).strip("'\"")
    dmi = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M))
    dm = re.search(r"^description:\s*(>-?|\|-?)?\s*(.*?)(?=\n[A-Za-z][\w-]*:|\Z)", fm, re.S | re.M)
    desc = ""
    if dm:
        desc = " ".join(dm.group(2).split())
    return name, desc, dmi


def tokens(desc):
    return {t for t in re.split(r"[^a-z]+", desc.lower()) if len(t) > 2 and t not in STOP}


def bigrams(desc):
    """UNORDERED adjacent word pairs (pure-stop pairs dropped): 'review, audit a skill' and
    'audit or review a skill' collide via COMMON words no unigram weighting can see, and the
    unordered form survives phrasing order."""
    seq = [t for t in re.split(r"[^a-z]+", desc.lower()) if len(t) > 2]
    return {" ".join(sorted((a, b))) for a, b in zip(seq, seq[1:])
            if not (a in STOP and b in STOP)}


def gather(root):
    """[(qualified_name, description)] for every routable menu entry."""
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in
                       (".git", "node_modules", "dist", ".refactor-attic", "worktrees")]
        plug = None
        rel = os.path.relpath(dirpath, root)
        plug = rel.split(os.sep)[0] if rel != "." else os.path.basename(os.path.abspath(root))
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            if fn == "SKILL.md":
                name, desc, dmi = parse_desc(open(path, encoding="utf-8", errors="ignore").read())
                if desc and not dmi:
                    entries.append((f"{plug}:{name or os.path.basename(dirpath)}", desc))
            elif fn.endswith(".md") and os.path.basename(dirpath) == "agents":
                name, desc, _ = parse_desc(open(path, encoding="utf-8", errors="ignore").read())
                if desc:
                    entries.append((f"{plug}:{name or fn[:-3]} (agent)", desc))
    return sorted(entries)


def collide(entries, threshold=THRESHOLD):
    import math
    toks = [(n, d, tokens(d), bigrams(d)) for n, d in entries]
    n_docs = max(len(toks), 2)
    df, bdf = {}, {}
    for _, _, ts, bs in toks:
        for t in ts:
            df[t] = df.get(t, 0) + 1
        for b in bs:
            bdf[b] = bdf.get(b, 0) + 1

    def idf(count):
        return math.log(n_docs / count)

    def family(name):
        base = name.split(":")[-1].replace(" (agent)", "")
        return base.rsplit("-", 1)[-1] if "-" in base else base

    flags = []
    for i in range(len(toks)):
        for j in range(i + 1, len(toks)):
            (na, da, ta, ba), (nb, db, tb, bb) = toks[i], toks[j]
            top = sorted([(idf(df[t]), 1, t) for t in ta & tb if 2 <= df[t] <= OWN_MAX] +
                         [(2 * idf(bdf[b]), 2, b) for b in ba & bb if 2 <= bdf[b] <= OWN_MAX],
                         reverse=True)
            score = sum(s for s, _, _ in top)
            if score < threshold:
                continue
            short_a, short_b = na.split(":")[-1].replace(" (agent)", ""), \
                nb.split(":")[-1].replace(" (agent)", "")
            fenced = (short_b.lower() in da.lower()) or (short_a.lower() in db.lower())
            if not fenced:
                flags.append({"a": na, "b": nb, "score": round(score, 1),
                              "shared": [t for _, w, t in top if w == 1],
                              "shared_bigrams": [t for _, w, t in top if w == 2],
                              # same name-family (both *-checker, both watch-*): template
                              # siblings — expected wording overlap, a separate finding class
                              "family": family(na) == family(nb),
                              "cross_plugin": na.split(":")[0] != nb.split(":")[0]})
    flags.sort(key=lambda x: (x["family"], -x["score"], x["a"], x["b"]))
    return flags


def neighbors(flags, k=5):
    """Per-artifact top-k selection — the report's recall mechanism. A global top-N window
    lets high-scoring boilerplate pairs crowd out a real twin (measured 2026-08-15: the three
    known-real pairs ranked 171/1000/1682 globally); every artifact surfacing its own k best
    matches keeps any pair that is SOMEONE'S near-twin in the report by construction."""
    per = {}
    for x in flags:
        per.setdefault(x["a"], []).append(x)
        per.setdefault(x["b"], []).append(x)
    keep = []
    seen = set()
    for name in sorted(per):
        for x in sorted(per[name], key=lambda y: -y["score"])[:k]:
            key = (x["a"], x["b"])
            if key not in seen:
                seen.add(key)
                keep.append(x)
    keep.sort(key=lambda x: (x["family"], -x["score"], x["a"], x["b"]))
    return keep


def selftest():
    twin1 = ("p1:alpha-audit", "Audit the widget frobnication economy — measure widget "
             "frobnication collision telemetry lineage across the whole estate menu surface.")
    twin2 = ("p2:beta-audit", "Review widget frobnication collision telemetry lineage costs "
             "for the estate menu surface and report the economy.")
    fenced = ("p2:gamma-audit", "Widget frobnication collision telemetry lineage judge — "
              "NOT for the economy sweep (alpha-audit).")
    vocab = [
        "cooking recipe ingredient baking oven flour yeast dough proofing crust",
        "astronomy telescope nebula galaxy redshift spectrum parallax orbit comet",
        "gardening compost mulch perennial pruning trellis seedling loam bulbs",
        "sailing keel rudder spinnaker tack jibe mooring halyard regatta",
        "chess openings gambit endgame zugzwang castling tempo blunder rook",
        "pottery kiln glaze wheel stoneware bisque slip trimming firing",
        "cycling derailleur cassette peloton cadence crankset drafting sprint",
        "typography kerning serif ligature baseline ascender descender glyph",
    ]
    others = [(f"p3:filler{i}", v) for i, v in enumerate(vocab)]
    # positive: twins collide, flagged cross-plugin
    f = collide([twin1, twin2] + others)
    assert any(x["a"] == "p1:alpha-audit" and x["b"] == "p2:beta-audit" for x in f), f
    assert all(x["cross_plugin"] for x in f if x["a"] == "p1:alpha-audit"), f
    # fence defuses: gamma names alpha-audit → pair (alpha,gamma) must NOT flag
    f2 = collide([twin1, fenced] + others)
    assert not any("gamma" in x["a"] + x["b"] and "alpha" in x["a"] + x["b"] for x in f2), f2
    # negative control: non-overlapping corpus → zero flags
    assert collide(others) == [], "negative control failed"
    # determinism: same input → identical output
    assert collide([twin1, twin2] + others) == collide([twin1, twin2] + others)
    print("collide.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--target")
    ap.add_argument("--threshold", type=float, default=THRESHOLD)
    ap.add_argument("--top", type=int, default=0,
                    help="cap the report at N pairs AFTER neighbor selection (0 = no cap)")
    ap.add_argument("--neighbors", type=int, default=5,
                    help="per-artifact top-k matches kept in the report (recall mechanism)")
    ap.add_argument("--against",
                    help="write-time pre-lint: rank only pairs involving this artifact "
                         "(substring of the qualified name, e.g. 'attention-audit')")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.mode == "selftest":
        return selftest()
    if not a.target:
        print("collide.py: --target required (or `selftest`)", file=sys.stderr)
        return 2
    flags = collide(gather(a.target), a.threshold)
    if a.against:
        flags = [x for x in flags if a.against in x["a"] or a.against in x["b"]]
    else:
        flags = neighbors(flags, a.neighbors)
    total = len(flags)
    if a.top:
        flags = flags[:a.top]
    if a.json:
        print(json.dumps({"total": total, "shown": len(flags), "collisions": flags}, indent=2))
    else:
        for x in flags:
            scope = "CROSS-PLUGIN" if x["cross_plugin"] else "same-plugin"
            fam = " [name-family]" if x["family"] else ""
            ev = ", ".join(x["shared"] + [f'"{b}"' for b in x["shared_bigrams"]])
            print(f"{x['score']:6.1f} {scope}{fam}: {x['a']}  <->  {x['b']}\n"
                  f"       evidence: {ev}")
        print(f"{total} pair(s) over threshold; showing {len(flags)}. Classify each: routing "
              f"twin (unfenced, same ask) / boilerplate tax (shared template sentences) / "
              f"coincidence — the judgment layer's job, not this script's.")
    return 1 if total else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"collide.py error: {e}", file=sys.stderr)
        sys.exit(2)
