#!/usr/bin/env python3
"""recurrence-audit scanner — deterministic ledger-inventory sweep (IDR-0006's primary measure).

Walks a target tree for two things, always kept separate:

1. Seeded `LEDGER-CLASS:` tags — a per-incident-class citation convention this skill's own
   build ships (lld-0011): `LEDGER-CLASS: <slug> | ids: #NNN[, #NNN...] | mechanized:
   YYYY-MM-DD`. Grep-able plain text, no bracket syntax (this estate's `[[skill-name]]` form is
   already a cross-reference convention — a second bracket-shaped marker would collide
   visually). Works unmodified in markdown prose, a Python/JS trailing comment, or a fixture's
   string value.
2. The bare-citation baseline — `#NNN` issue-number references inside `.md` files only (doctrine
   bullets / SKILL.md is where the overwhelming majority of citations already live; counting
   bare `#N` across code/config would drown in hex colors, anchors, and unrelated comments).

All interpretation — the live `gh issue` conjunct-A check, the per-class recurrence verdict,
rendering — belongs to the recurrence-audit SKILL, never here: this script is deterministic and
network-blind, selftest-provable offline.

Usage:
  scan.py --target PATH [--json]
  scan.py selftest                 prove the counters bite

Exit codes: 0 scanned, zero seeded LEDGER-CLASS entries (bare-citation baseline only);
1 at least one seeded class found; 2 usage error — target missing, or nothing survived the
skip-dir/binary filter.
"""

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIR_NAMES = {".git", "node_modules", "dist", ".claude-plugin", ".refactor-attic"}
SKIP_TWO_SEGMENT = (".claude", "worktrees")
# This skill's OWN directory is excluded from the sweep, deliberately — its bundled scripts'
# selftest fixtures and its own LLD/SKILL.md necessarily contain example LEDGER-CLASS: text
# (illustrating the tag's shape, or proving the parser), which is not a real citation about a
# production incident. Same self-exclusion principle a linter applies to its own fixture corpus
# (measured 2026-08-18: without this, scan.py's own selftest strings surfaced as 7 phantom
# seeded classes on the very first real run against this estate).
SKIP_SELF_PREFIX = ("authorkit", "skills", "recurrence-audit")

LEDGER_TAG_RE = re.compile(
    r"LEDGER-CLASS:\s*(?P<slug>[\w-]+)\s*\|\s*ids:\s*(?P<ids>[^|]+?)\s*\|\s*mechanized:\s*(?P<date>\d{4}-\d{2}-\d{2})"
)
ID_RE = re.compile(r"#\d+")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BARE_CITATION_RE = re.compile(r"(?<!#)#(\d{2,4})\b")


class ScanError(Exception):
    """A clean, expected usage failure — main() turns this into exit 2, never a traceback."""


def is_binary(path: Path) -> bool:
    try:
        chunk = path.open("rb").read(8192)
    except OSError:
        return True
    return b"\x00" in chunk


def under_skip_dir(path: Path, target: Path) -> bool:
    try:
        parts = path.relative_to(target).parts
    except ValueError:
        parts = path.parts
    if any(p in SKIP_DIR_NAMES for p in parts):
        return True
    for i in range(len(parts) - 1):
        if (parts[i], parts[i + 1]) == SKIP_TWO_SEGMENT:
            return True
    n = len(SKIP_SELF_PREFIX)
    for i in range(len(parts) - n + 1):
        if parts[i:i + n] == SKIP_SELF_PREFIX:
            return True
    return False


def discover_files(target: Path):
    if target.is_file():
        return [] if is_binary(target) else [target]
    files = sorted(p for p in target.rglob("*") if p.is_file())
    return [p for p in files if not under_skip_dir(p, target) and not is_binary(p)]


def rel(path: Path, target: Path) -> str:
    if path == target:
        return path.name
    try:
        return str(path.relative_to(target))
    except ValueError:
        return str(path)


