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
                        instead of a var(--c-*) reference                                [FAIL]
  br-in-mermaid-label  a literal <br/> or <br> inside a mermaid node-label bracket ["..."]  [FAIL]
  missing-ground       no `color-scheme` declared on :root, or no body/page-root background
                        bound to a --paper/neutral-background-family token               [FAIL]
  doctrine-font-stack  a font-family on body/interactive selectors naming neither the
                        system-ui nor mono doctrine stack, with no override comment        [WARN]

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
MERMAID_FENCE_RE = re.compile(r"```mermaid(.*?)```", re.S)
NODE_LABEL_BR_RE = re.compile(r"\[[^\]]*<br\s*/?>[^\]]*\]", re.I)
COLOR_SCHEME_RE = re.compile(r"color-scheme\s*:\s*light\s+dark")
BODY_BG_VAR_RE = re.compile(r"body\s*\{[^}]*background(?:-color)?\s*:\s*var\(--(?:(?:c-)?paper|[\w-]*background[\w-]*)\)", re.S | re.I)
STYLE_BLOCK_RE = re.compile(r"<style[^>]*>(.*?)</style>", re.S | re.I)
STYLE_ATTR_RE = re.compile(r"style\s*=\s*\"([^\"]*)\"|style\s*=\s*'([^']*)'", re.I)
HTML_TAG_RE = re.compile(r"<[a-zA-Z][^>]*>")
DOCTRINE_SANS_RE = re.compile(r"system-ui")
DOCTRINE_MONO_RE = re.compile(r"ui-monospace")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;]+);")
OVERRIDE_COMMENT_RE = re.compile(r"/\*\s*override\b", re.I)


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
    rest = "\n".join(ROOT_BLOCK_RE.sub("", css) for css in _css_regions(text))
    for m in COLOR_LITERAL_RE.finditer(rest):
        findings.append(("FAIL", "literal-outside-root", f"color literal outside :root, not a var(--c-*) reference: {m.group(0)}"))
    return findings


def check_br_in_mermaid_label(text: str):
    findings = []
    for fence in MERMAID_FENCE_RE.findall(text):
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
    for m in FONT_FAMILY_RE.finditer(text):
        value = m.group(1)
        start = max(0, m.start() - 120)
        preceding = text[start : m.start()]
        if OVERRIDE_COMMENT_RE.search(preceding):
            continue
        if not (DOCTRINE_SANS_RE.search(value) or DOCTRINE_MONO_RE.search(value)):
            findings.append(("WARN", "doctrine-font-stack", f"font-family off doctrine, no override comment: {value.strip()}"))
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

    codes = {c for _, c, _ in check_missing_ground(BAD_FIXTURE_GROUND)}
    assert "missing-ground" in codes, "missing-ground must bite when color-scheme/body-token binding are absent"
    assert check_missing_ground(GOOD_FIXTURE) == [], "reverse control: clean fixture has both color-scheme and body token binding"
    # gh#660 negative control: css_build.py emits var(--c-paper) — a conforming page must pass ground
    assert check_missing_ground(GOOD_FIXTURE_PROSE_HASH) == [], "body background var(--c-paper) must satisfy missing-ground"

    codes = {c for _, c, _ in check_doctrine_font_stack(BAD_FIXTURE_FONT)}
    assert "doctrine-font-stack" in codes, "doctrine-font-stack must warn on an off-doctrine font with no override comment"
    assert check_doctrine_font_stack(GOOD_FIXTURE) == [], "reverse control: clean fixture's fonts match doctrine"

    # override comment suppresses the doctrine-font-stack warning (named-gap path, never silent)
    overridden = "/* override: brand requires this face */\nbody { font-family: 'Custom Brand Font', serif; }"
    assert check_doctrine_font_stack(overridden) == [], "an explicit override comment must suppress the font-stack warning"

    print("artifact_check selftest · PASS · 6 checks, negative + reverse controls, override-comment path")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(args))
