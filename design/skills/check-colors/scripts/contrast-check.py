#!/usr/bin/env python3
"""contrast-check.py — the check-colors mechanism gate. Self-contained (stdlib only).

check-colors owns the *how* of color proof: it takes candidate pairs and proves they behave.
Two things matter when judging a palette, and they are different in kind:

  - WCAG 2.x contrast is ARITHMETIC — sRGB → linearized relative luminance → (L1+0.05)/(L2+0.05).
    An LLM eyeballing "looks fine" fails silently here, so the contrast floor is ROUTED TO CODE:
    this gate computes the ratio and flags any pair under its AA floor. (computation → code.)
  - CVD safety and perceptual evenness are PERCEPTUAL JUDGMENT — they stay a review in SKILL.md.

A "color surface card" is the small declarative artifact the skill emits (or re-derives when
grading a palette) listing the foreground/background pairs that carry text or UI indication:

  {
    "meta":  {"theme": "default", "scheme": "light", "contrast": "normal"},
    "pairs": [
      {"name": "body text",   "fg": "#1a1a1a",                "bg": "#ffffff", "role": "text"},
      {"name": "accent link", "fg": "oklch(0.558 0.135 255)", "bg": "#ffffff", "fgToken": "--accent-600"},
      {"name": "outline",     "fg": "#00000059",              "bg": "#ffffff", "over": "#ffffff", "role": "ui"}
    ]
  }

Card meta (optional): {"theme", "scheme", "contrast"} — `scheme` ("light"|"dark") picks the
light-dark() leg; theme/contrast are provenance, passed through to --json.

The card interface's canon is SKILL.md's "The card" section — this docstring is a working
summary, never a second canon.

Per pair (all keys optional except fg + bg):
  name    — a label for the report (default "<pair>")
  fg/bg   — #rgb | #rrggbb | #rrggbbaa | rgb()/rgba() | oklch(L C H [/ A]) | light-dark(X, Y).
            oklch: L as 0–1 or %, H in degrees (optional "deg"); standard OKLab → linear-sRGB
            matrices, gamma-encoded; a result outside sRGB gamut is CLAMPED and warned
            (OKLCH_OUT_OF_GAMUT). light-dark(X, Y) resolves via the card's meta.scheme
            ("light"→X, "dark"→Y); on a card with NO scheme it is a per-pair ERROR — never a
            silent first-leg pick.
  size    — "normal" (default) | "large"   — large text is 18.66px bold or 24px+ regular.
  role    — "text" (default) | "ui"         — ui/non-text (borders, icons, controls).
  over    — optional backdrop: an fg with alpha < 1 is composited over it (source-over in
            gamma-encoded sRGB, as browsers composite CSS colors) before the ratio vs bg.
            An fg with alpha < 1 and NO "over" is a per-pair ERROR — silently treating it as
            opaque inverts to false-PASS on exactly the riskiest pairs. bg and "over" must be
            opaque (resolve any translucent backdrop upstream).
  fgToken/bgToken — optional free-text provenance (token names); passed through to --json.

Flags (per the contrast floors in assets/verification/contrast-pairs.json):
  CONTRAST_FAIL_AA   (gate)      text below 4.5 (normal) / 3.0 (large); ui/non-text below 3.0.
  CONTRAST_FAIL_AAA  (advisory)  text below 7.0 (normal) / 4.5 (large) — only when AA already passes.
  OKLCH_OUT_OF_GAMUT (advisory)  an oklch() color outside sRGB gamut — clamped for the ratio;
                                 the upstream fix is C-only reduction (see SKILL.md gamut invariant).
  per-pair errors    (gate)      malformed color · light-dark() with no meta.scheme · alpha fg
                                 with no "over" · translucent bg/"over" — reported, never a crash.

--json emits the FULL per-pair table — every pair, pass AND fail (the skill's ColorProof
requires it): {name, fg, bg, ratio, target, pass, fgToken?, bgToken?, meta?, error?}.

This gate is a PRE-FILTER, not an oracle: clearing it means the arithmetic floor holds — it
does NOT prove the palette CVD-safe or perceptually even. Confirm those in review.

  python3 scripts/contrast-check.py selftest
  python3 scripts/contrast-check.py <card.json | dir>     # dirs walk *.surface.json / *.contrast.json
  python3 scripts/contrast-check.py --json <card.json>

Python 3.8+.
"""
import collections
import json
import math
import os
import re
import sys

