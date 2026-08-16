#!/usr/bin/env python3
"""doctrine-audit sweeper — mechanizes the three deterministic edge types from a
doctrine.manifest.json (issue #379): verbatim-line, ledger-sync, vocab-term. A fourth
type, judgment, is deliberately NOT mechanized (Kim's 2026-08-16 ruling: "name only —
queued, not built") — it is reported as a finding of its own kind naming the owning
checker, never silently dropped and never dispatched from here.

Deterministic checks only: does a dependent file contain (or not contain) a pattern,
does a ledger's named path exist on disk, does a dependent use a banned alias for a
canonical term. Judgment (is a finding real drift or a false positive, how to fix it)
belongs to the doctrine-audit SKILL, not here.

Usage:
  sweep.py --root PATH [--manifest PATH] [--json]
  sweep.py validate --manifest PATH             schema-check a manifest, no target sweep
  sweep.py selftest                             prove the counters bite

Exit codes: 0 clean (no mechanizable findings; judgment edges may still be reported),
1 mechanizable findings present, 2 usage error (root/manifest missing, malformed JSON,
invalid edge shape, or an edge naming a type outside the four known ones).
"""

import argparse
import json
import re
import sys
from pathlib import Path

KNOWN_TYPES = {"verbatim-line", "ledger-sync", "vocab-term", "judgment"}
REQUIRED_TOP = {"edges"}


class SweepError(Exception):
    """A clean, expected usage failure — main() turns this into exit 2, never a
    traceback."""


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise SweepError(f"manifest not found: {path}")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        raise SweepError(f"manifest is not valid JSON: {e}")
    if not isinstance(data, dict) or "edges" not in data:
        raise SweepError("manifest missing required top-level 'edges' array")
    if not isinstance(data["edges"], list):
        raise SweepError("manifest 'edges' must be an array")
    return data


def validate_edge_shape(edge: dict, idx: int) -> list:
    """Returns a list of shape-error strings for one edge dict; empty means valid."""
    errs = []
    prefix = f"edge[{idx}]"
    eid = edge.get("id", f"<unnamed {prefix}>")
    if "id" not in edge:
        errs.append(f"{prefix}: missing 'id'")
    etype = edge.get("type")
    if etype not in KNOWN_TYPES:
        errs.append(f"{eid}: unknown or missing type {etype!r} (must be one of {sorted(KNOWN_TYPES)})")
        return errs  # can't type-check further fields without a known type
    if etype == "verbatim-line":
        if edge.get("mode") not in ("require", "forbid"):
            errs.append(f"{eid}: verbatim-line edge needs mode 'require' or 'forbid'")
        if not edge.get("canon_file"):
            errs.append(f"{eid}: verbatim-line edge needs canon_file")
        deps = edge.get("dependents")
        if not deps or not isinstance(deps, list):
            errs.append(f"{eid}: verbatim-line edge needs a non-empty dependents array")
        else:
            for d in deps:
                if not d.get("file") or not d.get("pattern"):
                    errs.append(f"{eid}: each dependent needs 'file' and 'pattern'")
    elif etype == "ledger-sync":
        if not edge.get("canon_file"):
            errs.append(f"{eid}: ledger-sync edge needs canon_file")
        if not edge.get("ledger_pattern"):
            errs.append(f"{eid}: ledger-sync edge needs ledger_pattern")
        if not edge.get("actual_path"):
            errs.append(f"{eid}: ledger-sync edge needs actual_path")
    elif etype == "vocab-term":
        if not edge.get("canonical_term"):
            errs.append(f"{eid}: vocab-term edge needs canonical_term")
        if not edge.get("banned_aliases"):
            errs.append(f"{eid}: vocab-term edge needs a non-empty banned_aliases array")
        deps = edge.get("dependents")
        if not deps or not isinstance(deps, list):
            errs.append(f"{eid}: vocab-term edge needs a non-empty dependents array")
    elif etype == "judgment":
        if not edge.get("owning_checker"):
            errs.append(f"{eid}: judgment edge needs owning_checker (the checker it's routed to)")
    return errs


