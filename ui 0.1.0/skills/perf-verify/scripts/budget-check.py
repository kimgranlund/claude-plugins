#!/usr/bin/env python3
"""budget-check.py — the perf-verifier performance-budget gate. Self-contained (stdlib only).

perf-verifier reasons about *perceived* latency — the judgment-heavy half (skeleton vs spinner,
streaming presentation, what feedback a surface owes the user) stays a review in SKILL.md. But one
half of the job is pure arithmetic: a measured number vs a budgeted number. *Computation routes to
code, never to inference* — so the budget comparison lives here, deterministic and self-tested.

A "performance budget card" pairs measured metrics with their budget, and may also classify the
async operations of a surface:

  {
    "page": "/checkout",                         # optional label
    "metrics": {                                  # what was measured (any subset)
      "lcp_ms": 3200, "cls": 0.18, "inp_ms": 150, "tbt_ms": 420,
      "bundle_kb": 680, "image_kb": 1200, "requests": 95
    },
    "budget": {                                   # what was budgeted (any subset; CWV have defaults)
      "lcp_ms": 2500, "cls": 0.1, "inp_ms": 200, "tbt_ms": 300,
      "bundle_kb": 300, "image_kb": 500, "requests": 50
    },
    "operations": [                               # async-surface classification (optional)
      {"id": "load-dashboard", "expectedLatencyP50Ms": 600, "expectedLatencyP95Ms": 900,
       "outcomeShape": "known", "idempotent": true, "cancelable": false, "reversible": true,
       "recipe": "skeleton"}                      # recipe optional; cross-checked when present
    ]
  }

Per metric the gate compares measured vs effective-budget and classifies:

  - FAIL (gate)     — measured is over the CWV "poor" threshold (lcp>4000ms, cls>0.25, inp>500ms).
                      Poor is poor regardless of an indulgent local budget.
  - ADVISORY (warn) — over budget but not poor: a regression to watch, not a hard block.
  - OK              — within budget.
  - SKIPPED         — neither a measured value NOR an effective budget exists: nothing to compare.
                      Reported, never silently passed.

Core Web Vitals have canonical budgets, so a missing budget key for lcp/cls/inp/tbt falls back to a
default (lcp 2500ms, cls 0.1, inp 200ms, tbt 300ms). bundle_kb / image_kb / requests have no
universal "good" number, so they are only checked when the card supplies a budget for them.

Per operation (the feedback-window ladder — SKILL.md + thresholds/perception.json):

  - OP_UNCLASSIFIED (advisory) — an operations[] entry missing any required field (id,
                      expectedLatencyP50Ms, expectedLatencyP95Ms, outcomeShape, idempotent,
                      cancelable, reversible). An unclassified async surface is the first finding.
  - RECIPE_MISMATCH (gate)     — a declared recipe contradicts the ladder: the op's P95 falls
                      outside the recipe's valid window. Windows (ms, from the ladder):
                      none/instant 0-100 · busy 0-300 · spinner 300-1000 · skeleton 300-3000 ·
                      skeleton-or-spinner 300-3000 (the union of its legs) ·
                      skeleton+subtle-continuous 300-3000 (the skeleton window) ·
                      progress(+eta+cancel[+explain]) 3000+. A skeleton on a P95<300ms op flashes;
                      none/instant past its ceiling under-indicates (e.g. P95>1000ms with "none").
                      The composite forms are the canon's own vocabulary (thresholds/
                      perception.json); the canon speaks p50, this gate holds P95 — the canon's
                      upgrade rule ("if p95 crosses a boundary, upgrade; never downgrade") made
                      mechanical.
  - CANCEL_MISSING (gate)      — a progress-family recipe WITHOUT "+cancel" on an op with
                      P95 >= 3000ms that is not cancelable:true. The ladder makes cancel
                      mandatory past 3s — the user is otherwise trapped.
  - SHAPE_MISMATCH (advisory)  — a recipe that commits to a skeleton ("skeleton",
                      "skeleton+subtle-continuous") on an op declaring outcomeShape "unknown":
                      a skeleton reserves a known shape; unknown shape wants a spinner
                      ("skeleton-or-spinner" defers the choice, so it is exempt).
  - CWV: UNMEASURED (reported) — the card carries operations[] but no metrics{}: the summary line
                      states it explicitly; unmeasured is never a pass.

  python3 scripts/budget-check.py selftest
  python3 scripts/budget-check.py <card.json | dir>

Python 3.8+.
"""
import json
import os
import sys