# WCAG 2.x contrast floors --------------------------------------------------------------------
# keyed (role, size) -> (AA floor, AAA floor). ui/non-text has no separate large/AAA tier (1.4.11).
AA = {
    ("text", "normal"): 4.5,
    ("text", "large"):  3.0,
    ("ui",   "normal"): 3.0,
    ("ui",   "large"):  3.0,
}
AAA = {
    ("text", "normal"): 7.0,
    ("text", "large"):  4.5,
    # ui/non-text: 3.0 is the only graphical floor; AAA does not raise it -> no advisory tier.
    ("ui",   "normal"): None,
    ("ui",   "large"):  None,
}

_RGB_RE = re.compile(r"rgba?\(\s*([^)]*)\)", re.IGNORECASE)
_OKLCH_RE = re.compile(r"oklch\(\s*([^)]*)\)", re.IGNORECASE)

# OKLab -> sRGB (Björn Ottosson's published matrices — the CSS Color 4 reference constants).
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
_GAMUT_EPS = 1e-4  # float-noise tolerance before a linear channel counts as out of gamut


class ColorError(ValueError):
    """A color string that cannot be resolved into an sRGB triple."""


# Parsed color: 8-bit sRGB triple + alpha (0..1) + out-of-sRGB-gamut flag (oklch only).
Parsed = collections.namedtuple("Parsed", ["rgb", "alpha", "oog"])


def _oklch_to_srgb8(L, C, H):
    """OKLCH -> (8-bit sRGB triple, out_of_gamut flag). Out-of-gamut channels are clamped."""
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    lms = [r0 * L + r1 * a + r2 * b for (r0, r1, r2) in _OKLAB_TO_LMS]
    lms = [v * v * v for v in lms]
    lin = [r0 * lms[0] + r1 * lms[1] + r2 * lms[2] for (r0, r1, r2) in _LMS_TO_LINEAR_SRGB]
    oog = any(v < -_GAMUT_EPS or v > 1.0 + _GAMUT_EPS for v in lin)
    out = []
    for v in lin:
        v = min(1.0, max(0.0, v))
        enc = 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
        out.append(int(round(enc * 255.0)))
    return tuple(out), oog


def _num(p, s):
    try:
        return float(p)
    except ValueError:
        raise ColorError("bad number %r in %r" % (p, s))


def _alpha(p, s):
    """Parse an alpha component: 0-1 number or percentage."""
    v = _num(p[:-1], s) / 100.0 if p.endswith("%") else _num(p, s)
    if not (0.0 <= v <= 1.0):
        raise ColorError("alpha %r out of range [0, 1] in %r" % (p, s))
    return v


def _split_top(s):
    """Split on commas at paren depth 0 (so light-dark legs may themselves be functions)."""
    parts, depth, cur = [], 0, []
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return [p.strip() for p in parts]


