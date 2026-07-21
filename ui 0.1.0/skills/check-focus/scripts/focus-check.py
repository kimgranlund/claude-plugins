#!/usr/bin/env python3
"""focus-check.py — the check-focus mechanism gate. Self-contained (stdlib only).

A "focus order card" is the small declarative artifact the skill emits (or re-derives when grading
an existing UI) to describe the keyboard-focus structure of a view: the focusable elements with
their tabindex / focus-visibility, the DOM source order, and any open modal's focus story. This
linter routes the MECHANIZABLE facts of focus management to code — does a *positive* tabindex
override natural order? does a focusable element paint a visible focus indicator? does the DOM
order survive the tab sequence? is an open modal trapped and does it restore focus on close? —
while the judgment-heavy review (is the *order* sensible? does the sequence match reading order
and task flow?) stays in SKILL.md. A tabindex value, a `trap:false`, a missing visible-focus flag
are mechanical; whether the resulting walk makes *sense* is a human read.

Focus order card shape (all top-level keys optional; report — never silently pass — when absent):
  {
    "elements": [
      {"id": "skip-link", "tabindex": 0,  "focusable": true, "visible_focus": true},
      {"id": "hero-cta",  "tabindex": 3,  "focusable": true, "visible_focus": false},
      {"id": "decorative","tabindex": -1, "focusable": false}
    ],
    "dom_order": ["skip-link", "nav", "hero-cta", "footer"],
    "modals": [                                    # one entry per overlay (sheet, drawer, dialog)
      {"id": "sheet",  "open": true, "trap": true,  "restore_focus": true},
      {"id": "drawer", "open": false,"trap": false, "restore_focus": false}
    ],
    "modal": {"open": true, "trap": false, "restore_focus": false},   # legacy single-modal form (still accepted)
    "targets": [                                   # hit-target sizes + the SC 2.5.8 exceptions
      {"id": "icon-btn", "w": 20, "h": 20, "inline_text": false, "spacing_ok": false}
    ],
    "ring": {"width_px": 2, "contrast_light": 3.2, "contrast_dark": 4.5}
  }

Per-element keys:
  id            — stable identifier (string). Used to correlate dom_order with elements.
  tabindex      — the tabindex attribute value (int). 0 = natural order; -1 = programmatic only;
                  >0 = EXPLICIT positive index (the anti-pattern — overrides DOM order globally).
  focusable     — whether the element takes keyboard focus at all (bool).
  visible_focus — whether the element paints a visible focus indicator when focused (bool).

Checks (gate = a hard FAIL; advisory = a WARN that surfaces a risk for human review):
  POSITIVE_TABINDEX  (gate)     — any element with tabindex > 0. A positive tabindex yanks the
                                  element out of DOM order and ahead of every tabindex:0 element on
                                  the page — the canonical focus-order anti-pattern.
  NO_VISIBLE_FOCUS   (gate)     — a focusable element with visible_focus:false. A focusable element
                                  with no visible indicator strands keyboard users (WCAG 2.4.7).
  ORDER_MISMATCH     (advisory) — when explicit tabindex>0 values are present, the resulting tab
                                  order (positive-tabindex elements first, ascending, then the
                                  tabindex:0 elements in DOM order) diverges from dom_order. Surfaces
                                  the exact reorder the positive tabindex caused.
  MODAL_NO_TRAP      (gate)     — an OPEN modal with trap:false. Focus can escape the dialog to the
                                  page behind it — a keyboard user is lost. (Gate only while open;
                                  a closed modal's trap setting is not exercised.) Runs per entry of
                                  modals[]; the legacy single modal{} is still accepted.
  MODAL_NO_RESTORE   (advisory) — an OPEN modal with restore_focus:false. On close, focus will not
                                  return to the trigger — recoverable, so advisory, not a gate.
                                  Runs per modals[] entry too.
  TARGET_TOO_SMALL   (gate)     — a target with w or h < 24 CSS px and neither inline_text nor
                                  spacing_ok declared — the SC 2.5.8 exceptions (inline text link,
                                  or >= 24px center-to-center spacing).
  RING_TOO_THIN      (gate)     — ring.width_px < 2 CSS px (SC 2.4.13).
  RING_LOW_CONTRAST  (gate)     — ring.contrast_light or ring.contrast_dark < 3.0:1 — the ring must
                                  clear 3:1 in BOTH schemes (SC 1.4.11/2.4.13).

A check whose data is absent is SKIPPED and reported as a skip (no silent pass): no elements[] ->
the element-level checks can't run; no dom_order -> ORDER_MISMATCH can't run; no modal/modals ->
the modal checks can't run; no targets[] / no ring{} -> those checks can't run. A malformed card
yields a clear error, not a traceback.

  python3 scripts/focus-check.py selftest
  python3 scripts/focus-check.py <card.json | dir>

Python 3.8+.
"""
import json
import os
import sys