def validate_manifest(data: dict) -> list:
    """Returns a flat list of shape-error strings across the whole manifest."""
    errs = []
    edges = data.get("edges", [])
    seen_ids = set()
    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errs.append(f"edge[{i}]: not an object")
            continue
        errs.extend(validate_edge_shape(edge, i))
        eid = edge.get("id")
        if eid:
            if eid in seen_ids:
                errs.append(f"duplicate edge id: {eid}")
            seen_ids.add(eid)
    return errs


def check_verbatim_line(edge: dict, root: Path) -> list:
    findings = []
    mode = edge["mode"]
    for dep in edge["dependents"]:
        f = root / dep["file"]
        pattern = dep["pattern"]
        if not f.exists():
            findings.append({
                "edge": edge["id"], "type": "verbatim-line", "file": dep["file"],
                "reason": "dependent file not found", "severity": edge.get("severity", "minor"),
            })
            continue
        text = f.read_text(errors="replace")
        hit = re.search(pattern, text) is not None
        if mode == "require" and not hit:
            findings.append({
                "edge": edge["id"], "type": "verbatim-line", "file": dep["file"],
                "reason": f"required pattern absent: {pattern!r}",
                "severity": edge.get("severity", "minor"),
            })
        elif mode == "forbid" and hit:
            findings.append({
                "edge": edge["id"], "type": "verbatim-line", "file": dep["file"],
                "reason": f"forbidden pattern present: {pattern!r}",
                "severity": edge.get("severity", "minor"),
            })
    return findings


def check_ledger_sync(edge: dict, root: Path) -> list:
    findings = []
    canon = root / edge["canon_file"]
    if not canon.exists():
        return [{
            "edge": edge["id"], "type": "ledger-sync", "file": edge["canon_file"],
            "reason": "ledger (canon) file not found", "severity": edge.get("severity", "minor"),
        }]
    text = canon.read_text(errors="replace")
    ledger_pattern = edge["ledger_pattern"]
    actual = root / edge["actual_path"]
    if ledger_pattern in text and not actual.exists():
        findings.append({
            "edge": edge["id"], "type": "ledger-sync", "file": edge["canon_file"],
            "reason": f"ledger still references {ledger_pattern!r} but actual path "
                      f"{edge['actual_path']!r} does not exist on disk (drift)",
            "severity": edge.get("severity", "minor"),
        })
    elif ledger_pattern in text and actual.exists() and ledger_pattern != edge["actual_path"]:
        # Ledger names a string that isn't the actual path, even though the actual
        # path DOES exist elsewhere — the row is stale, not just broken.
        findings.append({
            "edge": edge["id"], "type": "ledger-sync", "file": edge["canon_file"],
            "reason": f"ledger references {ledger_pattern!r}; actual artifact lives at "
                      f"{edge['actual_path']!r} instead",
            "severity": edge.get("severity", "minor"),
        })
    return findings


def check_vocab_term(edge: dict, root: Path) -> list:
    findings = []
    aliases = edge["banned_aliases"]
    for dep in edge["dependents"]:
        f = root / dep["file"]
        if not f.exists():
            findings.append({
                "edge": edge["id"], "type": "vocab-term", "file": dep["file"],
                "reason": "dependent file not found", "severity": edge.get("severity", "minor"),
            })
            continue
        text = f.read_text(errors="replace")
        for alias in aliases:
            if alias in text:
                findings.append({
                    "edge": edge["id"], "type": "vocab-term", "file": dep["file"],
                    "reason": f"banned alias {alias!r} present; canonical term is "
                              f"{edge['canonical_term']!r}",
                    "severity": edge.get("severity", "minor"),
                })
    return findings


