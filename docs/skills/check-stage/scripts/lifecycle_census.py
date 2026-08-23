#!/usr/bin/env python3
"""lifecycle_census.py — read-only typed-record census for the check-stage skill.

Usage:
  lifecycle_census.py [<repo-root>]     print the JSON snapshot
  lifecycle_census.py selftest          prove the parsers on inline fixtures

No args defaults the root to `.` — mirrors check-state's doc_state.py collector
(a deliberate, disclosed deviation from the no-args-prints-usage anatomy: the
default target is meaningful for a collector).

Walks `<docs-root>/{adr,idr,rdd}/*.md`, parses doc_lint-compatible frontmatter,
and emits per-type counts, status distributions, and the orphan-ADR (doc_lint's
T6 WARN — no `intent-refs:` citation) count, plus roadmap presence/status —
root `ROADMAP.md` first, else the typed `<docs-root>/roadmap/*.md` (#882). Reuses docs/scripts/doc_lint.py's own TYPES/LEDGER_LOCK contract
(sources-flow-outward) rather than re-declaring the type/status enums here.

`<docs-root>` resolves per doc-writing-rules' "Where documents live" ladder
(issue #514): `docs/ops/` if it exists at the repo root, else `.claude/docs/`
if THAT exists, else `docs/ops/` (the portable default, reported as all-zero
counts when nothing has been filed there yet). This script does not parse a
host CLAUDE.md's stated override text — presence-based degrade only.

This is the SCRIPT-DETECTABLE half only (PRD resolution (b)) — presence, counts,
status distributions. The judgment-tier reading (POC boundary crossed, which loop
is emphasized, bug-vs-requirement-gap, whether Retro lessons landed) is narrated
by the check-stage skill body from this JSON plus other project signals; it is
never computed here.

Exit: 0 snapshot printed · 1 unexpected failure · 2 usage.
Selftest: 0 proven · 1 a control failed.
"""
import importlib.util
import json
import sys
from pathlib import Path

LEDGER_TYPES = ("adr", "idr", "rdd")


