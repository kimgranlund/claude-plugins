#!/usr/bin/env python3
"""journal_check.py — arithmetic shape-check of an investigation journal (research-methods).

Checks the three LINE-CHECKABLE gates of references/rubric.md against a run's journal:

  R1 scorer-first : a baseline line carrying a NUMBER appears BEFORE the loop begins
  R3 one-variable : a single-variable declaration exists, or no round block carries >1 change
  R7 termination  : the journal ends on a NAMED stop predicate, not mid-loop

Three-valued per gate — PASS / FAIL / UNMEASURED — because an arithmetic check can only
grade the structures it can see: a journal written in an unrecognized shape is UNMEASURED
(a skipped check surfaced honestly), never laundered into a pass. This is a TRIAGE aid for
the consumer-as-critic (the dispatching seat that grades the run); judgment dimensions
(R2/R4/R5/R6/R8) are not checkable here and are not attempted.

Usage:
  python3 journal_check.py <JOURNAL.md>     # exit 0 = no FAIL; exit 2 = >=1 gate FAILED
  python3 journal_check.py selftest         # prove the checks fire and hold
"""
import re
import sys
import pathlib

# The loop starts where Phase 1 / the first round entry begins.
_LOOP_START = re.compile(r"(?im)^#+ *phase *1\b|^#+ *round *1\b|^round *1[:\s]")
# A baseline line must carry a number (a baseline without a value is not a baseline).
_BASELINE = re.compile(r"(?im)^.*\bbaseline\b[^\n]*?[-+]?\d[\d.,]*")
# Declared single-variable forms (the sweep fixture: "one variable: threshold").
_ONE_VAR = re.compile(r"(?i)\b(?:one|single) (?:variable|parameter|change per round)\b")
# A round block header, and a change declaration inside one.
_ROUND = re.compile(r"(?im)^(?:#+ *)?round *\d+\b")
_CHANGE = re.compile(r"(?im)^\s*(?:[-*] *)?change[d]?\s*[:=]")
# Named stop predicates from the method files' exit conditions.
_PREDICATE = re.compile(
    r"(?i)\b(?:space exhausted|exhausted|plateau|local optimum|target (?:reached|held|hit)|"
    r"perfect|max[_ ]?rounds|budget|stuck|\d+ consecutive reverts|cause (?:isolated|found)|"
    r"converged?)\b")
# A stop marker: a heading/line that says the loop stopped.
_STOP_LINE = re.compile(r"(?im)^.*\b(?:stop|stopped|predicate)\b.*$")


def check(text):
    """Return {'R1'|'R3'|'R7': ('PASS'|'FAIL'|'UNMEASURED', reason)}."""
    out = {}
    loop = _LOOP_START.search(text)

    # R1 — a numeric baseline BEFORE the loop.
    base = _BASELINE.search(text)
    if not loop:
        out["R1"] = ("UNMEASURED", "no recognizable loop marker (Phase 1 / Round 1) — shape unknown")
    elif base and base.start() < loop.start():
        out["R1"] = ("PASS", "numeric baseline recorded before the loop")
    elif base:
        out["R1"] = ("FAIL", "baseline appears only AFTER the loop began — scorer not fixed first")
    else:
        out["R1"] = ("FAIL", "no numeric baseline line found")

    # R3 — single-variable discipline.
    rounds = list(_ROUND.finditer(text))
    if _ONE_VAR.search(text):
        out["R3"] = ("PASS", "single-variable declaration present")
    elif rounds:
        worst = 0
        spans = [m.start() for m in rounds] + [len(text)]
        for i in range(len(rounds)):
            block = text[spans[i]:spans[i + 1]]
            worst = max(worst, len(_CHANGE.findall(block)))
        if worst > 1:
            out["R3"] = ("FAIL", f"a round block declares {worst} changes — batched round")
        else:
            out["R3"] = ("PASS", "every round block declares at most one change")
    else:
        out["R3"] = ("UNMEASURED", "no single-variable declaration and no round blocks — shape unknown")

    # R7 — a named stop predicate at/near the close.
    stops = [m for m in _STOP_LINE.finditer(text) if _PREDICATE.search(m.group(0))]
    if not stops:
        # allow predicate named on the line after a bare stop marker (fixture: "## Phase 1 — stop\nPredicate: ...")
        for m in _STOP_LINE.finditer(text):
            tail = text[m.end():m.end() + 200]
            if _PREDICATE.search(tail.split("\n\n")[0]):
                stops.append(m)
                break
    if stops:
        out["R7"] = ("PASS", "stop line names a registered predicate")
    elif _STOP_LINE.search(text):
        out["R7"] = ("FAIL", "a stop line exists but names no registered predicate — stopped on patience?")
    else:
        out["R7"] = ("UNMEASURED", "no stop line found — journal may be truncated or an unrecognized shape")

    return out