def analyze(target: Path):
    """Core sweep logic, pure of argv/exit-code concerns. Raises ScanError on a usage
    failure. Returns the result dict on success — callers translate to exit codes."""
    if not target.exists():
        raise ScanError(f"target not found: {target}")

    files = discover_files(target)
    if not files:
        raise ScanError(
            "no files survived filtering (skip-dir/binary pruning left nothing to scan)"
        )

    classes = {}  # slug -> {"ids": [...], "mechanized": date, "citations": [...]}
    bare_files = set()
    bare_count = 0

    for path in files:
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        f = rel(path, target)
        lines = text.split("\n")

        for lineno, line_text in enumerate(lines, start=1):
            for m in LEDGER_TAG_RE.finditer(line_text):
                slug = m.group("slug")
                ids_raw = m.group("ids")
                date = m.group("date")
                ids = ID_RE.findall(ids_raw)
                # A malformed tag (no ids parsed, or an unparseable date) is skipped
                # entirely — never crashes, never silently counted as seeded.
                if not ids or not DATE_RE.match(date):
                    continue
                entry = classes.setdefault(
                    slug, {"class": slug, "ids": [], "mechanized": date, "citations": []}
                )
                for i in ids:
                    if i not in entry["ids"]:
                        entry["ids"].append(i)
                entry["citations"].append({"file": f, "line": lineno})

        if path.suffix == ".md":
            for lineno, line_text in enumerate(lines, start=1):
                # A LEDGER-CLASS line's own ids are structured citations, not bare ones —
                # exclude that line from the bare-citation baseline so the two counters stay
                # genuinely independent (never double-counted).
                if LEDGER_TAG_RE.search(line_text):
                    continue
                hits = BARE_CITATION_RE.findall(line_text)
                if hits:
                    bare_count += len(hits)
                    bare_files.add(f)

    seeded_classes = sorted(classes.values(), key=lambda c: c["class"])
    seeded_citations = sum(len(c["citations"]) for c in seeded_classes)

    return {
        "target": str(target),
        "files_scanned": len(files),
        "seeded_classes": seeded_classes,
        "bare_citations": {"count": bare_count, "files": len(bare_files)},
        "totals": {
            "seeded_classes": len(seeded_classes),
            "seeded_citations": seeded_citations,
            "bare_citations": bare_count,
        },
    }


