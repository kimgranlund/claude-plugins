#!/usr/bin/env python3
"""calibration-replay — drive the brand-guidelines machinery end to end on a recorded ledger.

A behavioral proof (CI-replayable, no model agent): the interactive 2x2 (propose options -> designer
picks A/B/C/D + comments) PRODUCES a choice-ledger; this replays the deterministic half the catalog
can gate — validate -> coverage -> coherence -> assemble -> **corpus-provenance clean** -> project a
brand-spec card, against the recorded "Meridian" ledger (bundled inline below; the original worked
example + its own walkthrough narrative live verbatim in
`calibration/guidelines-walkthrough/`, incl. `meridian.ledger.json` and its README). It
proves the loop closes on a realistic, coherent brand (with a superseded first color pass that the
restrained palette replaces, and a `constrains` coherence edge), and doubles as the worked example.

Drives the sibling `guidelines_ledger.py` and `corpus_provenance.py` scripts exactly as a user would
from the command line (subprocess, not import) — the proof is of the real CLI surface.

Usage:
  calibration_replay.py            # replay the bundled Meridian ledger end to end; exit 0 = loop closes
  calibration_replay.py selftest   # reverse control (the good ledger closes) + negative control (a
                                    # broken ledger is rejected at validate) via the real subprocess path
Stdlib only; Python 3.8+.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GL = os.path.join(HERE, "guidelines_ledger.py")
CP = os.path.join(HERE, "corpus_provenance.py")

# The recorded Meridian ledger — verbatim copy of calibration/guidelines-walkthrough/
# meridian.ledger.json's own content, inlined so this script has no relative-path dependency on
# where it's invoked from (a bundled scripts/ script must be self-contained).
MERIDIAN_LEDGER = {
    "brand": "Meridian",
    "created": "2026-06-20",
    "entries": [
        {
            "id": "mark-r1", "domain": "mark", "round": 1,
            "axes": ["literal-metaphorical", "systematic-organic"],
            "presented": ["A", "B", "C", "D"], "chosen": "A",
            "comment": "the stitch reference is the whole idea — keep it literal",
            "move": {
                "move": "A geometric 'M' monogram constructed from a Coptic bookbinding stitch pattern",
                "rationale": "literal + systematic: the mark IS the craft, drawn on a grid so it holds at a favicon",
                "expected_effect": "ownable, trademark-clean, legible at every size",
                "severity": "must",
                "exemplar_evidence": [{"brand": "Penguin", "what": "the orange-band system",
                                        "why_cited": "a publishing mark that is a constructed system, not a picture"}],
                "confidence": 0.9,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": None,
        },
        {
            "id": "voice-r1", "domain": "voice", "round": 1,
            "axes": ["institutional-conversational", "functional-expressive"],
            "presented": ["A", "B", "C", "D"], "chosen": "A",
            "comment": "no hype; the objects speak",
            "move": {
                "move": "Spare and considered — name the craft and the material, never the hype; lead with the made thing",
                "rationale": "institutional + functional restraint: gravitas through under-statement, the opposite of disposable-age noise",
                "expected_effect": "copy a stranger can extend without drifting into marketing-speak",
                "severity": "should",
                "exemplar_evidence": [{"brand": "Aesop", "what": "ingredient-first product copy",
                                        "why_cited": "restraint that reads as authority"}],
                "confidence": 0.85,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": None,
        },
        {
            "id": "color-r1", "domain": "color", "round": 1,
            "axes": ["functional-expressive", "restraint-loudness"],
            "presented": ["A", "B", "C", "D"], "chosen": "D",
            "comment": "first pass — felt too loud against the spare voice",
            "move": {
                "move": "A saturated jewel-tone palette, color-forward across every surface",
                "rationale": "expressive + loud: maximum shelf presence",
                "expected_effect": "high energy, hard to miss",
                "severity": "should",
                "confidence": 0.6,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": None,
        },
        {
            "id": "color-r2", "domain": "color", "round": 2,
            "axes": ["functional-expressive", "restraint-loudness"],
            "presented": ["A", "B", "C", "D"], "chosen": "B",
            "comment": "this — restrained, with the one gold tell",
            "move": {
                "move": "Ink-black and cream as the system; a single foredge-gold accent used sparingly as the brand's 'tell'",
                "rationale": "expressive + restrained: one ownable color that coheres with the spare voice instead of fighting it",
                "expected_effect": "recognition through the gold detail; high contrast headroom for accessibility",
                "severity": "should",
                "exemplar_evidence": [{"brand": "Rizzoli", "what": "ink-on-cream with metallic detail",
                                        "why_cited": "restrained-expressive in the book world"}],
                "confidence": 0.88,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": "color-r1",
        },
        {
            "id": "type-r1", "domain": "type", "round": 1,
            "axes": ["systematic-organic", "functional-expressive"],
            "presented": ["A", "B", "C", "D"], "chosen": "C",
            "move": {
                "move": "A book-faced serif for display (the voice), a neutral grotesque workhorse for UI and specs",
                "rationale": "organic + expressive display carries the craft; a systematic workhorse keeps it operable",
                "expected_effect": "the page feels bound, not branded; specs stay legible",
                "severity": "should",
                "exemplar_evidence": [{"brand": "The Paris Review", "what": "editorial serif + quiet sans",
                                        "why_cited": "type that reads as a publication, not a product"}],
                "confidence": 0.82,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": None,
        },
        {
            "id": "expression-r1", "domain": "expression", "round": 1,
            "axes": ["quiet-loud", "restraint-loudness"],
            "presented": ["A", "B", "C", "D"], "chosen": "A",
            "comment": "let the objects breathe",
            "move": {
                "move": "Generous margins, a slow grid, product-true photography of the bound objects on cream — no stock, no campaign loudness",
                "rationale": "quiet + premium: the expression grammar is the restraint the color and voice already chose",
                "expected_effect": "the room reads as considered; new work is generated from the grid, not copied",
                "severity": "should",
                "exemplar_evidence": [{"brand": "Kinfolk", "what": "slow editorial layout",
                                        "why_cited": "quiet-premium expression as a generative grammar"}],
                "confidence": 0.8,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": None,
        },
        {
            "id": "governance-r1", "domain": "governance", "round": 1,
            "axes": ["systematic-organic", "product-led-human-led"],
            "presented": ["A", "B", "C", "D"], "chosen": "B",
            "move": {
                "move": "A named brand steward + a one-page principles sheet; partner lockups require the steward's sign-off",
                "rationale": "organic + human-led: a small studio steward beats a heavy token system the team won't maintain",
                "expected_effect": "the brand survives contact with real work without a bureaucracy",
                "severity": "must",
                "confidence": 0.78,
            },
            "contributors": [
                {"who": "S. (strategist)", "role": "chooser", "date": "2026-06-20"},
                {"who": "brand-guidelines", "role": "proposer", "date": "2026-06-20"},
            ],
            "supersedes": None,
        },
    ],
    "graph": [
        {"from": "color-r2", "to": "expression", "relationship": "constrains"},
        {"from": "voice-r1", "to": "expression", "relationship": "supports"},
    ],
}


def _run(script, *args):
    return subprocess.run([sys.executable, script, *args], capture_output=True, text=True)


def walkthrough(ledger_dict, log=print):
    """Drive validate -> coverage -> coherence -> assemble -> corpus-provenance -> card over
    `ledger_dict`, written to a temp file so the CLI tools see a real path. Returns a list of
    failure strings (empty = the loop closed cleanly)."""
    fails = []

    def expect(c, m):
        if not c:
            fails.append(m)

    d = tempfile.mkdtemp(prefix="calibration-replay-")
    try:
        ledger_path = os.path.join(d, "ledger.json")
        json.dump(ledger_dict, open(ledger_path, "w", encoding="utf-8"))

        r = _run(GL, "validate", ledger_path)
        expect(r.returncode == 0, f"ledger does not validate: {r.stderr.strip()}")
        if r.returncode != 0:
            return fails  # every later step depends on a valid ledger; stop here

        r = _run(GL, "coverage", ledger_path)
        expect("6/6 domains resolved" in r.stdout,
               f"not all six domains resolved (supersession honored?): {r.stdout.strip()}")

        r = _run(GL, "coherence", ledger_path)
        expect(r.returncode == 0 and "constrains" in r.stdout,
               f"coherence did not surface the constrains edge: {r.stdout.strip()}")

        out = os.path.join(d, "corpus")
        os.makedirs(os.path.join(out, "00-sources"))
        ledger_in_corpus = os.path.join(out, "00-sources", "guidelines-elicitation.json")
        shutil.copy(ledger_path, ledger_in_corpus)

        r = _run(GL, "assemble", ledger_in_corpus, "--out", out, "--apply")
        expect(r.returncode == 0, f"assemble failed: {r.stderr.strip()}")
        for layer, dom in (("03-identity", "mark"), ("04-expression", "color"), ("04-expression", "type"),
                           ("04-expression", "expression"), ("05-voice", "voice"), ("07-guidelines", "governance")):
            expect(os.path.isfile(os.path.join(out, layer, f"{dom}.md")), f"assemble did not write {layer}/{dom}.md")

        color_doc = os.path.join(out, "04-expression", "color.md")
        if os.path.isfile(color_doc):
            txt = open(color_doc).read()
            expect("foredge-gold" in txt, "assembled color doc lost the live (restrained) choice")
            expect("jewel-tone" not in txt, "assembled color doc kept the SUPERSEDED loud choice")

        r = _run(CP, out)
        expect(r.returncode == 0, f"corpus-provenance is not clean on the assembled corpus: "
                                   f"{r.stdout.strip()} {r.stderr.strip()}")

        card = os.path.join(out, "meridian.brand.json")
        r = _run(GL, "card", ledger_in_corpus, "--idea", "The pleasure of permanence in a disposable age.",
                  "-o", card)
        expect(os.path.isfile(card), "brand-spec card was not projected")
        if os.path.isfile(card):
            c = json.load(open(card))
            expect(len(c.get("rules", [])) >= 6, "projected card has fewer than the six domain rules")
            expect(c["strategy"]["brand_idea"].startswith("The pleasure of permanence"), "card lost the brand idea")
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return fails


def main():
    fails = walkthrough(MERIDIAN_LEDGER)
    if fails:
        sys.stderr.write("calibration-replay: FAIL\n")
        for m in fails:
            sys.stderr.write(f"  - {m}\n")
        return 1
    print("calibration-replay: OK (Meridian ledger -> validate -> 6/6 coverage -> coherence (constrains) -> "
          "assemble [superseded loud color dropped, restrained kept] -> corpus-provenance clean -> brand-spec "
          "card; the loop closes end to end on a realistic brand)")
    return 0


def selftest():
    fails = []

    def expect(c, m):
        if not c:
            fails.append(m)

    # Reverse control: the bundled good ledger closes the whole loop clean.
    good_fails = walkthrough(MERIDIAN_LEDGER)
    expect(good_fails == [], f"the bundled Meridian ledger must replay clean; got: {good_fails}")

    # Negative control: a ledger missing a required top-level field must be REJECTED at validate,
    # and the walkthrough must report exactly that failure (not silently proceed).
    broken = copy.deepcopy(MERIDIAN_LEDGER)
    del broken["created"]
    broken_fails = walkthrough(broken)
    expect(any("does not validate" in m for m in broken_fails),
           f"a ledger missing `created` must fail at the validate step; got: {broken_fails}")
    expect(len(broken_fails) == 1,
           f"validate failure must short-circuit the rest of the pipeline (one finding, not a cascade); "
           f"got: {broken_fails}")

    if fails:
        sys.stderr.write("calibration-replay selftest: FAIL\n")
        for m in fails:
            sys.stderr.write(f"  - {m}\n")
        return 1
    print("calibration-replay selftest: OK (the bundled Meridian ledger replays clean end to end; a ledger "
          "missing a required field is rejected at validate and the pipeline short-circuits rather than "
          "cascading)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(selftest())
    if len(sys.argv) > 1:
        print("usage: calibration_replay.py [selftest]", file=sys.stderr)
        sys.exit(2)
    sys.exit(main())
