#!/usr/bin/env python3
"""css_build.py — the make-artifact token->CSS build mechanism. Self-contained (stdlib only).

Token consumption is DETERMINISTIC DERIVATION, not judgment (artifact-rules'
design-system-consumption.md describes the mapping; this script IS the check — script-writing-
rules' mechanization test). Accepts JSON in EITHER of a design system's two legal shapes and
normalizes both into one internal role -> value model before emitting CSS:

  tokens shape       — `colors`/`colorsDark` two parallel flat objects (role -> bare oklch
                       string); `type.scale` (role -> {size, lineHeight, weight, letterSpacing?},
                       bare numbers); `type.fonts` (category -> family name); `spacing` a flat
                       ordered array of 10 numbers; `radii` an object of 7 named numbers.
  frontmatter shape  — a DESIGN.md's extracted YAML frontmatter, already turned to JSON by the
                       invoking session (stdlib ships no YAML parser — script-writing-rules'
                       stdlib-only constraint, a stated mechanical step, never a judgment one):
                       ONE flat `colors` map with `-dark`-suffixed sibling keys; `typography`
                       (role -> {fontFamily, fontSize, fontWeight, lineHeight, letterSpacing?},
                       CSS-flavored strings); `spacing`/`rounded` objects of named px strings.

Emission (Resolution 6, lld-0013): `:root { color-scheme: light dark; --c-<role>:
light-dark(<light>, <dark>); ... }` plus `[data-theme="light|dark"]` one-line toggles (never a
duplicated variable block); `--text-<role>-{size,weight,lh,ls}` per type role; `--font-<slug>`
per distinct font family, ALWAYS with a system-fallback tail (sans-serif or monospace, chosen by
whether the family name contains "mono", case-insensitive — never invented per family); `--space-
<name>` / `--r-<name>` for the spacing/radii scales; a fixed mermaid re-theme block
(`!important` overrides bound to the same `--c-*` roles, referencing artifact-rules' Adia neutral
family names — the first-citizen system).

Judgment stays with the model (make-artifact's SKILL.md): choosing the page shell, assembling
content, the human render-fidelity check. This script never chooses a shell or writes prose — it
turns tokens into custom properties, nothing else.

A role present in one color representation but missing its dark counterpart is a build failure
(exit 1), never a silent light-only variable (R-2, lld-0013) — the negative control below proves
it bites; a complete fixture builds clean with every expected pair present (the reverse control).

  python3 scripts/css_build.py selftest
  python3 scripts/css_build.py tokens.json --out page.css
  python3 scripts/css_build.py normalized-design-frontmatter.json

Exit codes: 0 clean build (or selftest pass) · 1 a normalization finding (missing dark
counterpart, scale-count mismatch, no recognizable color shape) · 2 usage error (no args, unknown
flag, unreadable/non-JSON input file) — stdlib-only, no runtime dependency to tri-state-skip on.
Python 3.8+.
"""
import contextlib
import io
import json
import os
import sys

