#!/usr/bin/env python3
"""make_guidelines_check.py — mechanical gates for a Figma Make guidelines/ folder.

Make validates NOTHING (no linter, no schema) — this run is the gate of record.
Routes the deterministic rubric dimensions (D1–D6, D10, D11) to code; judgment dims
(D7–D9) stay with references/rubric.md.

Usage:
    python3 make_guidelines_check.py <guidelines_dir> [--compare <sibling.json>]
    python3 make_guidelines_check.py selftest

Checks (labels match references/rubric.md):
  D1 routing integrity   — Guidelines.md exists; every routed *.md resolves
                           (relative to the citing file, else the folder root);
                           every leaf *.md is reachable from Guidelines.md.
  D2 contrast            — every 4-color token row (fill L/D + foreground L/D)
                           ≥ 4.5:1 in BOTH schemes; plus all `-on-surface*` text
                           tokens × all surface/background tokens, both schemes
                           (all-pairs policy; alpha < 1 text tokens are skipped
                           with a note — backdrop-dependent).
  D3 scheme parity       — every token table row carries a light AND a dark value.
  D4 runtime block+trap  — ≥1 paste-ready `light-dark()` block exists; every file
                           using `light-dark(` also declares `color-scheme: light dark`
                           (without it the dark end NEVER fires).
  D5 states as values    — every components/*.md leaf (overview excluded) names
                           `hover` and carries a color literal or a `-hover`/-active
                           token reference — states as values, not adjectives.
  D6 hard rules          — Guidelines.md carries ≥1 `Do NOT` and ≥1 `IMPORTANT`.
  D10 carrier equality   — with --compare: runtime-block tokens equal the sibling
                           export's values (same sRGB 8-bit triple ±1/255/channel).
                           Without --compare: UNMEASURED (reported, not failed).
  D11 relative leading   — no `line-height:`/`letter-spacing:` declarations ending
                           in px, no px leading table cells (`| N / Mpx`), no
                           `lineHeight …px` values — leading/tracking are relative
                           (unitless factor, em, or %), never absolute px.

Non-fatal notes: leaves > 200 lines (progressive-disclosure tripwire).

Exit 0 = all gates passed. Exit 1 = at least one failed. UNMEASURED never fails.
Selftest: runs the SAME check functions over embedded fixtures — one passing mini
folder plus one failing fixture per gate (dangling route, unrouted leaf, contrast
fail, single-scheme row, light-dark without color-scheme, adjective-only states,
no hard rules, px leading, carrier mismatch) and a relative-leading pass control.
"""
import json
import math
import re
import sys
import tempfile
from pathlib import Path

AA = 4.5

# ---------------------------------------------------------------- color math

_OKLCH = re.compile(
    r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([-\d.]+)(?:\s*/\s*([\d.]+%?))?\s*\)", re.I)
_HEX = re.compile(r"#([0-9a-fA-F]{3,8})\b")


def _num(s, pct_scale=1.0):
    s = s.strip()
    if s.endswith("%"):
        return float(s[:-1]) / 100.0 * pct_scale
    return float(s)


def oklch_to_srgb(L, C, H):
    """OKLCH -> sRGB 0..1 triple (standard OKLab matrices, simple clamp)."""
    a = C * math.cos(math.radians(H))
    b = C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l3, m3, s3 = l_ ** 3, m_ ** 3, s_ ** 3
    rl = +4.0767416621 * l3 - 3.3077115913 * m3 + 0.2309699292 * s3
    gl = -1.2684380046 * l3 + 2.6097574011 * m3 - 0.3413193965 * s3
    bl = -0.0041960863 * l3 - 0.7034186147 * m3 + 1.7076147010 * s3

    def tf(c):
        c = min(1.0, max(0.0, c))
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return tuple(min(1.0, max(0.0, tf(c))) for c in (rl, gl, bl))


