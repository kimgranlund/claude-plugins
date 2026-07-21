#!/usr/bin/env python3
"""typeface-check.py — the pick-fonts craft-correctness checker. Self-contained
(stdlib only).

Metric-ratio and axis-apart arithmetic is deterministic derivation once the inputs (two named
fonts, their chosen weights) are fixed, so it routes to code (right tool for the job) rather than
being eyeballed. Python, not `.mjs`: this is pure numeric/classification computation over a small
fixed table, not a scan of live UI source files — the job font-token-rules' `type-check.mjs`
does. It matches the corpus's Python convention for deterministic-derivation checkers
(`ramp_build.py`, `contrast-check.py`, `routing_eval.py`).

Checks three things for a same-baseline pairing (a headline over its body, a lead pull-quote
over its citation, a kicker over the display it introduces):

  metric ratio   — x-height AND cap-height (when both fonts have a verified figure) compatibility:
                   ratio = min(a, b) / max(a, b); compatible when ratio >= METRIC_TOLERANCE (0.90,
                   i.e. within +-10%). A missing cap-height on either side is reported as
                   "unmeasured" for that axis, never silently assumed compatible.
  axis apart     — at least ONE real axis separates the pairing so "contrast" reads as a decision,
                   not an accident: classification (serif/sans/mono) differs, OR register
                   (neutral/distinctive/editorial/technical/code) differs, OR the weight gap
                   between the two chosen weights is >= WEIGHT_AXIS_MIN (300 units — a stated
                   house judgment call: chosen just above the pairing doctrine's documented
                   accidental bound (200, "400 vs 600") and below its considered bound (800,
                   "100 vs 900"); no exact boundary is given in the source, see SKILL.md's
                   numbers table). Failing this
                   with NO real axis apart is the "near-identical pairing" anti-pattern
                   (lettering-facts/references/techniques/pairing.md's own named failure).
  size jump      — OPTIONAL (pass sizeA/sizeB): ratio = max(a, b) / min(a, b) between the two
                   voices' actual sizes at the step in question. >= SIZE_JUMP_HIERARCHY (3.0) reads
                   as intentional hierarchy; <= SIZE_JUMP_ROUNDING (1.5) reads as an ordinary
                   same-tier step; the open interval between the two is the "ambiguous" anti-pattern
                   — a gap too big to be a rounding step, too small to read as a decision.

The embedded FONTS table mirrors references/font-craft.md's metrics table exactly (7 rows
inherited from font-token-rules/references/font-selection.md's pre-migration revision, 2 rows
from lettering-facts/references/voice/neutral-by-design.md's Roboto/Arial figures — cited
per-row below). Extend it ONLY with a verified, cited source — never a guessed number; `selftest`
mechanically re-parses font-craft.md's table and fails if the two tables ever drift apart.

Usage:
    python3 typeface-check.py pair <fontA> <weightA> <fontB> <weightB> [<sizeA> <sizeB>]
    python3 typeface-check.py fonts
    python3 typeface-check.py selftest

selftest: the Inter/Fraunces worked pairing (ratio ~0.908, in tolerance, classification-distant);
the IBM Plex Sans/Serif metric-matched pair (ratio 1.0, classification-distant); a real
out-of-tolerance pair (JetBrains Mono against Fraunces, ratio ~0.892, flagged, still
axis-apart-distant on classification — the pairing-doctrine caveat that axis-apart does not rescue
a metric mismatch); the near-identical anti-pattern (Inter 400 against Inter 600 — no real axis
apart); the considered-range pass (Inter 100 against Inter 900 — one family at real weight
extremes, axis apart on weight alone); a size-jump hierarchy pass (12/48, ratio 4.0), a size-jump
rounding-range pass (16/18, ratio 1.125), and a size-jump ambiguous anti-pattern (16/32, ratio 2.0);
a table-drift check that re-parses font-craft.md's metrics table and fails if it ever disagrees
with the embedded FONTS dict. Python 3.8+.
"""
import re
import sys
from pathlib import Path

METRIC_TOLERANCE = 0.90      # ratio >= this = within +-10% (min/max form)
WEIGHT_AXIS_MIN = 300        # weight-unit gap that reads as a considered, deliberate axis
SIZE_JUMP_HIERARCHY = 3.0    # size ratio >= this reads as intentional hierarchy
SIZE_JUMP_ROUNDING = 1.5     # size ratio <= this reads as a rounding error, not a decision

