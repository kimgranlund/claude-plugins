#!/usr/bin/env python3
"""Validate a plan-skill-merge manifest: reconciled consolidation, description budget, delta stated.

Usage:
    python3 consolidation_check.py <manifest.json>
    python3 consolidation_check.py selftest

Exit 0 = clean (only soft warnings, if any). Exit 1 = a hard failure (see printed report).
The counterpart to plan-skill-split/scripts/manifest_check.py — same checker-as-gate convention.
"""
import json
import sys

DESC_LIMIT = 1024
AXIS_MIN, AXIS_MAX = 3, 7


def check(manifest):
    """Return (hard_failures: list[str], warnings: list[str])."""
    fails, warns = [], []

    verdict = manifest.get("verdict")
    if verdict not in ("consolidate", "keep-separate"):
        fails.append(f"verdict must be 'consolidate' or 'keep-separate' — got {verdict!r}")
        return fails, warns

    if verdict == "keep-separate":
        if not manifest.get("reasoning") and not manifest.get("source_candidates"):
            warns.append("keep-separate verdict carries no stated reasoning — "
                         "a keep-separate call still needs cited evidence (D1)")
        return fails, warns

    candidates = manifest.get("source_candidates", [])
    if len(candidates) < 2:
        fails.append(f"verdict is 'consolidate' but only {len(candidates)} source_candidate(s) "
                     "given — synthesis needs at least two")

    target = manifest.get("target_pack")
    if not target:
        fails.append("verdict is 'consolidate' but no target_pack given")
        return fails, warns

    desc = target.get("description", "")
    if not desc:
        fails.append("target_pack has no description")
    elif len(desc) > DESC_LIMIT:
        fails.append(f"target_pack description is {len(desc)} chars, over the "
                     f"{DESC_LIMIT}-char org export limit")

    if "invocation_posture" not in target:
        fails.append("target_pack has no stated invocation_posture — D-gate requires a deliberate decision")

    axes = target.get("axes", [])
    if len(axes) < AXIS_MIN or len(axes) > AXIS_MAX:
        warns.append(f"target_pack has {len(axes)} axes, outside the healthy "
                    f"{AXIS_MIN}-{AXIS_MAX} range — if this trips, self-check against "
                    "plan-skill-split before shipping (D4): the merge may just be a relabeled monolith")

    # Reconcile every candidate file: must appear in file_map as either moved or superseded.
    all_candidate_files = set()
    for c in candidates:
        for f in c.get("files", []):
            all_candidate_files.add((c["name"], f))

    file_map = target.get("file_map", [])
    accounted = set()
    for entry in file_map:
        key = (entry.get("from"), entry.get("file"))
        accounted.add(key)
        if "superseded_by" in entry and "reason" not in entry:
            fails.append(f"file {entry.get('file')!r} marked superseded_by but has no 'reason' — "
                        "duplicates must never be silently dropped (D3)")

    missing = all_candidate_files - accounted
    if missing:
        for name, f in sorted(missing):
            fails.append(f"candidate file {f!r} from {name!r} is not accounted for in file_map "
                        "(not moved, not superseded, not flagged as a gap)")

    if not target.get("flagged_gaps") and manifest.get("_has_known_gaps"):
        warns.append("manifest hints at known gaps but flagged_gaps is empty — check D7 (gap honesty)")

    delta = manifest.get("context_efficiency_delta")
    if not delta:
        fails.append("no context_efficiency_delta given — an efficiency claim with no number fails D5")
    else:
        before = delta.get("before_chars_total")
        after = delta.get("after_chars_total")
        if before is None or after is None:
            fails.append("context_efficiency_delta missing before_chars_total/after_chars_total")
        elif after >= before:
            warns.append(f"after_chars_total ({after}) is not smaller than before_chars_total "
                        f"({before}) — the consolidation may not actually be more efficient")

    if not manifest.get("referrer_repair_map"):
        warns.append("no referrer_repair_map present — confirm the union-of-all-candidates "
                    "referrer survey (D6) actually ran, even if the result was an empty map")

    return fails, warns


def report(fails, warns, label):
    print(f"plan-skill-merge consolidation check — {label}")
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
        "source_candidates": [
            {"name": "old-a", "files": ["r1.md", "r2.md"]},
            {"name": "old-b", "files": ["r3.md"]},
        ],
        "verdict": "consolidate",
        "target_pack": {
            "name": "new-pack",
            "axes": ["x", "y", "z"],
            "file_map": [
                {"file": "r1.md", "from": "old-a"},
                {"file": "r2.md", "from": "old-a", "superseded_by": "r3.md", "reason": "r3 is more current"},
                {"file": "r3.md", "from": "old-b"},
            ],
            "flagged_gaps": [],
            "description": "d" * 100,
            "invocation_posture": "default",
        },
        "context_efficiency_delta": {"before_chars_total": 1000, "after_chars_total": 600,
                                      "packs_before": 2, "packs_after": 1},
        "referrer_repair_map": [],
    }
    fails, warns = check(good)
    assert not fails, f"good fixture should have zero hard failures, got: {fails}"

    bad = {
        "source_candidates": [
            {"name": "old-a", "files": ["r1.md", "r2.md"]},
            {"name": "old-b", "files": ["r3.md"]},
        ],
        "verdict": "consolidate",
        "target_pack": {
            "name": "new-pack",
            "axes": ["x"],
            "file_map": [
                {"file": "r1.md", "from": "old-a"},
                {"file": "r2.md", "from": "old-a", "superseded_by": "r3.md"},  # missing 'reason'
                # r3.md from old-b never accounted for -> orphan
            ],
            "description": "d" * (DESC_LIMIT + 1),  # over budget, no invocation_posture
        },
        "context_efficiency_delta": {"before_chars_total": 500, "after_chars_total": 900},  # got bigger
    }
    fails, warns = check(bad)
    assert any("over the" in f for f in fails), "should catch over-budget description"
    assert any("invocation_posture" in f for f in fails), "should catch missing invocation_posture"
    assert any("not accounted for" in f for f in fails), "should catch orphaned candidate file"
    assert any("no 'reason'" in f for f in fails), "should catch superseded_by with no reason"
    assert any("not smaller" in w for w in warns), "should warn when after >= before"

    print("selftest: PASS — good fixture clean, bad fixture caught (over-budget desc, "
          "missing posture, orphaned file, unreasoned duplicate, non-improving delta)")
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