def parse_color(s, scheme=None):
    """Parse a CSS color into Parsed(rgb=(r,g,b) 0-255, alpha 0..1, oog flag).

    Accepts #rgb | #rrggbb | #rrggbbaa | rgb()/rgba() | oklch(L C H [/ A]) | light-dark(X, Y).
    light-dark() needs `scheme` ("light"|"dark") — with scheme=None it raises (per-pair error,
    never a silent first-leg pick). Raises ColorError on anything malformed."""
    if not isinstance(s, str):
        raise ColorError("color must be a string, got %r" % (s,))
    t = s.strip()

    if t.lower().startswith("light-dark(") and t.endswith(")"):
        legs = _split_top(t[len("light-dark("):-1])
        if len(legs) != 2 or not all(legs):
            raise ColorError("light-dark() needs exactly 2 comma-separated colors, got %r" % s)
        if scheme not in ("light", "dark"):
            raise ColorError("light-dark() value %r needs card meta.scheme "
                             "(\"light\"|\"dark\") — refusing a silent first-leg pick" % s)
        return parse_color(legs[0] if scheme == "light" else legs[1], scheme)

    if t.startswith("#"):
        h = t[1:]
        if len(h) == 3:
            if not re.fullmatch(r"[0-9a-fA-F]{3}", h):
                raise ColorError("bad hex %r" % s)
            return Parsed(tuple(int(c * 2, 16) for c in h), 1.0, False)
        if len(h) in (6, 8):
            if not re.fullmatch(r"[0-9a-fA-F]+", h):
                raise ColorError("bad hex %r" % s)
            rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            alpha = int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0
            return Parsed(rgb, alpha, False)
        raise ColorError("hex must be #rgb, #rrggbb, or #rrggbbaa, got %r" % s)

    m = _OKLCH_RE.fullmatch(t)
    if m:
        body = m.group(1).strip()
        if "/" in body:
            lch, _, a_s = body.partition("/")
            alpha = _alpha(a_s.strip(), s)
        else:
            lch, alpha = body, 1.0
        parts = lch.split()
        if len(parts) != 3:
            raise ColorError("oklch() needs 'L C H' (+ optional '/ A'), got %r" % s)
        L = _num(parts[0][:-1], s) / 100.0 if parts[0].endswith("%") else _num(parts[0], s)
        if not (0.0 <= L <= 1.0):
            raise ColorError("oklch L %r out of range [0, 1] in %r" % (parts[0], s))
        C = _num(parts[1], s)
        if C < 0:
            raise ColorError("oklch C must be >= 0 in %r" % s)
        hp = parts[2]
        H = _num(hp[:-3], s) if hp.lower().endswith("deg") else _num(hp, s)
        rgb, oog = _oklch_to_srgb8(L, C, H)
        return Parsed(rgb, alpha, oog)

    m = _RGB_RE.fullmatch(t)
    if m:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1).strip()) if p.strip()]
        if len(parts) not in (3, 4):
            raise ColorError("rgb() needs 3 or 4 components, got %r" % s)
        out = []
        for p in parts[:3]:
            v = _num(p[:-1], s) / 100.0 * 255.0 if p.endswith("%") else _num(p, s)
            if not (0 <= v <= 255):
                raise ColorError("rgb component out of range in %r" % s)
            out.append(int(round(v)))
        alpha = _alpha(parts[3], s) if len(parts) == 4 else 1.0
        return Parsed(tuple(out), alpha, False)

    raise ColorError("unrecognized color %r (use #rgb, #rrggbb, #rrggbbaa, rgb()/rgba(), "
                     "oklch(), or light-dark())" % s)


