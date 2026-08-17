#!/usr/bin/env python3
"""pattern_census.py — grep-tier census for pattern-sweeping, with built-in census proofs.

Usage:
  pattern_census.py census --pattern NAME=REGEX [--pattern NAME=REGEX ...]
                           [--must-match STRING ...] [--must-not-match STRING ...]
                           PATH [PATH ...]
  pattern_census.py selftest

census: walks PATHs (files or directories), applies each named regex per line, and prints a JSON
report {total, patterns: {name: {hits, files: {path: count}}}, checks}. Exit 0 = census clean
(all checks passed); exit 1 = a check failed (undercount or over-match — the census is not
trustworthy); exit 2 = usage/config error. --must-match STRING fails the run unless STRING
appears in some matched line (known-member proof); --must-not-match STRING fails the run if
STRING appears in any matched line (known-nonmember proof).
"""

import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "dist", "build", ".claude"}


def iter_files(paths):
    for p in map(Path, paths):
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and not any(part in SKIP_DIRS for part in f.parts):
                    yield f


def census(args):
    patterns, musts, must_nots, paths = {}, [], [], []
    it = iter(args)
    for a in it:
        if a == "--pattern":
            name, _, rx = next(it, "").partition("=")
            if not rx:
                print("--pattern needs NAME=REGEX", file=sys.stderr)
                return 2
            patterns[name] = re.compile(rx)
        elif a == "--must-match":
            musts.append(next(it, ""))
        elif a == "--must-not-match":
            must_nots.append(next(it, ""))
        else:
            paths.append(a)
    if not patterns or not paths:
        print("need at least one --pattern and one PATH", file=sys.stderr)
        return 2

    report = {"total": 0, "patterns": {n: {"hits": 0, "files": {}} for n in patterns}}
    matched_lines = []
    for f in iter_files(paths):
        try:
            text = f.read_text(errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for name, rx in patterns.items():
                if rx.search(line):
                    entry = report["patterns"][name]
                    entry["hits"] += 1
                    entry["files"][str(f)] = entry["files"].get(str(f), 0) + 1
                    report["total"] += 1
                    matched_lines.append(line)

    checks = []
    for s in musts:
        ok = any(s in line for line in matched_lines)
        checks.append({"type": "must-match", "value": s, "ok": ok})
    for s in must_nots:
        ok = not any(s in line for line in matched_lines)
        checks.append({"type": "must-not-match", "value": s, "ok": ok})
    report["checks"] = checks
    print(json.dumps(report, indent=2))
    return 0 if all(c["ok"] for c in checks) else 1


def selftest():
    """Fixtures encode the two known grep-blindness classes + one over-match class."""
    import subprocess
    import tempfile

    me = str(Path(__file__).resolve())
    with tempfile.TemporaryDirectory() as td:
        fx = Path(td, "fixture.ts")
        fx.write_text(
            "const cfg = { style: 'flex:1;min-width:240px;' }\n"  # TS-assembled string
            "el.style = 'min-width: 0'\n"                          # load-bearing idiom
            "const icons = { 'chart-bar': chartBar,\n"             # quoted map entry
            "  robot,\n"                                           # shorthand property
            "}\n"
        )

        def run(*extra):
            return subprocess.run(
                [sys.executable, me, "census", *extra, td],
                capture_output=True, text=True,
            )

        failures = []

        # 1. Assembled-string blindness: a census given the assembled-string pattern MUST see
        #    the TS-built min-width; the known-member check proves it.
        r = run("--pattern", r"mw=min-width:\s*[1-9]", "--must-match", "min-width:240px")
        if r.returncode != 0:
            failures.append("assembled-string member not found (grep-blindness class 1)")

        # 2. Numeric vs semantic: the [1-9]-guarded pattern MUST NOT match min-width: 0.
        r = run("--pattern", r"mw=min-width:\s*[1-9]", "--must-not-match", "min-width: 0")
        if r.returncode != 0:
            failures.append("[1-9] guard matched min-width: 0 (load-bearing deletion class)")

        # 2b. Negative control: the naive [0-9] pattern DOES match min-width: 0 — the check
        #     must FAIL (exit 1), proving must-not-match actually bites.
        r = run("--pattern", r"mw=min-width:\s*[0-9]", "--must-not-match", "min-width: 0")
        if r.returncode != 1:
            failures.append("negative control passed — must-not-match is inert")

        # 3. Registry undercount: both quoted and shorthand entries must be countable, and the
        #    quoted-only pattern must fail the shorthand known-member check (exit 1).
        r = run("--pattern", r"reg=^\s*('?[a-z0-9-]+'?\s*:\s*\w+|[a-zA-Z0-9_]+,)\s*$",
                "--must-match", "robot,")
        if r.returncode != 0:
            failures.append("shorthand property missed by the both-forms pattern")
        r = run("--pattern", r"reg=^\s*'?[a-z0-9-]+'?\s*:", "--must-match", "robot,")
        if r.returncode != 1:
            failures.append("negative control passed — quoted-only pattern claimed the shorthand")

        if failures:
            print("SELFTEST FAIL:\n  " + "\n  ".join(failures))
            return 1
        print("SELFTEST OK: 5 checks (2 member proofs, 1 nonmember proof, 2 negative controls)")
        return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    if sys.argv[1] == "census":
        sys.exit(census(sys.argv[2:]))
    print(f"unknown command {sys.argv[1]!r}", file=sys.stderr)
    sys.exit(2)