def _tab_order(elements):
    """The browser tab sequence: positive-tabindex elements first (ascending tabindex, ties by DOM
    appearance), THEN the tabindex:0 / natural-order elements in their elements[] (DOM) appearance.
    Elements that are not keyboard-focusable (tabindex < 0 or focusable:false) take no part."""
    positives, naturals = [], []
    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            continue
        ti = el.get("tabindex", 0)
        if not isinstance(ti, int) or isinstance(ti, bool):
            continue  # malformed tabindex handled by the validity pass; not orderable here
        focusable = el.get("focusable", True)
        if ti > 0:
            positives.append((ti, i, el.get("id")))
        elif ti == 0 and focusable:
            naturals.append(el.get("id"))
    positives.sort(key=lambda t: (t[0], t[1]))
    return [pid for _, _, pid in positives] + naturals


def check_card(card):
    """Return (fails, warns, skips) for one focus order card.

    Raises ValueError on a structurally malformed card (caller turns it into a clean error)."""
    if not isinstance(card, dict):
        raise ValueError("card must be a JSON object")
    fails, warns, skips = [], [], []
    name = card.get("id") or card.get("view") or card.get("name") or "<card>"

    # --- validity pass: a malformed element shape is an error, not a silent skip ---
    elements = card.get("elements")
    if elements is not None and not isinstance(elements, list):
        raise ValueError("%s: 'elements' must be a list" % name)
    if isinstance(elements, list):
        for i, el in enumerate(elements):
            if not isinstance(el, dict):
                raise ValueError("%s: elements[%d] must be an object" % (name, i))
            ti = el.get("tabindex", 0)
            if isinstance(ti, bool) or not isinstance(ti, int):
                raise ValueError("%s: element %r has non-integer tabindex %r"
                                 % (name, el.get("id", i), ti))

    # --- POSITIVE_TABINDEX (gate) + NO_VISIBLE_FOCUS (gate), per element ---
    if isinstance(elements, list) and elements:
        for el in elements:
            eid = el.get("id", "<el>")
            ti = el.get("tabindex", 0)
            if ti > 0:
                fails.append("%s: element '%s' has POSITIVE_TABINDEX (tabindex=%d) — a positive "
                             "tabindex overrides DOM order and jumps ahead of every tabindex:0 "
                             "element; use 0 (natural) or -1 (programmatic), never >0" % (name, eid, ti))
            # a focusable element that explicitly declares no visible focus indicator
            if el.get("focusable", True) and el.get("visible_focus") is False:
                fails.append("%s: focusable element '%s' has NO_VISIBLE_FOCUS (visible_focus:false) "
                             "— a focusable element must paint a visible focus indicator (WCAG 2.4.7); "
                             "don't `outline:none` without a replacement" % (name, eid))
    else:
        skips.append("%s: no elements[] — POSITIVE_TABINDEX / NO_VISIBLE_FOCUS checks skipped" % name)

    # --- ORDER_MISMATCH (advisory): only meaningful when explicit positive tabindex is present ---
    dom_order = card.get("dom_order")
    if dom_order is not None and not isinstance(dom_order, list):
        raise ValueError("%s: 'dom_order' must be a list" % name)
    has_positive = isinstance(elements, list) and any(
        isinstance(e, dict) and isinstance(e.get("tabindex", 0), int)
        and not isinstance(e.get("tabindex", 0), bool) and e.get("tabindex", 0) > 0
        for e in elements)
    if not isinstance(elements, list) or not elements:
        pass  # already reported the elements[] skip above
    elif not dom_order:
        skips.append("%s: no dom_order — ORDER_MISMATCH check skipped" % name)
    elif not has_positive:
        skips.append("%s: no positive tabindex present — ORDER_MISMATCH not applicable (tab order "
                     "follows DOM order)" % name)
    else:
        tab = _tab_order(elements)
        # compare the resulting tab walk to the DOM order, restricted to the ids that participate
        dom_focusable = [d for d in dom_order if d in set(tab)]
        if tab != dom_focusable:
            warns.append("%s: ORDER_MISMATCH — positive tabindex reorders the tab walk %s away from "
                         "DOM order %s; is this sequence intended? (review)" % (name, tab, dom_focusable))

    # --- modal focus story: MODAL_NO_TRAP (gate, only while open) + MODAL_NO_RESTORE (advisory) ---
    # modals[] carries one entry per overlay (real screens stack sheets/drawers/dialogs); the
    # legacy single modal{} is still accepted — both feed the same per-entry checks.
    modal = card.get("modal")
    modals = card.get("modals")
    if modals is not None and not isinstance(modals, list):
        raise ValueError("%s: 'modals' must be a list" % name)
    if modal is not None and not isinstance(modal, dict):
        raise ValueError("%s: 'modal' must be an object" % name)
    entries = []
    if isinstance(modals, list):
        for i, m in enumerate(modals):
            if not isinstance(m, dict):
                raise ValueError("%s: modals[%d] must be an object" % (name, i))
            entries.append((m.get("id", "modals[%d]" % i), m))
    if isinstance(modal, dict):
        entries.append((modal.get("id", "modal"), modal))
    if modal is None and modals is None:
        skips.append("%s: no modal/modals — MODAL_NO_TRAP / MODAL_NO_RESTORE checks skipped" % name)
    elif not entries:
        skips.append("%s: modals[] is empty — MODAL_NO_TRAP / MODAL_NO_RESTORE checks skipped" % name)
    else:
        for mid, m in entries:
            if not m.get("open"):
                skips.append("%s: modal '%s' not open — trap/restore not exercised, skipped"
                             % (name, mid))
                continue
            if m.get("trap") is not True:
                fails.append("%s: MODAL_NO_TRAP — open modal '%s' with trap:%r — focus can escape "
                             "to the page behind the dialog; trap Tab/Shift+Tab inside the modal "
                             "while open" % (name, mid, m.get("trap")))
            if m.get("restore_focus") is not True:
                warns.append("%s: MODAL_NO_RESTORE — open modal '%s' with restore_focus:%r — on "
                             "close, focus won't return to the element that opened it (review)"
                             % (name, mid, m.get("restore_focus")))

    # --- hit targets: TARGET_TOO_SMALL (gate) with the SC 2.5.8 exceptions ---
    targets = card.get("targets")
    if targets is not None and not isinstance(targets, list):
        raise ValueError("%s: 'targets' must be a list" % name)
    if targets is None:
        skips.append("%s: no targets[] — TARGET_TOO_SMALL check skipped" % name)
    elif not targets:
        skips.append("%s: targets[] is empty — TARGET_TOO_SMALL check skipped" % name)
    else:
        for i, tg in enumerate(targets):
            if not isinstance(tg, dict):
                raise ValueError("%s: targets[%d] must be an object" % (name, i))
            tid = tg.get("id", "targets[%d]" % i)
            dims = []
            for axis in ("w", "h"):
                v = tg.get(axis)
                if isinstance(v, bool) or not isinstance(v, (int, float)):
                    raise ValueError("%s: target %r has non-numeric %s: %r" % (name, tid, axis, v))
                dims.append(v)
            w, h = dims
            if (w < 24 or h < 24) and not (tg.get("inline_text") or tg.get("spacing_ok")):
                fails.append("%s: TARGET_TOO_SMALL — target '%s' is %sx%s CSS px (< 24x24, SC 2.5.8) "
                             "and declares neither inline_text nor spacing_ok exception — expand the "
                             "hit area (padding/pseudo-element) or declare the exception"
                             % (name, tid, w, h))

    # --- focus ring: RING_TOO_THIN (gate) + RING_LOW_CONTRAST (gate, per scheme) ---
    ring = card.get("ring")
    if ring is not None and not isinstance(ring, dict):
        raise ValueError("%s: 'ring' must be an object" % name)
    if ring is None:
        skips.append("%s: no ring{} — RING_TOO_THIN / RING_LOW_CONTRAST checks skipped" % name)
    else:
        def _ring_num(key):
            v = ring.get(key)
            if v is None:
                return None
            if isinstance(v, bool) or not isinstance(v, (int, float)):
                raise ValueError("%s: ring.%s is not a number: %r" % (name, key, v))
            return v
        width = _ring_num("width_px")
        if width is None:
            skips.append("%s: ring.width_px absent — RING_TOO_THIN check skipped" % name)
        elif width < 2:
            fails.append("%s: RING_TOO_THIN — ring width_px %s < 2 CSS px (SC 2.4.13 minimum)"
                         % (name, width))
        for key, scheme in (("contrast_light", "light"), ("contrast_dark", "dark")):
            c = _ring_num(key)
            if c is None:
                skips.append("%s: ring.%s absent — RING_LOW_CONTRAST (%s scheme) check skipped"
                             % (name, key, scheme))
            elif c < 3.0:
                fails.append("%s: RING_LOW_CONTRAST — ring contrast %s:1 in the %s scheme < 3.0:1 "
                             "(SC 1.4.11/2.4.13) — the ring must clear 3:1 against every adjacent "
                             "surface in BOTH schemes" % (name, c, scheme))

    return fails, warns, skips


