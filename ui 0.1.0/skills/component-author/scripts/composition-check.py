#!/usr/bin/env python3
"""composition-check.py — the COMPOSITION card gate (component-author's COMPOSE A4 / A5).

This is the multi-component *composition card* gate — the complement to component-contract-check.py
(the single-component contract card). Where contract-check lints ONE component's anatomy/API/FACE,
this lints how components NEST and WIRE up the tier ladder (primitive → component → module). The
composition rubric is mostly judgment (the COMPOSE A4 Composition / A5 Coherence rungs in SKILL.md),
but a few joints are arithmetic, not taste, and are routed here so a clean-looking composition card
can't hide a mis-cut boundary or a seamless component:

  • tier-consistency  — a primitive composes nothing; a component composes >=1 piece AND has a seam;
                        a module arranges >=2 components and does not tier-skip to a raw primitive
                        (the A4 tier ladder).
  • the SEAM gate      — a component MUST expose a seam: named slots, or an overflow mechanism. A
                        seamless component is "boxed but inert" (A4 — the cross-component slot/state
                        seam, which folds into REALIZE B3/B4 as a cross-component note).
  • overflow-declared  — a capacity-constrained axis carrying many action-primitives MUST declare an
                        overflow mechanism (A4 / the cross-component interaction note on B4).
  • god-component fanout — a component composing > 7 pieces smells like a mis-cut module (A4).
  • no self-margin     — a piece must not set its own outer margin; spacing BETWEEN pieces is the
                        parent composition's gap / region grid (A5 — the same no-outer-margin rule
                        component-contract-check warns on for a single component).

And one generator — the slot-presence -> grid-columns mapping: the deterministic layout the
slot-presence grid rests on, where an ABSENT slot leaves NO phantom column. The MODULE → app-shell
boundary hands UP to layout-decompose (this gate stops at the module; the page / region grid it sits
in is layout-decompose's).

Usage:
  composition-check.py lint <card.composition.json>     # the A4 / A5 composition-card linter
  composition-check.py lint [--json] <card.composition.json>   # machine-readable report
  composition-check.py slot-grid <comma,slots>          # slot-presence -> grid-template-columns
  composition-check.py selftest                          # good / bad fixtures (the law, proven)

A *.composition.json card:
  {"name":"toolbar","tier":"component",
   "contains":[{"name":"x-button","tier":"primitive","role":"action"}, ...],
   "slots":["actions"],"axis":"horizontal","overflow":"priority-menu","selfMargin":false}

`--json` (additive reporting flag; parse-anywhere after `lint`) prints ONE machine-readable report
object to stdout and NOTHING else there — the shared schema every lint bin emits:
  {"tool": "composition-check", "ok": <bool>, "summary": "<one line>",
   "findings": [{"kind", "severity": fail|advisory, "location": "<component label>", "message"}, ...]}
`ok` is true iff no error (the exact condition that gives exit 0 in `lint` mode). A gate error
(tier/seam/overflow/self-margin) maps to severity `fail`; a warning (god-component / tier-skip) to
`advisory`. The exit code is UNCHANGED by --json. `--json` applies to `lint` only — `slot-grid` is a
generator, not a lint. Without --json, output + exit are byte-identical.
"""
import json
import sys

TIERS = ("primitive", "component", "module")
# the canonical content slot gets `1fr`; every other present slot gets an `auto` column.
CONTENT_SLOTS = ("content", "body", "label")
# a component composing more than this many pieces smells like a module / god-component (A4).
GOD_COMPONENT_FANOUT = 7


