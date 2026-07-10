#!/usr/bin/env python3
"""bundle_gates.py — deterministic gates for a Claude Design / Claude Code
design-system export bundle (DESIGN.md + tokens.json + components/*.html).

Python 3.8+, stdlib only — runnable in any repo, no install.

Usage:
    python3 bundle_gates.py <bundle-dir>     # run all gates, exit 0 iff no FAIL
    python3 bundle_gates.py selftest         # lock the color math + pair logic
    python3 bundle_gates.py --selftest       # (alias, kept for back-compat)

Gates (details: ../references/gates.md):
  G1 contrast          every derivable fill/on pair MEASURED against 4.5:1, BOTH
                       schemes (WCAG AA normal-text bar; -disabled and alpha<1
                       tokens excluded and reported as SKIP). KIT FIDELITY: when
                       the bundle's README.md carries the onColorMode disclosure
                       ("N derivable fill/on-pair(s) below 4.5:1 ... ADR-003"),
                       sub-4.5 pairs report as DISCLOSED (not FAIL) and the
                       disclosed count must be COUNT-EXACT vs the measurement
                       (a wrong count IS a FAIL). Without the disclosure, any
                       sub-4.5 pair FAILs as before.
  G2 scheme parity     identical role inventory: frontmatter light <-> -dark siblings;
                       tokens.json colors <-> colorsDark
  G3 carrier equality  frontmatter OKLCH == tokens.json hex, notation-aware:
                       equal when both resolve to the same sRGB 8-bit triple
                       within +-1/255 per channel (alpha compared the same way)
  G4 previews          @dsCard first-line marker; no external fetches; color-scheme
                       present in any file using light-dark() (else the dark end
                       never fires)
  G5 references        every {group.token} reference in DESIGN.md resolves
  G6 sections          canonical ## names in canonical order, no duplicates;
                       Responsive Behavior + Agent Prompt Guide present (Claude profile)
  G7 required roles    every family base fill has an on-partner (value-equal aliases
                       pass); literal `primary` missing -> WARN (Stitch-compat alias)
  G8 relative leading  leading/tracking are always relative — unitless factor, em,
                       or % (standing rule); never absolute px in any carrier:
                       frontmatter lineHeight/letterSpacing, tokens.json type.scale
                       (a string ending px, or a lineHeight number > 4 — a px
                       length, not a factor), preview inline styles
  G9 pill padding      badge/chip padding (border-radius:9999px elements) is
                       consistent across every preview — the scale floor (4px) is
                       too coarse for compact pills, so a compound below-scale
                       value is the one sanctioned exception (gates.md); the
                       violation isn't being off-scale, it's being off-scale
                       DIFFERENTLY in different places (live-generation evidence:
                       2 independent runs against the same bundle, one scattered
                       5 ad-hoc values across every chip, the other converged on 1)
  W  orphans           color roles never referenced in prose/components/previews -> WARN
  DIV divergence       on-colors constant across schemes -> DIVERGENCE info line;
                       NEVER a failure — an upstream authorial decision to record in
                       the receipt, not to silently override

Exit code: 0 iff zero FAIL lines. WARN / SKIP / DIVERGENCE never gate.
"""
import json
import math
import re
import sys
from pathlib import Path

AA = 4.5

# ---------------------------------------------------------------- color math

def _f(x):  # number or percentage token -> float
    x = x.strip()
    return float(x[:-1]) / 100.0 if x.endswith("%") else float(x)


OKLCH_RE = re.compile(
    r"oklch\(\s*([\d.]+%?)\s+([\d.]+%?)\s+([\d.]+)(?:deg)?\s*(?:/\s*([\d.]+%?)\s*)?\)",
    re.I,
)


