#!/usr/bin/env python3
"""artifact_check — mechanical grep-gates for Claude Artifact styling doctrine.

Usage:
  artifact_check.py <page.html|page.css> [...]   check one or more pages/stylesheets
  artifact_check.py selftest                      prove the six checks on inline fixtures

Six checks (artifact-styling-rules' rubric.md R1/R2/R4/R6/R7 mechanical half; each check name is
its own rubric citation):
  theme-block-only     colors defined only inside @media(prefers-color-scheme), no light-dark()
                        pair anywhere under :root                                        [FAIL]
  external-url         a url(http...)/@import/<link href="http..."> outside the doctrine-
                        approved CDN allowlist (cdnjs.cloudflare.com, fonts.googleapis.com)  [FAIL]
  literal-outside-root a bare hex/oklch/rgb color literal used in a rule body OUTSIDE :root,
                        instead of a var(--<short-role>) reference                        [FAIL]
  br-in-mermaid-label  a literal <br/> or <br> inside a mermaid node-label bracket ["..."]  [FAIL]
  missing-ground       no `color-scheme` declared on :root, or no body/page-root background
                        bound to a --paper/neutral-background-family token               [FAIL]
  doctrine-font-stack  a font-family on body/interactive selectors naming neither the
                        system-ui nor mono doctrine stack, with no override comment. A pure
                        var(--font-*) reference is RESOLVED to the token's own definition on the
                        page and the RESOLVED stack is judged (#684, refining #662): a token
                        resolving to a doctrine stack passes, one resolving to an off-doctrine
                        literal stack warns citing the resolved value, an unresolvable token
                        warns naming it                                                   [WARN]

Exit 0 clean, 1 on any FAIL, 2 on a usage error (no target, unreadable path). Verdict line first:
`artifact_check · <verdict> · N fail / M warn · <path>`.
"""
import re
import sys
from pathlib import Path

CDN_ALLOWLIST = ("cdnjs.cloudflare.com", "fonts.googleapis.com", "fonts.gstatic.com")