def lint(card):
    """Return (errors, warnings) for a composition descriptor (COMPOSE A4 / A5)."""
    errs, warns = [], []
    tier = card.get("tier")
    if tier not in TIERS:
        return ([f"tier {tier!r} is not one of {TIERS} (A4 tier ladder)"], [])

    contains = card.get("contains", []) or []
    slots = card.get("slots", []) or []
    overflow = card.get("overflow")
    axis = card.get("axis", "none")
    has_seam = bool(slots) or bool(overflow)

    # A5 — no self-owned outer margin
    if card.get("selfMargin"):
        errs.append("selfMargin: true — a piece must not set its own outer margin; spacing BETWEEN "
                    "pieces is the parent's gap / region grid (A5)")

    if tier == "primitive":
        if contains:
            errs.append(f"a primitive composes {len(contains)} piece(s); a primitive is an atom "
                        "(the leaf — its own contract card) — re-tier to 'component' (A4)")
    elif tier == "component":
        if not contains:
            errs.append("a component composes no pieces — it is a primitive, or its children are missing (A4)")
        if not has_seam:
            errs.append("SEAM gate: a component exposes no slots and no overflow — 'boxed but inert'; "
                        "give it named slots or an overflow mechanism (A4 / REALIZE B3 seam)")
        if len(contains) > GOD_COMPONENT_FANOUT:
            warns.append(f"a component composes {len(contains)} pieces (> {GOD_COMPONENT_FANOUT}) — "
                         "possible god-component; is this really a module? (A4)")
    elif tier == "module":
        comp_children = [c for c in contains if c.get("tier") == "component"]
        if len(comp_children) < 2:
            errs.append(f"a module arranges {len(comp_children)} component(s); a module needs >=2 components "
                        "in regions with cross-component state — else it is a component (A4)")
        skips = [c.get("name") for c in contains if c.get("tier") == "primitive"]
        if skips:
            warns.append(f"a module nests raw primitive(s) {skips} with no component between (tier-skip) — "
                         "wrap them in a component, or mark the exception (A4). The module's app shell "
                         "hands UP to layout-decompose.")

    # A4 / REALIZE B4 — overflow on a capacity-constrained axis carrying many actions
    actions = [c for c in contains if c.get("role") == "action"]
    if axis in ("horizontal", "vertical") and len(actions) >= 4 and not overflow:
        errs.append(f"a {axis} axis carries {len(actions)} actions but declares no overflow mechanism — "
                    "it will clip or wrap; declare a priority-overflow seam (A4 / REALIZE B4)")

    return (errs, warns)


def slot_grid(present):
    """The deterministic slot-presence -> grid-template-columns mapping (an absent slot => no column)."""
    cols = ["1fr" if s in CONTENT_SLOTS else "auto" for s in present]
    return " ".join(cols) if cols else "(none — no slots present)"


# --- machine-readable report (--json) ----------------------------------------------------------
# ONE shared schema across every lint bin: {tool, ok, summary, findings:[{kind, severity, location,
# message}]}. `ok` is true iff no blocking finding (the same condition that gives exit 0 in `lint`).
# Printed via json.dumps(indent=2); nothing else goes to stdout under --json.
def _report_json(tool, ok, summary, findings):
    """Emit the shared report object to stdout (and nothing else). `findings` is a list of dicts already
    in {kind, severity, location, message} shape. Returns the dict so callers/selftests can reuse it."""
    report = {"tool": tool, "ok": ok, "summary": summary, "findings": findings}
    print(json.dumps(report, indent=2))
    return report


def _finding_kind(message):
    """Derive a stable KIND for a lint() message string (lint() yields plain prose, so the kind is
    classified from the message's anchor words). Matches the A4/A5 finding families in lint()."""
    m = message.lower()
    if "selfmargin" in m or "outer margin" in m:
        return "SELF_MARGIN"
    if "tier" in m and "not one of" in m:
        return "BAD_TIER"
    if "seam gate" in m:
        return "NO_SEAM"
    if "overflow mechanism" in m:
        return "NO_OVERFLOW"
    if "god-component" in m:
        return "GOD_COMPONENT"
    if "tier-skip" in m:
        return "TIER_SKIP"
    if "a primitive composes" in m:
        return "PRIMITIVE_COMPOSES"
    if "a component composes no pieces" in m:
        return "EMPTY_COMPONENT"
    if "a module arranges" in m:
        return "THIN_MODULE"
    return "COMPOSITION"