# --- selftest fixtures -------------------------------------------------------------------------
# must-FLAG: a positive tabindex, a no-visible-focus element, AND an open untrapped modal.
BAD = {
    "id": "hero-view",
    "elements": [
        {"id": "skip-link", "tabindex": 0, "focusable": True, "visible_focus": True},
        {"id": "hero-cta", "tabindex": 3, "focusable": True, "visible_focus": False},
        {"id": "decoration", "tabindex": -1, "focusable": False},
    ],
    "dom_order": ["skip-link", "hero-cta"],
    "modal": {"open": True, "trap": False, "restore_focus": False},
}
# must-NOT-flag: all tabindex 0/-1, every focusable element visible, modal trapped + restoring,
# targets >= 24x24, ring >= 2px clearing 3:1 in both schemes. Exercises the legacy modal{} form.
GOOD = {
    "id": "settings-view",
    "elements": [
        {"id": "skip-link", "tabindex": 0, "focusable": True, "visible_focus": True},
        {"id": "name-input", "tabindex": 0, "focusable": True, "visible_focus": True},
        {"id": "avatar", "tabindex": -1, "focusable": False},
    ],
    "dom_order": ["skip-link", "name-input"],
    "modal": {"open": True, "trap": True, "restore_focus": True},
    "targets": [{"id": "skip-link", "w": 44, "h": 44}, {"id": "name-input", "w": 200, "h": 32}],
    "ring": {"width_px": 2, "contrast_light": 3.2, "contrast_dark": 4.5},
}
# a closed modal with trap:false must NOT fire MODAL_NO_TRAP (the trap isn't exercised while closed).
CLOSED_MODAL = {"id": "x", "elements": [{"id": "a", "tabindex": 0, "focusable": True, "visible_focus": True}],
                "dom_order": ["a"], "modal": {"open": False, "trap": False, "restore_focus": False}}