# Canonical scale name orders (DESIGN.md's own spacing/rounded keys; tokens.json's `spacing` array
# is positional against this same list — verified against the Adia source, 2026-08-17).
SPACING_NAMES = ["none", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl", "5xl"]
RADII_NAMES = ["none", "xs", "sm", "md", "lg", "xl", "full"]

SANS_FALLBACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO_FALLBACK = "ui-monospace, 'SF Mono', monospace"


class NormalizeError(ValueError):
    """A content-shaped build failure (exit 1) — never a usage error (exit 2)."""


# --- parsing helpers -------------------------------------------------------------------------

def parse_px(v):
    """Numbers pass through; a 'NNpx' string strips its unit. Returns a float."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s.endswith("px"):
        s = s[:-2]
    return float(s)


def parse_em_factor(v):
    """Numbers (a bare em factor) pass through; an 'Xem' string strips its unit."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if s.endswith("em"):
        s = s[:-2]
    return float(s)


def slugify(name):
    """'GT America Mono' -> 'gt-america-mono'. Deterministic derivation, not a semantic mapping —
    the property name is a function of the literal family string, nothing else."""
    out, prev_dash = [], False
    for ch in name.strip().lower():
        if ch.isalnum():
            out.append(ch)
            prev_dash = False
        elif not prev_dash:
            out.append("-")
            prev_dash = True
    return "".join(out).strip("-") or "font"


def fmt_px(v):
    return "%dpx" % int(v) if float(v).is_integer() else "%gpx" % v


def fmt_num(v):
    return "%d" % int(v) if float(v).is_integer() else "%g" % v


def order_named(d, canon):
    """Return [(name, value), ...] in `canon` order first, then any extra keys in insertion
    order — never drops a key the input actually carries, never invents one it didn't."""
    out = [(name, d[name]) for name in canon if name in d]
    extra = [(name, val) for name, val in d.items() if name not in canon]
    return out + extra


# --- shape detection + per-section normalizers -----------------------------------------------

def detect_shape(data):
    if not isinstance(data, dict):
        raise ValueError("input JSON must be an object at the top level")
    if "colorsDark" in data:
        return "tokens"
    if "colors" in data:
        return "frontmatter"
    raise NormalizeError(
        "no recognizable color shape: expected either 'colors'+'colorsDark' (tokens.json) or a "
        "single 'colors' map with '-dark'-suffixed siblings (DESIGN.md frontmatter, extracted to "
        "JSON) — neither found")


def normalize_colors(data, shape):
    roles = {}
    missing = []
    if shape == "tokens":
        light = data.get("colors", {}) or {}
        dark = data.get("colorsDark", {}) or {}
        for role in sorted(set(light) | set(dark)):
            if role not in light or role not in dark:
                missing.append(role)
                continue
            roles[role] = (light[role], dark[role])
    else:
        flat = data.get("colors", {}) or {}
        base_roles = sorted(k for k in flat if not k.endswith("-dark"))
        for role in base_roles:
            dark_key = role + "-dark"
            if dark_key not in flat:
                missing.append(role)
                continue
            roles[role] = (flat[role], flat[dark_key])
    if missing:
        raise NormalizeError(
            "color role(s) missing their dark counterpart: %s" % ", ".join(missing))
    if not roles:
        raise NormalizeError("no color roles found at all")
    return roles


def normalize_type(data, shape):
    """Returns (type_roles, fonts) — type_roles: role -> {size, lh, weight, ls}; fonts:
    slug -> family name (deduplicated by the literal family string, both shapes)."""
    type_roles = {}
    fonts = {}
    if shape == "tokens":
        scale = ((data.get("type") or {}).get("scale")) or {}
        for role, spec in scale.items():
            ls = spec.get("letterSpacing")
            type_roles[role] = {
                "size": parse_px(spec["size"]) if "size" in spec else None,
                "lh": float(spec["lineHeight"]) if "lineHeight" in spec else None,
                "weight": spec.get("weight"),
                "ls": parse_em_factor(ls) if ls is not None else None,
            }
        fonts_map = ((data.get("type") or {}).get("fonts")) or {}
        for family in fonts_map.values():
            fonts[slugify(family)] = family
    else:
        typography = data.get("typography") or {}
        for role, spec in typography.items():
            ls = spec.get("letterSpacing")
            type_roles[role] = {
                "size": parse_px(spec["fontSize"]) if "fontSize" in spec else None,
                "lh": float(spec["lineHeight"]) if "lineHeight" in spec else None,
                "weight": spec.get("fontWeight"),
                "ls": parse_em_factor(ls) if ls is not None else None,
            }
            family = spec.get("fontFamily")
            if family:
                fonts[slugify(family)] = family
    return type_roles, fonts


def normalize_spacing(data, shape):
    if shape == "tokens":
        raw = data.get("spacing")
        if raw is None:
            return []
        if not isinstance(raw, list):
            raise NormalizeError("tokens shape 'spacing' must be an array (got %s)" % type(raw).__name__)
        if len(raw) != len(SPACING_NAMES):
            raise NormalizeError(
                "spacing array has %d entries, expected %d (%s) — a scale-count mismatch, "
                "the R-2 input-shape-drift case" % (len(raw), len(SPACING_NAMES), ", ".join(SPACING_NAMES)))
        return list(zip(SPACING_NAMES, (parse_px(v) for v in raw)))
    raw = data.get("spacing") or {}
    return [(name, parse_px(v)) for name, v in order_named(raw, SPACING_NAMES)]


def normalize_radii(data, shape):
    raw = data.get("radii") if shape == "tokens" else data.get("rounded")
    raw = raw or {}
    return [(name, parse_px(v)) for name, v in order_named(raw, RADII_NAMES)]


def normalize(data):
    shape = detect_shape(data)
    colors = normalize_colors(data, shape)
    type_roles, fonts = normalize_type(data, shape)
    spacing = normalize_spacing(data, shape)
    radii = normalize_radii(data, shape)
    return {"shape": shape, "colors": colors, "type_roles": type_roles, "fonts": fonts,
            "spacing": spacing, "radii": radii}


# --- CSS emission ------------------------------------------------------------------------------

MERMAID_REHEME_BLOCK = """
/* Mermaid house re-theme (artifact-rules/references/mermaid-style.md): the rendered SVG ships
   its own inline styles, so re-theming requires token-driven !important overrides bound to the
   same --c-* roles as the rest of the page — one mechanism, both schemes. */
.mermaid svg .node rect,
.mermaid svg .node circle,
.mermaid svg .node polygon {
  fill: var(--c-neutral-surface) !important;
  stroke: var(--c-neutral-outline-variant) !important;
}
.mermaid svg .node text,
.mermaid svg .nodeLabel {
  fill: var(--c-neutral-on-surface) !important;
  color: var(--c-neutral-on-surface) !important;
}
.mermaid svg .edgePath .path,
.mermaid svg .flowchart-link {
  stroke: var(--c-neutral-outline-variant) !important;
}
.mermaid svg .edgeLabel {
  background-color: var(--c-neutral-surface) !important;
  color: var(--c-neutral-on-surface-variant) !important;
}

/* Width-preserving hidden-tab-panel technique (mermaid-style.md): never display:none a panel
   holding a mermaid diagram -- it corrupts the measured container permanently, even after the
   tab is shown again. */
[data-tab-panel][hidden] {
  visibility: hidden;
  position: absolute;
  inset: 0;
  pointer-events: none;
}
""".strip("\n")


def build_css(norm):
    lines = ["/* Generated by make-artifact's css_build.py (docs plugin) — do not hand-edit. */",
             "", ":root {", "  color-scheme: light dark;"]
    for role in sorted(norm["colors"]):
        light, dark = norm["colors"][role]
        lines.append("  --c-%s: light-dark(%s, %s);" % (role, light, dark))
    for role in sorted(norm["type_roles"]):
        spec = norm["type_roles"][role]
        if spec["size"] is not None:
            lines.append("  --text-%s-size: %s;" % (role, fmt_px(spec["size"])))
        if spec["weight"] is not None:
            lines.append("  --text-%s-weight: %s;" % (role, fmt_num(spec["weight"])))
        if spec["lh"] is not None:
            lines.append("  --text-%s-lh: %s;" % (role, fmt_num(spec["lh"])))
        if spec["ls"] is not None:
            lines.append("  --text-%s-ls: %sem;" % (role, fmt_num(spec["ls"])))
    for slug in sorted(norm["fonts"]):
        family = norm["fonts"][slug]
        fallback = MONO_FALLBACK if "mono" in slug else SANS_FALLBACK
        lines.append("  --font-%s: '%s', %s;" % (slug, family, fallback))
    for name, value in norm["spacing"]:
        lines.append("  --space-%s: %s;" % (name, fmt_px(value)))
    for name, value in norm["radii"]:
        lines.append("  --r-%s: %s;" % (name, fmt_px(value)))
    lines.append("}")
    lines.append("")
    lines.append('[data-theme="light"] { color-scheme: light; }')
    lines.append('[data-theme="dark"] { color-scheme: dark; }')
    lines.append("")
    lines.append(MERMAID_REHEME_BLOCK)
    return "\n".join(lines) + "\n"


def build(data):
    norm = normalize(data)
    css = build_css(norm)
    return norm, css


# --- selftest fixtures ---------------------------------------------------------------------------

FIXTURE_TOKENS = {
    "colors": {
        "primary": "oklch(0.5837 0.1265 236.48)",
        "primary-on-primary": "oklch(1 0 0)",
        "neutral-surface": "oklch(0.9335 0.0017 247.84)",
        "neutral-on-surface": "oklch(0.1776 0 0)",
    },
    "colorsDark": {
        "primary": "oklch(0.6716 0.1414 234.43)",
        "primary-on-primary": "oklch(1 0 0)",
        "neutral-surface": "oklch(0.2597 0.0024 247.92)",
        "neutral-on-surface": "oklch(1 0 0)",
    },
    "type": {
        "fonts": {"display": "GT America", "heading": "GT America", "mono": "GT America Mono"},
        "scale": {
            "display-sm": {"size": 72, "lineHeight": 0.806, "weight": 700, "letterSpacing": -0.02},
            "body-md": {"size": 16, "lineHeight": 1.5, "weight": 440},
        },
    },
    "spacing": [0, 4, 8, 12, 16, 24, 32, 48, 64, 96],
    "radii": {"none": 0, "xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 28, "full": 9999},
}

FIXTURE_FRONTMATTER = {
    "colors": {
        "primary": "oklch(0.5837 0.1265 236.48)",
        "primary-dark": "oklch(0.6716 0.1414 234.43)",
        "primary-on-primary": "oklch(1 0 0)",
        "primary-on-primary-dark": "oklch(1 0 0)",
        "neutral-surface": "oklch(0.9335 0.0017 247.84)",
        "neutral-surface-dark": "oklch(0.2597 0.0024 247.92)",
        "neutral-on-surface": "oklch(0.1776 0 0)",
        "neutral-on-surface-dark": "oklch(1 0 0)",
    },
    "typography": {
        "display-sm": {"fontFamily": "GT America", "fontSize": "72px", "fontWeight": 700,
                       "lineHeight": 0.806, "letterSpacing": "-0.02em"},
        "body-md": {"fontFamily": "GT America", "fontSize": "16px", "fontWeight": 440,
                    "lineHeight": 1.5},
        "kicker-md": {"fontFamily": "GT America Mono", "fontSize": "13px", "fontWeight": 500,
                      "lineHeight": 1.385, "letterSpacing": "0.14em"},
    },
    "spacing": {"none": "0px", "xs": "4px", "sm": "8px", "md": "12px", "lg": "16px", "xl": "24px",
                "2xl": "32px", "3xl": "48px", "4xl": "64px", "5xl": "96px"},
    "rounded": {"none": "0px", "xs": "4px", "sm": "8px", "md": "12px", "lg": "16px", "xl": "28px",
                "full": "9999px"},
}


def _fixture(base, mutate=None):
    data = json.loads(json.dumps(base))  # deep copy, stdlib-only
    if mutate:
        mutate(data)
    return data


def selftest():
    errs = []

    # 1. reverse control — a complete tokens-shape fixture builds clean with every expected pair
    norm, css = build(FIXTURE_TOKENS)
    if norm["shape"] != "tokens":
        errs.append("tokens fixture must detect shape 'tokens', got %r" % norm["shape"])
    if "--c-primary: light-dark(oklch(0.5837 0.1265 236.48), oklch(0.6716 0.1414 234.43));" not in css:
        errs.append("tokens build missing the expected --c-primary light-dark() pair")
    if "--space-none: 0px;" not in css or "--space-5xl: 96px;" not in css:
        errs.append("tokens build missing expected --space-none/--space-5xl values")
    if "--r-full: 9999px;" not in css or "--r-none: 0px;" not in css:
        errs.append("tokens build missing expected --r-full/--r-none values")
    if ":root {" not in css or "color-scheme: light dark;" not in css:
        errs.append("tokens build missing the :root color-scheme declaration")
    if '[data-theme="light"] { color-scheme: light; }' not in css:
        errs.append("tokens build missing the [data-theme=light] toggle rule")
    if "--text-display-sm-size: 72px;" not in css or "--text-display-sm-ls: -0.02em;" not in css:
        errs.append("tokens build missing expected type-role custom properties")
    if ".mermaid svg" not in css or "[data-tab-panel][hidden]" not in css:
        errs.append("tokens build missing the mermaid re-theme / tab-panel-hiding block")

    # 2. the SAME fixture's facts, reached through the OTHER representation, must normalize
    #    to the equivalent role set (both color representations handled — Resolution 6)
    norm2, css2 = build(FIXTURE_FRONTMATTER)
    if norm2["shape"] != "frontmatter":
        errs.append("frontmatter fixture must detect shape 'frontmatter', got %r" % norm2["shape"])
    if set(norm["colors"]) != set(norm2["colors"]):
        errs.append("tokens vs frontmatter fixtures normalized to different role sets: %s vs %s"
                    % (sorted(norm["colors"]), sorted(norm2["colors"])))
    if norm["colors"]["primary"] != norm2["colors"]["primary"]:
        errs.append("tokens vs frontmatter fixtures disagree on the primary role's (light, dark) pair")
    if "--space-lg: 16px;" not in css2 or "--r-xl: 28px;" not in css2:
        errs.append("frontmatter build missing expected --space-lg/--r-xl values")
    if "--text-kicker-md-ls: 0.14em;" not in css2:
        errs.append("frontmatter build missing expected letterSpacing-bearing type role")

    # 3. font fallback invariant — EVERY emitted --font-* line carries a system fallback tail;
    #    a mono-named family gets the monospace stack, everything else the sans-serif stack
    font_lines = [ln for ln in css2.splitlines() if ln.strip().startswith("--font-")]
    if len(font_lines) < 2:
        errs.append("expected at least 2 distinct --font-* lines (GT America + GT America Mono)")
    for ln in font_lines:
        if not (ln.rstrip(";").endswith(SANS_FALLBACK) or ln.rstrip(";").endswith(MONO_FALLBACK)):
            errs.append("a --font-* line shipped without its system-fallback tail: %r" % ln)
    mono_line = next((ln for ln in font_lines if "mono" in ln), None)
    if mono_line is None or not mono_line.rstrip(";").endswith(MONO_FALLBACK):
        errs.append("the 'GT America Mono' family must resolve to the monospace fallback stack")
    sans_line = next((ln for ln in font_lines if "mono" not in ln), None)
    if sans_line is None or not sans_line.rstrip(";").endswith(SANS_FALLBACK):
        errs.append("the 'GT America' family must resolve to the sans-serif fallback stack")
    # Literal-string checks alongside the constant-based ones above — a regression INSIDE
    # SANS_FALLBACK/MONO_FALLBACK themselves (e.g. hollowed to a bare "serif") would pass the
    # constant-comparison asserts above unnoticed; these anchor to actual expected substrings so
    # the fallback stacks' own content is under test, not just their presence.
    if mono_line is not None and "ui-monospace" not in mono_line:
        errs.append("mono font-fallback tail must literally contain 'ui-monospace': %r" % mono_line)
    if sans_line is not None and not sans_line.rstrip(";").endswith(", sans-serif"):
        errs.append("sans font-fallback tail must literally end with ', sans-serif': %r" % sans_line)

    # 4. NEGATIVE CONTROL — a role missing its dark counterpart must bite (exit 1 at the CLI
    #    layer; a NormalizeError naming the role at the function layer)
    def _drop_dark(d):
        del d["colorsDark"]["neutral-on-surface"]
    broken = _fixture(FIXTURE_TOKENS, _drop_dark)
    try:
        normalize(broken)
        errs.append("a color role missing its dark counterpart must raise NormalizeError")
    except NormalizeError as e:
        if "neutral-on-surface" not in str(e):
            errs.append("the missing-dark-counterpart error must name the role: %s" % e)

    def _drop_dark_fm(d):
        del d["colors"]["primary-dark"]
    broken_fm = _fixture(FIXTURE_FRONTMATTER, _drop_dark_fm)
    try:
        normalize(broken_fm)
        errs.append("(frontmatter shape) a role missing its -dark sibling must raise NormalizeError")
    except NormalizeError as e:
        if "primary" not in str(e):
            errs.append("(frontmatter shape) the missing-dark-counterpart error must name the role: %s" % e)

    # 5. NEGATIVE CONTROL — a scale-count mismatch (R-2 input-shape drift) must bite
    def _short_spacing(d):
        d["spacing"] = d["spacing"][:-1]
    broken_spacing = _fixture(FIXTURE_TOKENS, _short_spacing)
    try:
        normalize(broken_spacing)
        errs.append("a 9-entry spacing array (expected 10) must raise NormalizeError")
    except NormalizeError as e:
        if "10" not in str(e):
            errs.append("the spacing-count-mismatch error must name the expected count: %s" % e)

    # 6. NEGATIVE CONTROL — no recognizable color shape at all
    try:
        normalize({"spacing": [0, 4, 8, 12, 16, 24, 32, 48, 64, 96]})
        errs.append("input with no 'colors' key at all must raise NormalizeError")
    except NormalizeError:
        pass

    # 7. CLI-layer exit codes AND the verdict-line-first contract, exercised through main()
    #    directly (no subprocess needed) — stdout/stderr captured so the selftest's OWN report
    #    stays a clean single verdict line, not a transcript of every sub-invocation it drives.
    def _run_main(args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = main(args)
        return code, out.getvalue(), err.getvalue()

    code, out, _ = _run_main([])
    if code != 2:
        errs.append("no args must exit 2 (usage: print __doc__)")
    if "css_build.py" not in out:
        errs.append("no-args invocation must print the module docstring")

    code, _, err = _run_main(["--bogus-flag"])
    if code != 2 or "unknown flag" not in err:
        errs.append("an unknown flag must exit 2 with a named reason")

    code, _, err = _run_main(["/no/such/file-css-build-selftest.json"])
    if code != 2:
        errs.append("an unreadable input file must exit 2 (usage error, not a content finding)")

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        good_path = os.path.join(td, "tokens.json")
        with open(good_path, "w", encoding="utf-8") as f:
            json.dump(FIXTURE_TOKENS, f)
        out_path = os.path.join(td, "page.css")
        code, out, _ = _run_main([good_path, "--out", out_path])
        if code != 0:
            errs.append("a complete fixture file via the CLI must exit 0")
        elif not out.splitlines() or out.splitlines()[0] != "css_build · ok · 0 fail":
            errs.append("a clean build's verdict line must be first and read "
                        "'css_build · ok · 0 fail', got: %r" % out)
        elif not os.path.isfile(out_path):
            errs.append("--out must write the CSS file")
        else:
            with open(out_path, encoding="utf-8") as f:
                if "--c-primary: light-dark(" not in f.read():
                    errs.append("--out file must contain the built CSS")

        bad_path = os.path.join(td, "broken.json")
        with open(bad_path, "w", encoding="utf-8") as f:
            json.dump(broken, f)
        code, out, err = _run_main([bad_path])
        if code != 1:
            errs.append("a content-level normalization failure via the CLI must exit 1")
        elif out.strip() != "css_build · fail · 1 fail":
            errs.append("a failed build's verdict line must read 'css_build · fail · 1 fail', "
                        "got: %r" % out)
        if "neutral-on-surface" not in err:
            errs.append("the CLI failure path must report the missing role by name on stderr")

        notjson_path = os.path.join(td, "not-json.txt")
        with open(notjson_path, "w", encoding="utf-8") as f:
            f.write("not json at all {{{")
        code, _, _ = _run_main([notjson_path])
        if code != 2:
            errs.append("an unparseable JSON file must exit 2 (usage error)")

    return errs


# --- CLI -----------------------------------------------------------------------------------------

def main(argv):
    if not argv:
        sys.stdout.write(__doc__ + "\n")
        return 2
    if argv == ["selftest"]:
        errs = selftest()
        if errs:
            print("css_build · fail · %d fail" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("css_build · ok · 0 fail")
        return 0

    path, out_path = None, None
    args = list(argv)
    while args:
        arg = args.pop(0)
        if arg == "--out":
            if not args:
                sys.stderr.write("css_build: --out needs a path\n")
                return 2
            out_path = args.pop(0)
        elif arg.startswith("--"):
            sys.stderr.write("css_build: unknown flag %r\n" % arg)
            sys.stderr.write("usage: css_build.py <tokens.json|normalized-design-frontmatter.json> "
                              "[--out page.css] | selftest\n")
            return 2
        elif path is None:
            path = arg
        else:
            sys.stderr.write("css_build: unexpected extra argument %r\n" % arg)
            return 2

    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        sys.stderr.write("css_build · usage-error · %s\n" % e)
        return 2

    try:
        _, css = build(data)
    except NormalizeError as e:
        print("css_build · fail · 1 fail")
        sys.stderr.write("  - %s\n" % e)
        return 1
    except ValueError as e:
        # a malformed (non-object, non-numeric-where-expected) input is a usage error, not a
        # content finding — distinct from NormalizeError's content-shaped failures above.
        sys.stderr.write("css_build · usage-error · %s\n" % e)
        return 2

    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(css)
        except OSError as e:
            sys.stderr.write("css_build: --out write failed: %s\n" % e)
            return 2
        print("css_build · ok · 0 fail")
    else:
        print("css_build · ok · 0 fail")
        print(css)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
