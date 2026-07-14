#!/usr/bin/env python3
"""corpus_check — mechanical validation of a knowledge pack's reference corpus.

Usage:
  corpus_check.py <skill-dir> [...]     validate pack(s) (needs references/INDEX.md to apply)
  corpus_check.py selftest              prove the counters bite

Rules (pack-authoring-standards, checkable slice):
  K1 INDEX <-> tree reconciliation, both directions: every references/*.md (except INDEX itself
     and .wave-* ledgers) appears in INDEX; every INDEX path names a real file  [FAIL]
  K2 load budget: any reference file over 1000 lines  [WARN]
  K3 grounding coverage: a reference file with zero [verified]/[inferred]/[drift-prone] markers  [WARN]
  K4 axis count: INDEX section headings outside 3-7  [WARN]
  K5 INDEX budget: over ~150 lines  [WARN]

A skill dir without references/INDEX.md is not a pack — reported as 'not a pack', exit 0.
Exit 0 clean/warnings, 1 on any FAIL.
"""
import re
import sys
from pathlib import Path

MARKER_RE = re.compile(r"\[(verified|inferred|drift-prone)\]")
LINK_RE = re.compile(r"([\w./-]+\.md)")


def check_pack(skill_dir: Path):
    refs = skill_dir / "references"
    index = refs / "INDEX.md"
    if not index.is_file():
        return None
    findings = []
    text = index.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    listed = set()
    for line in lines:
        for m in LINK_RE.findall(line):
            name = m[len("references/"):] if m.startswith("references/") else m
            if name != "INDEX.md":
                listed.add(name)
    on_disk = {str(p.relative_to(refs)) for p in refs.rglob("*.md")
               if p.name != "INDEX.md" and not p.name.startswith(".wave-")}

    for f in sorted(on_disk - listed):
        findings.append(("FAIL", "K1", f"references/{f} is not in INDEX.md -> unreachable file; add its ask line"))
    for f in sorted(listed - on_disk):
        findings.append(("FAIL", "K1", f"INDEX.md names references/{f} which does not exist -> ghost route; fix or cut the line"))

    for f in sorted(on_disk):
        p = refs / f
        n = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        if n > 1000:
            findings.append(("WARN", "K2", f"references/{f} is {n} lines (>1000) -> retrieval degrades; split by ask"))
        if not MARKER_RE.search(p.read_text(encoding="utf-8", errors="replace")):
            findings.append(("WARN", "K3", f"references/{f} has no grounding markers -> orphan claims; mark [verified]/[inferred]/[drift-prone]"))

    axes = [ln for ln in lines if ln.startswith("## ")]
    if axes and not (3 <= len(axes) <= 7):
        findings.append(("WARN", "K4", f"{len(axes)} axis headings in INDEX -> healthy range is 3-7; "
                                       f"{'consider skill-synthesize' if len(axes) < 3 else 'consider skill-decompose'}"))
    if len(lines) > 150:
        findings.append(("WARN", "K5", f"INDEX.md is {len(lines)} lines (>150) -> the pack may answer too many kinds of question"))
    return findings


def run(paths):
    worst = 0
    for path in paths:
        d = Path(path)
        fs = check_pack(d)
        if fs is None:
            print(f"corpus_check · not a pack (no references/INDEX.md) · {path}")
            continue
        verdict = "FAIL" if any(f[0] == "FAIL" for f in fs) else ("warn" if fs else "clean")
        print(f"corpus_check · {verdict} · {path}")
        for sev, code, msg in fs:
            print(f"  {sev:5} {code}  {msg}")
        worst = max(worst, 1 if verdict == "FAIL" else 0)
    return worst


def selftest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        d = Path(td) / "demo-pack"; refs = d / "references"; refs.mkdir(parents=True)
        (refs / "which-standard-applies.md").write_text("APCA vs WCAG. [verified] docs, 2026-07.")
        (refs / "how-to-mix.md").write_text("Mixing model. [inferred] from the spec.")
        (refs / "INDEX.md").write_text(
            "# INDEX\n## standards\nwhich-standard-applies.md — which contrast standard applies\n"
            "## mixing\nhow-to-mix.md — how to mix\n## history\nwhich-standard-applies.md — origins\n")
        assert not check_pack(d), f"clean pack must have zero findings, got {check_pack(d)}"
        assert check_pack(Path(td)) is None, "dir without INDEX is not a pack"
        (refs / "orphan.md").write_text("claims with no markers, " + "x\n" * 1200)
        (refs / "INDEX.md").write_text((refs / "INDEX.md").read_text() + "ghost-file.md — nothing\n")
        codes = {f[1] for f in check_pack(d)}
        assert {"K1", "K2", "K3"} <= codes, f"expected K1+K2+K3 in {codes}"
        assert any("orphan.md is not in INDEX" in f[2] for f in check_pack(d)), "unlisted file caught"
        assert any("ghost-file.md" in f[2] for f in check_pack(d)), "ghost route caught"
        (refs / ".wave-1-ledger.md").write_text("working ledger, exempt")
        assert not any(".wave-1" in f[2] for f in check_pack(d)), "wave ledgers exempt from K1"
    print("corpus_check selftest · PASS · reconciliation both directions, budgets, markers, ledger exemption")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "selftest":
        sys.exit(selftest())
    sys.exit(run(args))