def analyze(root: Path, manifest: dict) -> dict:
    """Core sweep, pure of argv/exit-code concerns so it is directly callable from
    both main() and selftest(). Raises SweepError on a manifest shape failure —
    never partially sweeps a malformed manifest."""
    shape_errs = validate_manifest(manifest)
    if shape_errs:
        raise SweepError("manifest failed shape validation: " + "; ".join(shape_errs))

    findings = []
    judgment_queue = []
    for edge in manifest["edges"]:
        etype = edge["type"]
        if etype == "verbatim-line":
            findings.extend(check_verbatim_line(edge, root))
        elif etype == "ledger-sync":
            findings.extend(check_ledger_sync(edge, root))
        elif etype == "vocab-term":
            findings.extend(check_vocab_term(edge, root))
        elif etype == "judgment":
            judgment_queue.append({
                "edge": edge["id"], "title": edge.get("title", ""),
                "owning_checker": edge["owning_checker"],
                "status": edge.get("status", "queued, not built"),
            })

    unrecovered = manifest.get("unrecovered_findings")

    result = {
        "root": str(root),
        "edges_checked": len([e for e in manifest["edges"] if e["type"] != "judgment"]),
        "findings": findings,
        "judgment_queue": judgment_queue,
        "unrecovered_findings": unrecovered,
        "totals": {
            "findings": len(findings),
            "judgment_edges": len(judgment_queue),
        },
    }
    # The verdict string is embedded in the dict itself (not just printed in
    # non-JSON mode) so a --json caller can quote it without a second,
    # non-JSON run — skill-checker finding, 2026-08-16: a JSON-only caller
    # had no way to satisfy the "quote the verdict line" contract otherwise.
    result["verdict"] = verdict_line(result)
    return result


def verdict_line(result: dict) -> str:
    """The one non-JSON contract surface — selftest asserts THIS exact function's
    output (pattern-audit's own precedent), so a format drift in main()'s print can
    never pass silently."""
    n = result["totals"]["findings"]
    j = result["totals"]["judgment_edges"]
    verdict = "FINDINGS" if n else "CLEAN"
    return (f"doctrine-audit sweep · {verdict} · {n} findings / "
            f"{result['edges_checked']} mechanizable edges · {j} judgment edges queued")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default=None)
    ap.add_argument("--root")
    ap.add_argument("--manifest")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.mode == "validate":
        if not args.manifest:
            print("doctrine-audit sweep: validate mode needs --manifest")
            sys.exit(2)
        try:
            data = load_manifest(Path(args.manifest).resolve())
        except SweepError as e:
            print(f"doctrine-audit sweep: {e}")
            sys.exit(2)
        errs = validate_manifest(data)
        if errs:
            print("doctrine-audit manifest validate · INVALID")
            for e in errs:
                print(f"  - {e}")
            sys.exit(1)
        print(f"doctrine-audit manifest validate · VALID · {len(data['edges'])} edges")
        sys.exit(0)

    if not args.root:
        print("doctrine-audit sweep: --root is required (or use the 'validate' subcommand)")
        sys.exit(2)

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"doctrine-audit sweep: root not found: {root}")
        sys.exit(2)
    manifest_path = Path(args.manifest).resolve() if args.manifest else root / "doctrine.manifest.json"

    try:
        manifest = load_manifest(manifest_path)
        result = analyze(root, manifest)
    except SweepError as e:
        print(f"doctrine-audit sweep: {e}")
        sys.exit(2)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(verdict_line(result))
        for f in result["findings"]:
            print(f"  [{f['type']}/{f['severity']}] {f['edge']} {f['file']}: {f['reason']}")
        for j in result["judgment_queue"]:
            print(f"  [judgment] {j['edge']} -> {j['owning_checker']} ({j['status']})")
        if result["unrecovered_findings"]:
            u = result["unrecovered_findings"]
            print(f"  [gap] {u.get('count', '?')} findings unrecovered: {u.get('note', '')}")

    sys.exit(1 if result["totals"]["findings"] else 0)