# Canonical Core-Web-Vitals "good" budgets — used when the card omits the key.
# (web.dev field thresholds: LCP 2.5s, CLS 0.1, INP 200ms; TBT lab proxy for INP at 300ms.)
CWV_DEFAULT_BUDGET = {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200, "tbt_ms": 300}

# CWV "poor" thresholds — over these is a gate FAIL regardless of the local budget.
# bundle/image/requests have no universal "poor" line, so over-budget there is only ever advisory.
POOR = {"lcp_ms": 4000, "cls": 0.25, "inp_ms": 500}

# Every metric the gate understands; bundle/image/requests are budget-only (no default).
KNOWN_METRICS = ["lcp_ms", "cls", "inp_ms", "tbt_ms", "bundle_kb", "image_kb", "requests"]

# "lower is better" is true for every metric here (latency, shift, weight, count).

# An operations[] entry missing any of these is OP_UNCLASSIFIED (recipe stays optional).
REQUIRED_OP_FIELDS = ["id", "expectedLatencyP50Ms", "expectedLatencyP95Ms", "outcomeShape",
                      "idempotent", "cancelable", "reversible"]

# Valid P95 window (ms) per recipe — the feedback-window ladder (SKILL.md invariants +
# thresholds/perception.json): <100ms instant/none · 100-300ms busy (also harmless below) ·
# 300ms-1s spinner · 300ms-3s skeleton · 3s+ progress(+eta+cancel[, +explain past 10s]).
# The canon's own composite tokens are accepted: skeleton-or-spinner (the union of its two
# legs) and skeleton+subtle-continuous (the skeleton window). P95 below the floor: the
# indicator never earns its window (a skeleton flashes). P95 above the ceiling: the recipe
# under-indicates (perception.json: "if p95 crosses a threshold boundary, upgrade the recipe;
# never downgrade").
RECIPE_WINDOWS = {
    "none": (0, 100),
    "instant": (0, 100),
    "busy": (0, 300),
    "spinner": (300, 1000),
    "skeleton": (300, 3000),
    "skeleton-or-spinner": (300, 3000),
    "skeleton+subtle-continuous": (300, 3000),
    "progress": (3000, None),
    "progress+eta": (3000, None),
    "progress+eta+cancel": (3000, None),
    "progress+eta+cancel+explain": (3000, None),
}

# Recipes that COMMIT to a skeleton (SHAPE_MISMATCH applies); skeleton-or-spinner defers the
# choice, so it is exempt.
SKELETON_COMMITTED = {"skeleton", "skeleton+subtle-continuous"}
# Progress-family recipes whose window starts at the cancel-mandatory boundary (3s).
PROGRESS_FAMILY = {r for r in RECIPE_WINDOWS if r.startswith("progress")}
CANCEL_MANDATORY_MS = 3000


def _num(v):
    """A finite real number, or None. Rejects bool — JSON true must not read as 1."""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
        if f != f or f in (float("inf"), float("-inf")):  # NaN / inf
            return None
        return f
    return None


