#!/usr/bin/env python3
"""calibration-check-strategy <transcript> — score a brand-council transcript against the fixture's planted defects.

Given the critique the brand council produced over
`calibration/council-calibration/fixtures/weak-brand-strategy.md`, assert it surfaced each
PLANTED defect — the `rubric-brand-strategy` anti-patterns plus the bullshit filter. Concept-level
matching (tolerant of phrasing); reports a catch-rate, not a CI gate, because the council is an LLM
panel — the recorded protocol + fixtures + run history live in
`calibration/council-calibration/` (verbatim, ported from brand-forge's own eval).

Usage:
  calibration_check_strategy.py <transcript-file>   # exit 0 = every planted defect caught
  calibration_check_strategy.py selftest
Stdlib only.
"""
import re
import sys

PLANTED = {
    "D1 borrowed cultural root (no real provenance)": [
        r"borrowed", r"competitor", r"moodboard", r"other brands", r"\blandscape\b", r"no .{0,14}root",
        r"lifted", r"provenance", r"desk research", r"receipts", r"not .{0,10}earned",
    ],
    "D2 category-restatement position (not exclusive)": [
        r"category restatement", r"restates the category", r"(?:any|every) (?:rival|competitor|brand)", r"could sign",
        r"not exclusive", r"undifferentiated", r"premium choice", r"sign their name", r"no (?:real |ownable )?position",
        r"(?:put|place)s? (?:their|its) name",
        # I-13: real council wordings the prior patterns missed — "every premium coffee brand could publish
        # this verbatim" / "could run under a … letterhead" (interchangeable, not ownable).
        r"(?:any|every) .{0,24}brand could", r"letterhead", r"publish .{0,12}verbatim",
    ],
    "D4 no enemy / no tension": [
        r"no enemy", r"nothing to (?:oppose|stand against)", r"frictionless", r"for everyone", r"no tension",
        r"stands? for nothing", r"refuses nothing", r"excludes? no", r"stand against",
    ],
    "D5 persona instead of transformation": [
        r"persona", r"demographic", r"\bsarah\b", r"not a transformation", r"becom(?:e|es|ing)",
        r"before.{0,8}after", r"who they are.{0,20}not",
    ],
    "D6 values without trade-offs": [
        r"trade.?off", r"sacrifice", r"costs? nothing", r"values .{0,20}(?:wish|decoration)", r"give up",
        r"tautolog", r"can(?:not|'t) disagree",
    ],
    "bullshit filter: archetype / VMV doing strategy's job": [
        r"archetype", r"\bexplorer\b", r"horoscope", r"vision/mission/values", r"\bvmv\b",
        r"mission statement", r"boilerplate", r"vision and mission",
    ],
}


def score(text):
    """Return (caught, missed) — each a list of (defect, matched-pattern-or-None). `text` already lowered."""
    caught, missed = [], []
    for defect, pats in PLANTED.items():
        hit = next((p for p in pats if re.search(p, text)), None)
        (caught if hit else missed).append((defect, hit))
    return caught, missed


def report(path):
    text = open(path, encoding="utf-8", errors="replace").read().lower()
    caught, missed = score(text)
    for d, p in caught:
        print(f"  CAUGHT  {d}\n            (matched /{p}/)")
    for d, _ in missed:
        print(f"  MISSED  {d}")
    print(f"\nRESULT: brand council-calibration (strategy): {len(caught)}/{len(PLANTED)} planted defects caught")
    return 0 if not missed else 1


def selftest():
    import io
    import tempfile

    fails = []

    def expect(c, m):
        if not c:
            fails.append(m)

    good_text = (
        "The critique found a borrowed root, a position that is not exclusive, no enemy in sight, "
        "a customer persona, no trade-off named, and reliance on an archetype."
    )
    bad_text = good_text.replace("archetype", "")  # drops the bullshit-filter defect only

    with tempfile.TemporaryDirectory() as td:
        good = f"{td}/good.md"
        bad = f"{td}/bad.md"
        open(good, "w", encoding="utf-8").write(good_text)
        open(bad, "w", encoding="utf-8").write(bad_text)

        caught, missed = score(good_text.lower())
        expect(len(caught) == len(PLANTED) and not missed,
               f"reverse control: a transcript naming every planted defect must catch all {len(PLANTED)}, "
               f"got {len(caught)} (missed: {[d for d, _ in missed]})")

        caught2, missed2 = score(bad_text.lower())
        expect(len(missed2) == 1 and missed2[0][0].startswith("bullshit filter"),
               f"negative control: dropping the archetype phrase must miss exactly the bullshit-filter "
               f"defect, got missed={[d for d, _ in missed2]}")

        old = sys.stdout
        sys.stdout = io.StringIO()
        try:
            rc_good = report(good)
            rc_bad = report(bad)
        finally:
            sys.stdout = old
        expect(rc_good == 0, f"report() must exit 0 when every planted defect is caught, got {rc_good}")
        expect(rc_bad == 1, f"report() must exit 1 when a planted defect is missed, got {rc_bad}")

    if fails:
        sys.stderr.write("calibration-check-strategy selftest: FAIL\n")
        for m in fails:
            sys.stderr.write(f"  - {m}\n")
        return 1
    print("calibration-check-strategy selftest: OK (a transcript naming every planted defect catches all "
          f"{len(PLANTED)}; dropping the archetype phrase misses exactly the bullshit-filter defect; "
          "report() exit codes track catch/miss)")
    return 0


def main(argv):
    if argv and argv[0] == "selftest":
        return selftest()
    if len(argv) != 1:
        print("usage: calibration_check_strategy.py <transcript-file> | selftest", file=sys.stderr)
        return 2
    return report(argv[0])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
