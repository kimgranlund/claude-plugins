#!/usr/bin/env python3
"""prelint.py — offline structural checks + lint-JSON classifier for a Google Stitch DESIGN.md.

Zero dependencies (stdlib only; parses the frontmatter's restricted YAML subset itself).

Usage:
  python3 prelint.py check DESIGN.md        # offline pre-lint checks (lint-gate.md §5)
  python3 prelint.py classify lint.json     # classify `npx @google/design.md lint` JSON output
                                            # (either arg may be '-' for stdin)

Classify accepts an optional bundle README receipt as a third argument:
    python3 prelint.py classify <lint.json> [<bundle-README.md>]
When the receipt carries the kit-fidelity contrast disclosure ("N derivable
fill/on-pair(s) below 4.5:1 ... ADR-003", per onColorMode: fixed — PR #229),
contrast findings classify as EXPECTED (a disclosed measurement), not ACTION.

Exit codes: 0 clean · 1 error-level findings (check) / errors or ACTION findings (classify)
          · 2 unreadable/unparseable input.

Derived from the Stitch DESIGN.md spec, version alpha (github.com/google-labs-code/design.md,
fetched 2026-07-05). Severities mirror the platform: ERROR = the linter rejects or errors;
WARN = a lint warning or a method-level defect; INFO = tolerated/informational.
"""

import difflib
import json
import re
import sys
from pathlib import Path

KNOWN_TOP = {"version", "name", "description", "colors", "typography", "rounded", "spacing", "components"}
CANONICAL = [  # (canonical name, aliases) — spec section order
    ("Overview", {"brand & style"}),
    ("Colors", set()),
    ("Typography", set()),
    ("Layout", {"layout & spacing"}),
    ("Elevation & Depth", {"elevation"}),
    ("Shapes", set()),
    ("Components", set()),
    ("Do's and Don'ts", set()),
]
STATE_SUFFIXES = {"hover", "active", "pressed", "focus", "disabled", "selected"}
REF_RE = re.compile(r"\{([A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)+)\}")