def check_card(card):
    """Return (fails, advisories, skipped, oks) for one budget card.

    Each list holds human-readable strings. Raises ValueError on a malformed card so the caller
    can report a clean error rather than crash.
    """
    if not isinstance(card, dict):
        raise ValueError("budget card must be a JSON object, got %s" % type(card).__name__)
    metrics = card.get("metrics", {})
    budget = card.get("budget", {})
    if not isinstance(metrics, dict):
        raise ValueError("'metrics' must be an object")
    if not isinstance(budget, dict):
        raise ValueError("'budget' must be an object")

    label = card.get("page") or card.get("label") or "<card>"
    # surface any key the card used that the gate doesn't model — a typo'd metric would otherwise
    # vanish silently (no measured + no budget => skipped, but the user thinks it was checked).
    unknown = sorted((set(metrics) | set(budget)) - set(KNOWN_METRICS))

    fails, advisories, skipped, oks = [], [], [], []
    for m in KNOWN_METRICS:
        measured = _num(metrics.get(m))
        # validate a present-but-non-numeric value rather than treating it as absent
        if m in metrics and measured is None:
            raise ValueError("%s: metric '%s' is not a number: %r" % (label, m, metrics.get(m)))
        bud = _num(budget.get(m))
        if m in budget and bud is None:
            raise ValueError("%s: budget '%s' is not a number: %r" % (label, m, budget.get(m)))

        # effective budget: explicit budget wins; else the CWV default; else none (skip-eligible).
        eff = bud if bud is not None else CWV_DEFAULT_BUDGET.get(m)

        if measured is None and eff is None:
            skipped.append("%s: '%s' — no measured value and no budget; nothing to compare" % (label, m))
            continue
        if measured is None:
            skipped.append("%s: '%s' — budget %s set but no measured value" % (label, m, eff))
            continue
        if eff is None:
            skipped.append("%s: '%s' = %s — no budget (no universal default); supply one to check"
                           % (label, m, _fmt(measured)))
            continue

        src = "" if m in budget else " (CWV default)"
        if m in POOR and measured > POOR[m]:
            fails.append("%s: '%s' = %s over POOR threshold %s (budget %s%s) — gate FAIL"
                         % (label, m, _fmt(measured), _fmt(POOR[m]), _fmt(eff), src))
        elif measured > eff:
            advisories.append("%s: '%s' = %s OVER_BUDGET %s%s (not yet 'poor') — advisory"
                              % (label, m, _fmt(measured), _fmt(eff), src))
        else:
            oks.append("%s: '%s' = %s within budget %s%s" % (label, m, _fmt(measured), _fmt(eff), src))

    for u in unknown:
        skipped.append("%s: unknown metric '%s' — not modeled by this gate; ignored" % (label, u))

    # --- operations[]: async-surface classification + recipe-vs-ladder cross-check --------------
    ops = card.get("operations")
    if ops is not None and not isinstance(ops, list):
        raise ValueError("%s: 'operations' must be a list" % label)
    if ops is None:
        skipped.append("%s: no operations[] — operation-classification checks skipped" % label)
    elif not ops:
        skipped.append("%s: operations[] is empty — operation-classification checks skipped" % label)
    else:
        for i, op in enumerate(ops):
            if not isinstance(op, dict):
                raise ValueError("%s: operations[%d] must be an object" % (label, i))
            oid = op.get("id", "operations[%d]" % i)
            missing = [k for k in REQUIRED_OP_FIELDS if k not in op]
            if missing:
                advisories.append("%s: op '%s' OP_UNCLASSIFIED — missing %s — an async surface "
                                  "with no classification is the first finding"
                                  % (label, oid, ", ".join(missing)))
            p50 = _num(op.get("expectedLatencyP50Ms"))
            if "expectedLatencyP50Ms" in op and p50 is None:
                raise ValueError("%s: op '%s' expectedLatencyP50Ms is not a number: %r"
                                 % (label, oid, op.get("expectedLatencyP50Ms")))
            p95 = _num(op.get("expectedLatencyP95Ms"))
            if "expectedLatencyP95Ms" in op and p95 is None:
                raise ValueError("%s: op '%s' expectedLatencyP95Ms is not a number: %r"
                                 % (label, oid, op.get("expectedLatencyP95Ms")))
            if p50 is not None and p95 is not None and p50 > p95:
                raise ValueError("%s: op '%s' P50 %s > P95 %s — percentiles out of order"
                                 % (label, oid, _fmt(p50), _fmt(p95)))
            recipe = op.get("recipe")
            if recipe is None:
                continue  # recipe is optional; nothing to cross-check
            if not isinstance(recipe, str):
                raise ValueError("%s: op '%s' recipe is not a string: %r" % (label, oid, recipe))
            window = RECIPE_WINDOWS.get(recipe)
            if window is None:
                skipped.append("%s: op '%s' recipe %r not in the feedback-window ladder — "
                               "RECIPE_MISMATCH not evaluated" % (label, oid, recipe))
            elif p95 is None:
                skipped.append("%s: op '%s' declares recipe '%s' but no expectedLatencyP95Ms — "
                               "RECIPE_MISMATCH not evaluated" % (label, oid, recipe))
            else:
                lo, hi = window
                if p95 < lo:
                    fails.append("%s: op '%s' RECIPE_MISMATCH — P95 %sms never reaches the '%s' "
                                 "window (%s–%sms): the indicator would flash; pick the ladder "
                                 "recipe for %sms — gate FAIL"
                                 % (label, oid, _fmt(p95), recipe, _fmt(lo),
                                    "∞" if hi is None else _fmt(hi), _fmt(p95)))
                elif hi is not None and p95 > hi:
                    fails.append("%s: op '%s' RECIPE_MISMATCH — P95 %sms outruns the '%s' window "
                                 "(ceiling %sms): the recipe under-indicates; upgrade per the "
                                 "ladder — gate FAIL" % (label, oid, _fmt(p95), recipe, _fmt(hi)))
                if (recipe in PROGRESS_FAMILY and "+cancel" not in recipe
                        and p95 >= CANCEL_MANDATORY_MS and op.get("cancelable") is not True):
                    fails.append("%s: op '%s' CANCEL_MISSING — '%s' at P95 %sms with no '+cancel' "
                                 "and not cancelable:true: cancel is mandatory past %sms; the "
                                 "user is trapped — gate FAIL"
                                 % (label, oid, recipe, _fmt(p95), _fmt(CANCEL_MANDATORY_MS)))
            if recipe in SKELETON_COMMITTED and op.get("outcomeShape") == "unknown":
                advisories.append("%s: op '%s' SHAPE_MISMATCH — '%s' with outcomeShape 'unknown': "
                                  "a skeleton reserves a known shape; unknown shape wants a "
                                  "spinner (or 'skeleton-or-spinner' to defer) — advisory"
                                  % (label, oid, recipe))
        # operations declared but nothing measured: say so — unmeasured is never a pass.
        if not metrics:
            skipped.append("%s: operations[] declared but no metrics{} — CWV: UNMEASURED "
                           "(reported, never a pass)" % label)

    return fails, advisories, skipped, oks