def selftest():
    """Prove analyze()'s counters bite, per edge type, plus manifest shape
    validation and negative controls:
      - verbatim-line require: absent pattern flags; present pattern is clean.
      - verbatim-line forbid: present pattern flags; absent pattern is clean.
      - ledger-sync: a ledger row naming a path that doesn't exist on disk flags;
        a synced ledger is clean.
      - vocab-term: a banned alias flags; the canonical term alone is clean.
      - judgment: never mechanically checked, always surfaces in judgment_queue,
        never silently dropped, never counted toward totals.findings.
      - a malformed manifest (unknown type, missing required field) raises
        SweepError via validate_manifest, never a false-clean sweep.
      - unrecovered_findings passes through verbatim when present.
      - the pinned verdict-line string is exact; CLI exit tri-state (0/1/2)
        verified through actual subprocess runs of main(), including the
        'validate' subcommand.
    """
    import subprocess
    import tempfile

    # verbatim-line require: missing clause flags.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "dep.md").write_text("nothing relevant here\n")
        manifest = {"edges": [{
            "id": "T1", "type": "verbatim-line", "mode": "require",
            "canon_file": "dep.md", "dependents": [{"file": "dep.md", "pattern": "MUST_HAVE"}],
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 1, "require mode must flag an absent pattern"
        assert result["findings"][0]["reason"].startswith("required pattern absent")

    # verbatim-line require: present clause is clean (reverse control).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "dep.md").write_text("this file has MUST_HAVE right here\n")
        manifest = {"edges": [{
            "id": "T2", "type": "verbatim-line", "mode": "require",
            "canon_file": "dep.md", "dependents": [{"file": "dep.md", "pattern": "MUST_HAVE"}],
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 0, "require mode must be clean when pattern present"

    # verbatim-line forbid: present clause flags.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "dep.md").write_text("description: |\n  blah blah <example> oops\n")
        manifest = {"edges": [{
            "id": "T3", "type": "verbatim-line", "mode": "forbid",
            "canon_file": "dep.md", "dependents": [{"file": "dep.md", "pattern": "<example>"}],
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 1, "forbid mode must flag a present pattern"
        assert result["findings"][0]["reason"].startswith("forbidden pattern present")

    # verbatim-line forbid: absent clause is clean (reverse control).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "dep.md").write_text("description: |\n  clean, no bad token here\n")
        manifest = {"edges": [{
            "id": "T4", "type": "verbatim-line", "mode": "forbid",
            "canon_file": "dep.md", "dependents": [{"file": "dep.md", "pattern": "<example>"}],
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 0, "forbid mode must be clean when pattern absent"

    # ledger-sync: ledger names a path that doesn't exist on disk -> flags.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "README.md").write_text("See agents/lead-team for the coordinator.\n")
        manifest = {"edges": [{
            "id": "T5", "type": "ledger-sync", "canon_file": "README.md",
            "ledger_pattern": "agents/lead-team", "actual_path": "agents/team-lead.md",
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 1, "ledger-sync must flag drift"
        assert "drift" in result["findings"][0]["reason"]

    # ledger-sync: synced ledger is clean (reverse control).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agents").mkdir()
        (r / "agents" / "team-lead.md").write_text("# team-lead\n")
        (r / "README.md").write_text("See agents/team-lead.md for the coordinator.\n")
        manifest = {"edges": [{
            "id": "T6", "type": "ledger-sync", "canon_file": "README.md",
            "ledger_pattern": "agents/lead-team", "actual_path": "agents/team-lead.md",
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 0, "ledger-sync must be clean when ledger already synced"

    # vocab-term: banned alias flags.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agent.md").write_text("Dispatch this via the Task tool.\n")
        manifest = {"edges": [{
            "id": "T7", "type": "vocab-term", "canonical_term": "Agent",
            "banned_aliases": ["Task tool"], "dependents": [{"file": "agent.md"}],
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 1, "vocab-term must flag a banned alias"

    # vocab-term: canonical term alone is clean (reverse control).
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "agent.md").write_text("Dispatch this via the Agent tool.\n")
        manifest = {"edges": [{
            "id": "T8", "type": "vocab-term", "canonical_term": "Agent",
            "banned_aliases": ["Task tool"], "dependents": [{"file": "agent.md"}],
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 0, "vocab-term must be clean with no banned alias present"

    # judgment: always surfaces in judgment_queue, never in findings/totals.findings.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        manifest = {"edges": [{
            "id": "T9", "type": "judgment", "title": "needs a human judgment call",
            "owning_checker": "harness:wording-checker",
        }]}
        result = analyze(r, manifest)
        assert result["totals"]["findings"] == 0, "a judgment edge must never count toward findings"
        assert result["totals"]["judgment_edges"] == 1, "a judgment edge must surface in the queue"
        assert result["judgment_queue"][0]["status"] == "queued, not built"

    # Malformed manifest: unknown type raises SweepError, never a false-clean sweep.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        manifest = {"edges": [{"id": "T10", "type": "not-a-real-type"}]}
        try:
            analyze(r, manifest)
            raised = False
        except SweepError:
            raised = True
        assert raised, "an unknown edge type must raise SweepError, not sweep silently"

    # Malformed manifest: missing required field raises SweepError.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        manifest = {"edges": [{"id": "T11", "type": "verbatim-line", "mode": "require"}]}
        try:
            analyze(r, manifest)
            raised = False
        except SweepError:
            raised = True
        assert raised, "a verbatim-line edge missing canon_file/dependents must raise SweepError"

    # unrecovered_findings passes through verbatim when present.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        manifest = {"edges": [], "unrecovered_findings": {"count": 3, "note": "gap"}}
        result = analyze(r, manifest)
        assert result["unrecovered_findings"] == {"count": 3, "note": "gap"}, \
            "unrecovered_findings must pass through unchanged"

    # Verdict-line shape pinned exactly.
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "dep.md").write_text("no clause here\n")
        manifest = {"edges": [{
            "id": "T12", "type": "verbatim-line", "mode": "require",
            "canon_file": "dep.md", "dependents": [{"file": "dep.md", "pattern": "NEEDED"}],
        }]}
        result = analyze(r, manifest)
        assert verdict_line(result) == (
            "doctrine-audit sweep · FINDINGS · 1 findings / 1 mechanizable edges · 0 judgment edges queued"
        ), "verdict-line shape must be pinned exactly"
        assert result["verdict"] == verdict_line(result), \
            "the dict's own 'verdict' key must match verdict_line() exactly — a --json caller has no other way to quote it"

    # CLI exit tri-state through actual subprocess runs of main().
    with tempfile.TemporaryDirectory() as td:
        r = Path(td)
        (r / "dep.md").write_text("no clause here\n")
        manifest_path = r / "doctrine.manifest.json"
        manifest_path.write_text(json.dumps({"edges": [{
            "id": "T13", "type": "verbatim-line", "mode": "require",
            "canon_file": "dep.md", "dependents": [{"file": "dep.md", "pattern": "NEEDED"}],
        }]}))

        hit = subprocess.run(
            [sys.executable, __file__, "--root", str(r)],
            capture_output=True, text=True,
        )
        assert hit.returncode == 1, f"findings must exit 1, got {hit.returncode}"
        assert hit.stdout.splitlines()[0].startswith("doctrine-audit sweep · FINDINGS"), \
            f"CLI findings line drifted: {hit.stdout.splitlines()[0]!r}"

        clean_manifest = r / "clean.manifest.json"
        clean_manifest.write_text(json.dumps({"edges": []}))
        clean = subprocess.run(
            [sys.executable, __file__, "--root", str(r), "--manifest", str(clean_manifest)],
            capture_output=True, text=True,
        )
        assert clean.returncode == 0, f"clean must exit 0, got {clean.returncode}"
        assert clean.stdout.startswith("doctrine-audit sweep · CLEAN"), \
            f"CLI clean line drifted: {clean.stdout!r}"

        missing = subprocess.run(
            [sys.executable, __file__, "--root", str(r), "--manifest", str(r / "absent.json")],
            capture_output=True, text=True,
        )
        assert missing.returncode == 2, f"missing manifest must exit 2, got {missing.returncode}"
        assert "Traceback" not in missing.stderr, f"SweepError must not traceback: {missing.stderr}"

        # 'validate' subcommand: VALID and INVALID both exercised through the real CLI.
        good = subprocess.run(
            [sys.executable, __file__, "validate", "--manifest", str(clean_manifest)],
            capture_output=True, text=True,
        )
        assert good.returncode == 0, f"a valid manifest must exit 0, got {good.returncode}"
        assert "VALID" in good.stdout

        bad_manifest = r / "bad.manifest.json"
        bad_manifest.write_text(json.dumps({"edges": [{"id": "X", "type": "vocab-term"}]}))
        bad = subprocess.run(
            [sys.executable, __file__, "validate", "--manifest", str(bad_manifest)],
            capture_output=True, text=True,
        )
        assert bad.returncode == 1, f"an invalid manifest must exit 1, got {bad.returncode}"
        assert "INVALID" in bad.stdout

    print(
        "doctrine-audit sweep selftest · PASS · verbatim-line/ledger-sync/vocab-term/"
        "judgment/shape-validation/unrecovered-passthrough/verdict/exit-tristate counters bite"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "selftest":
        sys.exit(selftest())
    main()