ROOT_BLOCK_RE = re.compile(r":root\s*\{([^}]*)\}", re.S)
MEDIA_SCHEME_RE = re.compile(r"@media\s*\(\s*prefers-color-scheme", re.I)
LIGHT_DARK_RE = re.compile(r"light-dark\s*\(")
URL_RE = re.compile(r"url\(\s*['\"]?(https?://[^'\")\s]+)", re.I)
IMPORT_RE = re.compile(r"@import\s+url\(\s*['\"]?(https?://[^'\")\s]+)", re.I)
LINK_HREF_RE = re.compile(r"<link[^>]+href=[\"'](https?://[^\"']+)", re.I)
COLOR_LITERAL_RE = re.compile(r"(?<![\w-])(#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|oklch\([^)]*\))")
# A CSS comment can legitimately carry a `#NNN` issue reference (this same file's own generated
# mermaid-block comments do, e.g. "#662") — the gh#660 prose-hash class, recurring INSIDE a CSS
# comment rather than HTML prose text (checker finding, #662): strip comments before the literal
# scan the same way _css_regions already strips prose.
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
MERMAID_FENCE_RE = re.compile(r"```mermaid(.*?)```", re.S)
# #681: the markdown fence above never matches the HTML-artifact-native embedding form
# (`<pre class="mermaid">...</pre>`) — the primary genre this check exists to protect, per
# artifact-styling-rules' mermaid-reference.md. Both forms are scanned in check_br_in_mermaid_label.
MERMAID_HTML_BLOCK_RE = re.compile(r'<pre\s+class="mermaid"[^>]*>(.*?)</pre>', re.S | re.I)
NODE_LABEL_BR_RE = re.compile(r"\[[^\]]*<br\s*/?>[^\]]*\]", re.I)
COLOR_SCHEME_RE = re.compile(r"color-scheme\s*:\s*light\s+dark")
# #662: css_build.py now emits the unprefixed --paper short role name only (never --c-paper /
# --c-neutral-background) — the (?:c-)? acceptance PR #661 added is redundant against fresh
# css_build output post-#662, but stays (per #662's own "harmless to keep" note) as a legacy-page
# acceptance for content built against the pre-#662 --c-paper emission.
BODY_BG_VAR_RE = re.compile(r"body\s*\{[^}]*background(?:-color)?\s*:\s*var\(--(?:(?:c-)?paper|[\w-]*background[\w-]*)\)", re.S | re.I)
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
STYLE_ATTR_RE = re.compile(r"style\s*=\s*\"([^\"]*)\"|style\s*=\s*'([^']*)'", re.I)
HTML_TAG_RE = re.compile(r"<[a-zA-Z][^>]*>")
DOCTRINE_SANS_RE = re.compile(r"system-ui")
DOCTRINE_MONO_RE = re.compile(r"ui-monospace")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;]+);")
OVERRIDE_COMMENT_RE = re.compile(r"/\*\s*override\b", re.I)
# #684 (marshal ruling 2026-08-19, refining #662 — NOT reversing it): a pure var(--font-*)
# reference is no longer trusted blindly; the check FOLLOWS the indirection. The token's own
# declaration within the page is resolved and the RESOLVED stack is judged against the doctrine
# names — a doctrine-resolving token (#662's own locked cases) still passes with zero findings,
# a token resolving to an off-doctrine literal stack (the Comic Sans case, or a source design
# system's brand face used with no override comment) warns citing the resolved value, and an
# unresolvable token warns naming it. Anchored to the WHOLE value (never a bare `.search`) — a
# mixed value like `var(--font-x), 'Comic Sans MS'` still names a literal fallback and takes the
# literal path (checker finding C, #662).
FONT_VAR_ONLY_RE = re.compile(r"^\s*var\(\s*(--font-[\w-]+)\s*\)\s*$")
# Definition-side half (checker finding C, #662): a --font-* token itself must carry the
# mandatory fallback tail — this checker has no way to know a `--font-*` custom property was
# really built by css_build.py vs. hand-authored badly, so it verifies the token's OWN
# definition directly (mirrors css_build.py's selftest invariant: every emitted --font-* value
# ends in the sans-serif or monospace system stack). #684's resolve-then-check reuses the same
# regex to build the token→value map it resolves against.
FONT_TOKEN_DEF_RE = re.compile(r"(--font-[\w-]+)\s*:\s*([^;]+);")
FONT_FALLBACK_TAIL_RE = re.compile(r"(sans-serif|monospace)\s*$")


def check_theme_block_only(text: str):
    if MEDIA_SCHEME_RE.search(text) and not LIGHT_DARK_RE.search(text):
        return [("FAIL", "theme-block-only", "colors gated behind @media(prefers-color-scheme) with no light-dark() pair under :root")]
    return []


def check_external_url(text: str):
    findings = []
    for rx in (URL_RE, IMPORT_RE, LINK_HREF_RE):
        for m in rx.finditer(text):
            url = m.group(1)
            if not any(host in url for host in CDN_ALLOWLIST):
                findings.append(("FAIL", "external-url", f"external resource outside the CDN allowlist: {url}"))
    return findings


def _css_regions(text: str):
    """CSS-only slices of the input: <style> blocks + style=\"\" attrs on an HTML
    page; the whole text when it carries no HTML tags (a bare stylesheet).
    Prose is never CSS — a GitHub issue ref like `#541` in body text is not a
    color literal (gh#660)."""
    blocks = STYLE_BLOCK_RE.findall(text)
    attrs = [a or b for a, b in STYLE_ATTR_RE.findall(text)]
    if blocks or attrs:
        return blocks + attrs
    if HTML_TAG_RE.search(text):
        return []
    return [text]


def check_literal_outside_root(text: str):
    findings = []
    # Strip comments FIRST, :root SECOND (re-verification finding, #662): a `}` inside a :root
    # comment would otherwise truncate ROOT_BLOCK_RE's `[^}]*` match early, leaking :root's own
    # literals into the outside-root scan — comment-stripping first removes that `}` before
    # ROOT_BLOCK_RE ever sees it.
    regions = [CSS_COMMENT_RE.sub("", css) for css in _css_regions(text)]
    rest = "\n".join(ROOT_BLOCK_RE.sub("", css) for css in regions)
    for m in COLOR_LITERAL_RE.finditer(rest):
        findings.append(("FAIL", "literal-outside-root", f"color literal outside :root, not a var(--<short-role>) reference: {m.group(0)}"))
    return findings