def _fmt(n):
    """Print 0.18 not 0.18000000001, and 3200 not 3200.0."""
    if n == int(n):
        return str(int(n))
    return ("%.4f" % n).rstrip("0").rstrip(".")


def _summary_line(n, oks, advisories, skipped, unmeasured):
    """The one-line verdict. When a card carries operations[] but no metrics{}, say
    'CWV: UNMEASURED' out loud — unmeasured must never read as a pass."""
    line = ("budget-check: OK — %d card(s); %d metric(s) within budget, %d advisory, %d skipped"
            % (n, len(oks), len(advisories), len(skipped)))
    if unmeasured:
        line += "; CWV: UNMEASURED (operations[] declared, no metrics{})"
    return line


# --- selftest fixtures -------------------------------------------------------------------------
# must-FLAG: lcp over-budget (advisory), cls over the POOR line (FAIL), bundle over-budget (advisory)
FLAG = {
    "page": "/checkout",
    "metrics": {"lcp_ms": 3200, "cls": 0.3, "inp_ms": 150, "tbt_ms": 420,
                "bundle_kb": 680, "image_kb": 1200, "requests": 95},
    "budget":  {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200, "tbt_ms": 300,
                "bundle_kb": 300, "image_kb": 500, "requests": 50},
}
# must-NOT-flag: every metric within budget
CLEAN = {
    "page": "/home",
    "metrics": {"lcp_ms": 1800, "cls": 0.05, "inp_ms": 120, "tbt_ms": 150,
                "bundle_kb": 240, "image_kb": 380, "requests": 32},
    "budget":  {"lcp_ms": 2500, "cls": 0.1, "inp_ms": 200, "tbt_ms": 300,
                "bundle_kb": 300, "image_kb": 500, "requests": 50},
}
# must-NOT-flag: bundle present with no budget + no default -> skipped, reported, not flagged
SKIP = {"page": "/x", "metrics": {"bundle_kb": 999}}
# CWV default kicks in: cls 0.3 with NO budget key still FAILs on the poor line (default 0.1 < 0.3)
DEFAULT_FAIL = {"page": "/y", "metrics": {"cls": 0.3}}
# CWV default: lcp 2600 with no budget -> over the 2500 default but under poor 4000 -> advisory
DEFAULT_ADVISORY = {"page": "/z", "metrics": {"lcp_ms": 2600}}
# empty-ish card: no metrics, no budget -> everything skipped, no fail/advisory, no crash
EMPTY = {"page": "/empty"}
BAD_TYPE = {"metrics": {"lcp_ms": True}}            # bool must not read as 1 -> ValueError
BAD_SHAPE = {"metrics": [1, 2, 3]}                   # metrics not an object -> ValueError
# operations[] fully classified, recipes consistent with the feedback-window ladder -> clean
OPS_CLEAN = {
    "page": "/ops",
    "metrics": {"lcp_ms": 1800, "cls": 0.05},
    "operations": [
        {"id": "save-note", "expectedLatencyP50Ms": 60, "expectedLatencyP95Ms": 90,
         "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True,
         "recipe": "instant"},
        {"id": "load-dashboard", "expectedLatencyP50Ms": 600, "expectedLatencyP95Ms": 900,
         "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True,
         "recipe": "skeleton"},
        {"id": "export-report", "expectedLatencyP50Ms": 4000, "expectedLatencyP95Ms": 9000,
         "outcomeShape": "streamed", "idempotent": True, "cancelable": True, "reversible": True,
         "recipe": "progress+eta+cancel"},
    ],
}
# an op missing its classification fields -> OP_UNCLASSIFIED advisory, never a FAIL
OPS_UNCLASSIFIED = {"page": "/u", "metrics": {"lcp_ms": 1000},
                    "operations": [{"id": "mystery-fetch"}]}
