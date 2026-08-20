#!/usr/bin/env python3
"""brand-lint — structural brand-smell checker (the mechanizable slice of the Foundation Canon's "bullshit filter").

SCOPE (be honest): this checks only PATTERN-MATCHABLE STRUCTURAL smells —
archetype language, the vision/mission/values template, fictional personas, brand-DNA/essence
word-clouds, and values stated without trade-offs. It does NOT judge cultural authority or
"is this on brand" — that is irreducible judgment and lives in the brand-methodology skill +
the council. A clean brand-lint says "no structural tells," never "this brand is good."

Usage:
  brand-lint <file.md>...     # lint files; exit 1 if any smell found, else 0
  brand-lint -                # lint stdin
  brand-lint --hook           # PostToolUse hook mode: read event JSON on stdin, lint the
                              #   written .md/.txt file, print advisory findings, ALWAYS exit 0
Stdlib only (Python 3.8+).
"""
import json
import re
import sys

SMELLS = [
    ("ARCHETYPE",
     re.compile(r"\b(brand\s+archetypes?|(?:the\s+)?(hero|sage|outlaw|magician|innocent|explorer|ruler|creator|caregiver|everyman|jester|lover)\s+archetype|(?:12|twelve)\s+archetypes)\b", re.I),
     "the Foundation Canon rejects archetypes — they substitute a borrowed taxonomy for specific cultural research"),
    ("VMV-TEMPLATE",
     re.compile(r"\b(vision,?\s+mission,?\s+(?:and\s+)?values|mission\s+statement|our\s+mission\s+is\s+to|our\s+vision\s+is\b|core\s+values\s*:)", re.I),
     "the vision/mission/values template is a corporate default, not a brand foundation — name the cultural conviction instead"),
    ("PERSONA",
     re.compile(r"\b((buyer|user|customer|audience)\s+personas?\b|meet\s+[A-Z][a-z]+,?\s+(?:a\s+)?\d{2}[\s-]?year[\s-]?old)", re.I),
     "demographic personas are market research, not cultural research — they describe what customers do, not what the world means"),
    ("BRAND-DNA",
     re.compile(r"\bbrand\s+(dna|essence)\b", re.I),
     "brand DNA / essence word-clouds assert distinctiveness without earning it through cultural depth"),
]

EMPTY_VALUES = {
    "integrity", "excellence", "innovation", "passion", "quality", "respect",
    "teamwork", "authenticity", "trust", "collaboration", "accountability", "transparency",
}
# Contrastive constructions only — a real value names what it gives up. Bare " not "/" before "
# were dropped: any incidental negation must not defuse a genuine empty-values list.
TRADEOFF_MARKERS = (" over ", " instead of ", "we choose", "even when", "at the expense",
                    "rather than", " never ", " refuse", " sacrifice", " trade ")


def lint_text(text):
    findings = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        for name, rx, why in SMELLS:
            m = rx.search(line)
            if m:
                snippet = line.strip()[:90]
                findings.append((name, i, snippet, why))
    # doc-level: a VALUES LIST stated without trade-offs. Localized to a single block (not scattered
    # across unrelated prose) AND only when the block reads like a values list — so ordinary use of
    # "quality"/"excellence"/"innovation" in unrelated sentences doesn't trip it (Scott W. N1).
    for blk in re.split(r"\n\s*\n", text):
        blow = blk.lower()
        present = {v for v in EMPTY_VALUES if re.search(r"\b" + re.escape(v) + r"\b", blow)}
        looks_like_values = ("value" in blow) or bool(re.search(r"(?m)^\s*[-*•\d]", blk))
        if len(present) >= 3 and looks_like_values and not any(mk in blow for mk in TRADEOFF_MARKERS):
            findings.append(("VALUES-WITHOUT-TRADEOFFS", 0,
                             "values: " + ", ".join(sorted(present)[:6]),
                             "values that exclude nothing are not values — a real value names what the brand gives up for it"))
            break
    return findings


def _render(path, findings):
    out = [f"brand-lint: {len(findings)} structural smell(s) in {path}"]
    for name, ln, snip, why in findings:
        loc = f"line {ln}" if ln else "document"
        out.append(f"  [{name}] {loc}: {snip}")
        out.append(f"      → {why}")
    return "\n".join(out)


def _hook():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    ti = event.get("tool_input", {}) or {}
    path = ti.get("file_path", "") or ""
    if not path.lower().endswith((".md", ".txt", ".mdx")):
        return 0  # only brand artifacts (prose); stay quiet otherwise
    text = ti.get("content")
    if text is None:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            return 0
    findings = lint_text(text)
    if findings:
        print("⚠ brand-lint (advisory — structural smells only, not a cultural verdict):")
        print(_render(path, findings))
    return 0  # advisory: never block a write