def _lin(c):
    """sRGB 8-bit channel -> linear-light component (WCAG 2.x transfer)."""
    cs = c / 255.0
    return cs / 12.92 if cs <= 0.03928 else ((cs + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    r, g, b = rgb
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(fg, bg):
    """WCAG 2.x contrast ratio of two sRGB triples: (Llight + 0.05) / (Ldark + 0.05) ∈ [1, 21]."""
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = (l1, l2) if l1 >= l2 else (l2, l1)
    return (hi + 0.05) / (lo + 0.05)


def composite_over(fg_rgb, alpha, over_rgb):
    """Source-over in gamma-encoded sRGB — what browsers do when compositing CSS colors."""
    return tuple(int(round(f * alpha + o * (1.0 - alpha))) for f, o in zip(fg_rgb, over_rgb))


def check_pair(pair, scheme=None, meta=None):
    """Check one pair. Returns (record, fails, warns).

    record is the per-pair report row {name, fg, bg, ratio, target, pass} plus fgToken/bgToken/
    meta pass-through and an "error" key on a per-pair error. Emitted for EVERY pair."""
    fails, warns = [], []
    name = pair.get("name", "<pair>")
    role = (pair.get("role") or "text").lower()
    size = (pair.get("size") or "normal").lower()
    if role not in ("text", "ui"):
        fails.append("%s: role %r not in {text, ui}" % (name, role))
        role = "text"
    if size not in ("normal", "large"):
        fails.append("%s: size %r not in {normal, large}" % (name, size))
        size = "normal"

    rec = {"name": name, "fg": pair.get("fg"), "bg": pair.get("bg"),
           "ratio": None, "target": AA[(role, size)], "pass": False}
    for k in ("fgToken", "bgToken"):
        if k in pair:
            rec[k] = pair[k]
    if meta:
        rec["meta"] = meta

    def err(msg):
        fails.append("%s: %s" % (name, msg))
        rec["error"] = msg
        return rec, fails, warns

    try:
        fg = parse_color(pair.get("fg"), scheme)
        bg = parse_color(pair.get("bg"), scheme)
        over = parse_color(pair["over"], scheme) if "over" in pair else None
    except ColorError as e:
        return err(str(e))

    for slot, c in (("fg", fg), ("bg", bg), ("over", over)):
        if c is not None and c.oog:
            warns.append("OKLCH_OUT_OF_GAMUT — %s: %s %r outside sRGB gamut; clamped to rgb%r "
                         "for the ratio (the upstream fix is C-only reduction)"
                         % (name, slot, pair.get(slot) if slot != "over" else pair["over"], c.rgb))

    if bg.alpha < 1.0:
        return err("bg has alpha %.3g — the backdrop must be opaque; resolve compositing "
                   "upstream, never judge contrast against a translucent bg" % bg.alpha)
    if over is not None and over.alpha < 1.0:
        return err("'over' has alpha %.3g — the compositing backdrop must be opaque" % over.alpha)

    fg_rgb = fg.rgb
    if fg.alpha < 1.0:
        if over is None:
            return err("fg has alpha %.3g and no \"over\" backdrop — refusing silent-opaque "
                       "substitution (it inverts to false-PASS); add \"over\"" % fg.alpha)
        fg_rgb = composite_over(fg.rgb, fg.alpha, over.rgb)

    ratio = contrast_ratio(fg_rgb, bg.rgb)
    rec["ratio"] = round(ratio, 2)
    aa = AA[(role, size)]
    rec["pass"] = ratio >= aa
    if ratio < aa:
        fails.append("CONTRAST_FAIL_AA — %s: %.2f:1 (%s, %s) below AA floor %.1f:1"
                     % (name, ratio, role, size, aa))
        return rec, fails, warns  # already an AA fail; AAA advisory only applies once AA passes

    aaa = AAA[(role, size)]
    if aaa is not None and ratio < aaa:
        warns.append("CONTRAST_FAIL_AAA — %s: %.2f:1 (%s %s) passes AA %.1f but below AAA floor %.1f:1"
                     % (name, ratio, role, size, aa, aaa))
    return rec, fails, warns


def check_card(card):
    """Check a surface card ({"meta": {...}, "pairs": [...]}) or a bare pair / pair list.

    Returns (records, fails, warns, n) — records is the full per-pair table, pass AND fail."""
    meta = None
    if isinstance(card, dict) and "pairs" in card:
        pairs = card["pairs"]
        meta = card.get("meta")
    elif isinstance(card, list):
        pairs = card
    elif isinstance(card, dict):
        pairs = [card]  # a single bare pair card
    else:
        return [], ["card is not an object or list"], [], 0
    if not isinstance(pairs, list):
        return [], ["'pairs' must be a list"], [], 0

    fails, warns = [], []
    scheme = None
    if meta is not None:
        if not isinstance(meta, dict):
            fails.append("card meta must be an object, got %r" % (meta,))
            meta = None
        else:
            scheme = meta.get("scheme")
            if scheme is not None and scheme not in ("light", "dark"):
                fails.append("card meta.scheme %r not in {light, dark}" % (scheme,))
                scheme = None

    records = []
    for p in pairs:
        if not isinstance(p, dict):
            fails.append("pair entry is not an object: %r" % (p,))
            continue
        rec, f, w = check_pair(p, scheme=scheme, meta=meta)
        records.append(rec)
        fails += f
        warns += w
    return records, fails, warns, len(pairs)


# --- selftest fixtures -------------------------------------------------------------------------
# must-FLAG (AA gate fails)
BAD_777 = {"pairs": [{"name": "muted", "fg": "#777", "bg": "#fff", "size": "normal", "role": "text"}]}  # ~4.48 < 4.5
BAD_3TO1_AS_TEXT = {"pairs": [{"name": "thin text", "fg": "#949494", "bg": "#ffffff",
                               "size": "normal", "role": "text"}]}                                       # ~3.03 < 4.5
# must-NOT-flag (AA passes)
OK_DARK = {"pairs": [{"name": "body", "fg": "#111", "bg": "#fff", "size": "normal", "role": "text"}]}    # ~18.88
OK_767676 = {"pairs": [{"name": "label", "fg": "#767676", "bg": "#ffffff",
                        "size": "normal", "role": "text"}]}                                              # ~4.54 >= 4.5
OK_3TO1_LARGE = {"pairs": [{"name": "big head", "fg": "#949494", "bg": "#ffffff",
                            "size": "large", "role": "text"}]}                                           # ~3.03 >= 3.0
OK_3TO1_UI = {"pairs": [{"name": "border", "fg": "#949494", "bg": "#ffffff", "role": "ui"}]}             # ~3.03 >= 3.0
# AAA advisory (passes AA, below AAA) — a WARN, never a FAIL
AAA_ADVISORY = {"pairs": [{"name": "label", "fg": "#767676", "bg": "#fff", "size": "normal", "role": "text"}]}
# malformed color -> a clear error, not a crash
BAD_COLOR = {"pairs": [{"name": "typo", "fg": "#gggggg", "bg": "#fff"}]}
BAD_RGB_RANGE = {"pairs": [{"name": "oob", "fg": "rgb(300, 0, 0)", "bg": "#fff"}]}
# rgb()/rgba() accepted (alpha 1.0 is opaque — fine anywhere)
OK_RGB = {"pairs": [{"name": "rgb body", "fg": "rgb(17,17,17)", "bg": "rgba(255,255,255,1.0)",
                     "size": "normal", "role": "text"}]}
# oklch — the documented agent-ui accent token: ≈ rgb(54,117,193), ratio vs white ≈ 4.70 (AA pass)
OKLCH_TOKEN = {"pairs": [{"name": "accent link", "fg": "oklch(0.558 0.135 255)", "bg": "#ffffff",
                          "size": "normal", "role": "text", "fgToken": "--accent-600"}]}
# oklch out of gamut — clamps to rgb(255,0,0) (≈4.00 vs white: a ui PASS) + an advisory warn
OKLCH_OOG = {"pairs": [{"name": "neon", "fg": "oklch(0.7 0.35 30)", "bg": "#ffffff", "role": "ui"}]}
# light-dark(): light leg #767676 ≈ 4.54 passes; dark leg #949494 ≈ 3.03 FAILS as normal text —
# so the scheme choosing the WRONG leg is detectable, not just "some leg parsed"
LD_LIGHT = {"meta": {"scheme": "light"},
            "pairs": [{"name": "muted ld", "fg": "light-dark(#767676, #949494)", "bg": "#ffffff"}]}
LD_DARK = {"meta": {"scheme": "dark"},
           "pairs": [{"name": "muted ld", "fg": "light-dark(#767676, #949494)", "bg": "#ffffff"}]}
LD_NO_SCHEME = {"pairs": [{"name": "orphan ld", "fg": "light-dark(#111, #eee)", "bg": "#ffffff"}]}
LD_BAD_SCHEME = {"meta": {"scheme": "auto"},
                 "pairs": [{"name": "auto ld", "fg": "light-dark(#111, #eee)", "bg": "#ffffff"}]}
# alpha compositing — the shakedown's composited-outline case: #00000059 (α≈0.35) reads 21:1
# opaque but composites over white to rgb(166,166,166) ≈ 2.43:1 — a ui FAIL
COMPOSITED_OUTLINE = {"pairs": [{"name": "outline", "fg": "#00000059", "bg": "#ffffff",
                                 "over": "#ffffff", "role": "ui"}]}
OUTLINE_OPAQUE = {"pairs": [{"name": "outline opaque", "fg": "#000000", "bg": "#ffffff", "role": "ui"}]}
ALPHA_NO_OVER = {"pairs": [{"name": "ghost ink", "fg": "rgba(0,0,0,0.35)", "bg": "#ffffff"}]}
ALPHA_OVER_OK = {"pairs": [{"name": "ink 90%", "fg": "rgba(0,0,0,0.9)", "bg": "#ffffff",
                            "over": "#ffffff"}]}                                                          # ≈17.4 pass
BAD_BG_ALPHA = {"pairs": [{"name": "glass bg", "fg": "#000", "bg": "rgba(255,255,255,0.5)"}]}


def selftest():
    errs = []

    # --- 1. ratio math is correct against a known value -------------------------------------
    r_777 = contrast_ratio((0x77, 0x77, 0x77), (0xff, 0xff, 0xff))
    if not (4.47 < r_777 < 4.49):
        errs.append("ratio #777/#fff = %.4f, expected ~4.48" % r_777)
    r_767 = contrast_ratio((0x76, 0x76, 0x76), (0xff, 0xff, 0xff))
    if not (4.53 < r_767 < 4.55):
        errs.append("ratio #767676/#fff = %.4f, expected ~4.54" % r_767)
    if abs(contrast_ratio((0, 0, 0), (255, 255, 255)) - 21.0) > 0.01:
        errs.append("black-on-white must be 21:1")
    if abs(contrast_ratio((255, 255, 255), (255, 255, 255)) - 1.0) > 1e-9:
        errs.append("white-on-white must be 1:1")
    # order-independent (max/min in numerator/denominator)
    if abs(contrast_ratio((0x77,)*3, (0xff,)*3) - contrast_ratio((0xff,)*3, (0x77,)*3)) > 1e-9:
        errs.append("ratio must be symmetric in fg/bg")

    def recs_of(c):
        return check_card(c)[0]

    def fails_of(c):
        return check_card(c)[1]

    def warns_of(c):
        return check_card(c)[2]

    # --- 2. must-FLAG --------------------------------------------------------------------------
    if not any("CONTRAST_FAIL_AA" in f for f in fails_of(BAD_777)):
        errs.append("#777 on #fff (~4.48) as normal text not flagged AA-fail")
    if not any("CONTRAST_FAIL_AA" in f for f in fails_of(BAD_3TO1_AS_TEXT)):
        errs.append("3:1 pair as normal text not flagged AA-fail")

    # --- 3. must-NOT-flag ----------------------------------------------------------------------
    if fails_of(OK_DARK):
        errs.append("#111 on #fff wrongly flagged: %s" % fails_of(OK_DARK))
    if fails_of(OK_767676):
        errs.append("#767676 on #fff (~4.54) wrongly flagged AA-fail: %s" % fails_of(OK_767676))
    if fails_of(OK_3TO1_LARGE):
        errs.append("3:1 pair as LARGE text wrongly flagged: %s" % fails_of(OK_3TO1_LARGE))
    if fails_of(OK_3TO1_UI):
        errs.append("3:1 pair as UI role wrongly flagged: %s" % fails_of(OK_3TO1_UI))

    # --- 4. AAA advisory is a WARN, never a FAIL ----------------------------------------------
    if fails_of(AAA_ADVISORY):
        errs.append("AAA-only shortfall produced a FAIL (must be advisory): %s" % fails_of(AAA_ADVISORY))
    if not any("CONTRAST_FAIL_AAA" in w for w in warns_of(AAA_ADVISORY)):
        errs.append("#767676 on #fff (~4.54, < AAA 7.0) not warned AAA")
    # a UI-role pass must NOT emit an AAA advisory (no AAA tier for graphics)
    if warns_of(OK_3TO1_UI):
        errs.append("UI-role pass wrongly emitted an AAA advisory: %s" % warns_of(OK_3TO1_UI))
    # a deep-contrast pass clears BOTH AA and AAA — no warn at all
    if warns_of(OK_DARK):
        errs.append("#111 on #fff (>AAA) wrongly emitted an AAA advisory: %s" % warns_of(OK_DARK))

    # --- 5. malformed colors -> clear error, not a crash --------------------------------------
    if not any("typo" in f for f in fails_of(BAD_COLOR)):
        errs.append("malformed hex not reported as an error")
    if not any("oob" in f for f in fails_of(BAD_RGB_RANGE)):
        errs.append("out-of-range rgb() not reported as an error")

    # --- 6. hex / rgb() parsing ----------------------------------------------------------------
    if fails_of(OK_RGB):
        errs.append("rgb()/rgba(α=1) body text wrongly flagged: %s" % fails_of(OK_RGB))
    if parse_color("#abc").rgb != (0xaa, 0xbb, 0xcc):
        errs.append("#abc shorthand expansion wrong")
    if parse_color("rgb(50%, 0%, 100%)").rgb != (128, 0, 255):
        errs.append("percentage rgb() parse wrong: %r" % (parse_color("rgb(50%, 0%, 100%)").rgb,))
    p8 = parse_color("#00000059")
    if p8.rgb != (0, 0, 0) or abs(p8.alpha - 0x59 / 255.0) > 1e-9:
        errs.append("#rrggbbaa parse wrong: %r" % (p8,))
    if abs(parse_color("rgba(0,0,0,50%)").alpha - 0.5) > 1e-9:
        errs.append("rgba percentage alpha parse wrong")

    # --- 7. oklch() parsing against known values -----------------------------------------------
    if parse_color("oklch(1 0 0)").rgb != (255, 255, 255):
        errs.append("oklch(1 0 0) must be white: %r" % (parse_color("oklch(1 0 0)").rgb,))
    if parse_color("oklch(0 0 0)").rgb != (0, 0, 0):
        errs.append("oklch(0 0 0) must be black")
    red = parse_color("oklch(0.62796 0.25768 29.234)")  # sRGB red roundtrip
    if any(abs(a - b) > 1 for a, b in zip(red.rgb, (255, 0, 0))) or red.oog:
        errs.append("oklch sRGB-red roundtrip wrong: %r" % (red,))
    if parse_color("oklch(55.8% 0.135 255)").rgb != parse_color("oklch(0.558 0.135 255)").rgb:
        errs.append("oklch percentage-L must equal 0-1 L")
    if parse_color("oklch(0.558 0.135 255deg)").rgb != parse_color("oklch(0.558 0.135 255)").rgb:
        errs.append("oklch 'deg' hue suffix must parse")
    # the documented agent-ui token: oklch(0.558 0.135 255) vs white — hand-computed ≈ 4.70
    tok = parse_color("oklch(0.558 0.135 255)")
    if tok.oog:
        errs.append("agent-ui accent token wrongly flagged out of gamut")
    r_tok = contrast_ratio(tok.rgb, (255, 255, 255))
    if not (4.65 < r_tok < 4.80):
        errs.append("oklch(0.558 0.135 255) vs white = %.4f, expected ~4.70" % r_tok)
    if fails_of(OKLCH_TOKEN):
        errs.append("agent-ui accent token (≈4.70 as normal text) wrongly flagged: %s"
                    % fails_of(OKLCH_TOKEN))
    if abs(parse_color("oklch(0.5 0.1 30 / 0.4)").alpha - 0.4) > 1e-9:
        errs.append("oklch '/ A' alpha parse wrong")
    # out of gamut: clamped + advisory warn, never a crash or silent pass-through
    oog = parse_color("oklch(0.7 0.35 30)")
    if not oog.oog or oog.rgb != (255, 0, 0):
        errs.append("oklch(0.7 0.35 30) must clamp to red with oog flag: %r" % (oog,))
    if not any("OKLCH_OUT_OF_GAMUT" in w for w in warns_of(OKLCH_OOG)):
        errs.append("out-of-gamut oklch not warned OKLCH_OUT_OF_GAMUT")
    if fails_of(OKLCH_OOG):
        errs.append("out-of-gamut clamp (red-on-white ui, ≈4.00) wrongly FAILED: %s" % fails_of(OKLCH_OOG))

    # --- 8. light-dark() + meta.scheme ----------------------------------------------------------
    if fails_of(LD_LIGHT):
        errs.append("light-dark light leg (#767676 ≈4.54) wrongly flagged: %s" % fails_of(LD_LIGHT))
    if not any("CONTRAST_FAIL_AA" in f for f in fails_of(LD_DARK)):
        errs.append("light-dark dark leg (#949494 ≈3.03 as normal text) not flagged — wrong leg picked")
    if not any("meta.scheme" in f for f in fails_of(LD_NO_SCHEME)):
        errs.append("light-dark() with no card scheme must be a per-pair error, got: %s"
                    % fails_of(LD_NO_SCHEME))
    if not any("meta.scheme" in f for f in fails_of(LD_BAD_SCHEME)):
        errs.append("meta.scheme 'auto' not rejected: %s" % fails_of(LD_BAD_SCHEME))

    # --- 9. alpha compositing -------------------------------------------------------------------
    if composite_over((0, 0, 0), 0x59 / 255.0, (255, 255, 255)) != (166, 166, 166):
        errs.append("source-over compositing math wrong")
    # the composited-outline inversion: opaque PASSES, composited FAILS — never silently substitute
    if fails_of(OUTLINE_OPAQUE):
        errs.append("opaque outline (#000 on #fff, ui) wrongly flagged: %s" % fails_of(OUTLINE_OPAQUE))
    if not any("CONTRAST_FAIL_AA" in f for f in fails_of(COMPOSITED_OUTLINE)):
        errs.append("composited outline (α≈0.35 black over white ≈2.43 ui) not flagged — "
                    "the opaque→composited inversion is the whole point")
    if not any("over" in f for f in fails_of(ALPHA_NO_OVER)):
        errs.append("alpha fg with no 'over' must be a per-pair error, got: %s" % fails_of(ALPHA_NO_OVER))
    if fails_of(ALPHA_OVER_OK):
        errs.append("alpha fg WITH 'over' (composited ≈17.4) wrongly flagged: %s" % fails_of(ALPHA_OVER_OK))
    if not any("opaque" in f for f in fails_of(BAD_BG_ALPHA)):
        errs.append("translucent bg must be a per-pair error, got: %s" % fails_of(BAD_BG_ALPHA))

    # --- 10. the report table carries EVERY pair, pass and fail --------------------------------
    recs = recs_of(OK_DARK) + recs_of(BAD_777)
    if len(recs) != 2:
        errs.append("report table must carry every pair (got %d of 2)" % len(recs))
    for rec in recs:
        missing = [k for k in ("name", "fg", "bg", "ratio", "target", "pass") if k not in rec]
        if missing:
            errs.append("report row %r missing keys %s" % (rec.get("name"), missing))
    if recs and not (recs[0]["pass"] is True and recs[1]["pass"] is False):
        errs.append("report rows must carry pass=True for passes AND pass=False for fails")
    tok_rec = recs_of(OKLCH_TOKEN)[0]
    if tok_rec.get("fgToken") != "--accent-600":
        errs.append("fgToken provenance not passed through to the report row")
    ld_rec = recs_of(LD_LIGHT)[0]
    if not (isinstance(ld_rec.get("meta"), dict) and ld_rec["meta"].get("scheme") == "light"):
        errs.append("card meta not passed through to the report row")
    err_rec = recs_of(ALPHA_NO_OVER)[0]
    if "error" not in err_rec or err_rec["pass"] is not False:
        errs.append("a per-pair error must still yield a report row with error + pass=False")

    return errs


def _iter_cards(path):
    if os.path.isdir(path):
        for dp, _, fns in os.walk(path):
            for fn in sorted(fns):
                if fn.endswith(".surface.json") or fn.endswith(".contrast.json"):
                    yield os.path.join(dp, fn)
    else:
        yield path


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("contrast-check: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("contrast-check: OK — WCAG ratio math + AA gate + AAA advisory + oklch/light-dark/"
              "alpha-compositing + report table verified over good/bad fixtures")
        return 0

    as_json = False
    args = list(argv)
    if args and args[0] == "--json":
        as_json = True
        args = args[1:]
    if not args:
        sys.stderr.write("usage: contrast-check.py [--json] <card.json | dir>\n")
        return 2

    records, fails, warns, n = [], [], [], 0
    for fp in _iter_cards(args[0]):
        try:
            doc = json.load(open(fp, encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            fails.append("%s: unreadable (%s)" % (fp, e))
            continue
        for card in (doc if isinstance(doc, list) else [doc]):
            r, f, w, c = check_card(card)
            records += r
            fails += f
            warns += w
            n += c

    if as_json:
        out = {"pairs_checked": n, "status": "FAIL" if fails else "OK",
               "pairs": records, "fails": fails, "warns": warns}
        print(json.dumps(out, indent=2))
        return 1 if fails else 0

    for w in warns:
        print("  ⚠ %s" % w)
    if fails:
        sys.stderr.write("contrast-check: FAIL (%d)\n" % len(fails))
        for f in fails:
            sys.stderr.write("  - %s\n" % f)
        return 1
    print("contrast-check: OK — %d pair(s) clear the AA contrast floor" % n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