# a fast op declaring skeleton -> RECIPE_MISMATCH (P95 250ms under the 300ms skeleton floor: flash)
OPS_FAST_SKELETON = {"page": "/f", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "toggle-star", "expectedLatencyP50Ms": 120, "expectedLatencyP95Ms": 250,
     "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "skeleton"}]}
# a slow op declaring instant/none -> RECIPE_MISMATCH (P95 2500ms over the 100ms instant ceiling)
OPS_SLOW_INSTANT = {"page": "/s", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "generate-summary", "expectedLatencyP50Ms": 900, "expectedLatencyP95Ms": 2500,
     "outcomeShape": "unknown", "idempotent": False, "cancelable": True, "reversible": False,
     "recipe": "instant"}]}
# operations[] with NO metrics{} -> CWV: UNMEASURED reported (and stated on the summary line)
OPS_NO_METRICS = {"page": "/n", "operations": [
    {"id": "load-feed", "expectedLatencyP50Ms": 500, "expectedLatencyP95Ms": 800,
     "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True}]}
# the canon's composite tokens are accepted and their windows bite (union / skeleton window)
OPS_COMPOSITE_CLEAN = {"page": "/c", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "load-panel", "expectedLatencyP50Ms": 500, "expectedLatencyP95Ms": 800,
     "outcomeShape": "unknown", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "skeleton-or-spinner"},
    {"id": "load-history", "expectedLatencyP50Ms": 1500, "expectedLatencyP95Ms": 2500,
     "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "skeleton+subtle-continuous"}]}
OPS_COMPOSITE_FAST = {"page": "/cf", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "quick-lookup", "expectedLatencyP50Ms": 80, "expectedLatencyP95Ms": 150,
     "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "skeleton-or-spinner"}]}                # P95 150 < the 300ms union floor: flash
# a >=3s progress op with no +cancel and cancelable false -> CANCEL_MISSING (gate)
OPS_CANCEL_MISSING = {"page": "/cm", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "build-archive", "expectedLatencyP50Ms": 4000, "expectedLatencyP95Ms": 5000,
     "outcomeShape": "known", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "progress+eta"}]}
# reverse controls: cancelable:true OR '+cancel' in the recipe satisfies the mandate
OPS_CANCEL_VIA_FLAG = {"page": "/cv", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "sync-library", "expectedLatencyP50Ms": 4000, "expectedLatencyP95Ms": 5000,
     "outcomeShape": "known", "idempotent": True, "cancelable": True, "reversible": True,
     "recipe": "progress+eta"}]}
OPS_CANCEL_VIA_RECIPE = {"page": "/cr", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "export-report", "expectedLatencyP50Ms": 4000, "expectedLatencyP95Ms": 9000,
     "outcomeShape": "streamed", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "progress+eta+cancel"}]}