def check_br_in_mermaid_label(text: str):
    findings = []
    for fence in MERMAID_FENCE_RE.findall(text) + MERMAID_HTML_BLOCK_RE.findall(text):
        for m in NODE_LABEL_BR_RE.finditer(fence):
            findings.append(("FAIL", "br-in-mermaid-label", f"<br/> inside a mermaid node label: {m.group(0)[:60]}"))
    return findings


def check_missing_ground(text: str):
    findings = []
    if not COLOR_SCHEME_RE.search(text):
        findings.append(("FAIL", "missing-ground", "no `color-scheme: light dark` declared"))
    if not BODY_BG_VAR_RE.search(text):
        findings.append(("FAIL", "missing-ground", "body background not bound to a --paper/*-background token"))
    return findings


def check_doctrine_font_stack(text: str):
    findings = []
    # Token→value map for #684's resolve-then-check: a var(--font-*) use is judged by the
    # RESOLVED stack its token declares on this same page, never trusted on indirection alone.
    token_defs = {name: value for name, value in FONT_TOKEN_DEF_RE.findall(text)}
    for m in FONT_FAMILY_RE.finditer(text):
        value = m.group(1)
        start = max(0, m.start() - 120)
        preceding = text[start : m.start()]
        has_override = bool(OVERRIDE_COMMENT_RE.search(preceding))
        var_m = FONT_VAR_ONLY_RE.match(value)
        if var_m:
            token = var_m.group(1)
            resolved = token_defs.get(token)
            if resolved is None:
                if not has_override:
                    findings.append(("WARN", "doctrine-font-stack",
                                     f"font-family reads {token} but the token is not declared on this page — resolved stack unverifiable (#684)"))
                continue
            if DOCTRINE_SANS_RE.search(resolved) or DOCTRINE_MONO_RE.search(resolved):
                continue  # the token resolves to a doctrine stack — #662's on-doctrine indirection, still PASS
            if not has_override:
                findings.append(("WARN", "doctrine-font-stack",
                                 f"font-family {token} resolves off doctrine, no override comment: {resolved.strip()}"))
            continue
        if has_override:
            continue
        if not (DOCTRINE_SANS_RE.search(value) or DOCTRINE_MONO_RE.search(value)):
            findings.append(("WARN", "doctrine-font-stack", f"font-family off doctrine, no override comment: {value.strip()}"))
    # Definition-side half of the same rule (checker finding C): a --font-* token itself must
    # carry the mandatory fallback tail — trusting its USE via var() is only safe if the token
    # was actually built right.
    for m in FONT_TOKEN_DEF_RE.finditer(text):
        value = m.group(2)
        if not FONT_FALLBACK_TAIL_RE.search(value.strip().rstrip("'\"")):
            findings.append(("WARN", "doctrine-font-stack",
                             f"--font-* token defined without the mandatory system-fallback tail: {value.strip()}"))
    return findings


CHECKS = (
    check_theme_block_only,
    check_external_url,
    check_literal_outside_root,
    check_br_in_mermaid_label,
    check_missing_ground,
    check_doctrine_font_stack,
)


def check_text(text: str):
    findings = []
    for fn in CHECKS:
        findings.extend(fn(text))
    return findings


def run(paths):
    worst = 0
    for path in paths:
        p = Path(path)
        if not p.is_file():
            print(f"artifact_check · usage-error · unreadable path · {path}")
            return 2
        text = p.read_text(encoding="utf-8", errors="replace")
        findings = check_text(text)
        n_fail = sum(1 for f in findings if f[0] == "FAIL")
        n_warn = sum(1 for f in findings if f[0] == "WARN")
        verdict = "FAIL" if n_fail else ("warn" if n_warn else "ok")
        print(f"artifact_check · {verdict} · {n_fail} fail / {n_warn} warn · {path}")
        for sev, code, msg in findings:
            print(f"  {sev:5} {code:22} {msg}")
        worst = max(worst, 1 if n_fail else 0)
    return worst


# --- selftest fixtures -------------------------------------------------------

