#!/usr/bin/env python3
"""pattern-audit scanner — deterministic match sweep for a caller-supplied pattern/instruction.

Sweeps a target tree for one or more literal, labeled regex probes and emits
a flat, structured dataset of matches (file/line/col/match/context/kind),
plus totals. All interpretation — natural-language instruction -> probe
compilation, false-positive judgment, downstream handoff — belongs to the
pattern-audit SKILL, never here: this script is deterministic and
instruction-blind, literal probes in, dataset out, selftest-provable.

Usage:
  scan.py --target PATH --pattern [LABEL=]REGEX [--pattern ...]
          [--glob GLOB ...] [--context N] [--json]
  scan.py selftest                 prove the counters bite

Exit codes: 0 scanned, no matches (CLEAN); 1 matches found (MATCHES);
2 usage error — target missing, invalid regex, or no files survived
filtering.

Note on [LABEL=]REGEX: the label split is on the FIRST `=` after a
label-shaped prefix, so a bare regex containing `=` (e.g. `a=b`) must carry
an explicit `LABEL=` prefix or it is mis-split (label `a`, regex `b`).
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Single-segment names pruned anywhere in the path, plus the one two-segment
# special case (.claude/worktrees — this repo's own campaign worktrees).
SKIP_DIR_NAMES = {".git", "node_modules", "dist", ".claude-plugin", ".refactor-attic"}
SKIP_TWO_SEGMENT = (".claude", "worktrees")

LABEL_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*)=(.*)$")
DEFAULT_LABEL = "match"


class ScanError(Exception):
    """A clean, expected usage failure — main() turns this into exit 2,
    never a traceback."""


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
    return False


def discover_files(target: Path, globs):
    """Every file under target, pruning SKIP_DIR_NAMES/.claude/worktrees and
    binaries (null-byte sniff on the first 8KB); --glob (repeatable) narrows
    the candidate set instead of the full recursive walk. A single-FILE target
    scans that one file (code-checker finding, 2026-08-15: it previously exited
    2 with a misleading "no files survived filtering")."""
    if target.is_file():
        return [] if is_binary(target) else [target]
    if globs:
        candidates = set()
        for g in globs:
            candidates.update(target.glob(g))
        files = sorted(p for p in candidates if p.is_file())
    else:
        files = sorted(p for p in target.rglob("*") if p.is_file())
    return [p for p in files if not under_skip_dir(p, target) and not is_binary(p)]


def parse_pattern_spec(spec: str):
    """[LABEL=]REGEX -> (label, regex_str, compiled). Bare regex defaults to
    kind DEFAULT_LABEL. Raises ScanError on an invalid regex — never lets
    re.error propagate as a traceback."""
    m = LABEL_RE.match(spec)
    if m:
        label, regex_str = m.group(1), m.group(2)
    else:
        label, regex_str = DEFAULT_LABEL, spec
    try:
        compiled = re.compile(regex_str)
    except re.error as e:
        raise ScanError(f"invalid regex in pattern {spec!r}: {e}")
    return label, regex_str, compiled


def rel(path: Path, target: Path) -> str:
    if path == target:
        return path.name  # single-FILE target: '.' would be useless in the dataset
    try:
        return str(path.relative_to(target))
    except ValueError:
        return str(path)


def analyze(target: Path, pattern_specs, globs=None, context: int = 0):
    """Core sweep logic, pure of argv/exit-code concerns so it is directly
    callable from both main() and selftest(). Raises ScanError on a usage
    failure (target missing, invalid regex, no files survived filtering).
    Returns the result dict on success — callers translate to exit codes."""
    if not target.exists():
        raise ScanError(f"target not found: {target}")

    probes = [parse_pattern_spec(spec) for spec in pattern_specs]

    files = discover_files(target, globs)
    if not files:
        raise ScanError(
            "no files survived filtering (skip-dir/binary/glob pruning left nothing to scan)"
        )

    raw_matches = []
    for path in files:
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        lines = text.split("\n")
        for label, _regex_str, compiled in probes:
            for lineno, line_text in enumerate(lines, start=1):
                for m in compiled.finditer(line_text):
                    col = m.start() + 1
                    if context and context > 0:
                        lo = max(0, lineno - 1 - context)
                        hi = min(len(lines), lineno + context)
                        ctx_text = "\n".join(lines[lo:hi])
                    else:
                        ctx_text = line_text
                    raw_matches.append(
                        (rel(path, target), lineno, col, m.group(0), ctx_text, label)
                    )

    # Stable id order: file-sorted, line-sorted, col-sorted — invariant
    # across reruns of an unchanged tree so a judged overlay or downstream
    # diff can key on it.
    raw_matches.sort(key=lambda t: (t[0], t[1], t[2]))
    width = max(3, len(str(len(raw_matches))))

    matches = []
    per_kind = {}
    files_with_matches = set()
    for i, (f, line, col, match_text, ctx_text, kind) in enumerate(raw_matches, start=1):
        matches.append({
            "id": f"m{i:0{width}d}",
            "file": f,
            "line": line,
            "col": col,
            "match": match_text,
            "context": ctx_text,
            "kind": kind,
        })
        per_kind[kind] = per_kind.get(kind, 0) + 1
        files_with_matches.add(f)

    return {
        "target": str(target),
        "probes": [
            {"label": label, "regex": regex_str, "globs": list(globs) if globs else []}
            for label, regex_str, _compiled in probes
        ],
        "files_scanned": len(files),
        "matches": matches,
        "totals": {
            "matches": len(matches),
            "files_with_matches": len(files_with_matches),
            "per_kind": per_kind,
        },
    }


def verdict_line(result):
    """The one non-JSON contract surface — selftest asserts THIS exact function's output,
    so a format drift in main()'s print can never pass silently (code-checker finding,
    2026-08-15: the prior fixture rebuilt the f-string locally, a tautology)."""
    n = result["totals"]["matches"]
    verdict = "MATCHES" if n else "CLEAN"
    return f"pattern-audit scan · {verdict} · {n} matches / {result['files_scanned']} files"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--pattern", action="append", dest="patterns", required=True)
    ap.add_argument("--glob", action="append", dest="globs")
    ap.add_argument("--context", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    target = Path(args.target).resolve()
    try:
        result = analyze(target, args.patterns, args.globs, args.context)
    except ScanError as e:
        print(f"pattern-audit scan: {e}")
        sys.exit(2)

    n = result["totals"]["matches"]

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(verdict_line(result))
        for m in result["matches"]:
            print(f"  [{m['kind']}] {m['file']}:{m['line']}:{m['col']} {m['match']!r} — {m['context']}")

    sys.exit(1 if n else 0)


def selftest():
    """Prove analyze()'s counters bite: a planted token is found with the
    right file/line/kind (positive); a clean tree scores zero matches
    (reverse); a bare regex defaults to kind 'match' (label plumbing); two
    probes partition totals.per_kind (multi-probe); --glob excludes an
    out-of-glob hit; skip-dir and binary pruning both apply; an invalid
    regex raises ScanError, never a traceback; an empty target raises
    ScanError rather than reporting a false-clean scan; ids are stable
    across two runs of an unchanged tree; the pinned verdict-line string is
    exact."""
    import tempfile

    # Positive control: a planted token is found with correct file/line/kind.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "sub").mkdir()
        (r / "sub" / "a.txt").write_text("line one\nTOKEN_HERE marks the spot\nline three\n")
        result = analyze(r, ["hit=TOKEN_HERE"])
        assert result["totals"]["matches"] == 1
        m = result["matches"][0]
        assert m["file"] == "sub/a.txt", "wrong file recorded"
        assert m["line"] == 2, "wrong line recorded"
        assert m["kind"] == "hit", "label must plumb through to kind"

    # Reverse control: a clean tree must score zero matches, not error.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "a.txt").write_text("nothing to see here\n")
        result = analyze(r, ["NEVER_MATCHES_ANYTHING_XYZ"])
        assert result["totals"]["matches"] == 0, "a clean tree must report zero matches"

    # Label plumbing: bare regex (no LABEL=) defaults to DEFAULT_LABEL.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "a.txt").write_text("plain PATTERNX here\n")
        result = analyze(r, ["PATTERNX"])
        assert result["matches"][0]["kind"] == DEFAULT_LABEL, "bare regex must default to 'match'"

    # Multi-probe: two probes partition totals.per_kind.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "a.txt").write_text("alpha thing\nbeta thing\n")
        result = analyze(r, ["a-kind=alpha", "b-kind=beta"])
        assert result["totals"]["per_kind"] == {"a-kind": 1, "b-kind": 1}, "two probes must partition per_kind"

    # Glob narrowing: excludes an out-of-glob hit.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "keep.md").write_text("NEEDLE inside markdown\n")
        (r / "skip.txt").write_text("NEEDLE inside text\n")
        result = analyze(r, ["NEEDLE"], globs=["*.md"])
        assert result["totals"]["matches"] == 1, "glob must exclude the non-matching file"
        assert result["matches"][0]["file"] == "keep.md"

    # Skip-dir + binary pruning both apply in the same sweep.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / ".git").mkdir()
        (r / ".git" / "hooked.txt").write_text("NEEDLE in git dir\n")
        (r / "binary.bin").write_bytes(b"NEEDLE\x00binary\x00stuff")
        (r / "clean.txt").write_text("NEEDLE in a real file\n")
        result = analyze(r, ["NEEDLE"])
        assert result["totals"]["matches"] == 1, "skip-dir and binary files must both be pruned"
        assert result["matches"][0]["file"] == "clean.txt"

    # Invalid regex -> ScanError, never a traceback (validate.py's #252 fail-clean precedent).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "a.txt").write_text("x\n")
        try:
            analyze(r, ["(unclosed"])
            raised = False
        except ScanError:
            raised = True
        assert raised, "an invalid regex must raise ScanError cleanly"

    # No files survived filtering -> ScanError, never a silent zero-match pass.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        try:
            analyze(r, ["anything"])
            raised = False
        except ScanError:
            raised = True
        assert raised, "an empty target must raise ScanError, not report a false-clean scan"

    # id stability across two runs of an unchanged tree.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "a.txt").write_text("NEEDLE one\nNEEDLE two\n")
        r1 = analyze(r, ["NEEDLE"])
        r2 = analyze(r, ["NEEDLE"])
        assert [m["id"] for m in r1["matches"]] == [m["id"] for m in r2["matches"]], "ids must be stable across reruns"

    # Verdict-line shape: assert the REAL helper main() prints (not a local rebuild —
    # the prior fixture was tautological), then the CLI's own exit tri-state + stdout
    # through actual subprocess runs of main().
    import subprocess
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "a.txt").write_text("NEEDLE\n")
        result = analyze(r, ["NEEDLE"])
        assert verdict_line(result) == "pattern-audit scan · MATCHES · 1 matches / 1 files", \
            "verdict-line shape must be pinned exactly"

        # exit 1 + pinned line on a match, through main() itself
        hit = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--pattern", "NEEDLE"],
            capture_output=True, text=True,
        )
        assert hit.returncode == 1, f"matches must exit 1, got {hit.returncode}"
        assert hit.stdout.splitlines()[0] == "pattern-audit scan · MATCHES · 1 matches / 1 files", \
            f"CLI verdict line drifted: {hit.stdout.splitlines()[0]!r}"

        # exit 0 + CLEAN on a miss
        clean = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--pattern", "ABSENT_TOKEN"],
            capture_output=True, text=True,
        )
        assert clean.returncode == 0, f"clean must exit 0, got {clean.returncode}"
        assert clean.stdout.startswith("pattern-audit scan · CLEAN ·"), \
            f"CLI clean line drifted: {clean.stdout!r}"

        # exit 2, no traceback, on an invalid regex
        bad = subprocess.run(
            [sys.executable, __file__, "--target", str(r), "--pattern", "["],
            capture_output=True, text=True,
        )
        assert bad.returncode == 2, f"ScanError must exit 2, got {bad.returncode}"
        assert "Traceback" not in bad.stderr, f"ScanError must not traceback: {bad.stderr}"

    # F3 (code-checker minor): a single-FILE --target scans that one file instead of
    # exiting 2 with a misleading "no files survived filtering".
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "one.md"
        f.write_text("NEEDLE here\n")
        single = analyze(f, ["NEEDLE"])
        assert single["totals"]["matches"] == 1, "a single-file target must be scanned"

    print(
        "pattern-audit scan selftest · PASS · match/label/multi-probe/glob/"
        "skip-dir/binary/regex/id/verdict counters bite"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    main()