# sparse card: only a single clean element — every absent section reports a SKIP, no fail, no warn.
SPARSE = {"id": "frag", "elements": [{"id": "a", "tabindex": 0, "focusable": True, "visible_focus": True}]}
# order-mismatch fixture: a positive tabindex pulls 'late' ahead of 'early' — advisory WARN, no fail
# beyond the POSITIVE_TABINDEX gate itself.
REORDER = {"id": "reorder", "elements": [
    {"id": "early", "tabindex": 0, "focusable": True, "visible_focus": True},
    {"id": "late", "tabindex": 1, "focusable": True, "visible_focus": True}],
    "dom_order": ["early", "late"]}
# multi-overlay card: modals[] runs the trap/restore checks PER ENTRY — 'sheet' (open, untrapped)
# gates, 'prefs-dialog' (open, no restore) warns, 'drawer' (closed) skips.
MULTI_MODALS = {"id": "stacked", "elements": [
    {"id": "a", "tabindex": 0, "focusable": True, "visible_focus": True}],
    "dom_order": ["a"],
    "modals": [
        {"id": "sheet", "open": True, "trap": False, "restore_focus": True},
        {"id": "prefs-dialog", "open": True, "trap": True, "restore_focus": False},
        {"id": "drawer", "open": False, "trap": False, "restore_focus": False},
    ]}