def oklch_to_srgb8(s):
    """'oklch(L C H [/ A])' -> ((r,g,b) 8-bit, alpha float) or None."""
    m = OKLCH_RE.fullmatch(s.strip())
    if not m:
        return None
    L, C, H = _f(m.group(1)), _f(m.group(2)), float(m.group(3))
    alpha = _f(m.group(4)) if m.group(4) else 1.0
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (
        +4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )

    def enc(c):
        c = min(1.0, max(0.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

    return tuple(round(enc(c) * 255) for c in lin), alpha


def hex_to_srgb8(s):
    s = s.strip().lstrip("#")
    if len(s) in (3, 4):
        s = "".join(ch * 2 for ch in s)
    if len(s) == 6:
        s += "FF"
    if len(s) != 8 or not re.fullmatch(r"[0-9a-fA-F]{8}", s):
        return None
    r, g, b, a = (int(s[i : i + 2], 16) for i in (0, 2, 4, 6))
    return (r, g, b), a / 255.0


def parse_color(s):
    if s.strip().startswith("#"):
        return hex_to_srgb8(s)
    return oklch_to_srgb8(s)


def rel_lum(rgb):
    def lin(u):
        u /= 255.0
        return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def contrast(c1, c2):
    hi, lo = sorted((rel_lum(c1), rel_lum(c2)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


# ------------------------------------------------------- DESIGN.md parsing

def split_design(text):
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
    return (m.group(1), text[m.end():]) if m else ("", text)


def fm_blocks(fm):
    """Top-level frontmatter keys -> {child-key: scalar-value} (2-space children;
    deeper nesting recorded as key with '' value; comment lines skipped)."""
    blocks, current = {}, None
    for line in fm.splitlines():
        if re.match(r"^\s*#", line):
            continue
        if re.match(r"^[A-Za-z][\w-]*:", line):
            current = line.split(":", 1)[0]
            blocks.setdefault(current, {})
        elif current is not None:
            m = re.match(r"^  ([A-Za-z0-9][\w-]*):\s*(.*)$", line)
            if m:
                blocks[current][m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return blocks


# --------------------------------------------------- grammar-driven pairing

SLOTS = [  # longest-first for family stripping (Ultimate Tokens slot registry)
    "surface-brightest", "surface-highest", "surface-dimmest", "surface-lowest",
    "scrim-strongest", "scrim-weakest", "inverse-surface", "outline-variant",
    "surface-variant", "container-high", "container-low", "surface-bright",
    "scrim-strong", "surface-high", "surface-dim", "surface-low", "background",
    "placeholder", "scrim-weak", "container", "disabled", "outline", "surface",
    "active", "bright", "hover", "scrim", "dim", "high", "low",
]


def family_of(key):
    if "-on-" in key:
        return None
    k, changed = key, True
    while changed:
        changed = False
        for suf in SLOTS:
            if k.endswith("-" + suf):
                k, changed = k[: -(len(suf) + 1)], True
                break
    return k or None


def derive_pairs(keys):
    """From one scheme's key set, derive (on_key, fill_key) text pairs by grammar.
    Returns (pairs, on_keys_without_fill)."""
    keys = set(keys)
    pairs, unfillable = [], []
    for k in sorted(keys):
        if "-on-" not in k:
            continue
        stem, tail = k.split("-on-", 1)
        tail_base = re.sub(r"-(hover|active|disabled)$", "", tail)
        if tail_base in ("surface", "surface-variant"):
            fills = [
                f for f in keys
                if "-on-" not in f
                and re.fullmatch(re.escape(stem) + r"-(background|surface(-[a-z]+)*)", f)
                and not f.endswith("-disabled")
            ]
        else:
            fills = [f for f in (tail_base, tail_base + "-hover", tail_base + "-active")
                     if f in keys]
        if fills:
            pairs += [(k, f) for f in fills]
        else:
            unfillable.append(k)
    return pairs, unfillable


# ------------------------------------------------------------------ reporting

class Report:
    def __init__(self):
        self.lines, self.fails, self.warns, self.disclosed = [], 0, 0, 0

    def emit(self, level, msg):
        self.lines.append(f"[{level}] {msg}")
        if level == "FAIL":
            self.fails += 1
        elif level == "WARN":
            self.warns += 1
        elif level == "DISCLOSED":
            self.disclosed += 1

    def ok(self, cond, gate, ok_msg, fail_msg):
        self.emit("PASS" if cond else "FAIL", f"{gate} {ok_msg if cond else fail_msg}")


# ------------------------------------------------------------------- gates

CANON = ["overview", "colors", "typography", "layout", "elevation and depth",
         "shapes", "components", "do's and don'ts"]
ALIASES = {"brand and style": "overview", "layout and spacing": "layout",
           "elevation": "elevation and depth"}
EXTRAS = ["responsive behavior", "agent prompt guide"]


def _norm(h):
    h = h.replace("’", "'").replace("&", "and")
    return re.sub(r"\s+", " ", h).strip().lower()


# KIT FIDELITY (ultimate-tokens PR #229): `onColorMode` is a USER SETTING — "fixed" ships
# uniform brand labels whose sub-4.5:1 pairs are an accepted brand override (ADR-003), disclosed
# in the bundle's README receipt; "contrast" re-points labels inside the role table. The gate
# stays the MEASUREMENT; the receipt is the DISCLOSURE. read_disclosure returns (count, mode)
# when the receipt carries a count-bearing contrast disclosure with the ADR-003 citation.
_DISCLOSURE_RE = re.compile(
    r"(\d+) derivable fill/on-pair\(s\) below 4\.5:1 under the kit's `onColorMode: (\w+)`")


def read_disclosure(root):
    readme = Path(root) / "README.md"
    if not readme.is_file():
        return None
    text = readme.read_text(encoding="utf-8")
    m = _DISCLOSURE_RE.search(text)
    if m and "ADR-003" in text:
        return int(m.group(1)), m.group(2)
    return None


def check_bundle(root, rep):
    root = Path(root)
    design_p, tokens_p, comp_dir = root / "DESIGN.md", root / "tokens.json", root / "components"
    if not design_p.is_file():
        rep.emit("FAIL", f"G0 missing {design_p}")
        return
    text = design_p.read_text(encoding="utf-8")
    fm, body = split_design(text)
    blocks = fm_blocks(fm)
    colors = blocks.get("colors", {})
    lights = {k: v for k, v in colors.items() if not k.endswith("-dark")}
    darks = {k[:-5]: v for k, v in colors.items() if k.endswith("-dark")}

    tj = {}
    if tokens_p.is_file():
        tj = json.loads(tokens_p.read_text(encoding="utf-8"))
    else:
        rep.emit("FAIL", "G0 missing tokens.json")

    # G2 scheme parity ------------------------------------------------------
    rep.ok(set(lights) == set(darks), "G2",
           f"frontmatter parity: {len(lights)} roles x 2 schemes",
           "frontmatter parity broken: only-light=%s only-dark=%s"
           % (sorted(set(lights) - set(darks)), sorted(set(darks) - set(lights))))
    tjl, tjd = tj.get("colors", {}), tj.get("colorsDark", {})
    rep.ok(set(tjl) == set(tjd) and bool(tjl), "G2",
           f"tokens.json parity: {len(tjl)} roles x 2 schemes",
           "tokens.json parity broken: only-colors=%s only-colorsDark=%s"
           % (sorted(set(tjl) - set(tjd)), sorted(set(tjd) - set(tjl))))

    # resolve every carrier value to sRGB8 ----------------------------------
    def resolve(d, label):
        out = {}
        for k, v in d.items():
            c = parse_color(v)
            if c is None:
                rep.emit("FAIL", f"G0 unparseable color {label}.{k} = {v!r}")
            else:
                out[k] = c
        return out

    L8, D8 = resolve(lights, "fm.light"), resolve(darks, "fm.dark")
    TL8, TD8 = resolve(tjl, "tokens.colors"), resolve(tjd, "tokens.colorsDark")

    # G3 carrier equality (notation-aware, +-1/255 incl. alpha) --------------
    if tjl:
        rep.ok(set(lights) == set(tjl), "G3",
               "carrier inventories match (frontmatter == tokens.json)",
               "carrier inventories differ: fm-only=%s tokens-only=%s"
               % (sorted(set(lights) - set(tjl)), sorted(set(tjl) - set(lights))))
        bad, maxdev = [], 0
        for scheme, A, B in (("light", L8, TL8), ("dark", D8, TD8)):
            for k in sorted(set(A) & set(B)):
                (ra, aa), (rb, ab) = A[k], B[k]
                dev = max(abs(x - y) for x, y in zip(ra, rb))
                dev = max(dev, abs(round(aa * 255) - round(ab * 255)))
                maxdev = max(maxdev, dev)
                if dev > 1:
                    bad.append(f"{scheme}.{k} (dev {dev}/255)")
        rep.ok(not bad, "G3",
               f"carrier equality within +-1/255 (max dev {maxdev})",
               "carrier values diverge beyond 1/255: " + ", ".join(bad))

    # G1 contrast — all derivable pairs, both schemes. A sub-4.5 pair is a FAIL unless the
    # bundle receipt DISCLOSES the kit-fidelity contrast measurement (then it reports as
    # DISCLOSED and the disclosed count must match the measurement exactly).
    disclosure = read_disclosure(root)
    measured_misses = 0
    for scheme, S in (("light", L8), ("dark", D8)):
        pairs, unfillable = derive_pairs(S.keys())
        for k in unfillable:
            rep.emit("FAIL", f"G1 {scheme}: on-color '{k}' has no fill to pair with")
        if not pairs:
            rep.emit("FAIL", f"G1 {scheme}: no on-pairs derivable — grammar violated "
                             "or the reduction dropped every on-color")
            continue
        fails = skips = 0
        worst = (99.0, "")
        for on_k, fill_k in pairs:
            (rgb1, a1), (rgb2, a2) = S[on_k], S[fill_k]
            if fill_k.endswith("-disabled"):
                skips += 1
                continue
            if a1 < 1.0 or a2 < 1.0:
                rep.emit("SKIP", f"G1 {scheme}: {on_k} / {fill_k} — alpha < 1, "
                                 "not a text pair")
                skips += 1
                continue
            ratio = contrast(rgb1, rgb2)
            if ratio < worst[0]:
                worst = (ratio, f"{on_k} / {fill_k}")
            if ratio < AA:
                measured_misses += 1
                if disclosure:
                    rep.emit("DISCLOSED",
                             f"G1 {scheme}: {on_k} / {fill_k} = {ratio:.2f}:1 < {AA}:1 "
                             f"(onColorMode: {disclosure[1]}, ADR-003 — disclosed in README.md)")
                else:
                    fails += 1
                    rep.emit("FAIL", f"G1 {scheme}: {on_k} / {fill_k} = {ratio:.2f}:1 < {AA}:1")
        if not fails:
            rep.emit("PASS", f"G1 {scheme}: {len(pairs) - skips} pairs >= {AA}:1 "
                             f"(worst {worst[0]:.2f}:1 {worst[1]})" if not (disclosure and measured_misses)
                     else f"G1 {scheme}: measured (worst {worst[0]:.2f}:1 {worst[1]}); misses disclosed")
    if disclosure:
        rep.ok(measured_misses == disclosure[0], "G1",
               f"disclosure count-exact: receipt discloses {disclosure[0]} pair(s), gate measured "
               f"{measured_misses} (onColorMode: {disclosure[1]}, ADR-003)",
               f"receipt discloses {disclosure[0]} pair(s) but the gate measured {measured_misses} "
               f"— the disclosure must be COUNT-EXACT (stale receipt or wrong measurement)")

    # G7 required roles ------------------------------------------------------
    fam_bases = {k for k in L8 if family_of(k) == k}
    missing_on = []
    for fam in sorted(fam_bases):
        has_on = any(k.startswith(fam + "-on-") or k.endswith("-on-" + fam) for k in L8)
        if not has_on:
            alias_of = [o for o in fam_bases - {fam} if L8[o][0] == L8[fam][0]
                        and any(k.startswith(o + "-on-") for k in L8)]
            if alias_of:
                rep.emit("INFO", f"G7 '{fam}' is a value-equal alias of "
                                 f"'{alias_of[0]}' (compat alias — document in receipt)")
            else:
                missing_on.append(fam)
    rep.ok(not missing_on, "G7",
           f"every family base has an on-partner ({len(fam_bases)} fills)",
           "fills without an on-partner: " + ", ".join(missing_on))
    if not any(k in L8 for k in ("primary", "primary-base")):
        rep.emit("WARN", "G7 no 'primary'/'primary-base' role — Stitch lints "
                         "missing-primary; ship a compat alias")

    # G5 reference resolution -----------------------------------------------
    refs = re.findall(r"\{(colors|typography|spacing|rounded)\.([A-Za-z0-9-]+)\}", text)
    dangling = sorted({f"{{{g}.{k}}}" for g, k in refs if k not in blocks.get(g, {})})
    rep.ok(not dangling, "G5", f"all {len(refs)} {{group.token}} references resolve",
           "dangling references: " + ", ".join(dangling))

    # G6 section grammar ------------------------------------------------------
    heads = [_norm(h) for h in re.findall(r"^##\s+(.+?)\s*$", body, re.M)]
    heads = [ALIASES.get(h, h) for h in heads]
    dupes = sorted({h for h in heads if heads.count(h) > 1})
    rep.ok(not dupes, "G6", "no duplicate section headings",
           "duplicate headings: " + ", ".join(dupes))
    present = [h for h in heads if h in CANON]
    rep.ok(present == sorted(present, key=CANON.index), "G6",
           "canonical sections in canonical order",
           f"canonical sections out of order: {present}")
    for miss in [c for c in CANON if c not in heads]:
        rep.emit("WARN", f"G6 canonical section missing: '{miss}' "
                         "(Stitch-omissible; the authored dialect ships all 8)")
    for ex in EXTRAS:
        rep.ok(ex in heads, "G6", f"'{ex}' present",
               f"'{ex}' missing — required by the Claude profile")

    # G4 previews --------------------------------------------------------------
    cards = sorted(comp_dir.glob("*.html")) if comp_dir.is_dir() else []
    rep.ok(bool(cards), "G4", f"{len(cards)} preview card(s) found",
           "no components/*.html preview cards")
    for card in cards:
        t = card.read_text(encoding="utf-8")
        first = t.lstrip().splitlines()[0] if t.strip() else ""
        okm = first.startswith("<!--") and "@dsCard" in first and \
            "group=" in first and "title=" in first
        rep.ok(okm, "G4", f"{card.name}: @dsCard marker on line 1",
               f"{card.name}: first line is not an @dsCard marker with group/title")
        ext = re.search(r'(?:src|href)\s*=\s*["\']\s*(?:https?:)?//', t) \
            or "url(http" in t or "@import" in t
        rep.ok(not ext, "G4", f"{card.name}: self-contained (no external fetches)",
               f"{card.name}: external fetch found — previews must be self-contained")
        if "light-dark(" in t:
            rep.ok("color-scheme" in t, "G4",
                   f"{card.name}: color-scheme present with light-dark()",
                   f"{card.name}: uses light-dark() without color-scheme — "
                   "the dark end never fires")

    # G8 relative leading/tracking — never absolute px, in any carrier ----------
    px_lt = []
    for m in re.finditer(r"(lineHeight|letterSpacing)\s*:\s*[\"']?\s*(-?[\d.]+\s*px)",
                         fm):
        px_lt.append(f"frontmatter {m.group(1)} = {m.group(2)}")
    scale = tj.get("type", {}).get("scale", {})
    for level, entry in (scale.items() if isinstance(scale, dict) else ()):
        if not isinstance(entry, dict):
            continue
        for field in ("lineHeight", "letterSpacing"):
            v = entry.get(field)
            if isinstance(v, str) and v.strip().endswith("px"):
                px_lt.append(f"tokens.json type.scale.{level}.{field} = {v!r}")
            elif field == "lineHeight" and isinstance(v, (int, float)) and v > 4:
                px_lt.append(f"tokens.json type.scale.{level}.{field} = {v} "
                             "(> 4 — a px length, not a factor)")
    for card in cards:
        t = card.read_text(encoding="utf-8")
        for m in re.finditer(
                r"(?:line-height|letter-spacing)\s*:\s*[^;\n]*?\d[\d.]*px", t, re.I):
            px_lt.append(f"{card.name}: `{m.group(0).strip()}`")
    rep.ok(not px_lt, "G8",
           "leading/tracking relative (unitless/em/%, never px)",
           "leading/tracking are always relative — unitless factor, em, or % "
           "(standing rule); px found: " + "; ".join(px_lt))

    # G9 pill/chip padding consistency ------------------------------------------
    # Not "is it on the closed scale" (a compound below-scale value is the one
    # sanctioned exception — the schema's Dimension type is single-valued, so a
    # pill's asymmetric padding can never be a frontmatter token; see gates.md).
    # The generic-output signal is INCONSISTENCY: the same shape padded five
    # different ad-hoc ways across the bundle. Theme-agnostic by design — this
    # never hardcodes a specific value; it only requires whatever value is chosen
    # to be chosen once.
    pill_padding = {}  # normalized padding value -> [card names]
    for card in cards:
        t = card.read_text(encoding="utf-8")
        groups = re.findall(r'style="([^"]*)"', t) + re.findall(r"\{([^{}]*)\}", t)
        for g in groups:
            if re.search(r"border-radius\s*:\s*9999px", g):
                m = re.search(r"padding\s*:\s*([^;]+)", g)
                if m:
                    val = re.sub(r"\s+", " ", m.group(1).strip())
                    pill_padding.setdefault(val, []).append(card.name)
    distinct = sorted(pill_padding)
    total = sum(len(v) for v in pill_padding.values())
    rep.ok(len(distinct) <= 1, "G9",
           f"pill/chip padding consistent ({distinct[0]!r}, {total} instance(s))"
           if distinct else "pill/chip padding consistent (none found)",
           "pill/chip padding is inconsistent across previews: " +
           "; ".join(f"{v!r} in {', '.join(sorted(set(cs)))}"
                     for v, cs in pill_padding.items()) +
           " — badges/chips must share ONE padding value bundle-wide; pick a "
           "compound value once and hardcode it everywhere (the scale's 4px "
           "floor is too coarse for compact pills — that's the sanctioned "
           "exception, not an invitation to improvise per-element)")

    # W orphans (never gates) ---------------------------------------------------
    card_text = "".join(c.read_text(encoding="utf-8") for c in cards)
    for k in sorted(lights):
        if f"{{colors.{k}}}" not in text and k not in card_text:
            rep.emit("WARN", f"W orphan role '{k}' — never referenced in prose, "
                             "components, or previews")

    # DIV divergence (never gates) -----------------------------------------------
    for k in sorted(set(tjl) & set(tjd)):
        if "-on-" in k and tjl[k] == tjd[k]:
            rep.emit("DIVERGENCE", f"on-color constant across schemes: {k} = {tjl[k]} "
                                   "— upstream authorial decision; record in the "
                                   "receipt, do not silently override")


# ------------------------------------------------------------------ selftest

def selftest():
    c, a = oklch_to_srgb8("oklch(1 0 89.88)")
    assert c == (255, 255, 255) and a == 1.0, c
    c, _ = oklch_to_srgb8("oklch(0 0 0)")
    assert c == (0, 0, 0), c
    c, _ = oklch_to_srgb8("oklch(0.5585 0.0245 288.45)")  # Studio 54 primary-base
    ref, _ = hex_to_srgb8("#737282")
    assert max(abs(x - y) for x, y in zip(c, ref)) <= 1, (c, ref)
    c, a = oklch_to_srgb8("oklch(0.6031 0.0256 288.31 / 30%)")
    assert abs(a - 0.30) < 0.001, a
    _, a = hex_to_srgb8("#807F904D")
    assert abs(a - 77 / 255) < 0.001, a
    assert contrast((0, 0, 0), (255, 255, 255)) > 20.9
    # F1 exemplar: constant white on the dark-scheme primary-base fill (#8E8D9C) ~3.3:1
    assert contrast((255, 255, 255), (142, 141, 156)) < AA
    assert family_of("primary-base-surface-high") == "primary-base"
    assert family_of("danger-hover") == "danger"
    assert family_of("accent-muted-on-accent-muted") is None
    pairs, unf = derive_pairs({"danger", "danger-hover", "danger-on-danger",
                               "n-surface", "n-background", "n-on-surface"})
    assert ("danger-on-danger", "danger") in pairs
    assert ("danger-on-danger", "danger-hover") in pairs
    assert ("n-on-surface", "n-surface") in pairs and ("n-on-surface", "n-background") in pairs
    assert not unf
    _, unf = derive_pairs({"ghost-on-ghost"})
    assert unf == ["ghost-on-ghost"]

    # End-to-end: the embedded mini-bundle must gate green (positive fixture) …
    import shutil
    import tempfile
    mini = Path(__file__).resolve().parent.parent / "examples" / "mini-bundle"
    assert mini.is_dir(), f"missing fixture: {mini}"
    rep = Report()
    check_bundle(mini, rep)
    assert rep.fails == 0, [ln for ln in rep.lines if ln.startswith("[FAIL]")]
    assert any(ln.startswith("[PASS] G8") for ln in rep.lines), rep.lines
    assert any(ln.startswith("[PASS] G9") for ln in rep.lines), rep.lines
    # … and a mutated copy must gate red (negative control: F1 constant-white
    # dark on-color -> G1+G3; a dropped colorsDark key -> G2).
    with tempfile.TemporaryDirectory() as td:
        broken = Path(td) / "broken"
        shutil.copytree(mini, broken)
        dp = broken / "DESIGN.md"
        dp.write_text(dp.read_text(encoding="utf-8").replace(
            'primary-on-primary-dark: "oklch(0.18 0 0)"',
            'primary-on-primary-dark: "oklch(1 0 0)"'), encoding="utf-8")
        tp = broken / "tokens.json"
        d = json.loads(tp.read_text(encoding="utf-8"))
        del d["colorsDark"]["neutral-surface"]
        tp.write_text(json.dumps(d), encoding="utf-8")
        rep2 = Report()
        check_bundle(broken, rep2)
        text = "\n".join(rep2.lines)
        assert rep2.fails >= 3, text
        for gate in ("G1 dark", "G2", "G3"):
            assert f"[FAIL] {gate}" in text, f"{gate} did not fire:\n{text}"
    # … kit-fidelity disclosure: a README disclosure flips sub-4.5 pairs to DISCLOSED, but the
    # count must be EXACT — a stale/wrong count is itself a FAIL (negative control below).
    with tempfile.TemporaryDirectory() as td:
        disc = Path(td) / "disclosed"
        shutil.copytree(mini, disc)
        (disc / "README.md").write_text(
            "- \U0001F7E1 Contrast measured: 5 derivable fill/on-pair(s) below 4.5:1 under the "
            "kit's `onColorMode: fixed` \u2014 accepted brand override (ADR-003).\n",
            encoding="utf-8")
        rep3 = Report()
        check_bundle(disc, rep3)
        text3 = "\n".join(rep3.lines)
        # the mini fixture measures 0 misses; disclosing 5 must FAIL count-exactness
        assert "[FAIL] G1 receipt discloses 5" in text3, text3
        # correct the count to the measurement (0) -> green again, count-exact PASS cited
        (disc / "README.md").write_text(
            "- \U0001F7E1 Contrast measured: 0 derivable fill/on-pair(s) below 4.5:1 under the "
            "kit's `onColorMode: fixed` \u2014 accepted brand override (ADR-003).\n",
            encoding="utf-8")
        rep4 = Report()
        check_bundle(disc, rep4)
        assert rep4.fails == 0, [ln for ln in rep4.lines if ln.startswith("[FAIL]")]
        assert any("disclosure count-exact" in ln for ln in rep4.lines), rep4.lines
    # … and a px-leading copy must trip G8 in every carrier (negative control:
    # frontmatter lineHeight px; tokens.json lineHeight 24 — a px length, not a
    # factor; preview inline line-height px).
    with tempfile.TemporaryDirectory() as td:
        pxb = Path(td) / "px-leading"
        shutil.copytree(mini, pxb)
        dp = pxb / "DESIGN.md"
        dp.write_text(dp.read_text(encoding="utf-8").replace(
            "lineHeight: 1.143", "lineHeight: 24px"), encoding="utf-8")
        tp = pxb / "tokens.json"
        d = json.loads(tp.read_text(encoding="utf-8"))
        d["type"]["scale"]["body-md"]["lineHeight"] = 24
        tp.write_text(json.dumps(d), encoding="utf-8")
        cp = pxb / "components" / "button.html"
        cp.write_text(cp.read_text(encoding="utf-8").replace(
            "line-height:1.5", "line-height:24px"), encoding="utf-8")
        rep3 = Report()
        check_bundle(pxb, rep3)
        g8 = [ln for ln in rep3.lines if ln.startswith("[FAIL] G8")]
        assert g8, "G8 did not fire:\n" + "\n".join(rep3.lines)
        for frag in ("frontmatter lineHeight", "type.scale.body-md.lineHeight",
                     "button.html"):
            assert frag in g8[0], g8[0]
    # … and a second, differently-padded pill must trip G9 (negative control:
    # the exact "inconsistent, not off-scale" failure mode the gate exists for).
    with tempfile.TemporaryDirectory() as td:
        pillb = Path(td) / "pill-inconsistent"
        shutil.copytree(mini, pillb)
        cp = pillb / "components" / "button.html"
        cp.write_text(cp.read_text(encoding="utf-8").replace(
            '<span class="chip">TAG</span>',
            '<span class="chip">TAG</span>'
            '<span style="border-radius:9999px;padding:4px 10px">TAG2</span>'),
            encoding="utf-8")
        rep4 = Report()
        check_bundle(pillb, rep4)
        g9 = [ln for ln in rep4.lines if ln.startswith("[FAIL] G9")]
        assert g9, "G9 did not fire on an inconsistent pill:\n" + "\n".join(rep4.lines)
        for frag in ("2px 8px", "4px 10px"):
            assert frag in g9[0], g9[0]
    print("selftest: all assertions passed "
          "(color math + pairing + fixture green + negative controls red)")


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[1] in ("--selftest", "selftest"):
        selftest()
        return 0
    rep = Report()
    check_bundle(argv[1], rep)
    print(f"== bundle_gates: {argv[1]} ==")
    for line in rep.lines:
        print(line)
    print(f"-- {rep.fails} FAIL, {rep.warns} WARN, {rep.disclosed} DISCLOSED --")
    return 0 if rep.fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