def report(path):
    text = pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")
    res = check(text)
    failed = False
    print(f"journal_check — {path}")
    for gate in ("R1", "R3", "R7"):
        status, why = res[gate]
        print(f"  [{status:>10}] {gate}: {why}")
        failed |= status == "FAIL"
    print("  note: triage only — R2/R4/R5/R6/R8 are judgment; the dispatching seat grades the run.")
    return 2 if failed else 0


# --- selftest fixtures (condensed from the real 2026-07-04 threshold-sweep journal) -------------
_GOOD = """# SWEEP round journal
Scorer (fixed BEFORE the loop): macro-F1 over every pair.
## Phase 0 — baseline
Baseline t=0.34: macro-F1 = 0.8699, trip = 1.
## Phase 1 — the sweep (one variable: threshold)
Coarse pass 0.10→0.60 ... fine pass 0.30→0.40 ...
## Phase 1 — stop
Predicate: SPACE EXHAUSTED (full coarse grid + one fine pass).
"""
_NO_BASELINE = _GOOD.replace("Baseline t=0.34: macro-F1 = 0.8699, trip = 1.", "We began sweeping right away.")
_LATE_BASELINE = """# journal
## Phase 1 — loop
Round 1: tried a change.
## Wrap-up
Baseline was 42 (measured at the end).
## Phase 1 — stop
Predicate: target reached.
"""
_BATCHED = """# autoresearch journal
## Phase 0 — baseline
Baseline: 61/100.
## Phase 1
Round 1:
  change: added input validation
  change: also rewrote the parser
## stop
Predicate: plateau.
"""
_NO_PREDICATE = _GOOD.replace("Predicate: SPACE EXHAUSTED (full coarse grid + one fine pass).",
                              "We felt done and wrapped up the loop here.")
_PROSE = "Some meeting notes about baselines and stopping by the office. No rounds, no phases."


def selftest():
    errs = []
    g = check(_GOOD)
    if not all(g[k][0] == "PASS" for k in g):
        errs.append(f"good fixture should pass all gates: {g}")
    if check(_NO_BASELINE)["R1"][0] != "FAIL":
        errs.append("missing baseline not flagged (R1)")
    if check(_LATE_BASELINE)["R1"][0] != "FAIL":
        errs.append("late baseline not flagged (R1)")
    if check(_BATCHED)["R3"][0] != "FAIL":
        errs.append("batched round not flagged (R3)")
    b = check(_BATCHED)
    if b["R1"][0] != "PASS" or b["R7"][0] != "PASS":
        errs.append(f"batched fixture's R1/R7 should still pass: {b}")
    if check(_NO_PREDICATE)["R7"][0] != "FAIL":
        errs.append("stop-on-patience not flagged (R7)")
    # negative control: unstructured prose must be UNMEASURED, never PASS.
    p = check(_PROSE)
    if any(p[k][0] == "PASS" for k in p):
        errs.append(f"prose negative control wrongly passed a gate: {p}")
    if errs:
        print("journal_check selftest: FAIL")
        for e in errs:
            print("  -", e)
        return 1
    print("journal_check selftest: OK — R1 (missing + late baseline), R3 (batched round), "
          "R7 (stop-on-patience) fire; the real-fixture shape passes; prose control stays UNMEASURED")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(selftest() if sys.argv[1] == "selftest" else report(sys.argv[1]))