# hit targets: 'icon-btn' (20x20, no exception) gates; the SC 2.5.8 exceptions clear
# 'footnote-link' (inline_text) and 'dense-cell' (spacing_ok).
BAD_TARGETS = {"id": "toolbar", "targets": [
    {"id": "icon-btn", "w": 20, "h": 20},
    {"id": "footnote-link", "w": 12, "h": 16, "inline_text": True},
    {"id": "dense-cell", "w": 20, "h": 20, "spacing_ok": True},
]}
# ring: 1px (too thin) + light-scheme contrast 2.1 (below 3.0) gate; dark 4.5 passes.
BAD_RING = {"id": "ring-view", "ring": {"width_px": 1, "contrast_light": 2.1, "contrast_dark": 4.5}}
# a ring failing only in the DARK scheme must gate too ("either scheme" rule).
BAD_RING_DARK = {"id": "ring-dark", "ring": {"width_px": 2, "contrast_light": 3.5, "contrast_dark": 2.9}}
# a partial ring: absent contrast keys are skipped-and-reported, never silently passed.
PARTIAL_RING = {"id": "ring-partial", "ring": {"width_px": 2}}
# malformed: a non-integer tabindex (true) must raise, not crash or silently pass.
MALFORMED = {"id": "bad", "elements": [{"id": "a", "tabindex": True, "focusable": True}]}
# malformed new sections must raise too (clear error, not a traceback or silent pass).
MALFORMED_MODALS = {"id": "mm", "modals": {"open": True}}
MALFORMED_TARGET = {"id": "mt", "targets": [{"id": "a", "w": "wide", "h": 30}]}
MALFORMED_RING = {"id": "mr", "ring": {"width_px": True}}