def build_report(card, errs, warns):
    """Build the JSON report from lint()'s (errs, warns). Each error → severity `fail`; each warning →
    `advisory`. `ok` is true iff no error — the exact exit-0 condition of the `lint` subcommand.
    `location` is the named component the card describes (composition findings are component-scoped)."""
    label = card.get("name") or "?"
    out = []
    for e in errs:
        out.append({"kind": _finding_kind(e), "severity": "fail", "location": label, "message": e})
    for w in warns:
        out.append({"kind": _finding_kind(w), "severity": "advisory", "location": label, "message": w})
    ok = not errs
    if not out:
        summary = "composition sound — tier ladder + seam + spacing law hold"
    else:
        summary = ("%d finding(s) (%d error, %d advisory) — confirm composition by review"
                   % (len(out), len(errs), len(warns)))
    return {"tool": "composition-check", "ok": ok, "summary": summary, "findings": out}


# ── fixtures: the law, proven by construction ───────────────────────────────────────────────
def _actions(n):
    return [{"name": "ui-button", "tier": "primitive", "role": "action"} for _ in range(n)]


FIXTURES = [
    ("GOOD toolbar+overflow", {"name": "toolbar", "tier": "component", "contains": _actions(6),
                               "slots": ["actions"], "axis": "horizontal", "overflow": "priority-menu",
                               "selfMargin": False}, False),
    ("seamless component (B2)", {"name": "card", "tier": "component",
                                 "contains": [{"name": "div", "tier": "primitive"}],
                                 "slots": [], "overflow": None, "selfMargin": False}, True),
    ("missing overflow (B2/B4)", {"name": "toolbar", "tier": "component", "contains": _actions(6),
                                  "slots": ["actions"], "axis": "horizontal", "overflow": None,
                                  "selfMargin": False}, True),
    ("self-margin (A5)", {"name": "card", "tier": "component",
                          "contains": [{"name": "ui-heading", "tier": "primitive"}],
                          "slots": ["header", "body"], "selfMargin": True}, True),
    ("module with 1 component (A1)", {"name": "settings", "tier": "module",
                                      "contains": [{"name": "ui-nav", "tier": "component"}],
                                      "selfMargin": False}, True),
    ("primitive that composes (A1)", {"name": "button", "tier": "primitive",
                                      "contains": [{"name": "ui-menu", "tier": "primitive"}],
                                      "selfMargin": False}, True),
]


