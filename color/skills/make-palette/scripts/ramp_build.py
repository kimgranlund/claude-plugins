#!/usr/bin/env python3
"""ramp_build.py — the make-palette build mechanism. Self-contained (stdlib only).

Ramp construction is DETERMINISTIC DERIVATION, not judgment — so its arithmetic routes to code
(right tool for the job). This script builds one family's ramp from its curve JSON (assets/ramps/ — the
canon) in three stages:

  skeleton     — the L grid: anchors from the curve JSON's lightnessAnchors; any step the JSON
                 does not anchor is linearly interpolated in label space between its bracketing
                 anchors. A stated brand anchor overrides the anchor step's (default 500) ideal L.
  chroma bell  — C(L) = C_max * exp(-k * (L - L_peak)^2); C_max is SOLVED so the anchor step
                 reproduces the anchor's C exactly; L_peak / k come from the curve JSON's
                 chromaBell; caps applied per the JSON (chromaCeiling for neutrals, extremeFloors
                 for accents).
  gamut walk   — an out-of-sRGB-gamut step reduces C in 0.005 steps until in gamut — C only,
                 NEVER L or H (the rule both make-palette and check-colors state); the ΔC is
                 recorded in provenance; anchor-step ΔC > 0.05 → DecompositionGap (the anchor
                 itself is out of gamut).

Judgment stays with the model (SKILL.md): anchor NEGOTIATION (this script reports the gap, it
does not renegotiate), the ≤ ±8° hue-drift trade (this script never drifts hue), role mapping,
and dark-scheme review.

The OKLab→linear-sRGB matrices are the same CSS Color 4 reference constants (Björn Ottosson's
published matrices) that check-colors/scripts/contrast-check.py uses — one math on both sides of
the design→verify contract, each selftest-locked against the same known values.

Invariants checked on EVERY build (check-colors's ramp invariants):
  - L strictly monotonic in the curve's declared direction
  - per-label-unit evenness: adjacent gap-to-gap ratio of (ΔL ÷ Δlabel) ≤ 1.5
  - every emitted step in sRGB gamut (post-walk)
A violation is reported as a DecompositionGap and the build exits 1 — never silently shipped.

  python3 scripts/ramp_build.py selftest
  python3 scripts/ramp_build.py neutral --json
  python3 scripts/ramp_build.py accent --anchor "oklch(0.62 0.18 270)" --json
  python3 scripts/ramp_build.py danger --curve assets/ramps/accent-curve.json --anchor "oklch(0.58 0.19 25)"

<family>: `neutral` resolves to assets/ramps/neutral-curve.json; every other family (accent, danger,
warning, success, info, …) resolves to assets/ramps/accent-curve.json unless --curve overrides.
Accent-curve families REQUIRE --anchor (C_max and hue inherit from the brand anchor); a neutral
built without --anchor uses the tinted default (C_max = chromaCeiling, hue = hueDefault).

selftest: builds the neutral family from the checked-in curve and asserts monotone L, per-label-
unit evenness ≤ 1.5, and all steps in gamut; builds an anchored accent and asserts the anchor's C
is reproduced exactly; NEGATIVE CONTROL — an anchor forced out of gamut (oklch(0.62 0.35 30))
must come back with reduced C, byte-identical L and H, and a DecompositionGap; plus broken-curve
fixtures that must trip the monotonicity and evenness detectors. Python 3.8+.
"""
import json
import math
import os
import re
import sys

EVENNESS_MAX = 1.5      # check-colors's per-label-unit evenness gate (ΔL ÷ Δlabel, gap-to-gap)
GAMUT_C_STEP = 0.005    # the C-only reduction step
ANCHOR_DC_MAX = 0.05    # anchor-step ΔC beyond this = the anchor itself is out of gamut
DEFAULT_ANCHOR_STEP = 500