def load_doc_lint():
    """Import docs/scripts/doc_lint.py by path — a same-plugin sibling script,
    never a cross-plugin import (plugin-authoring.md's hard-boundary rule is for
    preloads/${CLAUDE_PLUGIN_ROOT} paths crossing PLUGINS, not sibling scripts
    inside one plugin's own scripts/ tree)."""
    here = Path(__file__).resolve()
    doc_lint_path = here.parent.parent.parent.parent / "scripts" / "doc_lint.py"
    spec = importlib.util.spec_from_file_location("doc_lint", doc_lint_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def resolve_docs_root(root):
    """doc-writing-rules' host-override ladder, presence-based (no CLAUDE.md parsing):
    `docs/ops/` wins if it exists, else `.claude/docs/` if that exists, else the
    portable default `docs/ops/` (reported empty when nothing's filed there yet)."""
    ops_root = Path(root) / "docs" / "ops"
    legacy_root = Path(root) / ".claude" / "docs"
    if ops_root.is_dir():
        return ops_root
    if legacy_root.is_dir():
        return legacy_root
    return ops_root


def census_dir(docs_root, dtype, parse_frontmatter):
    d = docs_root / dtype
    files = sorted(d.glob("*.md")) if d.is_dir() else []
    statuses = {}
    orphans = 0
    for p in files:
        fm = parse_frontmatter(p.read_text(errors="replace")) or {}
        status = fm.get("status", "unknown")
        statuses[status] = statuses.get(status, 0) + 1
        if dtype == "adr":
            intent_refs = fm.get("intent-refs", "").strip().lower()
            if intent_refs in ("", "null", "none", "[]"):
                orphans += 1
    entry = {"count": len(files), "status_distribution": statuses}
    if dtype == "adr":
        entry["orphan_count"] = orphans
    return entry


def roadmap_state(root, docs_root, parse_frontmatter):
    """Root-level `ROADMAP.md` first (the portable convention), else the typed
    `<docs-root>/roadmap/*.md` location doc-writing-rules' folder ladder names —
    the only place a repo on the `.claude/docs/` override files one (#882).
    Reports the resolved path so the reader can tell which rung matched."""
    candidates = [Path(root) / "ROADMAP.md"]
    typed_dir = Path(docs_root) / "roadmap"
    if typed_dir.is_dir():
        candidates.extend(sorted(typed_dir.glob("*.md")))
    for p in candidates:
        if not p.is_file():
            continue
        fm = parse_frontmatter(p.read_text(errors="replace")) or {}
        if p.parent == typed_dir and fm.get("doc-type", "roadmap") != "roadmap":
            continue
        return {"present": True, "status": fm.get("status"),
                "path": str(p.relative_to(root))}
    return {"present": False, "status": None, "path": None}


def collect(root):
    doc_lint = load_doc_lint()
    docs_root = resolve_docs_root(root)
    ledger = {t: census_dir(docs_root, t, doc_lint.parse_frontmatter) for t in LEDGER_TYPES}
    return {"ledger": ledger,
            "roadmap": roadmap_state(root, docs_root, doc_lint.parse_frontmatter),
            "types_known": sorted(doc_lint.TYPES), "ledger_lock": doc_lint.LEDGER_LOCK}


def selftest():
    fails = []
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        adr_dir = root / "docs" / "ops" / "adr"
        adr_dir.mkdir(parents=True)
        (adr_dir / "0001-x.md").write_text(
            "---\ndoc-type: adr\nid: ADR-0001\nstatus: accepted\n"
            "intent-refs: IDR-0001\n---\n## Context\n## Decision\n## Consequences\n")
        (adr_dir / "0002-y.md").write_text(
            "---\ndoc-type: adr\nid: ADR-0002\nstatus: proposed\n---\n"
            "## Context\n## Decision\n## Consequences\n")
        result = collect(root)
        adr = result["ledger"]["adr"]
        if adr["count"] != 2:
            fails.append(f"negative control: adr count wrong (got {adr['count']}, want 2)")
        if adr["status_distribution"] != {"accepted": 1, "proposed": 1}:
            fails.append(f"status distribution wrong: {adr['status_distribution']}")
        if adr["orphan_count"] != 1:
            fails.append(f"orphan count wrong (got {adr['orphan_count']}, want 1 — the "
                          f"no-intent-refs ADR)")
        for t in ("idr", "rdd"):
            if result["ledger"][t]["count"] != 0:
                fails.append(f"reverse control: empty {t} dir reported nonzero count")
        if result["roadmap"]["present"]:
            fails.append("reverse control: no ROADMAP.md but reported present")
        if "adr" not in result["types_known"] or "idr" not in result["types_known"]:
            fails.append("types_known didn't pass through doc_lint's live TYPES dict")

        (root / "ROADMAP.md").write_text("---\ndoc-type: roadmap\nid: r1\nstatus: active\n---\n"
                                          "## Now\n## Next\n## Later\n")
        result2 = collect(root)
        if not (result2["roadmap"]["present"] and result2["roadmap"]["status"] == "active"):
            fails.append(f"negative control: ROADMAP.md present/status not read "
                         f"({result2['roadmap']})")

    with tempfile.TemporaryDirectory() as td2:
        legacy_root = Path(td2)
        legacy_adr = legacy_root / ".claude" / "docs" / "adr"
        legacy_adr.mkdir(parents=True)
        (legacy_adr / "0001-z.md").write_text(
            "---\ndoc-type: adr\nid: ADR-0001\nstatus: accepted\n"
            "intent-refs: IDR-0001\n---\n## Context\n## Decision\n## Consequences\n")
        legacy_result = collect(legacy_root)
        if legacy_result["ledger"]["adr"]["count"] != 1:
            fails.append("host-override ladder: .claude/docs/ fallback not read when "
                         f"docs/ops/ absent (got {legacy_result['ledger']['adr']['count']}, want 1)")

        # #882: the typed roadmap location under the override root, with no root ROADMAP.md.
        # A non-roadmap .md in that folder must NOT count (doc-type gate); a real one must.
        typed_dir = legacy_root / ".claude" / "docs" / "roadmap"
        typed_dir.mkdir(parents=True)
        (typed_dir / "README.md").write_text("---\ndoc-type: plan\nid: p1\nstatus: active\n---\n")
        decoy = collect(legacy_root)["roadmap"]
        if decoy["present"]:
            fails.append(f"#882 reverse control: non-roadmap file in roadmap/ counted ({decoy})")
        (typed_dir / "roadmap-x.md").write_text(
            "---\ndoc-type: roadmap\nid: roadmap-x\nstatus: active\n---\n## Now\n")
        typed = collect(legacy_root)["roadmap"]
        if not (typed["present"] and typed["status"] == "active"
                and typed["path"] == ".claude/docs/roadmap/roadmap-x.md"):
            fails.append(f"#882 negative control: typed roadmap under .claude/docs/ not read ({typed})")

        # Precedence: when BOTH roots exist, docs/ops/ must win (catches a swapped if-order).
        both_ops = legacy_root / "docs" / "ops" / "adr"
        both_ops.mkdir(parents=True)
        (both_ops / "0001-w.md").write_text(
            "---\ndoc-type: adr\nid: ADR-0001\nstatus: proposed\n---\n"
            "## Context\n## Decision\n## Consequences\n")
        both_result = collect(legacy_root)
        both_adr = both_result["ledger"]["adr"]
        if both_adr["count"] != 1 or both_adr["status_distribution"] != {"proposed": 1}:
            fails.append("host-override ladder: docs/ops/ did not win precedence over "
                         f".claude/docs/ when both exist (got {both_adr})")

        # Neither root exists → all-zero, never a crash.
        with tempfile.TemporaryDirectory() as td3:
            empty_result = collect(Path(td3))
            if empty_result["ledger"]["adr"]["count"] != 0:
                fails.append("host-override ladder: neither root present but reported nonzero")

    if fails:
        print(f"lifecycle_census · selftest FAIL · {len(fails)} fail / 0 warn")
        [print(f"  - {f}") for f in fails]
        sys.exit(1)
    print("lifecycle_census · selftest ok · 0 fail / 0 warn")
    sys.exit(0)


def main(argv):
    if len(argv) == 2 and argv[1] == "selftest":
        selftest()
    root = argv[1] if len(argv) > 1 else "."
    if root.startswith("-"):
        print(__doc__)
        sys.exit(2)
    try:
        print(json.dumps(collect(root), indent=2))
    except OSError as e:
        print(f"lifecycle_census · FAIL · {e}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)
