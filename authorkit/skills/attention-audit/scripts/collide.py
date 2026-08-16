#!/usr/bin/env python3
"""collide.py — deterministic lexical-collision pre-detection between menu descriptions.

Scans every ROUTABLE description (skills without disable-model-invocation:true, plus all
agents) across the whole estate — cross-plugin BY DEFAULT, because that's the proven blind
spot: same-plugin siblings fence reciprocally, cross-plugin pairs don't, and per-plugin eval
runs never see the collision. A pair is flagged when it shares >= THRESHOLD distinctive terms
AND neither description names the other artifact (a NOT-fence naming the sibling defuses it).

This is the cheap deterministic tier UPSTREAM of harness /check-routing's LLM-judged blind
simulation — it pre-filters, it never replaces the judged run.

Each flagged pair also carries `headroom_a`/`headroom_b` (chars left before that side's OWN
description alone trips skill_lint's W8 700-char ceiling) and `fence_tight` (issue #297: true
when either headroom is under this estate's own shortest measured NOT-clause — no realistic
fence fits without a diet first, the signal the judgment layer uses to prefer a structural-
reduction fix — demote-to-wiring/merge/centralize-boilerplate/retire — over stacking a fence).

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

W8_BUDGET = 700       # harness skill_lint.py's W8 ceiling for a model-invocable description
                      # (issue #79) — every entry collide.py sees is already non-dmi (gather()
                      # excludes disable-model-invocation:true), so W8 applies uniformly here.
MIN_FENCE_CHARS = 23  # shortest real NOT-fence clause measured across this estate's own
                      # descriptions (2026-08-16, n=232 clauses, median 58) — headroom under
                      # this floor means no fence this estate has ever actually shipped would
                      # fit without dieting the description first (issue #297's fence-vs-
                      # reduction criterion: "the fence would blow W8").

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
                # W8-budget headroom (issue #297): chars left before either side's OWN
                # description alone would trip skill_lint's W8 warn ceiling — a proxy for
                # "can this pair even afford a reciprocal fence", not the fence's exact cost
                # (unknowable here: the actual NOT-clause text is a judgment-layer decision).
                headroom_a = W8_BUDGET - len(da)
                headroom_b = W8_BUDGET - len(db)
                flags.append({"a": na, "b": nb, "score": round(score, 1),
                              "shared": [t for _, w, t in top if w == 1],
                              "shared_bigrams": [t for _, w, t in top if w == 2],
                              # same name-family (both *-checker, both watch-*): template
                              # siblings — expected wording overlap, a separate finding class
                              "family": family(na) == family(nb),
                              "cross_plugin": na.split(":")[0] != nb.split(":")[0],
                              "headroom_a": headroom_a,
                              "headroom_b": headroom_b,
                              "fence_tight": headroom_a < MIN_FENCE_CHARS or
                                             headroom_b < MIN_FENCE_CHARS})
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
    # fence-budget headroom (issue #297): both twin1/twin2 sit well under 700 chars → not tight
    assert all(not x["fence_tight"] for x in f if x["a"] == "p1:alpha-audit"), f
    # a description padded to just under the W8 ceiling on one side of a colliding pair MUST
    # flag fence_tight — headroom under MIN_FENCE_CHARS means no realistic NOT-clause fits
    long_desc = twin1[1] + " Joins every plugin's rent figures against real usage evidence " \
        "and a per-release trend series so the report stays verdict-first, evidence-backed. "
    long_desc += "x" * max(0, (W8_BUDGET - MIN_FENCE_CHARS + 5) - len(long_desc))
    assert len(long_desc) > W8_BUDGET - MIN_FENCE_CHARS, len(long_desc)
    tight = ("p1:delta-audit", long_desc)
    f3 = collide([tight, twin2] + others)
    hit = next((x for x in f3 if "delta-audit" in x["a"] + x["b"]), None)
    assert hit is not None, f3
    assert hit["fence_tight"], hit
    tight_headroom = hit["headroom_a"] if "delta-audit" in hit["a"] else hit["headroom_b"]
    assert tight_headroom < MIN_FENCE_CHARS, hit
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
            tight = (f" FENCE-TIGHT (headroom a={x['headroom_a']} b={x['headroom_b']}, "
                     f"min real fence ~{MIN_FENCE_CHARS})" if x["fence_tight"] else "")
            ev = ", ".join(x["shared"] + [f'"{b}"' for b in x["shared_bigrams"]])
            print(f"{x['score']:6.1f} {scope}{fam}{tight}: {x['a']}  <->  {x['b']}\n"
                  f"       evidence: {ev}")
        print(f"{total} pair(s) over threshold; showing {len(flags)}. Classify each and name a "
              f"structural fix (issue #297): routing twin -> reciprocal fence (default) unless "
              f"FENCE-TIGHT or already-fenced-once, then demote-to-wiring/merge/retire; "
              f"boilerplate tax -> centralize-boilerplate; coincidence -> dismiss.")
    return 1 if total else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"collide.py error: {e}", file=sys.stderr)
        sys.exit(2)