def selftest():
    import io
    import os
    import tempfile
    fails = []

    def expect(cond, msg):
        if not cond:
            fails.append(msg)

    # lint_text: reverse control — ordinary brand prose must come back clean
    clean = ("The studio ships one accent color and says no to the rest. Terracotta over blue, "
             "always. The mark stays quiet so the work can be loud.\n")
    expect(lint_text(clean) == [], f"clean prose flagged (false positive): {lint_text(clean)}")

    # inversion fixtures — each structural smell must be caught by name
    cases = {
        "ARCHETYPE": "Our brand speaks as the Sage archetype, wise and knowing.\n",
        "VMV-TEMPLATE": "Our mission is to empower creators everywhere.\n",
        "PERSONA": "Meet Sarah, a 34-year-old marketing manager who loves productivity apps.\n",
        "BRAND-DNA": "This captures our brand DNA in one word cloud.\n",
    }
    for code, text in cases.items():
        names = {f[0] for f in lint_text(text)}
        expect(code in names, f"missed {code} smell in {text!r}")

    # VALUES-WITHOUT-TRADEOFFS: doc-level, localized to a values-shaped block
    values_no_tradeoff = "Our values:\n- integrity\n- excellence\n- innovation\n"
    expect(any(f[0] == "VALUES-WITHOUT-TRADEOFFS" for f in lint_text(values_no_tradeoff)),
           "values list with no trade-off language was not flagged")
    # reverse control: the same three empty-values words, but WITH a trade-off marker, must NOT flag
    values_with_tradeoff = "Our values:\n- integrity\n- excellence\n- innovation, chosen over speed\n"
    expect(not any(f[0] == "VALUES-WITHOUT-TRADEOFFS" for f in lint_text(values_with_tradeoff)),
           "a values list WITH trade-off language was wrongly flagged")
    # reverse control: incidental, non-values use of the same words must not trip the doc-level check
    incidental = "The build has excellent test coverage. Quality tooling caught the innovation regression.\n"
    expect(not any(f[0] == "VALUES-WITHOUT-TRADEOFFS" for f in lint_text(incidental)),
           "incidental prose (not a values list) was wrongly flagged as VALUES-WITHOUT-TRADEOFFS")

    # _hook(): advisory only — a smelly write is reported but NEVER blocks (always exit 0)
    with tempfile.TemporaryDirectory() as td:
        smelly = os.path.join(td, "brand.md")
        open(smelly, "w", encoding="utf-8").write(cases["ARCHETYPE"])
        event = json.dumps({"tool_input": {"file_path": smelly}})
        old_stdin, old_stdout = sys.stdin, sys.stdout
        sys.stdin, sys.stdout = io.StringIO(event), io.StringIO()
        try:
            rc = _hook()
            hook_out = sys.stdout.getvalue()
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout
        expect(rc == 0, f"--hook mode must always exit 0 (advisory), got {rc}")
        expect("ARCHETYPE" in hook_out, "--hook mode did not report the structural smell it found")

        # a non-.md/.txt/.mdx write is skipped entirely (not brand prose)
        pyfile = os.path.join(td, "script.py")
        open(pyfile, "w", encoding="utf-8").write(cases["ARCHETYPE"])
        event2 = json.dumps({"tool_input": {"file_path": pyfile}})
        sys.stdin, sys.stdout = io.StringIO(event2), io.StringIO()
        try:
            rc2 = _hook()
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout
        expect(rc2 == 0, "--hook mode on a non-prose file must still exit 0")

        # malformed hook event (not valid JSON) must not crash — advisory, exit 0
        sys.stdin, sys.stdout = io.StringIO("not json{{{"), io.StringIO()
        try:
            rc3 = _hook()
        finally:
            sys.stdin, sys.stdout = old_stdin, old_stdout
        expect(rc3 == 0, "--hook mode on a malformed event must not crash (exit 0)")

    # main(): file-arg mode — a smelly file exits 1, a clean file exits 0
    with tempfile.TemporaryDirectory() as td:
        bad = os.path.join(td, "bad.md")
        good = os.path.join(td, "good.md")
        open(bad, "w", encoding="utf-8").write(cases["PERSONA"])
        open(good, "w", encoding="utf-8").write(clean)
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
        try:
            rc_bad = main([bad])
            rc_good = main([good])
            # negative control: an unreadable path must not crash — reported, not a false-clean silent pass
            missing = os.path.join(td, "does-not-exist.md")
            rc4 = main([missing])
            err = sys.stderr.getvalue()
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr
        expect(rc_bad == 1, "main() did not exit 1 on a file with a real structural smell")
        expect(rc_good == 0, "main() did not exit 0 on a clean file")
        expect(rc4 == 0, "an unreadable file alone should not itself count as a finding")
        expect("cannot read" in err, "an unreadable file did not report a cannot-read error")

    if fails:
        sys.stderr.write("brand-lint selftest: FAIL\n")
        for m in fails:
            sys.stderr.write(f"  - {m}\n")
        return 1
    print("brand-lint selftest: OK (clean prose passes; archetype/VMV/persona/brand-DNA each caught; "
          "values-without-trade-offs flagged, trade-off language + incidental word use both clear it; "
          "--hook mode is always advisory (exit 0) on smelly/clean/non-prose/malformed input; "
          "main() file mode exits 1/0 correctly and survives an unreadable path)")
    return 0


def main(argv):
    if argv and argv[0] == "selftest":
        return selftest()
    if "--hook" in argv:
        return _hook()
    args = [a for a in argv if not a.startswith("-")]
    if not args or argv == ["-"]:
        text = sys.stdin.read()
        findings = lint_text(text)
        print(_render("<stdin>", findings) if findings else "brand-lint: clean (no structural smells)")
        return 1 if findings else 0
    any_found = False
    for path in args:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as e:
            print(f"brand-lint: cannot read {path}: {e}", file=sys.stderr)
            continue
        findings = lint_text(text)
        if findings:
            any_found = True
            print(_render(path, findings))
        else:
            print(f"brand-lint: clean — {path}")
    return 1 if any_found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