# NOTE: this fixture's :root deliberately still models the pre-#662 `--c-*` naming — it exists to
# prove the checker's GENERIC grep-gates (theme/external-url/br/font checks) hold regardless of
# which naming generation a page's :root happens to use, not to model the current contract. The
# CURRENT contract (unprefixed short role names) is what `CSS_BUILD_OUTPUT_FIXTURE` below proves.
GOOD_FIXTURE = """
:root {
  color-scheme: light dark;
  --c-primary: light-dark(oklch(0.55 0.1 226), oklch(0.73 0.13 222));
  --c-paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237));
}
body { background-color: var(--paper); font-family: system-ui, -apple-system, sans-serif; }
button { font-family: ui-monospace, 'SF Mono', monospace; border-radius: var(--r-sm); }
```mermaid
graph LR
  A["Coordinator"] -->|dispatches| B["Builder"]
```
"""

BAD_FIXTURE_THEME_BLOCK = """
@media (prefers-color-scheme: dark) {
  body { background: #222; }
}
body { background: #fff; }
"""

BAD_FIXTURE_EXTERNAL_URL = """
@import url(https://evil.example.com/steal.css);
:root { color-scheme: light dark; }
body { background-color: var(--paper); font-family: system-ui; }
"""

BAD_FIXTURE_LITERAL = """
:root { color-scheme: light dark; --c-primary: light-dark(#000, #fff); }
body { background-color: var(--paper); color: #ff00ff; font-family: system-ui; }
"""

BAD_FIXTURE_BR = """
```mermaid
graph TD
  A["Coordinator<br/>dispatches build"] --> B["Builder"]
```
"""

BAD_FIXTURE_GROUND = """
body { color: black; font-family: system-ui; }
"""

# #681: the HTML-artifact-native embedding form (`<pre class="mermaid">`) with a real <br/>
# defect inside a node label — must bite exactly like BAD_FIXTURE_BR's markdown-fence form.
BAD_FIXTURE_BR_HTML = """
<pre class="mermaid">
graph TD
  A["Coordinator<br/>dispatches build"] --> B["Builder"]
</pre>
"""

# Reverse control: a clean `<pre class="mermaid">` block (single-line labels) must not trip
# br-in-mermaid-label just because it uses the HTML embedding form.
GOOD_FIXTURE_MERMAID_HTML = """
<pre class="mermaid">
graph LR
  A["Coordinator"] -->|dispatches| B["Builder"]
</pre>
"""

GOOD_FIXTURE_PROSE_HASH = """
<style>
:root { color-scheme: light dark; --c-paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237)); }
body { background: var(--c-paper); font-family: system-ui, sans-serif; }
</style>
<p>Fixed in #123 and #541; see also issue #1122 for the follow-up.</p>
<p style="color: var(--c-primary)">Styled prose, still no literal.</p>
"""

BAD_FIXTURE_STYLE_BLOCK_LITERAL = """
<style>
:root { color-scheme: light dark; }
body { background: var(--c-paper); color: #ff00ff; font-family: system-ui; }
</style>
<p>Prose mentioning #123 must not add findings.</p>
"""

BAD_FIXTURE_FONT = """
:root { color-scheme: light dark; }
body { background-color: var(--paper); font-family: 'Comic Sans MS', cursive; }
"""

# #662 third checker-alignment note, refined by #684 (2026-08-19): font-family via var(--font-*)
# token indirection is the doctrine's own prescribed mechanism — and under #684's
# resolve-then-check the check now FOLLOWS the indirection to the token's declaration and judges
# the RESOLVED stack. Locked reverse control (#684 acceptance criterion: this fixture staying
# PASS is the proof the change is a refinement, not a policy reversal of #662): zero
# doctrine-font-stack findings on a page that only ever references DOCTRINE-RESOLVING tokens,
# never the literal stack at the point of use.
GOOD_FIXTURE_FONT_VAR = """
:root { color-scheme: light dark; --paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237));
  --font-system-ui: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-ui-monospace: ui-monospace, 'SF Mono', monospace; }
body { background-color: var(--paper); font-family: var(--font-system-ui); }
button { font-family: var(--font-ui-monospace); }
"""