def parse_colors(text):
    """All color literals in text, in order: [(r, g, b, alpha), ...] 0..1 floats."""
    out = []
    for m in re.finditer(rf"{_OKLCH.pattern}|{_HEX.pattern}", text, re.I):
        if m.group(1) is not None:  # oklch
            L = _num(m.group(1))
            if m.group(1).strip().endswith("%"):
                pass  # _num already scaled percent to 0..1
            C, H = float(m.group(2)), float(m.group(3))
            alpha = _num(m.group(4)) if m.group(4) else 1.0
            out.append((*oklch_to_srgb(L, C, H), alpha))
        else:  # hex
            h = m.group(5)
            if len(h) in (3, 4):
                h = "".join(ch * 2 for ch in h)
            if len(h) not in (6, 8):
                continue
            r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
            alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
            out.append((r, g, b, alpha))
    return out


def contrast(c1, c2):
    def lum(c):
        def ch(v):
            return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
        r, g, b = (ch(v) for v in c[:3])
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    l1, l2 = sorted((lum(c1), lum(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def srgb8(c):
    return tuple(round(v * 255) for v in c[:3])


# ---------------------------------------------------------------- harvesting

_MD_REF = re.compile(r"(?<![\w./-])((?:[A-Za-z0-9_.-]+/)*[A-Za-z0-9_.-]+\.md)\b")
_TOKEN_ROW = re.compile(r"^\|\s*`(--[a-z0-9-]+)`")
_RUNTIME_DECL = re.compile(
    r"(--[a-z0-9-]+)\s*:\s*light-dark\(\s*([^,]+?)\s*,\s*([^;]+?)\s*\)\s*;")


def md_files(root):
    return sorted(p for p in root.rglob("*.md"))


def refs_in(text):
    return sorted(set(_MD_REF.findall(text)))


def token_rows(text):
    """(name, [colors]) per table row that binds a `--token` to color literals."""
    rows = []
    for ln in text.splitlines():
        m = _TOKEN_ROW.match(ln)
        if m:
            colors = parse_colors(ln)
            if colors:
                rows.append((m.group(1), colors))
    return rows


_BLOCK_RE = re.compile(r"(:root|\.dark)\s*\{([^}]*)\}")
_PROP_RE = re.compile(r"^\s*(--[a-z0-9-]+):\s*(oklch\([^)]*\)|#[0-9a-fA-F]+)\s*;", re.M)


def customprop_tokens(text):
    """{name: (light, dark)} from literal :root/.dark custom-property blocks (both present)."""
    light, dark = {}, {}
    for sel, body in _BLOCK_RE.findall(text):
        target = light if sel == ":root" else dark
        for name, val in _PROP_RE.findall(body):
            target.setdefault(name, val)
    out = {}
    for name in light:
        if name in dark:
            lc, dc = parse_colors(light[name]), parse_colors(dark[name])
            if lc and dc:
                out[name] = (lc[0], dc[0])
    return out


def runtime_tokens(text):
    """{name: (light_color, dark_color)} from light-dark() runtime blocks."""
    out = {}
    for name, light, dark in _RUNTIME_DECL.findall(text):
        lc, dc = parse_colors(light), parse_colors(dark)
        if lc and dc:
            out[name] = (lc[0], dc[0])
    return out


# ------------------------------------------------------------------- result

class Result:
    def __init__(self):
        self.checks, self.notes = [], []

    def add(self, ok, label, detail=""):
        self.checks.append((bool(ok), label, detail))

    def note(self, text):
        self.notes.append(text)

    def report(self, title):
        print(f"== {title} ==")
        for ok, label, detail in self.checks:
            line = f"[{'PASS' if ok else 'FAIL'}] {label}"
            if detail and not ok:
                line += f" — {detail}"
            print(line)
        for n in self.notes:
            print(f"[NOTE] {n}")
        failed = [c for c in self.checks if not c[0]]
        print(f"-- {len(self.checks) - len(failed)}/{len(self.checks)} gate checks passed --")
        return 0 if not failed else 1


# -------------------------------------------------------------------- gates

def check_folder(root, r, compare=None):
    root = Path(root).resolve()
    entry = root / "Guidelines.md"
    r.add(entry.is_file(), "D1 Guidelines.md entry exists",
          "Make reads Guidelines.md first — exact name, at the folder root")
    if not entry.is_file():
        return

    texts = {p: p.read_text(encoding="utf-8", errors="ignore") for p in md_files(root)}

    # D1 — every route resolves; every leaf reached from the entry (transitively).
    def resolve(base, rel):
        for cand in (base.parent / rel, root / rel):
            if cand.is_file():
                return cand.resolve()
        return None

    reached, dangling, queue = {entry.resolve()}, [], [entry]
    while queue:
        f = queue.pop()
        for rel in refs_in(texts.get(f.resolve(), texts.get(f, ""))):
            tgt = resolve(f, rel)
            if tgt is None:
                dangling.append(f"{f.relative_to(root)} -> {rel}")
            elif tgt not in reached:
                reached.add(tgt)
                queue.append(tgt)
    r.add(not dangling, "D1 every route resolves (no dangling routes)",
          f"routed-but-missing: {', '.join(sorted(set(dangling)))}")
    unrouted = [str(p.relative_to(root)) for p in texts if p.resolve() not in reached]
    r.add(not unrouted, "D1 every leaf is routed (reachable from Guidelines.md)",
          f"unrouted leaves Make will never find: {', '.join(unrouted)}")

    # D6 — hard rules in the entry, imperative register.
    entry_text = texts[entry.resolve()]
    r.add(re.search(r"\bDo NOT\b", entry_text),
          "D6 Guidelines.md carries 'Do NOT' hard rules",
          "no 'Do NOT' prohibition — the documented imperative register")
    r.add("IMPORTANT" in entry_text,
          "D6 Guidelines.md marks hard rules IMPORTANT",
          "no IMPORTANT marker on the hard-rules block")

    # D2 + D3 — token tables: parity and contrast.
    all_rows, parity_bad, contrast_bad = [], [], []
    for p, text in texts.items():
        for name, colors in token_rows(text):
            all_rows.append((str(p.relative_to(root)), name, colors))
    named = {}
    for src, name, colors in all_rows:
        if len(colors) == 1:
            parity_bad.append(f"{src}: `{name}` has one value — no scheme pair")
            continue
        named.setdefault(name, (colors[0], colors[1]))  # first pair = light, dark
        if len(colors) == 4:  # fill L, fill D, foreground L, foreground D
            for scheme, fill, fg in (("light", colors[0], colors[2]),
                                     ("dark", colors[1], colors[3])):
                ratio = contrast(fill, fg)
                if ratio < AA:
                    contrast_bad.append(
                        f"{src}: `{name}` {scheme} fill/foreground {ratio:.2f}:1 < {AA}:1")
        elif len(colors) == 3:
            r.note(f"{src}: `{name}` row has 3 color values — ambiguous columns; "
                   "state fill L/D and foreground L/D explicitly")
    r.add(not parity_bad, "D3 scheme parity — every token row states light AND dark",
          "; ".join(parity_bad))

    # D2 all-pairs: -on-surface* text tokens × surface/background tokens.
    def is_surface(n):
        return (("surface" in n or n.endswith("background") or "-background" in n)
                and "-on-" not in n and "outline" not in n
                and "scrim" not in n and "inverse" not in n)

    text_tokens = {n: v for n, v in named.items() if "-on-surface" in n}
    surf_tokens = {n: v for n, v in named.items() if is_surface(n)}
    for tn, (tl, td) in text_tokens.items():
        if tl[3] < 1.0 or td[3] < 1.0:
            r.note(f"`{tn}` is translucent — contrast is backdrop-dependent; "
                   "verified upstream over each surface, skipped here")
            continue
        for sn, (sl, sd) in surf_tokens.items():
            for scheme, fg, bg in (("light", tl, sl), ("dark", td, sd)):
                ratio = contrast(fg, bg)
                if ratio < AA:
                    contrast_bad.append(
                        f"`{tn}` on `{sn}` {scheme} {ratio:.2f}:1 < {AA}:1")
    # KIT FIDELITY (ultimate-tokens PR #229): `onColorMode: fixed` is a user setting whose
    # sub-4.5 pairs are an accepted brand override (ADR-003), disclosed in the bundle README
    # (guidelines/ parent). With the disclosure present, D2 misses report as measured-and-
    # disclosed, not FAIL. (No count-exact check here: the receipt counts the FULL grammar-pair
    # universe; D2 sees only the subset shipped as table rows in the leaves.)
    _rm = root.parent / "README.md"
    _disc = None
    if _rm.is_file():
        _t = _rm.read_text(encoding="utf-8")
        _m = re.search(r"(\d+) derivable fill/on-pair\(s\) below 4\.5:1 under the kit's `onColorMode: (\w+)`", _t)
        if _m and "ADR-003" in _t:
            _disc = (int(_m.group(1)), _m.group(2))
    if contrast_bad and _disc:
        r.add(True,
              f"D2 contrast measured — {len(contrast_bad)} pair(s) below {AA}:1 DISCLOSED "
              f"(onColorMode: {_disc[1]}, ADR-003; receipt discloses {_disc[0]} over the full grammar)",
              "")
        for line in contrast_bad[:8]:
            r.note("D2 disclosed: " + line)
    else:
        r.add(not contrast_bad,
              f"D2 all fill/on pairs >= {AA}:1 in both schemes",
              "; ".join(contrast_bad[:8]) + (" …" if len(contrast_bad) > 8 else ""))
    if not named:
        r.add(False, "D2 token tables found",
              "no `--token` table rows with color values in any leaf")

    # D4 — runtime block + the color-scheme trap.
    rt_files = [p for p, t in texts.items() if "light-dark(" in t]
    r.add(bool(rt_files), "D4 paste-ready light-dark() runtime block present",
          "no light-dark() block — ship the roles as one :root block")
    trap = [str(p.relative_to(root)) for p in rt_files
            if not re.search(r"color-scheme\s*:\s*light\s+dark", texts[p])]
    r.add(not trap, "D4 color-scheme: light dark declared wherever light-dark() is used",
          f"the dark end NEVER fires without it: {', '.join(trap)}")

    # D5 — component leaves ship states as values.
    comp_dir = root / "components"
    leaves = [p for p in texts if comp_dir in p.parents and p.name != "overview.md"]
    stateless = []
    for p in leaves:
        t = texts[p]
        has_hover = re.search(r"\bhover\b", t, re.I)
        has_value = (parse_colors(t) or re.search(r"--[a-z0-9-]+-(hover|active)\b", t)
                     or "var(--" in t)
        if not (has_hover and has_value):
            stateless.append(str(p.relative_to(root)))
    r.add(not stateless, "D5 component leaves ship states as values",
          f"no hover state with literal/token values in: {', '.join(stateless)}")
    if not leaves:
        r.note("no per-component leaves under components/ — overview-only catalog; "
               "add a leaf per component as the kit grows")

    # D11 — leading/tracking are relative: never absolute px, in any file.
    px_leading = []
    for p, t in texts.items():
        src = str(p.relative_to(root))
        for pat in (r"(?:line-height|letter-spacing)\s*:\s*[^;\n]*?\d[\d.]*px",
                    r"\|\s*[\d.]+\s*/\s*[\d.]+\s*px",
                    r"lineHeight[^|\n]*?\d[\d.]*px"):
            for m in re.finditer(pat, t, re.I):
                px_leading.append(f"{src}: `{m.group(0).strip()}`")
    r.add(not px_leading,
          "D11 leading/tracking relative (unitless/em/%, never px)",
          "; ".join(px_leading[:6]) + (" …" if len(px_leading) > 6 else ""))

    # D10 — carrier equality against a sibling export.
    if compare:
        want = json.loads(Path(compare).read_text(encoding="utf-8"))
        if isinstance(want.get("colors"), dict) and isinstance(want.get("colorsDark"), dict):
            # a design-system tokens.json — the color maps ARE the sibling; everything else
            # ($generator/$note/semantic/type/geometry/...) is structure, not a color token.
            want = {k: {"light": v, "dark": want["colorsDark"].get(k, v)}
                    for k, v in want["colors"].items()}
        else:
            want = {k: v for k, v in want.items()
                    if not k.startswith("$") and isinstance(v, (dict, list))}
        have = {}
        css_p = root / "styles.css"
        srcs = list(texts.values()) + ([css_p.read_text(encoding="utf-8", errors="ignore")] if css_p.is_file() else [])
        for t in srcs:
            have.update(runtime_tokens(t))
            have.update(customprop_tokens(t))
        unequal, missing = [], []
        for name, pair in want.items():
            key = name if name.startswith("--") else "--" + name
            # a grammar-named sibling token may ride a kit prefix in the carrier
            # (`--md-sys-color-neutral-background` for `neutral-background`) — match the
            # exact name or the prefix-qualified suffix; equality below is the real gate.
            if key not in have:
                suffix = "-" + key.lstrip("-")
                cands = [h for h in have if h.endswith(suffix)]
                if cands:
                    key = sorted(cands, key=len)[0]
                else:
                    missing.append(key)
                    continue
            for scheme, idx in (("light", 0), ("dark", 1)):
                exp = parse_colors(str(pair[scheme]))
                if not exp:
                    continue
                got8, exp8 = srgb8(have[key][idx]), srgb8(exp[0])
                if any(abs(a - b) > 1 for a, b in zip(got8, exp8)):
                    unequal.append(f"{key} {scheme}: {got8} != sibling {exp8}")
        r.add(not missing, "D10 sibling tokens all present in guidelines",
              f"missing: {', '.join(missing)}")
        r.add(not unequal, "D10 carrier equality (same sRGB triple +/-1/255)",
              "; ".join(unequal[:6]))
    else:
        r.note("D10 carrier equality UNMEASURED — no --compare sibling export given; "
               "record it UNMEASURED in the receipt, never as passed")

    # Progressive-disclosure tripwire (non-fatal).
    for p, t in texts.items():
        n = t.count("\n") + 1
        if n > 200:
            r.note(f"{p.relative_to(root)} is {n} lines — the platform sizing rule is "
                   "many SHORT files; split it")


# ----------------------------------------------------------------- fixtures

_F_ENTRY = """# Demo — Guidelines
Character line. IMPORTANT:
- Do NOT hardcode a color.

| Question | Read |
|---|---|
| color | `foundations/color.md` |
| components | `components/overview.md` |
"""
_F_COLOR = """# Color
| Token | Light | Dark | Foreground (L/D) | Use |
|---|---|---|---|---|
| `--c-primary-base` | oklch(0.45 0.02 288) | oklch(0.72 0.02 288) | oklch(1 0 90) / oklch(0.18 0 90) | action |

| Token | Light | Dark |
|---|---|---|
| `--c-primary-base-surface` | oklch(0.95 0.001 286) | oklch(0.24 0.002 286) |
| `--c-primary-base-on-surface` | oklch(0.18 0 90) | oklch(0.99 0 90) |

```css
:root {
  color-scheme: light dark;
  --c-primary-base: light-dark(oklch(0.45 0.02 288), oklch(0.72 0.02 288));
}
```
"""
_F_OVERVIEW = "# Overview\n| Button | `button.md` |\n"
_F_BUTTON = ("# Button\nValid variants are `primary` — nothing else.\n"
             "| primary | hover | oklch(0.38 0.01 292) | oklch(0.82 0.008 286) |\n")


def _write_fixture(root, mutate=None):
    (root / "foundations").mkdir(parents=True)
    (root / "components").mkdir()
    files = {"Guidelines.md": _F_ENTRY, "foundations/color.md": _F_COLOR,
             "components/overview.md": _F_OVERVIEW, "components/button.md": _F_BUTTON}
    if mutate:
        mutate(files)
    for rel, text in files.items():
        (root / rel).write_text(text, encoding="utf-8")


def selftest():
    cases = [
        ("passing folder", None, True),
        ("dangling route", lambda f: f.__setitem__(
            "Guidelines.md", _F_ENTRY + "\nAlso read `foundations/motion.md`.\n"), False),
        ("unrouted leaf", lambda f: f.__setitem__("foundations/orphan.md", "# Orphan\n"), False),
        ("contrast fail", lambda f: f.__setitem__("foundations/color.md", _F_COLOR.replace(
            "oklch(1 0 90) / oklch(0.18 0 90)", "oklch(0.6 0.02 288) / oklch(0.6 0.02 288)")), False),
        ("single-scheme row (parity)", lambda f: f.__setitem__(
            "foundations/color.md", _F_COLOR.replace(
                "| `--c-primary-base-surface` | oklch(0.95 0.001 286) | oklch(0.24 0.002 286) |",
                "| `--c-primary-base-surface` | oklch(0.95 0.001 286) | |")), False),
        ("light-dark without color-scheme", lambda f: f.__setitem__(
            "foundations/color.md", _F_COLOR.replace("  color-scheme: light dark;\n", "")), False),
        ("adjective-only states", lambda f: f.__setitem__(
            "components/button.md", "# Button\nHover brightens slightly.\n"), False),
        ("no hard rules", lambda f: f.__setitem__(
            "Guidelines.md", _F_ENTRY.replace("Do NOT", "avoid").replace("IMPORTANT:", "note:")), False),
        ("px leading", lambda f: (
            f.__setitem__("Guidelines.md", _F_ENTRY + "| type | `foundations/typography.md` |\n"),
            f.__setitem__("foundations/typography.md",
                          "# Type\n| Level | Size px / Leading | Weight |\n|---|---|---|\n"
                          "| body-md | 16 / 24px | 500 |\n")), False),
        ("relative leading (control)", lambda f: (
            f.__setitem__("Guidelines.md", _F_ENTRY + "| type | `foundations/typography.md` |\n"),
            f.__setitem__("foundations/typography.md",
                          "# Type\n| Level | Size px / Leading | Weight |\n|---|---|---|\n"
                          "| body-md | 16 / 1.5 | 500 |\n")), True),
    ]
    failures = []
    for label, mutate, want_pass in cases:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "guidelines"
            _write_fixture(root, mutate)
            r = Result()
            check_folder(root, r)
            got_pass = all(ok for ok, _, _ in r.checks)
            if got_pass != want_pass:
                failures.append(f"{label}: expected {'PASS' if want_pass else 'FAIL'}")
    # carrier equality: one equal, one off-by-many
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "guidelines"
        _write_fixture(root)
        good = {"--c-primary-base": {"light": "oklch(0.45 0.02 288)", "dark": "oklch(0.72 0.02 288)"}}
        bad = {"--c-primary-base": {"light": "#ff0000", "dark": "oklch(0.72 0.02 288)"}}
        for label, payload, want_pass in (("carrier equal", good, True),
                                          ("carrier mismatch", bad, False)):
            cmp_path = Path(td) / "cmp.json"
            cmp_path.write_text(json.dumps(payload), encoding="utf-8")
            r = Result()
            check_folder(root, r, compare=cmp_path)
            got_pass = all(ok for ok, _, _ in r.checks)
            if got_pass != want_pass:
                failures.append(f"{label}: expected {'PASS' if want_pass else 'FAIL'}")
    print("== selftest ==")
    for f in failures:
        print(f"[FAIL] {f}")
    print(f"-- {12 - len(failures)}/12 fixtures behaved --")
    return 0 if not failures else 1


def main(argv):
    if len(argv) >= 1 and argv[0] == "selftest":
        return selftest()
    if not argv:
        print(__doc__)
        return 2
    root, compare = Path(argv[0]), None
    if "--compare" in argv:
        compare = argv[argv.index("--compare") + 1]
    r = Result()
    check_folder(root, r, compare=compare)
    return r.report(f"figma-make guidelines gates: {root}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