# --- the embedded metrics table (verified, cited) -------------------------------------------------
# x_height / cap_height as a fraction of em; cap_height is None where the source didn't state one.
# family: serif | sans | mono.  register: neutral | distinctive | editorial | technical | code.
FONTS = {
    "Inter":            {"x_height": 0.545, "cap_height": 0.73, "family": "sans",  "register": "neutral",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "Fraunces":         {"x_height": 0.495, "cap_height": 0.72, "family": "serif", "register": "editorial",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "Source Serif 4":   {"x_height": 0.515, "cap_height": None, "family": "serif", "register": "editorial",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "IBM Plex Sans":    {"x_height": 0.516, "cap_height": 0.70, "family": "sans",  "register": "technical",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "IBM Plex Serif":   {"x_height": 0.516, "cap_height": 0.70, "family": "serif", "register": "technical",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "Geist":            {"x_height": 0.52,  "cap_height": None, "family": "sans",  "register": "distinctive",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "JetBrains Mono":   {"x_height": 0.555, "cap_height": 0.73, "family": "mono",  "register": "code",
                          "source": "font-craft.md (inherited from font-selection.md pre-migration rev., 2026-07-05)"},
    "Roboto":           {"x_height": 0.528, "cap_height": None, "family": "sans",  "register": "neutral",
                          "source": "lettering-facts/references/voice/neutral-by-design.md"},
    "Arial":            {"x_height": 0.519, "cap_height": None, "family": "sans",  "register": "neutral",
                          "source": "lettering-facts/references/voice/neutral-by-design.md"},
}


def _ratio(a, b):
    """min/max ratio -- 1.0 is identical, lower is more divergent."""
    return min(a, b) / max(a, b)


def metric_ratio(font_a, font_b):
    """x-height (always) and cap-height (when both sides have one) ratio + tolerance verdict."""
    fa, fb = FONTS[font_a], FONTS[font_b]
    x_ratio = _ratio(fa["x_height"], fb["x_height"])
    result = {
        "x_ratio": round(x_ratio, 4),
        "x_compatible": x_ratio >= METRIC_TOLERANCE,
        "cap_ratio": None,
        "cap_compatible": None,
        "cap_unmeasured": fa["cap_height"] is None or fb["cap_height"] is None,
    }
    if not result["cap_unmeasured"]:
        cap_ratio = _ratio(fa["cap_height"], fb["cap_height"])
        result["cap_ratio"] = round(cap_ratio, 4)
        result["cap_compatible"] = cap_ratio >= METRIC_TOLERANCE
    return result


def classification_distance(font_a, font_b):
    """True if family OR register differs -- either alone is a real axis."""
    fa, fb = FONTS[font_a], FONTS[font_b]
    return fa["family"] != fb["family"] or fa["register"] != fb["register"]


def weight_axis(weight_a, weight_b):
    gap = abs(weight_a - weight_b)
    return gap, gap >= WEIGHT_AXIS_MIN


def size_jump(size_a, size_b):
    """Size-JUMP ratio (a step-to-step comparison, not the metric ratio above): >= SIZE_JUMP_HIERARCHY
    reads as intentional hierarchy; <= SIZE_JUMP_ROUNDING reads as a rounding error; the open
    interval between the two is ambiguous -- neither clearly a decision nor clearly an accident."""
    ratio = max(size_a, size_b) / min(size_a, size_b)
    if ratio >= SIZE_JUMP_HIERARCHY:
        verdict = "hierarchy"
    elif ratio <= SIZE_JUMP_ROUNDING:
        verdict = "rounding-error-range"
    else:
        verdict = "ambiguous"
    return round(ratio, 3), verdict


def pair_check(font_a, weight_a, font_b, weight_b, size_a=None, size_b=None):
    """Full pairing verdict: metric ratio, axis-apart verdict, anti-pattern flag, a
    font-size-adjust suggestion when the metric ratio misses tolerance, and (when both sizes are
    given) the size-jump verdict."""
    if font_a not in FONTS:
        raise KeyError("unknown font %r -- run `typeface-check.py fonts` to list the embedded table" % font_a)
    if font_b not in FONTS:
        raise KeyError("unknown font %r -- run `typeface-check.py fonts` to list the embedded table" % font_b)

    metrics = metric_ratio(font_a, font_b)
    class_dist = classification_distance(font_a, font_b)
    weight_gap, weight_real_axis = weight_axis(weight_a, weight_b)
    real_axis_apart = class_dist or weight_real_axis

    axis_reasons = []
    if class_dist:
        fa, fb = FONTS[font_a], FONTS[font_b]
        if fa["family"] != fb["family"]:
            axis_reasons.append("classification (%s vs %s)" % (fa["family"], fb["family"]))
        if fa["register"] != fb["register"]:
            axis_reasons.append("register (%s vs %s)" % (fa["register"], fb["register"]))
    if weight_real_axis:
        axis_reasons.append("weight gap %d >= %d" % (weight_gap, WEIGHT_AXIS_MIN))

    metric_ok = metrics["x_compatible"] and (metrics["cap_compatible"] is not False)
    font_size_adjust = None
    if not metrics["x_compatible"]:
        font_size_adjust = round(FONTS[font_b]["x_height"] / FONTS[font_a]["x_height"], 4)

    size_jump_ratio, size_jump_verdict = (None, None)
    if size_a is not None and size_b is not None:
        size_jump_ratio, size_jump_verdict = size_jump(size_a, size_b)

    anti_patterns = []
    if not real_axis_apart:
        anti_patterns.append(
            "near-identical pairing: no classification/register distance and weight gap %d < %d "
            "-- reads as an accident, not a decision" % (weight_gap, WEIGHT_AXIS_MIN))
    if not metrics["x_compatible"]:
        anti_patterns.append(
            "x-height ratio %.3f below tolerance %.2f with no stated font-size-adjust "
            "compensation" % (metrics["x_ratio"], METRIC_TOLERANCE))
    if metrics["cap_compatible"] is False:
        anti_patterns.append("cap-height ratio %.3f below tolerance %.2f" % (metrics["cap_ratio"], METRIC_TOLERANCE))
    if size_jump_verdict == "ambiguous":
        anti_patterns.append(
            "size-jump ratio %.2f is neither a hierarchy jump (>= %.1f) nor a same-tier rounding "
            "range (<= %.1f) -- an in-between size gap reads as an accident, not a decision"
            % (size_jump_ratio, SIZE_JUMP_HIERARCHY, SIZE_JUMP_ROUNDING))

    return {
        "font_a": font_a, "weight_a": weight_a, "font_b": font_b, "weight_b": weight_b,
        "metrics": metrics, "classification_distance": class_dist,
        "weight_gap": weight_gap, "weight_real_axis": weight_real_axis,
        "real_axis_apart": real_axis_apart, "axis_reasons": axis_reasons,
        "metric_ok": metric_ok, "font_size_adjust_suggestion": font_size_adjust,
        "size_jump_ratio": size_jump_ratio, "size_jump_verdict": size_jump_verdict,
        "anti_patterns": anti_patterns,
    }


def _fmt(result):
    lines = []
    m = result["metrics"]
    lines.append("%s (%d) vs %s (%d)" % (result["font_a"], result["weight_a"], result["font_b"], result["weight_b"]))
    lines.append("  x-height ratio  %.3f  %s" % (m["x_ratio"], "OK" if m["x_compatible"] else "OUT OF TOLERANCE"))
    if m["cap_unmeasured"]:
        lines.append("  cap-height ratio  unmeasured (a source figure is missing on one side)")
    else:
        lines.append("  cap-height ratio  %.3f  %s" % (m["cap_ratio"], "OK" if m["cap_compatible"] else "OUT OF TOLERANCE"))
    lines.append("  axis apart  %s  (%s)" % (result["real_axis_apart"], ", ".join(result["axis_reasons"]) or "none"))
    if result["font_size_adjust_suggestion"] is not None:
        lines.append("  suggested font-size-adjust: %.4f (or state the compensation explicitly)"
                      % result["font_size_adjust_suggestion"])
    if result["size_jump_verdict"] is not None:
        lines.append("  size-jump ratio  %.2f  %s" % (result["size_jump_ratio"], result["size_jump_verdict"]))
    for ap in result["anti_patterns"]:
        lines.append("  !! %s" % ap)
    return "\n".join(lines)


# --- table-drift check: font-craft.md's metrics table must agree with FONTS -----------------------

def _parse_font_craft_table():
    """Re-parse references/font-craft.md's '## The metrics table' rows into the same shape as
    FONTS (minus 'source'), so selftest can catch the two tables silently drifting apart."""
    path = Path(__file__).resolve().parent.parent / "references" / "font-craft.md"
    text = path.read_text()
    m = re.search(r"## The metrics table.*?\n\n(\|.*?\n)\n", text, re.S)
    if not m:
        raise RuntimeError("could not find the metrics table in font-craft.md")
    rows = [r for r in m.group(1).strip().split("\n") if r.startswith("|")]
    rows = rows[2:]  # drop the header row and the |---|---| separator
    parsed = {}
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        name, x_height, cap_height, family, register = cells[0], cells[1], cells[2], cells[3], cells[4]
        cap = None if cap_height.startswith("—") else float(cap_height)
        parsed[name] = {"x_height": float(x_height), "cap_height": cap, "family": family, "register": register}
    return parsed


# --- selftest ------------------------------------------------------------------------------------

def selftest():
    errs = []

    # 1. Inter/Fraunces worked pairing -- ratio ~0.908, in tolerance, classification-distant
    r = pair_check("Inter", 400, "Fraunces", 700)
    if abs(r["metrics"]["x_ratio"] - 0.908) > 0.001:
        errs.append("Inter/Fraunces x-height ratio wrong: got %.4f, want ~0.908" % r["metrics"]["x_ratio"])
    if not r["metrics"]["x_compatible"]:
        errs.append("Inter/Fraunces must be within metric tolerance")
    if not r["real_axis_apart"]:
        errs.append("Inter/Fraunces must be axis-apart (classification: sans vs serif)")
    if r["anti_patterns"]:
        errs.append("Inter/Fraunces must carry no anti-pattern flags: %s" % r["anti_patterns"])

    # 2. IBM Plex Sans/Serif -- metric-matched by design (ratio 1.0), classification-distant,
    #    axis-apart even at IDENTICAL weight (400 vs 400) -- the safest contrast pairing available
    r = pair_check("IBM Plex Sans", 400, "IBM Plex Serif", 400)
    if r["metrics"]["x_ratio"] != 1.0 or r["metrics"]["cap_ratio"] != 1.0:
        errs.append("IBM Plex Sans/Serif must be metric-matched exactly (ratio 1.0 both axes)")
    if not r["real_axis_apart"]:
        errs.append("IBM Plex Sans/Serif must be axis-apart on classification even at equal weight")
    if r["weight_real_axis"]:
        errs.append("IBM Plex Sans/Serif at equal weight must NOT satisfy the weight axis")

    # 3. NEGATIVE CONTROL -- JetBrains Mono/Fraunces: real out-of-tolerance pair (~0.892), still
    #    axis-apart on classification -- proves axis-apart does NOT rescue a metric mismatch
    r = pair_check("JetBrains Mono", 400, "Fraunces", 400)
    if abs(r["metrics"]["x_ratio"] - 0.892) > 0.001:
        errs.append("JetBrains Mono/Fraunces x-height ratio wrong: got %.4f, want ~0.892" % r["metrics"]["x_ratio"])
    if r["metrics"]["x_compatible"]:
        errs.append("JetBrains Mono/Fraunces must be OUT of metric tolerance (this is the negative control)")
    if not r["real_axis_apart"]:
        errs.append("JetBrains Mono/Fraunces must still be axis-apart on classification (mono vs serif)")
    if not any("tolerance" in a for a in r["anti_patterns"]):
        errs.append("JetBrains Mono/Fraunces must flag the metric-mismatch anti-pattern")
    if r["font_size_adjust_suggestion"] is None:
        errs.append("an out-of-tolerance pairing must suggest a font-size-adjust compensation")

    # 4. ANTI-PATTERN -- Inter 400 vs Inter 600: same font, same classification/register, weight
    #    gap 200 < 300 -- no real axis apart, must flag "near-identical pairing"
    r = pair_check("Inter", 400, "Inter", 600)
    if r["real_axis_apart"]:
        errs.append("Inter 400/600 must NOT be axis-apart (same classification, weight gap only 200)")
    if not any("near-identical" in a for a in r["anti_patterns"]):
        errs.append("Inter 400/600 must flag the near-identical-pairing anti-pattern")

    # 5. CONSIDERED-RANGE PASS -- Inter 100 vs Inter 900: same family used at real weight extremes,
    #    weight gap 800 >= 300 -- axis-apart on weight alone, no anti-pattern
    r = pair_check("Inter", 100, "Inter", 900)
    if not r["weight_real_axis"] or not r["real_axis_apart"]:
        errs.append("Inter 100/900 must be axis-apart on the weight gap alone (800 >= 300)")
    if any("near-identical" in a for a in r["anti_patterns"]):
        errs.append("Inter 100/900 must NOT flag near-identical -- it's a considered weight-extreme pairing")

    # 6. SIZE-JUMP HIERARCHY PASS -- kicker 12 vs display 48: ratio 4.0 >= 3.0, reads as intentional
    #    hierarchy, no anti-pattern
    r = pair_check("Inter", 600, "Inter", 800, size_a=12, size_b=48)
    if r["size_jump_verdict"] != "hierarchy":
        errs.append("Inter 12/48 must be a hierarchy size-jump (ratio 4.0 >= 3.0), got %r" % r["size_jump_verdict"])
    if any("size-jump" in a for a in r["anti_patterns"]):
        errs.append("a hierarchy size-jump must NOT flag the size-jump anti-pattern")

    # 7. SIZE-JUMP ROUNDING-RANGE PASS -- body 16 vs lead 18: ratio 1.125 <= 1.5, reads as same-tier
    #    rounding, no anti-pattern (a small, deliberate step-to-step bump, not a hierarchy claim)
    r = pair_check("Inter", 400, "Inter", 400, size_a=16, size_b=18)
    if r["size_jump_verdict"] != "rounding-error-range":
        errs.append("Inter 16/18 must be in the rounding-error range (ratio 1.125 <= 1.5), got %r" % r["size_jump_verdict"])
    if any("size-jump" in a for a in r["anti_patterns"]):
        errs.append("a rounding-range size-jump must NOT flag the size-jump anti-pattern")

    # 8. SIZE-JUMP AMBIGUOUS ANTI-PATTERN -- 16 vs 32: ratio 2.0, strictly between 1.5 and 3.0 --
    #    neither a hierarchy claim nor a same-tier bump; must flag
    r = pair_check("Inter", 400, "Inter", 700, size_a=16, size_b=32)
    if r["size_jump_verdict"] != "ambiguous":
        errs.append("Inter 16/32 must be ambiguous (ratio 2.0, between 1.5 and 3.0), got %r" % r["size_jump_verdict"])
    if not any("size-jump" in a for a in r["anti_patterns"]):
        errs.append("an ambiguous size-jump must flag the size-jump anti-pattern")

    # 9. no sizes given -- size-jump fields stay None, no size-jump anti-pattern possible
    r = pair_check("Inter", 400, "Fraunces", 700)
    if r["size_jump_ratio"] is not None or r["size_jump_verdict"] is not None:
        errs.append("size-jump fields must be None when no sizes are given")

    # 10. unknown font raises, not silently returns
    try:
        pair_check("Not A Real Font", 400, "Inter", 400)
        errs.append("an unknown font name must raise KeyError")
    except KeyError:
        pass

    # 11. TABLE DRIFT -- font-craft.md's metrics table must exactly agree with the embedded FONTS
    #    dict (the two are hand-maintained in two files; this is the mechanized sync check)
    try:
        parsed = _parse_font_craft_table()
        if set(parsed) != set(FONTS):
            errs.append("font-craft.md rows %s != FONTS keys %s" % (sorted(parsed), sorted(FONTS)))
        for name in set(parsed) & set(FONTS):
            p, f = parsed[name], FONTS[name]
            for key in ("x_height", "cap_height", "family", "register"):
                if p[key] != f[key]:
                    errs.append("%s.%s drifted: font-craft.md has %r, FONTS has %r" % (name, key, p[key], f[key]))
    except Exception as e:
        errs.append("could not verify font-craft.md against FONTS: %s" % e)

    return errs


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("typeface-check: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("typeface-check: OK -- Inter/Fraunces worked pairing, IBM Plex Sans/Serif metric-matched "
              "pair, JetBrains Mono/Fraunces out-of-tolerance negative control, Inter 400/600 "
              "near-identical anti-pattern, Inter 100/900 considered-range pass, size-jump "
              "hierarchy/rounding/ambiguous cases, and font-craft.md table-drift check all verified")
        return 0

    if argv[0] == "fonts":
        for name, f in sorted(FONTS.items()):
            cap = "%.3f" % f["cap_height"] if f["cap_height"] is not None else "unmeasured"
            print("%-16s x-height %.3f  cap-height %-10s  %-6s  %-12s  (%s)"
                  % (name, f["x_height"], cap, f["family"], f["register"], f["source"]))
        return 0

    if argv[0] == "pair":
        if len(argv) not in (5, 7):
            sys.stderr.write(
                "usage: typeface-check.py pair <fontA> <weightA> <fontB> <weightB> [<sizeA> <sizeB>]\n")
            return 2
        font_a, weight_a, font_b, weight_b = argv[1], argv[2], argv[3], argv[4]
        size_a, size_b = (argv[5], argv[6]) if len(argv) == 7 else (None, None)
        try:
            weight_a, weight_b = int(weight_a), int(weight_b)
            if size_a is not None:
                size_a, size_b = float(size_a), float(size_b)
            result = pair_check(font_a, weight_a, font_b, weight_b, size_a, size_b)
        except (KeyError, ValueError) as e:
            sys.stderr.write("typeface-check: error -- %s\n" % e)
            return 2
        print(_fmt(result))
        return 1 if result["anti_patterns"] else 0

    sys.stderr.write(
        "usage: typeface-check.py <pair <fontA> <weightA> <fontB> <weightB> [<sizeA> <sizeB>] | fonts | selftest>\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