def read_input(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        print(f"[FATAL] cannot read {path}: {e}")
        sys.exit(2)


# ---------------------------------------------------------------- YAML subset
def clean_value(raw):
    raw = raw.strip()
    if raw[:1] in {'"', "'"}:
        q = raw[0]
        end = raw.find(q, 1)
        return raw[1:end] if end > 0 else raw.strip(q)
    return raw.split(" #", 1)[0].strip()


def parse_frontmatter(fm_text):
    """Parse the restricted schema shape (nested string:string maps). Returns (tree, findings)."""
    root, findings = {}, []
    stack = [(0, root)]          # (indent of keys in this map, dict)
    pending = None               # (parent_indent, dict just opened)
    for n, raw in enumerate(fm_text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.expandtabs(2).lstrip(" ")) if "\t" in raw else len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            findings.append(("WARN", f"line {n}: not `key: value` — outside the subset this checker parses"))
            continue
        key, _, rest = line.partition(":")
        key, value = key.strip().strip('"').strip("'"), rest.strip()
        if pending is not None:
            if indent > pending[0]:
                stack.append((indent, pending[1]))
            pending = None
        while len(stack) > 1 and indent < stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if key in parent:
            findings.append(("ERROR", f"line {n}: duplicate key `{key}` in the same map — YAML keeps the last value silently"))
        if value == "":
            child = {}
            parent[key] = child
            pending = (indent, child)
        else:
            parent[key] = clean_value(value)
    return root, findings


# ---------------------------------------------------------------- check mode
def check(path):
    text = read_input(path)
    findings = []

    # frontmatter split
    fm_text, body = "", text
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if m:
        fm_text, body = m.group(1), text[m.end():]
    else:
        findings.append(("INFO", "no YAML frontmatter (legal — optional) but this method ships tokens; add the fences"))

    tree, fm_findings = parse_frontmatter(fm_text) if fm_text else ({}, [])
    findings += fm_findings

    # 7. light-dark() in frontmatter values (measured: linter errors)
    if "light-dark(" in fm_text:
        findings.append(("ERROR", "`light-dark()` in a frontmatter value — the linter rejects it ('not a valid color'); ship -dark siblings instead"))

    # 2/3. section headings: duplicates + canonical order
    heads = [h.strip().rstrip(":") for h in re.findall(r"^##(?!#)\s*(.+?)\s*$", body, re.M)]
    seen = {}
    for h in heads:
        k = h.lower().replace("’", "'")
        if k in seen:
            findings.append(("ERROR", f"duplicate `## {h}` heading — the file is rejected"))
        seen[k] = True

    def canon_index(h):
        k = h.lower().replace("’", "'")
        for i, (name, aliases) in enumerate(CANONICAL):
            if k == name.lower() or k in aliases:
                return i
        return None

    order, unknown = [], []
    for h in heads:
        i = canon_index(h)
        (order if i is not None else unknown).append((i, h) if i is not None else h)
    idxs = [i for i, _ in order]
    if idxs != sorted(idxs):
        bad = [h for (i, h), s in zip(order, sorted(idxs)) if i != s]
        findings.append(("WARN", f"canonical sections out of order (lint `section-order`): {', '.join(bad) or 'see heading sequence'}"))
    if unknown:
        findings.append(("INFO", f"unknown sections ride tolerance (preserved, unparsed): {', '.join(unknown)}"))

    # 4. {path.to.token} references resolve (frontmatter + prose)
    for ref in sorted(set(REF_RE.findall(text))):
        node = tree
        for part in ref.split("."):
            node = node.get(part) if isinstance(node, dict) else None
            if node is None:
                findings.append(("ERROR", f"broken reference {{{ref}}} — resolves to no defined token (lint `broken-ref`, the only error rule)"))
                break

    colors = tree.get("colors") if isinstance(tree.get("colors"), dict) else {}

    # 5. primary present
    if colors and "primary" not in colors:
        findings.append(("WARN", "no `primary` in colors (lint `missing-primary`: agents auto-generate one) — add the documented compat alias of the brand base fill"))

    # 6. scheme parity — only when the -dark convention is in use
    darks = {k for k in colors if k.endswith("-dark")}
    if darks:
        for k in sorted(darks):
            if k[:-5] not in colors:
                findings.append(("WARN", f"parity: `{k}` has no light base `{k[:-5]}` — identical role inventories per scheme"))
        for k in sorted(set(colors) - darks):
            if f"{k}-dark" not in colors:
                findings.append(("WARN", f"parity: `{k}` has no `-dark` sibling — identical role inventories per scheme (ignore only if single-scheme by design)"))

    # 8. base components with backgroundColor but no textColor
    comps = tree.get("components") if isinstance(tree.get("components"), dict) else {}
    for name, props in sorted(comps.items()):
        if not isinstance(props, dict) or name.rsplit("-", 1)[-1] in STATE_SUFFIXES:
            continue
        if "backgroundColor" in props and "textColor" not in props:
            findings.append(("WARN", f"component `{name}` sets backgroundColor without textColor — the contrast rule has nothing to check; the on-pair is probably missing"))

    # 9. leading/tracking relative-only (standing rule): lineHeight/letterSpacing never px
    typo_map = tree.get("typography") if isinstance(tree.get("typography"), dict) else {}
    for level, props in sorted(typo_map.items()):
        if not isinstance(props, dict):
            continue
        for field in ("lineHeight", "letterSpacing"):
            v = str(props.get(field, ""))
            if v.endswith("px"):
                findings.append(("ERROR", f"typography.{level}.{field} = `{v}` — leading/tracking are always relative: unitless factor, em, or % (never px; standing rule, and unitless lineHeight is Stitch's own recommendation)"))

    # 10. top-level extension keys + typo candidates
    for k in tree:
        if k in KNOWN_TOP:
            continue
        close = difflib.get_close_matches(k, KNOWN_TOP, n=1, cutoff=0.8)
        if close:
            findings.append(("WARN", f"top-level key `{k}` looks like a typo of `{close[0]}` (lint `unknown-key`)"))
        else:
            findings.append(("INFO", f"top-level key `{k}` is an extension group (tolerated by spec)"))

    # report
    if not findings:
        print("[OK] all offline checks pass — run the lint gate next")
        return 0
    rank = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for sev, msg in sorted(findings, key=lambda f: rank[f[0]]):
        print(f"[{sev}] {msg}")
    errs = sum(1 for s, _ in findings if s == "ERROR")
    print(f"\n{errs} error(s), {sum(1 for s, _ in findings if s == 'WARN')} warning(s), "
          f"{sum(1 for s, _ in findings if s == 'INFO')} info — "
          + ("fix errors before linting" if errs else "ready for the lint gate"))
    return 1 if errs else 0


# ------------------------------------------------------------- classify mode
def classify_finding(sev, path, message, rule="", disclosed=None):
    msg = message.lower()
    rule = (rule or "").lower()
    if "passes" in msg:
        return "OK", "informational pass — read the message, not the severity label"
    if sev == "error":
        return "ACTION", "error severity — the gate is zero errors, always"
    if sev == "info":
        return "INFO", "no response required"
    token = path.split(".")[-1] if path else ""
    if rule == "orphaned-tokens" or "never referenced" in msg or "orphan" in msg:
        if token.endswith("-dark"):
            return "EXPECTED", "-dark scheme sibling — inherent cost, the alpha schema has no scheme axis; record in the receipt"
        return "REVIEW", "non-dark orphan — legitimate only if prose-bound with no component property slot; verify and record, else cut the token"
    if rule == "missing-primary" or ("primary" in msg and ("auto-generate" in msg or "no" in msg)):
        return "ACTION", "add the documented `primary` compat alias of the brand base fill"
    if rule == "contrast-ratio" or "contrast" in msg:
        # KIT FIDELITY (ultimate-tokens PR #229): `onColorMode` is a user setting; "fixed"
        # ships uniform brand labels whose sub-4.5 pairs are an accepted brand override
        # (ADR-003), DISCLOSED in the bundle README. With that receipt passed as the second
        # classify argument, contrast findings are the disclosed measurement — not an ACTION.
        if disclosed:
            return "EXPECTED", (f"pair below WCAG AA 4.5:1 under `onColorMode: {disclosed[1]}` — the disclosed "
                                f"brand override (ADR-003; receipt discloses {disclosed[0]} pair(s)); verify it is recorded, never silently fix")
        return "ACTION", "pair below WCAG AA 4.5:1 — fix the on-color; never expected, never waived (no receipt disclosure was supplied)"
    if rule == "section-order" or "order" in msg:
        return "ACTION", "reorder to the canonical sequence"
    if rule == "missing-typography" or ("typography" in msg and "default" in msg):
        return "ACTION", "ship the type scale or agents fall back to default fonts"
    if rule == "unknown-key" or ("typo" in msg and "typograph" not in msg) or "unknown" in msg:
        return "REVIEW", "check for a schema-key typo; a deliberate extension key is fine — document it"
    return "REVIEW", "unrecognized warning — read the message and classify it in the receipt"


def classify(path, readme=None):
    try:
        report = json.loads(read_input(path))
    except json.JSONDecodeError as e:
        print(f"[FATAL] not valid lint JSON: {e}")
        return 2
    disclosed = None
    if readme:
        try:
            _t = Path(readme).read_text(encoding="utf-8")
            _m = re.search(r"(\d+) derivable fill/on-pair\(s\) below 4\.5:1 under the kit's `onColorMode: (\w+)`", _t)
            if _m and "ADR-003" in _t:
                disclosed = (int(_m.group(1)), _m.group(2))
            else:
                print("[NOTE] receipt supplied but carries no ADR-003 contrast disclosure — contrast stays ACTION")
        except OSError as e:
            print(f"[NOTE] receipt unreadable ({e}) — contrast stays ACTION")
    counts = {}
    for f in report.get("findings", []):
        cls, why = classify_finding(f.get("severity", ""), f.get("path", ""), f.get("message", ""), f.get("rule", ""), disclosed)
        counts[cls] = counts.get(cls, 0) + 1
        print(f"[{cls}] {f.get('path', '?')}: {f.get('message', '')}\n         -> {why}")
    s = report.get("summary", {})
    print(f"\nsummary: {s.get('errors', 0)} errors, {s.get('warnings', 0)} warnings, {s.get('info', 0)} info")
    print("classes: " + (", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "none"))
    fail = s.get("errors", 0) > 0 or counts.get("ACTION", 0) > 0
    print("gate: " + ("FAIL — fix ACTION items, re-run lint" if fail
                      else "PASS — classify EXPECTED/REVIEW lines into the receipt"))
    return 1 if fail else 0


def main():
    if len(sys.argv) not in (3, 4) or sys.argv[1] not in {"check", "classify"} or (len(sys.argv) == 4 and sys.argv[1] != "classify"):
        print(__doc__)
        return 2
    if sys.argv[1] == "check":
        return check(sys.argv[2])
    return classify(sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)


if __name__ == "__main__":
    sys.exit(main())