# #684 bite fixtures — the three resolve-then-check outcomes beyond the doctrine-token PASS:
# a token resolving to an off-doctrine literal stack (the Comic Sans case) warns citing the
# RESOLVED value; the same use with an override comment is suppressed; an undeclared token warns
# naming the token itself.
BAD_FIXTURE_FONT_VAR_OFF_DOCTRINE = """
:root { color-scheme: light dark; --paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237));
  --font-brand: 'Comic Sans MS', cursive, sans-serif; }
body { background-color: var(--paper); font-family: var(--font-brand); }
"""

GOOD_FIXTURE_FONT_VAR_OVERRIDE = """
:root { color-scheme: light dark; --paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237));
  --font-brand: 'Custom Brand Font', serif, sans-serif; }
/* override: brand requires this face for the masthead */
body { background-color: var(--paper); font-family: var(--font-brand); }
"""

BAD_FIXTURE_FONT_VAR_UNRESOLVABLE = """
:root { color-scheme: light dark; --paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237)); }
body { background-color: var(--paper); font-family: var(--font-phantom); }
"""

# CROSS-SCRIPT REGRESSION FIXTURE (#662 Acceptance criterion 2) — the FULL, VERBATIM
# `css_build.py` output for its own FIXTURE_TOKENS fixture (docs/skills/make-artifact/scripts/
# css_build.py's `build(FIXTURE_TOKENS)`, captured 2026-08-18 — every line, comments included,
# nothing trimmed), plus the synthetic body/font rule `make-artifact`'s own page assembly phase
# adds on top of a css_build :root block. Bundled scripts cannot import across a plugin boundary
# (.claude/rules/plugin-authoring.md's hard-boundary rule), so this is a literal, dated, cited
# COPY, not a live import — if css_build.py's emission shape ever changes, BOTH this fixture and
# css_build.py's own selftest (which asserts the same property names from the emitter's side)
# update in the same change, per #662's Acceptance criterion 2 (amended by #684, 2026-08-19:
# zero FAILs plus exactly the one ruled doctrine-font-stack WARN on the synthetic body rule's
# brand token — see the selftest assertion below). A prior draft of this fixture
# TRIMMED the generated comments/spacing/radii/mermaid blocks and so silently missed a real
# regression that only the full output exposes (checker finding, #662): css_build's own generated
# mermaid comment used to cite "#662" literally in-line, which `#[0-9a-fA-F]{3,8}` reads as a
# 3-hex-digit color literal outside :root — fixed two ways, at the source (the citation was
# dropped from the emitted comment, `css_build.py`'s MERMAID_REHEME_BLOCK) and at the checker
# (comments are now stripped before the literal scan, `CSS_COMMENT_RE` above) — this fixture, now
# genuinely verbatim, is what would have caught it.
CSS_BUILD_OUTPUT_FIXTURE = """
/* Generated by make-artifact's css_build.py (docs plugin) — do not hand-edit. */

:root {
  color-scheme: light dark;
  --accent: light-dark(oklch(0.5837 0.1265 236.48), oklch(0.6716 0.1414 234.43));
  --card: light-dark(oklch(0.9335 0.0017 247.84), oklch(0.2597 0.0024 247.92));
  --ink: light-dark(oklch(0.1776 0 0), oklch(1 0 0));
  --on-accent: light-dark(oklch(1 0 0), oklch(1 0 0));
  --paper: light-dark(oklch(0.9807 0 90), oklch(0.1421 0.0022 247.9));
  --text-body-md-size: 16px;
  --text-body-md-weight: 440;
  --text-body-md-lh: 1.5;
  --text-display-sm-size: 72px;
  --text-display-sm-weight: 700;
  --text-display-sm-lh: 0.806;
  --text-display-sm-ls: -0.02em;
  --font-gt-america: 'GT America', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-gt-america-mono: 'GT America Mono', ui-monospace, 'SF Mono', monospace;
  --space-none: 0px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;
  --space-xl: 24px;
  --space-2xl: 32px;
  --space-3xl: 48px;
  --space-4xl: 64px;
  --space-5xl: 96px;
  --r-none: 0px;
  --r-xs: 4px;
  --r-sm: 8px;
  --r-md: 12px;
  --r-lg: 16px;
  --r-xl: 28px;
  --r-full: 9999px;
}

[data-theme="light"] { color-scheme: light; }
[data-theme="dark"] { color-scheme: dark; }

/* Mermaid house re-theme (design:artifact-styling-rules' mermaid-reference.md): the rendered SVG
   ships its own inline styles, so re-theming requires token-driven !important overrides bound to
   the same short role custom properties as the rest of the page — one mechanism, both schemes,
   unprefixed short names, no legacy prefix. */
.mermaid svg .node rect,
.mermaid svg .node circle,
.mermaid svg .node polygon {
  fill: var(--card) !important;
  stroke: var(--line) !important;
}
.mermaid svg .node text,
.mermaid svg .nodeLabel {
  fill: var(--ink) !important;
  color: var(--ink) !important;
}
.mermaid svg .edgePath .path,
.mermaid svg .flowchart-link {
  stroke: var(--line) !important;
}
.mermaid svg .edgeLabel {
  background-color: var(--card) !important;
  color: var(--muted) !important;
}

/* Width-preserving hidden-tab-panel technique (design:artifact-styling-rules'
   mermaid-reference.md / type-and-layout.md): never display:none a panel
   holding a mermaid diagram -- it corrupts the measured container permanently, even after the
   tab is shown again. */
[data-tab-panel][hidden] {
  visibility: hidden;
  position: absolute;
  inset: 0;
  pointer-events: none;
}

body { background-color: var(--paper); color: var(--ink); font-family: var(--font-gt-america); }
button { font-family: var(--font-gt-america-mono); }
"""