# OKLab -> sRGB (Björn Ottosson's published matrices — the CSS Color 4 reference constants;
# identical to check-colors/scripts/contrast-check.py).
_OKLAB_TO_LMS = (
    (1.0,  0.3963377774,  0.2158037573),
    (1.0, -0.1055613458, -0.0638541728),
    (1.0, -0.0894841775, -1.2914855480),
)
_LMS_TO_LINEAR_SRGB = (
    ( 4.0767416621, -3.3077115913,  0.2309699292),
    (-1.2684380046,  2.6097574011, -0.3413193965),
    (-0.0041960863, -0.7034186147,  1.7076147010),
)
_GAMUT_EPS = 1e-4

_OKLCH_RE = re.compile(r"oklch\(\s*([^)]*)\)", re.IGNORECASE)


def oklch_to_linear_srgb(L, C, H):
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    lms = [r0 * L + r1 * a + r2 * b for (r0, r1, r2) in _OKLAB_TO_LMS]
    lms = [v * v * v for v in lms]
    return [r0 * lms[0] + r1 * lms[1] + r2 * lms[2] for (r0, r1, r2) in _LMS_TO_LINEAR_SRGB]


def in_gamut(L, C, H):
    return all(-_GAMUT_EPS <= v <= 1.0 + _GAMUT_EPS for v in oklch_to_linear_srgb(L, C, H))


def to_hex(L, C, H):
    out = []
    for v in oklch_to_linear_srgb(L, C, H):
        v = min(1.0, max(0.0, v))
        enc = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out.append(int(round(enc * 255.0)))
    return "#%02x%02x%02x" % tuple(out)


def parse_oklch(s):
    """'oklch(L C H)' -> (L, C, H). L as 0-1 or %; H in degrees (optional 'deg')."""
    m = _OKLCH_RE.fullmatch(s.strip())
    if not m:
        raise ValueError("anchor must be 'oklch(L C H)', got %r" % s)
    parts = m.group(1).split()
    if len(parts) != 3:
        raise ValueError("oklch() needs 'L C H', got %r" % s)
    L = float(parts[0][:-1]) / 100.0 if parts[0].endswith("%") else float(parts[0])
    C = float(parts[1])
    hp = parts[2]
    H = float(hp[:-3]) if hp.lower().endswith("deg") else float(hp)
    if not (0.0 <= L <= 1.0):
        raise ValueError("oklch L out of range [0, 1] in %r" % s)
    if C < 0:
        raise ValueError("oklch C must be >= 0 in %r" % s)
    return L, C, H


# --- the three stages ---------------------------------------------------------------------------

def skeleton(curve, anchor=None, anchor_step=DEFAULT_ANCHOR_STEP):
    """Stage 1 — the L grid. Anchored steps from the JSON; missing steps linearly interpolated in
    label space; a brand anchor overrides the anchor step's ideal L."""
    steps = list(curve["scaleSteps"])
    anchors = {int(k): float(v) for k, v in curve["lightnessAnchors"].items()}
    if anchor is not None:
        anchors[anchor_step] = anchor[0]
    known = sorted(k for k in anchors if k in steps)
    if len(known) < 2:
        raise ValueError("curve needs at least 2 lightness anchors on the scale")
    grid = {}
    for s in steps:
        if s in anchors:
            grid[s] = anchors[s]
            continue
        lo = max((k for k in known if k < s), default=None)
        hi = min((k for k in known if k > s), default=None)
        if lo is None or hi is None:
            raise ValueError("step %s outside the anchored range %s..%s" % (s, known[0], known[-1]))
        t = (s - lo) / (hi - lo)
        grid[s] = anchors[lo] + t * (anchors[hi] - anchors[lo])
    return steps, grid