# a skeleton recipe on an unknown-shape op -> SHAPE_MISMATCH (advisory, never a gate);
# skeleton-or-spinner defers the choice, so unknown shape there is NOT flagged (see
# OPS_COMPOSITE_CLEAN's load-panel).
OPS_SHAPE_MISMATCH = {"page": "/sm", "metrics": {"lcp_ms": 1000}, "operations": [
    {"id": "load-preview", "expectedLatencyP50Ms": 600, "expectedLatencyP95Ms": 900,
     "outcomeShape": "unknown", "idempotent": True, "cancelable": False, "reversible": True,
     "recipe": "skeleton"}]}
BAD_OPS_SHAPE = {"operations": {"id": "x"}}          # operations not a list -> ValueError
BAD_OPS_LATENCY = {"operations": [                   # non-numeric latency -> ValueError
    {"id": "x", "expectedLatencyP50Ms": "fast", "expectedLatencyP95Ms": 100,
     "outcomeShape": "known", "idempotent": True, "cancelable": True, "reversible": True}]}
BAD_OPS_ORDER = {"operations": [                     # P50 > P95 -> ValueError
    {"id": "x", "expectedLatencyP50Ms": 900, "expectedLatencyP95Ms": 100,
     "outcomeShape": "known", "idempotent": True, "cancelable": True, "reversible": True}]}