# NEGATIVE CONTROL (checker finding, #662): a CSS comment carrying a `#NNN` issue reference must
# never read as a color literal — the exact class the fixture above's history just proved bites
# for real, reproduced directly so a future regression on either side (the comment-strip fix, or
# a future edit that reintroduces a bare issue ref into generated CSS) is caught.
BAD_FIXTURE_HASH_IN_CSS_COMMENT = """
/* see issue #123 and #4096 for background */
:root { color-scheme: light dark; --paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237)); }
body { background-color: var(--paper); font-family: system-ui; }
"""

# NEGATIVE CONTROL (re-verification finding, #662): a `}` inside a :root comment must not
# truncate ROOT_BLOCK_RE's match and leak :root's own literals into the outside-root scan —
# proves the comment-strip-before-root-strip ORDER, not just that comments strip at all.
GOOD_FIXTURE_BRACE_IN_ROOT_COMMENT = """
:root {
  /* legacy } note: this brace used to truncate the :root match early */
  color-scheme: light dark;
  --x: #abcdef;
  --paper: light-dark(oklch(0.95 0 90), oklch(0.22 0.006 237));
}
body { background-color: var(--paper); font-family: system-ui; }
"""


def selftest():
    assert check_text(GOOD_FIXTURE) == [], f"clean fixture must have zero findings, got {check_text(GOOD_FIXTURE)}"

    codes = {c for _, c, _ in check_theme_block_only(BAD_FIXTURE_THEME_BLOCK)}
    assert "theme-block-only" in codes, "theme-block-only must bite on a prefers-color-scheme-only page"
    assert check_theme_block_only(GOOD_FIXTURE) == [], "reverse control: light-dark() page must not trip theme-block-only"

    codes = {c for _, c, _ in check_external_url(BAD_FIXTURE_EXTERNAL_URL)}
    assert "external-url" in codes, "external-url must bite on a non-allowlisted @import"
    assert check_external_url(GOOD_FIXTURE) == [], "reverse control: no external URLs in the clean fixture"

    codes = {c for _, c, _ in check_literal_outside_root(BAD_FIXTURE_LITERAL)}
    assert "literal-outside-root" in codes, "literal-outside-root must bite on a bare hex outside :root"
    assert check_literal_outside_root(GOOD_FIXTURE) == [], "reverse control: clean fixture uses only var() outside :root"
    # gh#660 negative control: prose issue refs (#123, #541) on an HTML page are not color literals
    assert check_literal_outside_root(GOOD_FIXTURE_PROSE_HASH) == [], "prose #NNN issue refs must not report as color literals"
    hits = check_literal_outside_root(BAD_FIXTURE_STYLE_BLOCK_LITERAL)
    assert len(hits) == 1 and "#ff00ff" in hits[0][2], "a real literal inside <style> must still bite exactly once (prose #123 excluded)"

    codes = {c for _, c, _ in check_br_in_mermaid_label(BAD_FIXTURE_BR)}
    assert "br-in-mermaid-label" in codes, "br-in-mermaid-label must bite on a <br/> inside a node label"
    assert check_br_in_mermaid_label(GOOD_FIXTURE) == [], "reverse control: clean fixture's mermaid label is single-line"

    # #681: the HTML-artifact-native `<pre class="mermaid">` embedding form must be scanned too —
    # the markdown-fence-only regex silently missed this genre entirely before this fix.
    codes = {c for _, c, _ in check_br_in_mermaid_label(BAD_FIXTURE_BR_HTML)}
    assert "br-in-mermaid-label" in codes, "br-in-mermaid-label must bite on a <br/> inside a <pre class=\"mermaid\"> node label"
    assert check_br_in_mermaid_label(GOOD_FIXTURE_MERMAID_HTML) == [], (
        "reverse control: a clean <pre class=\"mermaid\"> block with single-line labels must not bite")

    codes = {c for _, c, _ in check_missing_ground(BAD_FIXTURE_GROUND)}
    assert "missing-ground" in codes, "missing-ground must bite when color-scheme/body-token binding are absent"
    assert check_missing_ground(GOOD_FIXTURE) == [], "reverse control: clean fixture has both color-scheme and body token binding"
    # gh#660 negative control: a legacy pre-#662 page binds var(--c-paper) (fresh css_build.py
    # output now emits var(--paper) instead — accepted per #662's own harmless-to-keep note,
    # see the BODY_BG_VAR_RE comment above) — either way a conforming page must pass ground
    assert check_missing_ground(GOOD_FIXTURE_PROSE_HASH) == [], "body background var(--c-paper) must satisfy missing-ground"

    codes = {c for _, c, _ in check_doctrine_font_stack(BAD_FIXTURE_FONT)}
    assert "doctrine-font-stack" in codes, "doctrine-font-stack must warn on an off-doctrine font with no override comment"
    assert check_doctrine_font_stack(GOOD_FIXTURE) == [], "reverse control: clean fixture's fonts match doctrine"

    # override comment suppresses the doctrine-font-stack warning (named-gap path, never silent)
    overridden = "/* override: brand requires this face */\nbody { font-family: 'Custom Brand Font', serif; }"
    assert check_doctrine_font_stack(overridden) == [], "an explicit override comment must suppress the font-stack warning"

    # #662 third checker-alignment note, refined by #684: DOCTRINE-RESOLVING var(--font-*) token
    # indirection is on-doctrine, no override comment needed — this fixture staying PASS is
    # #684's own acceptance criterion that resolve-then-check is not a policy reversal of #662
    assert check_doctrine_font_stack(GOOD_FIXTURE_FONT_VAR) == [], (
        "a font-family reading a doctrine-resolving var(--font-*) must never warn — token indirection IS the doctrine")
    assert check_text(GOOD_FIXTURE_FONT_VAR) == [], (
        "the var(--font-*) fixture must be clean end to end, not just on the font check")

    # #684 resolve-then-check bites: a token resolving to an off-doctrine literal stack warns
    # CITING THE RESOLVED VALUE (the Comic Sans case)...
    hits = check_doctrine_font_stack(BAD_FIXTURE_FONT_VAR_OFF_DOCTRINE)
    assert any(c == "doctrine-font-stack" and "Comic Sans MS" in msg and "--font-brand" in msg
               for _, c, msg in hits), (
        "a var(--font-*) resolving to an off-doctrine stack must warn citing the resolved value (#684)")
    # ...the same use under an override comment is suppressed (the escape hatch generalizes)...
    assert check_doctrine_font_stack(GOOD_FIXTURE_FONT_VAR_OVERRIDE) == [], (
        "an override comment must suppress the resolved-off-doctrine warning, mirroring the literal path (#684)")
    # ...and an undeclared token warns naming the token itself
    hits = check_doctrine_font_stack(BAD_FIXTURE_FONT_VAR_UNRESOLVABLE)
    assert any(c == "doctrine-font-stack" and "--font-phantom" in msg and "not declared" in msg
               for _, c, msg in hits), (
        "an unresolvable var(--font-*) token must warn naming the token (#684)")

    # checker finding C — the var(--font-*) skip must be ANCHORED to the whole value: a MIXED
    # value naming a literal fallback alongside the token must still warn, never silently escape
    mixed_font = ":root { color-scheme: light dark; --paper: light-dark(#fff, #000); }\n" \
                 "body { background: var(--paper); font-family: var(--font-x), 'Comic Sans MS'; }"
    codes = {c for _, c, _ in check_doctrine_font_stack(mixed_font)}
    assert "doctrine-font-stack" in codes, (
        "a mixed var(--font-*)+literal-fallback value must still warn — the anchor must be whole-value")

    # checker finding C, other half — trusting var(--font-*) is only safe if the TOKEN ITSELF
    # carries the mandatory fallback tail; a badly-defined token must warn even though every USE
    # of it looks like clean token indirection
    bad_font_token = ":root { color-scheme: light dark; --paper: light-dark(#fff, #000);\n" \
                      "  --font-bad: 'Comic Sans MS', cursive; }\n" \
                      "body { background: var(--paper); font-family: var(--font-bad); }"
    codes = {c for _, c, _ in check_doctrine_font_stack(bad_font_token)}
    assert "doctrine-font-stack" in codes, (
        "a --font-* token defined without the mandatory fallback tail must warn even via var() use")

    # #662 Acceptance criterion 2, amended by #684 (marshal ruling 2026-08-19) — the FULL
    # verbatim css_build.py output must still pass with zero FAILs, and its --font-gt-america-mono
    # token resolves ON-doctrine (its stack carries ui-monospace), so the button rule stays clean.
    # The synthetic body rule's var(--font-gt-america), though, resolves to the source system's
    # brand stack with no override comment — #684 ruled that WARN is CORRECT behavior (the
    # artifact type doctrine owns faces; make-artifact's justification mechanism is #649's v2
    # build, noted there, not built here). Exactly that one WARN, nothing else.
    findings = check_text(CSS_BUILD_OUTPUT_FIXTURE)
    assert not any(sev == "FAIL" for sev, _, _ in findings), (
        "verbatim css_build.py output must never FAIL — the #662 cross-script regression "
        "fixture; got: %r" % (findings,))
    assert len(findings) == 1 and findings[0][1] == "doctrine-font-stack" \
        and "--font-gt-america" in findings[0][2] and "GT America" in findings[0][2], (
        "the css_build fixture must carry exactly the one #684-ruled WARN — the synthetic body "
        "rule's brand token resolving off doctrine with no override comment; got: %r" % (findings,))

    # checker finding A — a CSS comment's own `#NNN` issue reference must never read as a color
    # literal (the exact bug a trimmed fixture missed); reverse control alongside the negative
    assert check_literal_outside_root(BAD_FIXTURE_HASH_IN_CSS_COMMENT) == [], (
        "a #NNN issue ref inside a CSS COMMENT must never be read as a color literal (#662)")
    real_literal_still_bites = ":root { color-scheme: light dark; }\n" \
        "/* see #123 */\nbody { background: var(--paper); color: #ff00ff; font-family: system-ui; }"
    codes = {c for _, c, _ in check_literal_outside_root(real_literal_still_bites)}
    assert "literal-outside-root" in codes, (
        "a real literal must still bite even when a #NNN-carrying comment sits right next to it")

    # re-verification finding — a `}` inside a :root comment must not truncate ROOT_BLOCK_RE
    # and leak :root's own --x: #abcdef literal into the outside-root scan
    assert check_literal_outside_root(GOOD_FIXTURE_BRACE_IN_ROOT_COMMENT) == [], (
        "a `}` inside a :root comment must not truncate the :root match and leak its own literal")

    print("artifact_check selftest · PASS · 6 checks, negative + reverse controls, override-comment "
          "path, font-var resolve-then-check path (#684: doctrine-token PASS, resolved-off-doctrine "
          "WARN, override suppression, unresolvable-token WARN; anchored + token-definition halves), "
          "cross-script (#662) regression fixture (full verbatim, zero FAILs + the one #684-ruled WARN "
          "+ comment-hash negative control)")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(args))