def selftest():
    errs = []

    def of(card):
        return check_card(card)

    bf, bw, _ = of(BAD)
    if not any("POSITIVE_TABINDEX" in f for f in bf):
        errs.append("positive tabindex (tabindex:3) not flagged")
    if not any("NO_VISIBLE_FOCUS" in f for f in bf):
        errs.append("focusable element with visible_focus:false not flagged")
    if not any("MODAL_NO_TRAP" in f for f in bf):
        errs.append("open modal with trap:false not flagged")
    if not any("MODAL_NO_RESTORE" in w for w in bw):
        errs.append("open modal with restore_focus:false not warned")
    if not any("ORDER_MISMATCH" in w for w in bw):
        errs.append("positive-tabindex reorder did not surface ORDER_MISMATCH")

    gf, gw, gs = of(GOOD)
    if gf:
        errs.append("clean card produced fails: %s" % gf)
    if gw:
        errs.append("clean card produced warns: %s" % gw)
    # the GOOD card supplies every section, so the element + modal checks all RUN (no skip). The
    # only legitimate skip is ORDER_MISMATCH being "not applicable" (a clean card has no positive
    # tabindex to reorder anything) — anything else means a present section was silently skipped.
    bad_skips = [s for s in gs if "not applicable" not in s]
    if bad_skips:
        errs.append("fully-populated clean card silently skipped a present section: %s" % bad_skips)

    cf, _, cs = of(CLOSED_MODAL)
    if any("MODAL_NO_TRAP" in f for f in cf):
        errs.append("closed modal wrongly fired MODAL_NO_TRAP")
    if not any("not open" in s for s in cs):
        errs.append("closed modal did not report a skip")

    sf, sw, ss = of(SPARSE)
    if sf or sw:
        errs.append("sparse clean card produced fails/warns: %s / %s" % (sf, sw))
    if not (any("no dom_order" in s for s in ss) and any("no modal" in s for s in ss)):
        errs.append("sparse card did not report dom_order/modal skips (silent pass?)")
    if not (any("no targets" in s for s in ss) and any("no ring" in s for s in ss)):
        errs.append("sparse card did not report targets/ring skips (silent pass?)")

    rf, rw, _ = of(REORDER)
    if not any("POSITIVE_TABINDEX" in f for f in rf):
        errs.append("reorder fixture's tabindex:1 not flagged as positive")
    if not any("ORDER_MISMATCH" in w for w in rw):
        errs.append("reorder fixture did not surface ORDER_MISMATCH")

    # --- modals[]: per-entry trap/restore, closed entries skipped, legacy modal{} unaffected ---
    mf, mw, ms = of(MULTI_MODALS)
    if sum("MODAL_NO_TRAP" in f for f in mf) != 1 or not any(
            "MODAL_NO_TRAP" in f and "'sheet'" in f for f in mf):
        errs.append("modals[]: open untrapped 'sheet' not the exactly-one MODAL_NO_TRAP: %s" % mf)
    if not any("MODAL_NO_RESTORE" in w and "'prefs-dialog'" in w for w in mw):
        errs.append("modals[]: 'prefs-dialog' restore_focus:false not warned MODAL_NO_RESTORE")
    if any("'prefs-dialog'" in f for f in mf):
        errs.append("modals[]: trapped 'prefs-dialog' wrongly failed")
    if not any("'drawer'" in s and "not open" in s for s in ms):
        errs.append("modals[]: closed 'drawer' not reported as a skip")

    # --- targets[]: gate under 24px, honor the SC 2.5.8 exceptions ---
    tf, tw, _ = of(BAD_TARGETS)
    if sum("TARGET_TOO_SMALL" in f for f in tf) != 1 or not any(
            "TARGET_TOO_SMALL" in f and "'icon-btn'" in f for f in tf):
        errs.append("targets[]: 20x20 'icon-btn' not the exactly-one TARGET_TOO_SMALL: %s" % tf)
    if any("footnote-link" in f or "dense-cell" in f for f in tf):
        errs.append("targets[]: inline_text/spacing_ok exception not honored (SC 2.5.8)")
    if tw:
        errs.append("targets[]: produced unexpected warns: %s" % tw)

    # --- ring{}: width + per-scheme contrast gates; partial ring skips, never silently passes ---
    rgf, _, _ = of(BAD_RING)
    if not any("RING_TOO_THIN" in f for f in rgf):
        errs.append("ring: width_px 1 not gated RING_TOO_THIN")
    if not any("RING_LOW_CONTRAST" in f and "light" in f for f in rgf):
        errs.append("ring: light-scheme contrast 2.1 not gated RING_LOW_CONTRAST")
    if any("RING_LOW_CONTRAST" in f and "dark" in f for f in rgf):
        errs.append("ring: passing dark-scheme contrast 4.5 wrongly gated")
    rdf, _, _ = of(BAD_RING_DARK)
    if not any("RING_LOW_CONTRAST" in f and "dark" in f for f in rdf):
        errs.append("ring: dark-scheme contrast 2.9 not gated (either-scheme rule)")
    if any("RING_TOO_THIN" in f for f in rdf):
        errs.append("ring: width_px 2 wrongly gated RING_TOO_THIN")
    prf, _, prs = of(PARTIAL_RING)
    if prf:
        errs.append("partial ring produced fails: %s" % prf)
    if not (any("contrast_light absent" in s for s in prs) and
            any("contrast_dark absent" in s for s in prs)):
        errs.append("partial ring did not report absent contrast keys as skips")

    for label, bad in (("tabindex:true", MALFORMED), ("modals-not-a-list", MALFORMED_MODALS),
                       ("target w non-numeric", MALFORMED_TARGET), ("ring width bool", MALFORMED_RING)):
        try:
            of(bad)
            errs.append("malformed card (%s) did not raise" % label)
        except ValueError:
            pass

    return errs


def _iter_cards(path):
    if os.path.isdir(path):
        for dp, _, fns in os.walk(path):
            for fn in sorted(fns):
                if fn.endswith(".focus.json"):
                    yield os.path.join(dp, fn)
    else:
        yield path


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("focus-check: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("focus-check: OK — gate + advisory checks verified over good/bad/sparse/malformed fixtures")
        return 0
    fails, warns, skips, n = [], [], [], 0
    for fp in _iter_cards(argv[0]):
        try:
            doc = json.load(open(fp, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            fails.append("%s: unreadable (%s)" % (fp, e))
            continue
        for card in (doc if isinstance(doc, list) else [doc]):
            n += 1
            try:
                f, w, s = check_card(card)
            except ValueError as e:
                fails.append("%s: malformed card (%s)" % (fp, e))
                continue
            fails += f
            warns += w
            skips += s
    for s in skips:
        print("  - (skip) %s" % s)
    for w in warns:
        print("  ! %s" % w)
    if fails:
        sys.stderr.write("focus-check: FAIL (%d)\n" % len(fails))
        for f in fails:
            sys.stderr.write("  - %s\n" % f)
        return 1
    print("focus-check: OK — %d card(s) clear the focus gates" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