def selftest():
    errs = []

    def run(card):
        return check_card(card)

    # --- FLAG card -----------------------------------------------------------------------------
    f, a, s, o = run(FLAG)
    if not any("cls" in x and "POOR" in x for x in f):
        errs.append("FLAG: cls 0.3 should be a POOR/FAIL")
    if not any("lcp_ms" in x and "OVER_BUDGET" in x for x in a):
        errs.append("FLAG: lcp 3200 vs 2500 should be an over-budget advisory")
    if not any("bundle_kb" in x and "OVER_BUDGET" in x for x in a):
        errs.append("FLAG: bundle 680 vs 300 should be an over-budget advisory")
    if any("cls" in x for x in a):
        errs.append("FLAG: cls (a FAIL) leaked into advisories")
    if any("lcp_ms" in x for x in f):
        errs.append("FLAG: lcp 3200 (under poor 4000) wrongly classified as FAIL")

    # --- CLEAN card: zero fails, zero advisories ----------------------------------------------
    f, a, s, o = run(CLEAN)
    if f or a:
        errs.append("CLEAN card produced fails/advisories: %s %s" % (f, a))
    if len(o) != len(KNOWN_METRICS):
        errs.append("CLEAN card should pass all %d metrics, got %d OK" % (len(KNOWN_METRICS), len(o)))

    # --- SKIP card: bundle with no budget/default is reported-skipped, never flagged -----------
    f, a, s, o = run(SKIP)
    if f or a:
        errs.append("SKIP: bundle with no budget must not be flagged, got %s %s" % (f, a))
    if not any("bundle_kb" in x and "no budget" in x for x in s):
        errs.append("SKIP: bundle-with-no-budget should be reported as skipped (no silent pass)")

    # --- CWV defaults --------------------------------------------------------------------------
    f, a, s, o = run(DEFAULT_FAIL)
    if not any("cls" in x and "POOR" in x for x in f):
        errs.append("DEFAULT_FAIL: cls 0.3 with no budget should FAIL via the CWV default")
    f, a, s, o = run(DEFAULT_ADVISORY)
    if not any("lcp_ms" in x and "OVER_BUDGET" in x for x in a):
        errs.append("DEFAULT_ADVISORY: lcp 2600 with no budget should be advisory via CWV default")
    if any("lcp_ms" in x for x in f):
        errs.append("DEFAULT_ADVISORY: lcp 2600 (under poor 4000) wrongly a FAIL")

    # --- EMPTY card: all skipped, no crash, no fail/advisory ----------------------------------
    f, a, s, o = run(EMPTY)
    if f or a or o:
        errs.append("EMPTY card should produce no fails/advisories/oks, got %s %s %s" % (f, a, o))
    if not s:
        errs.append("EMPTY card should report skipped metrics, not silently pass")

    # --- operations[]: classification advisory + recipe-vs-ladder gate + UNMEASURED ------------
    f, a, s, o = run(OPS_CLEAN)
    if f or a:
        errs.append("OPS_CLEAN produced fails/advisories: %s %s" % (f, a))
    f, a, s, o = run(OPS_UNCLASSIFIED)
    if not any("OP_UNCLASSIFIED" in x and "mystery-fetch" in x for x in a):
        errs.append("OPS_UNCLASSIFIED: bare op should be an OP_UNCLASSIFIED advisory")
    if f:
        errs.append("OPS_UNCLASSIFIED wrongly FAILED (advisory, not gate): %s" % f)
    f, a, s, o = run(OPS_FAST_SKELETON)
    if not any("RECIPE_MISMATCH" in x and "toggle-star" in x for x in f):
        errs.append("OPS_FAST_SKELETON: skeleton on a P95 250ms op should gate RECIPE_MISMATCH")
    f, a, s, o = run(OPS_SLOW_INSTANT)
    if not any("RECIPE_MISMATCH" in x and "generate-summary" in x for x in f):
        errs.append("OPS_SLOW_INSTANT: 'instant' on a P95 2500ms op should gate RECIPE_MISMATCH")
    # --- composite recipes: the canon's own vocabulary is accepted, and its windows bite --------
    f, a, s, o = run(OPS_COMPOSITE_CLEAN)
    if f or a:
        errs.append("OPS_COMPOSITE_CLEAN produced fails/advisories: %s %s" % (f, a))
    if any("not in the feedback-window ladder" in x for x in s):
        errs.append("OPS_COMPOSITE_CLEAN: composite recipes wrongly skipped as unknown: %s" % s)
    f, a, s, o = run(OPS_COMPOSITE_FAST)
    if not any("RECIPE_MISMATCH" in x and "quick-lookup" in x for x in f):
        errs.append("OPS_COMPOSITE_FAST: skeleton-or-spinner on a P95 150ms op should gate "
                    "RECIPE_MISMATCH")

    # --- CANCEL_MISSING: cancel mandatory past 3s ----------------------------------------------
    f, a, s, o = run(OPS_CANCEL_MISSING)
    if not any("CANCEL_MISSING" in x and "build-archive" in x for x in f):
        errs.append("OPS_CANCEL_MISSING: progress+eta at P95 5000 with cancelable:false should "
                    "gate CANCEL_MISSING")
    f, a, s, o = run(OPS_CANCEL_VIA_FLAG)
    if any("CANCEL_MISSING" in x for x in f):
        errs.append("OPS_CANCEL_VIA_FLAG: cancelable:true must satisfy the cancel mandate: %s" % f)
    f, a, s, o = run(OPS_CANCEL_VIA_RECIPE)
    if any("CANCEL_MISSING" in x for x in f):
        errs.append("OPS_CANCEL_VIA_RECIPE: '+cancel' in the recipe must satisfy the mandate: %s" % f)

    # --- SHAPE_MISMATCH: skeleton commits to a known shape (advisory, never a gate) ------------
    f, a, s, o = run(OPS_SHAPE_MISMATCH)
    if not any("SHAPE_MISMATCH" in x and "load-preview" in x for x in a):
        errs.append("OPS_SHAPE_MISMATCH: skeleton on outcomeShape 'unknown' should be an advisory")
    if f:
        errs.append("OPS_SHAPE_MISMATCH wrongly FAILED (advisory, not gate): %s" % f)

    f, a, s, o = run(OPS_NO_METRICS)
    if f or a:
        errs.append("OPS_NO_METRICS produced fails/advisories: %s %s" % (f, a))
    if not any("CWV: UNMEASURED" in x for x in s):
        errs.append("OPS_NO_METRICS: operations[] without metrics{} should report CWV: UNMEASURED")
    if "CWV: UNMEASURED" not in _summary_line(1, o, a, s, True):
        errs.append("summary line does not state CWV: UNMEASURED for an unmeasured card")
    if "CWV: UNMEASURED" in _summary_line(1, o, a, s, False):
        errs.append("summary line states CWV: UNMEASURED for a measured card")

    # --- malformed cards raise ValueError, not a crash ----------------------------------------
    for label, bad in (("BAD_TYPE (bool-as-number)", BAD_TYPE),
                       ("BAD_SHAPE (metrics not object)", BAD_SHAPE),
                       ("BAD_OPS_SHAPE (operations not a list)", BAD_OPS_SHAPE),
                       ("BAD_OPS_LATENCY (non-numeric latency)", BAD_OPS_LATENCY),
                       ("BAD_OPS_ORDER (P50 > P95)", BAD_OPS_ORDER)):
        try:
            run(bad)
            errs.append("%s should have raised ValueError" % label)
        except ValueError:
            pass
        except Exception as e:  # any other exception = a crash, not a clean error
            errs.append("%s raised %s, not ValueError" % (label, type(e).__name__))

    return errs