def selftest():
    ok = True
    for label, card, want_err in FIXTURES:
        errs, warns = lint(card)
        passed = bool(errs) == want_err
        ok = ok and passed
        tag = "errors" if errs else "clean"
        print(f"  {'PASS' if passed else 'FAIL'} · {label}: {tag}" + (f" — {errs[0]}" if errs else ""))
    assert slot_grid(["icon", "content", "caret"]) == "auto 1fr auto"
    assert slot_grid(["content", "caret"]) == "1fr auto"
    assert slot_grid(["content"]) == "1fr"
    print("  PASS · slot-grid: icon,content,caret -> auto 1fr auto ; content,caret -> 1fr auto ; content -> 1fr")

    # --- --json report selftest (the shared schema) -------------------------------------------
    import io
    import contextlib

    jerrs = []

    def _capture_report(report_obj):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _report_json(report_obj["tool"], report_obj["ok"], report_obj["summary"],
                         report_obj["findings"])
        return json.loads(buf.getvalue())

    def _assert_report(rep, want_ok, want_nonempty, label):
        if not isinstance(rep, dict):
            jerrs.append("--json %s: report is not a dict" % label); return
        if rep.get("tool") != "composition-check":
            jerrs.append("--json %s: tool=%r, want 'composition-check'" % (label, rep.get("tool")))
        if rep.get("ok") is not want_ok:
            jerrs.append("--json %s: ok=%r, want %r" % (label, rep.get("ok"), want_ok))
        if not isinstance(rep.get("summary"), str) or not rep["summary"]:
            jerrs.append("--json %s: summary missing/empty" % label)
        f = rep.get("findings")
        if not isinstance(f, list):
            jerrs.append("--json %s: findings not a list" % label); return
        if want_nonempty and not f:
            jerrs.append("--json %s: findings should be non-empty" % label)
        if not want_nonempty and f:
            jerrs.append("--json %s: findings should be [] on clean input, got %s" % (label, f))
        for fd in f:
            if not isinstance(fd, dict) or any(k not in fd for k in ("kind", "severity", "location", "message")):
                jerrs.append("--json %s: a finding is missing a required key: %r" % (label, fd))
            elif fd["severity"] not in ("fail", "warn", "advisory"):
                jerrs.append("--json %s: bad severity %r" % (label, fd["severity"]))

    # dirty card (a seamless component ⇒ NO_SEAM error): tool right, ok false, findings non-empty
    dirty_card = {"name": "card", "tier": "component",
                  "contains": [{"name": "div", "tier": "primitive"}],
                  "slots": [], "overflow": None, "selfMargin": False}
    de, dw = lint(dirty_card)
    dirty_rep = _capture_report(build_report(dirty_card, de, dw))
    _assert_report(dirty_rep, False, True, "dirty")
    if not all(fd["severity"] in ("fail", "advisory") for fd in dirty_rep["findings"]):
        jerrs.append("--json dirty: an error finding should map to severity 'fail'")
    # advisory-only card (a god-component with a seam: 8 actions but overflow declared) keeps ok TRUE
    adv_card = {"name": "toolbar", "tier": "component", "contains": _actions(8),
                "slots": ["actions"], "axis": "horizontal", "overflow": "priority-menu",
                "selfMargin": False}
    ae, aw = lint(adv_card)
    adv_rep = _capture_report(build_report(adv_card, ae, aw))
    _assert_report(adv_rep, True, True, "advisory-only")
    if not any(fd["kind"] == "GOD_COMPONENT" and fd["severity"] == "advisory" for fd in adv_rep["findings"]):
        jerrs.append("--json advisory-only: GOD_COMPONENT should map to severity 'advisory'")
    # clean card ⇒ ok true, findings []
    clean_card = {"name": "toolbar", "tier": "component",
                  "contains": [{"name": "b", "tier": "primitive", "role": "action"}],
                  "slots": ["actions"], "axis": "horizontal", "overflow": "priority-menu",
                  "selfMargin": False}
    ce, cw = lint(clean_card)
    _assert_report(_capture_report(build_report(clean_card, ce, cw)), True, False, "clean")
    for e in jerrs:
        print("  FAIL ·", e)
    ok = ok and not jerrs

    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "selftest":
        return selftest()
    if cmd == "slot-grid":
        present = [s.strip() for s in argv[2].split(",") if s.strip()] if len(argv) > 2 else []
        print(slot_grid(present))
        return 0
    if cmd == "lint":
        # --json is a parse-anywhere reporting flag (after `lint`) — strip it, remember it.
        rest = [a for a in argv[2:] if a != "--json"]
        as_json = "--json" in argv[2:]
        if not rest:
            sys.stderr.write("usage: composition-check.py lint [--json] <card.composition.json>\n")
            return 2
        with open(rest[0]) as fh:
            card = json.load(fh)
        errs, warns = lint(card)
        if as_json:
            rep = build_report(card, errs, warns)
            _report_json(rep["tool"], rep["ok"], rep["summary"], rep["findings"])
            return 1 if errs else 0
        for w in warns:
            print(f"  WARN  {w}")
        for e in errs:
            print(f"  ERROR {e}")
        print(f"\n{card.get('name', '?')} ({card.get('tier', '?')}): {len(errs)} error(s), {len(warns)} warning(s)")
        return 1 if errs else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