def chroma_bell(curve, steps, grid, anchor=None, anchor_step=DEFAULT_ANCHOR_STEP):
    """Stage 2 — C(L) = C_max * exp(-k * (L - L_peak)^2), C_max solved so the anchor step
    reproduces the anchor's C exactly; caps per the curve JSON."""
    bell = curve.get("chromaBell", {})
    defaults = bell.get("defaults", {})
    L_peak = float(defaults.get("L_peak", 0.5))
    k = float(defaults.get("k", 8))
    ceiling = curve.get("chromaCeiling")

    if anchor is not None:
        c_ref, l_ref = anchor[1], grid[anchor_step]
        if ceiling is not None:
            c_ref = min(c_ref, float(ceiling))
        c_max = c_ref * math.exp(k * (l_ref - L_peak) ** 2)  # bell(l_ref) == c_ref
    elif ceiling is not None:
        c_max = float(ceiling)  # tinted-neutral default: the bell peaks at the ceiling
    else:
        raise ValueError("accent-curve families need --anchor (C_max inherits from the brand anchor)")

    floors = bell.get("extremeFloors", {})
    dark = floors.get("darkEnd", {})
    light = floors.get("lightEnd", {})

    out = {}
    for s in steps:
        L = grid[s]
        C = c_max * math.exp(-k * (L - L_peak) ** 2)
        if ceiling is not None:
            C = min(C, float(ceiling))
        if dark and L < float(dark["whenLBelow"]):
            C = min(C, float(dark["capC"]))
        if light and L > float(light["whenLAbove"]):
            C = min(C, float(light["capC"]))
        out[s] = C
    return out


def gamut_walk(steps, grid, chroma, hue):
    """Stage 3 — C-only reduction: chroma down in 0.005 steps until in sRGB gamut. L and H are
    NEVER touched (the walk rebinds C alone). Returns {step: (C_final, deltaC)}."""
    out = {}
    for s in steps:
        L, C0 = grid[s], chroma[s]
        C = C0
        while C > 0 and not in_gamut(L, C, hue):
            C = max(0.0, C - GAMUT_C_STEP)
        out[s] = (C, C0 - C)
    return out


# --- invariants (check-colors's ramp invariants) --------------------------------------------------

def check_monotone(steps, grid):
    """L strictly monotonic in the declared direction (the sign of last-anchor − first-anchor)."""
    ls = [grid[s] for s in steps]
    direction = "decreasing" if ls[-1] < ls[0] else "increasing"
    ok = all((b < a) if direction == "decreasing" else (b > a) for a, b in zip(ls, ls[1:]))
    return direction, ok


def evenness_max_ratio(steps, grid):
    """Max adjacent gap-to-gap ratio of per-label-unit ΔL (ΔL ÷ Δlabel)."""
    gaps = [abs(grid[b] - grid[a]) / (b - a) for a, b in zip(steps, steps[1:])]
    worst = 1.0
    for g1, g2 in zip(gaps, gaps[1:]):
        if min(g1, g2) <= 0:
            return math.inf
        worst = max(worst, max(g1, g2) / min(g1, g2))
    return worst


# --- build ---------------------------------------------------------------------------------------

def build(curve, family, anchor=None, anchor_step=DEFAULT_ANCHOR_STEP, curve_path=None):
    """Full pipeline. Returns the result dict ({family, steps, invariants, gaps, ...})."""
    steps, grid = skeleton(curve, anchor, anchor_step)
    hue = anchor[2] if anchor is not None else curve.get("hueDefault")
    if hue is None:
        raise ValueError("no hue: pass --anchor or use a curve with hueDefault")
    chroma = chroma_bell(curve, steps, grid, anchor, anchor_step)
    walked = gamut_walk(steps, grid, chroma, hue)

    gaps = []
    direction, mono = check_monotone(steps, grid)
    if not mono:
        gaps.append("DecompositionGap: L not strictly monotonic (%s) — renegotiate the anchor" % direction)
    ratio = evenness_max_ratio(steps, grid)
    if ratio > EVENNESS_MAX:
        gaps.append("DecompositionGap: per-label-unit evenness %.3f > %.1f — renegotiate the anchor"
                    % (ratio, EVENNESS_MAX))
    if anchor is not None and walked[anchor_step][1] > ANCHOR_DC_MAX:
        gaps.append("DecompositionGap: anchor out of gamut — ΔC = %.3f > %.2f at step %s; "
                    "ask for a different anchor" % (walked[anchor_step][1], ANCHOR_DC_MAX, anchor_step))
    all_in = all(in_gamut(grid[s], walked[s][0], hue) for s in steps)
    if not all_in:
        gaps.append("DecompositionGap: a step remains out of gamut after the C-only walk")

    rows = []
    for s in steps:
        L, (C, dC) = grid[s], walked[s]
        row = {"step": s, "L": round(L, 4), "C": round(C, 4), "H": hue,
               "oklch": "oklch(%.3f %.3f %g)" % (L, C, hue), "srgb": to_hex(L, C, hue)}
        if dC > 1e-12:
            row["provenance"] = "gamut-reduced: ΔC = %.3f" % dC
            row["gamutReducedDeltaC"] = round(dC, 4)
        rows.append(row)
    return {
        "family": family, "curve": curve_path, "anchor": anchor and list(anchor),
        "direction": direction, "steps": rows,
        "invariants": {"monotoneL": mono, "evennessMaxRatio": round(ratio, 4),
                       "evennessPass": ratio <= EVENNESS_MAX, "allInGamut": all_in},
        "gaps": gaps,
        # raw values for exact-equality assertions (the selftest's L/H-unchanged lock)
        "_raw": {s: {"L": grid[s], "C": walked[s][0], "H": hue, "preWalkC": chroma[s]} for s in steps},
    }


