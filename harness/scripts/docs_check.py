#!/usr/bin/env python3
"""docs_check — mechanical freshness of a plugin's human-facing docs.

Usage:
  docs_check.py <plugin-root>     validate README.md / MANUAL.md / CLAUDE.md coverage
  docs_check.py selftest          prove the counters bite

Rules (the checkable slice; description *accuracy* stays with /ship-plugin and /check-everything):
  R1 [FAIL] every skills/<name> appears in README.md
  R2 [FAIL] every skills/<name> appears in MANUAL.md (skipped if no MANUAL.md)
  R3 [FAIL] README footer's version equals .claude-plugin/plugin.json version
  R4 [WARN] CLAUDE.md's stated skill count matches the tree (skipped if no CLAUDE.md — it
            doesn't ship in the artifact)
  R5 [WARN] every scripts/*.py is mentioned in README.md
  R6 [WARN] footer ledger entries stay one physical line each (plugin-writing-rules' cap,
            issue #203: no more than one `vX.Y.Z · date ·` marker per line, no line past
            600 chars — the unbounded-paragraph-append shape caught once at 157 KB)

Exit 0 clean/warnings, 1 on any FAIL.
"""
import json
import re
import sys
from pathlib import Path


def check(root: Path):
    findings = []
    skills = sorted(p.parent.name for p in root.glob("skills/*/SKILL.md"))
    readme = root / "README.md"
    if not readme.is_file():
        return [("FAIL", "R1", "no README.md at plugin root -> the version ledger is mandatory")]
    rd = readme.read_text(encoding="utf-8", errors="replace")

    for s in skills:
        if s not in rd:
            findings.append(("FAIL", "R1", f"skills/{s} has no mention in README.md -> add its map row"))

    manual = root / "MANUAL.md"
    if manual.is_file():
        md = manual.read_text(encoding="utf-8", errors="replace")
        for s in skills:
            if s not in md:
                findings.append(("FAIL", "R2", f"skills/{s} is undocumented in MANUAL.md -> users can't discover it"))

    try:
        version = json.loads((root / ".claude-plugin" / "plugin.json").read_text()).get("version", "")
    except (OSError, ValueError):
        version = ""
    m = re.search(r"^v(\d+\.\d+\.\d+)\b", rd, re.M)
    if not m:
        findings.append(("FAIL", "R3", "README carries no `vX.Y.Z` footer ledger line"))
    elif version and m.group(1) != version:
        findings.append(("FAIL", "R3", f"README footer says v{m.group(1)} but plugin.json says {version} "
                                       "-> the ledger lies about the current release"))

    claude_md = root / "CLAUDE.md"
    if claude_md.is_file():
        cm = claude_md.read_text(encoding="utf-8", errors="replace")
        c = re.search(r"\((\d+),", cm)
        if c and int(c.group(1)) != len(skills):
            findings.append(("WARN", "R4", f"CLAUDE.md states {c.group(1)} skills; tree has {len(skills)} -> stale count"))

    for sc in sorted(root.glob("scripts/*.py")):
        if sc.name not in rd:
            findings.append(("WARN", "R5", f"scripts/{sc.name} is not mentioned in README.md"))

    ledger_marker = re.compile(r"v\d+\.\d+\.\d+ · \d{4}-\d{2}-\d{2} · ")
    for line in rd.splitlines():
        hits = len(ledger_marker.findall(line))
        if hits >= 2:
            findings.append(("WARN", "R6",
                              f"{hits} ledger entries blobbed onto one line -> split to one entry per line "
                              f"({line[:60]}...)"))
        elif hits == 1 and len(line) > 600:
            findings.append(("WARN", "R6",
                              f"ledger entry line is {len(line)} chars -> compress to one-line-per-version "
                              f"(plugin-writing-rules' cap, issue #203) ({line[:60]}...)"))
    return findings


def run(root: Path):
    fs = check(root)
    verdict = "FAIL" if any(f[0] == "FAIL" for f in fs) else ("warn" if fs else "clean")
    print(f"docs_check · {verdict} · {root}")
    for sev, code, msg in fs:
        print(f"  {sev:5} {code}  {msg}")
    return 1 if verdict == "FAIL" else 0


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / ".claude-plugin").mkdir()
        (r / ".claude-plugin" / "plugin.json").write_text('{"name": "demo", "version": "1.2.0"}')
        (r / "skills" / "demo-review").mkdir(parents=True)
        (r / "skills" / "demo-review" / "SKILL.md").write_text("x")
        (r / "scripts").mkdir()
        (r / "scripts" / "demo_check.py").write_text("x")
        (r / "README.md").write_text("map: demo-review · demo_check.py\n\nv1.2.0 · ledger\n")
        (r / "MANUAL.md").write_text("use demo-review\n")
        (r / "CLAUDE.md").write_text("skills (1, each)\n")
        assert not check(r), f"clean fixture must pass, got {check(r)}"
        (r / "skills" / "demo-forge").mkdir()
        (r / "skills" / "demo-forge" / "SKILL.md").write_text("x")
        codes = {f[1] for f in check(r)}
        assert {"R1", "R2", "R4"} <= codes, f"undocumented skill + stale count must fire, got {codes}"
        (r / "README.md").write_text("map: demo-review demo-forge demo_check.py\n\nv1.1.0 · ledger\n")
        (r / "MANUAL.md").write_text("demo-review demo-forge\n")
        assert any(f[1] == "R3" for f in check(r)), "version mismatch must fail R3"

        # R6: one-line-per-version ledger cap (issue #203) — negative control first.
        good_line = "v1.2.0 · 2026-08-13 · a compact one-line summary of the bump\n"
        (r / "README.md").write_text(
            "map: demo-review demo-forge demo_check.py\n\nv1.2.0 · ledger\n\n" + good_line
        )
        (r / "MANUAL.md").write_text("demo-review demo-forge\n")
        assert not any(f[1] == "R6" for f in check(r)), "a clean one-liner must not fire R6"
        blobbed = (
            "v1.2.0 · 2026-08-13 · first entry · v1.1.0 · 2026-08-12 · second entry blobbed onto the same line\n"
        )
        (r / "README.md").write_text(
            "map: demo-review demo-forge demo_check.py\n\nv1.2.0 · ledger\n\n" + blobbed
        )
        assert any(f[1] == "R6" for f in check(r)), "two markers on one line must fire R6"
        overlong = "v1.2.0 · 2026-08-13 · " + ("padding " * 90) + "\n"
        (r / "README.md").write_text(
            "map: demo-review demo-forge demo_check.py\n\nv1.2.0 · ledger\n\n" + overlong
        )
        assert any(f[1] == "R6" for f in check(r)), "a >600-char single entry must fire R6"
    print("docs_check selftest · PASS · coverage both docs, version ledger, stale count, script mentions, ledger one-liner cap")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(Path(args[0]).resolve()))