def _iter_cards(path):
    if os.path.isdir(path):
        for dp, _, fns in os.walk(path):
            for fn in sorted(fns):
                if fn.endswith(".budget.json"):
                    yield os.path.join(dp, fn)
    else:
        yield path


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("budget-check: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("budget-check: OK — budget comparison + operations classification verified over "
              "good/bad fixtures")
        return 0

    fails, advisories, skipped, oks, n = [], [], [], [], 0
    for fp in _iter_cards(argv[0]):
        try:
            doc = json.load(open(fp, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            fails.append("%s: unreadable (%s)" % (fp, e))
            continue
        for card in (doc if isinstance(doc, list) else [doc]):
            n += 1
            try:
                f, a, s, o = check_card(card)
            except ValueError as e:
                fails.append("%s: malformed card — %s" % (fp, e))
                continue
            fails += f
            advisories += a
            skipped += s
            oks += o

    for x in skipped:
        print("  · SKIP %s" % x)
    for x in advisories:
        print("  ⚠ %s" % x)
    if fails:
        sys.stderr.write("budget-check: FAIL (%d)\n" % len(fails))
        for x in fails:
            sys.stderr.write("  - %s\n" % x)
        return 1
    unmeasured = any("CWV: UNMEASURED" in s for s in skipped)
    print(_summary_line(n, oks, advisories, skipped, unmeasured))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