def _skill_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_curve(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def curve_path_for(family):
    name = "neutral-curve.json" if family == "neutral" else "accent-curve.json"
    return os.path.join(_skill_root(), "assets", "ramps", name)


# --- selftest ------------------------------------------------------------------------------------

def selftest():
    errs = []

    # 1. conversion locked against the shared known values (same fixtures as contrast-check.py)
    if to_hex(1.0, 0.0, 0.0) != "#ffffff":
        errs.append("oklch(1 0 0) must be white, got %s" % to_hex(1.0, 0.0, 0.0))
    if to_hex(0.0, 0.0, 0.0) != "#000000":
        errs.append("oklch(0 0 0) must be black")
    if to_hex(0.62796, 0.25768, 29.234) != "#ff0000" or not in_gamut(0.62796, 0.25768, 29.234):
        errs.append("sRGB-red roundtrip wrong: %s" % to_hex(0.62796, 0.25768, 29.234))
    if in_gamut(0.7, 0.35, 30):
        errs.append("oklch(0.7 0.35 30) must be out of sRGB gamut")

    # 2. the neutral family, built from its checked-in curve (the canon)
    np = curve_path_for("neutral")
    nc = load_curve(np)
    n = build(nc, "neutral", curve_path=np)
    if [r["step"] for r in n["steps"]] != nc["scaleSteps"] or len(n["steps"]) != 13:
        errs.append("neutral build must emit the canon's 13 scaleSteps")
    if n["direction"] != "decreasing" or not n["invariants"]["monotoneL"]:
        errs.append("neutral L must be strictly monotone decreasing (declared direction)")
    if not n["invariants"]["evennessPass"]:
        errs.append("neutral per-label-unit evenness %.3f exceeds %.1f"
                    % (n["invariants"]["evennessMaxRatio"], EVENNESS_MAX))
    if not n["invariants"]["allInGamut"] or n["gaps"]:
        errs.append("neutral build must be gap-free and fully in gamut: %s" % n["gaps"])
    if any(v["preWalkC"] != v["C"] for v in n["_raw"].values()):
        errs.append("a C ≤ 0.02 neutral must never need gamut reduction")
    ceiling = nc["chromaCeiling"]
    if any(v["C"] > ceiling + 1e-9 for v in n["_raw"].values()):
        errs.append("neutral C must respect the chroma ceiling %s" % ceiling)
    if any(v["H"] != nc["hueDefault"] for v in n["_raw"].values()):
        errs.append("neutral hue must be constant at hueDefault")

    # 3. an anchored accent: the brand anchor's C is reproduced EXACTLY at its step
    ap = curve_path_for("accent")
    ac = load_curve(ap)
    a = build(ac, "accent", anchor=(0.62, 0.18, 270.0), curve_path=ap)
    if a["gaps"] or not a["invariants"]["allInGamut"]:
        errs.append("in-gamut accent anchor must build gap-free: %s" % a["gaps"])
    if abs(a["_raw"][500]["C"] - 0.18) > 1e-12 or a["_raw"][500]["preWalkC"] != a["_raw"][500]["C"]:
        errs.append("anchor step must reproduce the anchor's C exactly (got %r)" % a["_raw"][500]["C"])
    if not a["invariants"]["monotoneL"] or not a["invariants"]["evennessPass"]:
        errs.append("accent canon grid must hold monotonicity + evenness: %s" % a["invariants"])

    # 4. NEGATIVE CONTROL — an anchor forced out of gamut: C reduced, L and H NEVER change
    bad = build(ac, "accent", anchor=(0.62, 0.35, 30.0), curve_path=ap)
    ref_steps, ref_grid = skeleton(ac, (0.62, 0.35, 30.0))
    if not any("anchor out of gamut" in g for g in bad["gaps"]):
        errs.append("out-of-gamut anchor (ΔC > 0.05) must raise a DecompositionGap: %s" % bad["gaps"])
    if not (bad["_raw"][500]["C"] < 0.35 and bad["_raw"][500]["preWalkC"] == 0.35):
        errs.append("gamut walk must REDUCE the anchor step's C (got %r)" % bad["_raw"][500]["C"])
    for s in ref_steps:
        if bad["_raw"][s]["L"] != ref_grid[s]:
            errs.append("gamut walk shifted L at step %s — the walk must be C-only" % s)
            break
    if any(v["H"] != 30.0 for v in bad["_raw"].values()):
        errs.append("gamut walk rotated H — the walk must be C-only")
    if not bad["invariants"]["allInGamut"]:
        errs.append("the C-only walk must land every step in gamut")

    # 5. the invariant detectors themselves must bite (broken-curve fixtures)
    broken_mono = {"scaleSteps": [0, 100, 200], "chromaCeiling": 0.02, "hueDefault": 260,
                   "lightnessAnchors": {"0": 0.5, "100": 0.6, "200": 0.4}}
    if not any("monotonic" in g for g in build(broken_mono, "x")["gaps"]):
        errs.append("non-monotone curve not detected")
    broken_even = {"scaleSteps": [0, 100, 200], "chromaCeiling": 0.02, "hueDefault": 260,
                   "lightnessAnchors": {"0": 0.90, "100": 0.85, "200": 0.50}}
    if not any("evenness" in g for g in build(broken_even, "x")["gaps"]):
        errs.append("uneven curve (gap ratio 7x) not detected")

    return errs


# --- CLI -----------------------------------------------------------------------------------------

def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("ramp-build: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("ramp-build: OK — conversion known-values + neutral canon build (monotone, "
              "per-label-unit evenness <= 1.5, in gamut) + exact anchor reproduction + "
              "C-only negative control (reduced C, unchanged L/H, DecompositionGap) verified")
        return 0

    family, curve_path, anchor, as_json = argv[0], None, None, False
    args = argv[1:]
    while args:
        arg = args.pop(0)
        if arg == "--curve":
            curve_path = args.pop(0) if args else None
        elif arg == "--anchor":
            anchor = parse_oklch(args.pop(0)) if args else None
        elif arg == "--json":
            as_json = True
        else:
            sys.stderr.write("usage: ramp_build.py <family> [--curve assets/ramps/<file>.json] "
                             "[--anchor \"oklch(L C H)\"] [--json] | selftest\n")
            return 2
    curve_path = curve_path or curve_path_for(family)
    try:
        result = build(load_curve(curve_path), family, anchor, curve_path=curve_path)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as e:
        sys.stderr.write("ramp-build: error — %s\n" % e)
        return 2

    raw = result.pop("_raw")
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        print("%s (%s)  direction=%s  evenness=%.3f" % (result["family"], curve_path,
              result["direction"], result["invariants"]["evennessMaxRatio"]))
        for r in result["steps"]:
            print("  %4s  L=%.3f  C=%.3f  H=%g  %s  %s"
                  % (r["step"], raw[r["step"]]["L"], raw[r["step"]]["C"], r["H"], r["srgb"],
                     r.get("provenance", "")))
        for g in result["gaps"]:
            print("  !! %s" % g)
    return 1 if result["gaps"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