def verdict_line(result):
    n = result["totals"]["seeded_classes"]
    verdict = "SEEDED" if n else "BASELINE-ONLY"
    return (
        f"recurrence-audit scan · {verdict} · {n} seeded classes / "
        f"{result['totals']['bare_citations']} bare citations / {result['files_scanned']} files"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    try:
        result = analyze(target)
    except ScanError as e:
        print(f"recurrence-audit scan: {e}")
        sys.exit(2)

    n = result["totals"]["seeded_classes"]

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(verdict_line(result))
        for c in result["seeded_classes"]:
            print(f"  [{c['class']}] ids={c['ids']} mechanized={c['mechanized']}"
                  f" ({len(c['citations'])} citation(s))")

    sys.exit(1 if n else 0)


def selftest():
    """Prove analyze()'s counters bite: a planted LEDGER-CLASS tag is found with correct
    slug/ids/mechanized/citations (positive); a bare-citation-only tree scores zero seeded
    classes and a nonzero baseline (reverse — proves the two counters are independent, not
    one masquerading as the other); two ids under one slug group correctly (multi-id); two
    different slugs stay separate (no cross-class bleed); a malformed tag is skipped, never
    crashes and never silently counted (negative control); skip-dir + binary pruning; an
    empty target raises ScanError, never a false-clean scan; the verdict line is pinned
    exactly; ids/output stable across two runs of an unchanged tree."""
    import tempfile

    # Positive control: a planted LEDGER-CLASS tag is found with the right fields.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "Some doctrine bullet.\n"
            "LEDGER-CLASS: watch-exit-0 | ids: #530, #546 | mechanized: 2026-08-14\n"
        )
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 1
        c = result["seeded_classes"][0]
        assert c["class"] == "watch-exit-0"
        assert c["ids"] == ["#530", "#546"], c["ids"]
        assert c["mechanized"] == "2026-08-14"
        assert c["citations"][0]["file"] == "doc.md"
        assert c["citations"][0]["line"] == 2

    # Reverse control: bare citations only -> zero seeded classes, nonzero baseline.
    # Proves the two counters are independent, not one masquerading as the other.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text("Fixed by the gate (#183) after a repeat of (#199).\n")
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 0
        assert result["totals"]["bare_citations"] == 2, result["totals"]

    # Multi-id: two ids under one slug group into one class entry, not two.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "LEDGER-CLASS: dup-slot | ids: #100 | mechanized: 2026-01-01\n"
            "LEDGER-CLASS: dup-slot | ids: #101 | mechanized: 2026-01-01\n"
        )
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 1
        assert set(result["seeded_classes"][0]["ids"]) == {"#100", "#101"}
        assert len(result["seeded_classes"][0]["citations"]) == 2

    # No cross-class bleed: two different slugs stay separate totals.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "LEDGER-CLASS: alpha-class | ids: #1 | mechanized: 2026-01-01\n"
            "LEDGER-CLASS: beta-class | ids: #2 | mechanized: 2026-01-02\n"
        )
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 2
        slugs = {c["class"] for c in result["seeded_classes"]}
        assert slugs == {"alpha-class", "beta-class"}

    # Malformed-tag negative control: missing ids, or an unparseable date, is skipped
    # entirely — never crashes, never silently counted as seeded.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "LEDGER-CLASS: no-ids-here | ids:  | mechanized: 2026-01-01\n"
            "LEDGER-CLASS: bad-date | ids: #5 | mechanized: not-a-date\n"
        )
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 0, result["totals"]

    # Skip-dir + binary pruning both apply in the same sweep.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / ".git").mkdir()
        (r / ".git" / "hooked.md").write_text(
            "LEDGER-CLASS: hidden | ids: #9 | mechanized: 2026-01-01\n"
        )
        (r / "binary.bin").write_bytes(b"LEDGER-CLASS\x00 stuff")
        (r / "clean.md").write_text("nothing incident-shaped here\n")
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 0
        assert result["files_scanned"] == 1, "only clean.md should survive pruning"

    # Self-exclusion: this skill's OWN directory never contributes phantom seeded classes
    # from its own selftest fixtures / doc examples (the incident this fixture proves fixed,
    # 2026-08-18 — measured 7 phantom hits on the first real estate run before this landed).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        own = r / "authorkit" / "skills" / "recurrence-audit" / "scripts"
        own.mkdir(parents=True)
        (own / "scan.py").write_text(
            "LEDGER-CLASS: phantom | ids: #1, #2 | mechanized: 2026-01-01\n"
        )
        (r / "real.md").write_text(
            "LEDGER-CLASS: real-class | ids: #3 | mechanized: 2026-01-01\n"
        )
        result = analyze(r)
        assert result["totals"]["seeded_classes"] == 1, (
            "the skill's own directory must never contribute a phantom seeded class: "
            f"{result['seeded_classes']}"
        )
        assert result["seeded_classes"][0]["class"] == "real-class"

    # Empty target -> ScanError, never a false-clean scan.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        try:
            analyze(r)
            raised = False
        except ScanError:
            raised = True
        assert raised, "an empty target must raise ScanError, not report a false-clean scan"

    # Verdict-line shape pinned exactly, through the real helper (not a local rebuild).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "LEDGER-CLASS: x | ids: #100 | mechanized: 2026-01-01\nsome (#77) citation too\n"
        )
        result = analyze(r)
        assert verdict_line(result) == (
            "recurrence-audit scan · SEEDED · 1 seeded classes / 1 bare citations / 1 files"
        ), verdict_line(result)

    # CLI exit tri-state through actual subprocess runs of main().
    import subprocess

    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "LEDGER-CLASS: x | ids: #1 | mechanized: 2026-01-01\n"
        )
        seeded = subprocess.run(
            [sys.executable, __file__, "--target", str(r)],
            capture_output=True, text=True,
        )
        assert seeded.returncode == 1, f"seeded classes must exit 1, got {seeded.returncode}"
        assert seeded.stdout.splitlines()[0].startswith(
            "recurrence-audit scan · SEEDED ·"
        ), seeded.stdout

    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text("no seeded tags, just prose\n")
        baseline = subprocess.run(
            [sys.executable, __file__, "--target", str(r)],
            capture_output=True, text=True,
        )
        assert baseline.returncode == 0, f"baseline-only must exit 0, got {baseline.returncode}"
        assert baseline.stdout.startswith(
            "recurrence-audit scan · BASELINE-ONLY ·"
        ), baseline.stdout

    missing = subprocess.run(
        [sys.executable, __file__, "--target", "/no/such/path/xyz"],
        capture_output=True, text=True,
    )
    assert missing.returncode == 2, f"missing target must exit 2, got {missing.returncode}"
    assert "Traceback" not in missing.stderr, f"ScanError must not traceback: {missing.stderr}"

    # id/output stability across two runs of an unchanged tree.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "doc.md").write_text(
            "LEDGER-CLASS: stable | ids: #1, #2 | mechanized: 2026-01-01\n"
        )
        r1 = analyze(r)
        r2 = analyze(r)
        assert r1 == r2, "output must be stable across reruns of an unchanged tree"

    print(
        "recurrence-audit scan selftest · PASS · seeded/bare/multi-id/multi-class/"
        "malformed/skip-dir/binary/empty-target/verdict/stability counters bite"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    main()
