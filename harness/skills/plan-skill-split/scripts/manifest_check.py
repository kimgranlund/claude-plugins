#!/usr/bin/env python3
"""Validate a plan-skill-split manifest: reconciled file mapping, description budget, axis sizing.

Usage:
    python3 manifest_check.py <manifest.json>
    python3 manifest_check.py selftest

Exit 0 = clean (only soft warnings, if any). Exit 1 = a hard failure (see printed report).
This mirrors the *checker-as-gate* convention used across this corpus (harness_checks.py,
coverage_check.py, corpus_index.py): the script is the gate, the SKILL.md prose is the method.
"""
import json
import sys

DESC_LIMIT = 1024
AXIS_MIN, AXIS_MAX = 3, 7


def check(manifest):
    """Return (hard_failures: list[str], warnings: list[str])."""
    fails, warns = [], []

    verdict = manifest.get("verdict")
    if verdict not in ("split", "no-split", "partial"):
        fails.append(f"verdict must be 'split', 'no-split', or 'partial' — got {verdict!r}")
        return fails, warns

    if verdict == "no-split":
        if not manifest.get("rejected_alternatives") and not manifest.get("reasoning"):
            warns.append("no-split verdict carries no stated reasoning/rejected_alternatives — "
                         "a no-split call still needs a cited reason (D1)")
        return fails, warns

    packs = manifest.get("packs", [])
    if not packs:
        fails.append(f"verdict is {verdict!r} but 'packs' is empty")
        return fails, warns

    source = manifest.get("source_corpus", {})
    total_declared = source.get("total_files")

    seen = {}
    all_files = []
    for i, pack in enumerate(packs):
        name = pack.get("name", f"<pack {i}>")
        files = pack.get("files", [])
        if not files:
            fails.append(f"pack {name!r} has no files assigned")
        all_files.extend(files)
        for f in files:
            seen.setdefault(f, []).append(name)

        desc = pack.get("description", "")
        if not desc:
            fails.append(f"pack {name!r} has no description")
        elif len(desc) > DESC_LIMIT:
            fails.append(f"pack {name!r} description is {len(desc)} chars, over the "
                         f"{DESC_LIMIT}-char org export limit")

        axes = pack.get("axes", [])
        if len(axes) < AXIS_MIN or len(axes) > AXIS_MAX:
            warns.append(f"pack {name!r} has {len(axes)} axes, outside the healthy "
                        f"{AXIS_MIN}-{AXIS_MAX} range (pack-writing-rules doctrine) — verify this is deliberate")

        if "invocation_posture" not in pack:
            fails.append(f"pack {name!r} has no stated invocation_posture — D5 requires a deliberate decision")

    dupes = {f: names for f, names in seen.items() if len(names) > 1}
    if dupes:
        for f, names in dupes.items():
            fails.append(f"file {f!r} assigned to multiple packs: {names}")

    if total_declared is not None:
        if len(all_files) != total_declared:
            fails.append(f"assigned file count ({len(all_files)}) != declared total_files "
                        f"({total_declared}) — every source file must be assigned exactly once")

    if verdict == "split" and not manifest.get("rejected_alternatives"):
        warns.append("split verdict with no rejected_alternatives — the recursive check "
                    "(sub-splits within this split) may have been skipped (D3)")

    if not manifest.get("referrer_repair_map") and verdict in ("split", "partial"):
        warns.append("no referrer_repair_map present — confirm the corpus-wide referrer "
                    "survey (D6) actually ran, even if the result was an empty map")

    return fails, warns


def report(fails, warns, label):
    print(f"plan-skill-split manifest check — {label}")
    for w in warns:
        print(f"  [WARN] {w}")
    for f in fails:
        print(f"  [FAIL] {f}")
    if not fails and not warns:
        print("  clean — no findings")
    print(f"  -> {'FAIL' if fails else 'PASS'} ({len(fails)} hard failure(s), {len(warns)} warning(s))")
    return 1 if fails else 0


def selftest():
    good = {
        "source_corpus": {"path": "skills/example", "total_files": 3},
        "verdict": "split",
        "packs": [
            {"name": "example-alpha", "files": ["a.md", "b.md"], "axes": ["x", "y", "z"],
             "description": "d" * 100, "invocation_posture": "default"},
            {"name": "example-beta", "files": ["c.md"], "axes": ["p", "q", "r"],
             "description": "d" * 100, "invocation_posture": "default"},
        ],
        "rejected_alternatives": [{"candidate": "example-gamma", "reason": "thin"}],
        "referrer_repair_map": [],
    }
    fails, warns = check(good)
    assert not fails, f"good fixture should have zero hard failures, got: {fails}"

    bad = {
        "source_corpus": {"path": "skills/example", "total_files": 5},
        "verdict": "split",
        "packs": [
            {"name": "example-alpha", "files": ["a.md", "b.md"], "axes": ["x"],
             "description": "d" * (DESC_LIMIT + 1)},  # over budget, no invocation_posture
            {"name": "example-beta", "files": ["b.md"], "axes": ["p", "q", "r"],
             "description": "d" * 100, "invocation_posture": "default"},  # dupes b.md
        ],
    }
    fails, warns = check(bad)
    assert any("over the" in f for f in fails), "should catch over-budget description"
    assert any("invocation_posture" in f for f in fails), "should catch missing invocation_posture"
    assert any("multiple packs" in f for f in fails), "should catch duplicate file assignment"
    assert any("!=" in f for f in fails), "should catch file-count mismatch (2 assigned incl. dup vs total 3)"

    print("selftest: PASS — good fixture clean, bad fixture caught (over-budget desc, "
          "missing posture, duplicate file, count mismatch)")
    return 0


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    if sys.argv[1] == "selftest":
        return selftest()
    with open(sys.argv[1]) as fh:
        manifest = json.load(fh)
    fails, warns = check(manifest)
    return report(fails, warns, sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
