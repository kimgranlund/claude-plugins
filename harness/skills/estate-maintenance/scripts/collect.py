#!/usr/bin/env python3
"""collect.py — one evidence bundle for estate-maintenance's retrospective (gh#629, lld-0019).

Reads the durable outputs sibling seats already produce (auto-memory, the two trend CSVs,
`.claude/ops/*` queues, a session-supplied `issues.json` dump, ADR/IDR status via same-plugin
import of `adr_checkpoint.py`'s parsers, and a context-surface census) into ONE bundle JSON that
`detect.py` consumes. Every input is feature-detected: an absent one yields a bundle entry
`{"present": false, "reason": "..."}` — never an exception (Resolution b's AC-predicate).

Usage:
  collect.py <root> [--memory DIR] [--issues issues.json] [--rent rent.json]
             [--window-days N] [--now YYYY-MM-DD] [--out bundle.json]
  collect.py selftest

Exit: 0 bundle written (or printed) · 1 unexpected write failure · 2 usage error (bad root, bad args).

`--window-days` (default 90) is stored in the bundle for detect.py's `fix_clusters` step to apply
(Procedure Phase 2) — this collector does NOT drop issues/memories outside the window from the
bundle itself; D1-D4 need the full history to see re-filed/repeated patterns regardless of window.
`--now` overrides "today" for deterministic selftests; defaults to the real date otherwise.
"""
import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

# --- same-plugin import: harness/scripts/adr_checkpoint.py's parsers, no re-derivation -----------
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # harness/scripts/
from adr_checkpoint import parse_frontmatter, parse_status_table  # noqa: E402

ENTRY_FILE_LINE_THRESHOLD = 200  # skill_lint.py C1's constant, cited (harness/scripts/skill_lint.py:591)

# The metric-source registry (Resolution b) — the ONLY seam a future metric input touches.
# `key_columns` group rows into series (e.g. one series per plugin); `series_columns` are the
# columns D3 watches for monotonic growth / all-absent.
METRIC_REGISTRY = [
    {
        "key": "attention_trend",
        "path": "attention-trend.csv",
        "key_columns": ["plugin"],
        "series_columns": ["routable_chars", "agent_chars", "dead", "stolen", "leaked"],
        "ordering": "append",
    },
    {
        "key": "recurrence_trend",
        "path": "recurrence-trend.csv",
        "key_columns": [],
        "series_columns": ["seeded_classes", "recurred_classes", "bare_citations",
                            "routing_pass_rate"],
        "ordering": "date",
    },
    {
        "key": "cost_ledger",
        "path": ".claude/ops/cost-ledger.csv",
        "key_columns": ["event-kind"],
        "series_columns": ["tokens"],
        "ordering": "append",
    },
]

FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
FIELD_RE = re.compile(r"^([A-Za-z_]+):\s?(.*)$", re.M)


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def parse_memory_frontmatter(text):
    """Extract name/description/metadata.type/modified/originSessionId from an auto-memory
    entry's YAML-ish frontmatter block. Pure — no I/O. Tolerant of the two-space `metadata:`
    block shape (`metadata:\\n  node_type: memory\\n  type: feedback\\n  ...`)."""
    m = FM_RE.match(text)
    if not m:
        return None
    fm = m.group(1)
    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
    desc_m = re.search(r"^description:\s*[\"']?(.+?)[\"']?$", fm, re.M)
    type_m = re.search(r"^\s+type:\s*(\S+)", fm, re.M)
    modified_m = re.search(r"^\s+modified:\s*(\S+)", fm, re.M)
    session_m = re.search(r"^\s+originSessionId:\s*(\S+)", fm, re.M)
    return {
        "name": name_m.group(1).strip() if name_m else None,
        "description": desc_m.group(1).strip() if desc_m else None,
        "type": type_m.group(1).strip() if type_m else None,
        "modified": modified_m.group(1).strip() if modified_m else None,
        "originSessionId": session_m.group(1).strip() if session_m else None,
    }


def collect_memory(memory_dir):
    """{present, reason, path, index_lines, entries[]} — frontmatter of every *.md in
    `memory_dir` (excluding MEMORY.md, the index itself) + MEMORY.md's own line count."""
    if memory_dir is None:
        return {"present": False, "path": None,
                "reason": "no --memory dir given (ADR-0022 exception: memory is user-scoped, "
                           "not resolvable from a bare repo root)",
                "index_lines": None, "entries": []}
    mdir = Path(memory_dir)
    if not mdir.is_dir():
        return {"present": False, "path": str(mdir),
                "reason": f"memory dir not found at {mdir} (fresh clone/worktree — ADR-0022 "
                           "named exception)",
                "index_lines": None, "entries": []}
    index_file = mdir / "MEMORY.md"
    index_lines = None
    if index_file.is_file():
        text = _read_text(index_file)
        index_lines = len(text.splitlines()) if text is not None else None
    entries = []
    for f in sorted(mdir.glob("*.md")):
        if f.name == "MEMORY.md":
            continue
        text = _read_text(f)
        if text is None:
            continue
        fm = parse_memory_frontmatter(text)
        if fm is None:
            continue
        entries.append({"file": f.name, **fm})
    return {"present": True, "path": str(mdir), "reason": None,
            "index_lines": index_lines, "entries": entries}


def collect_metric_source(root, entry):
    """One METRIC_REGISTRY entry -> {present, reason, path, columns, rows, ordering,
    key_columns, series_columns}. `key_columns`/`series_columns` ride through UNCONDITIONALLY
    (present or not) so detect.py's D3 can group rows by key regardless of which branch fired —
    the metric-source registry (Resolution b) is the only seam a future metric input touches,
    and detect.py never re-derives these from raw CSV headers (gh#645 MAJOR-1 fix)."""
    path = Path(root) / entry["path"]
    common = {"ordering": entry["ordering"], "key_columns": entry["key_columns"],
              "series_columns": entry["series_columns"]}
    if not path.is_file():
        return {"present": False, "path": str(path),
                "reason": f"{entry['path']} not found (registered, not yet present)",
                "columns": None, "rows": [], **common}
    text = _read_text(path)
    if not text or not text.strip():
        return {"present": False, "path": str(path), "reason": "file present but empty",
                "columns": None, "rows": [], **common}
    reader = csv.DictReader(text.splitlines())
    rows = list(reader)
    return {"present": True, "path": str(path), "reason": None,
            "columns": reader.fieldnames or [], "rows": rows, **common}


def collect_metrics(root):
    bundle = {}
    for entry in METRIC_REGISTRY:
        if entry["key"] == "cost_ledger" and not (Path(root) / entry["path"]).is_file():
            bundle[entry["key"]] = {"present": False, "path": str(Path(root) / entry["path"]),
                                     "reason": "cost ledger not yet shipped (gh#624)",
                                     "columns": None, "rows": [], "ordering": entry["ordering"],
                                     "key_columns": entry["key_columns"],
                                     "series_columns": entry["series_columns"]}
            continue
        bundle[entry["key"]] = collect_metric_source(root, entry)
    return bundle


def _scan_decision_dir(dir_path):
    """[{id, status, path}] for every *.md in dir_path parsed via adr_checkpoint's two
    dialect parsers — frontmatter first, then the H1+status-table dialect. Never re-derives
    the parsing rules themselves."""
    out = []
    if not dir_path.is_dir():
        return out
    for f in sorted(dir_path.glob("*.md")):
        text = _read_text(f)
        if not text:
            continue
        parsed = parse_frontmatter(text) or parse_status_table(text)
        if parsed and parsed.get("id") and parsed.get("status"):
            out.append({"id": parsed["id"], "status": parsed["status"], "path": str(f)})
    return out


def _count_plan_pending(plan_path):
    """Best-effort proxy: number of numbered queue entries (`### N. ...`) under a
    chore-planner-shaped plan.md. Documented as a proxy, not an exact parse of prose."""
    text = _read_text(plan_path)
    if not text:
        return 0
    return len(re.findall(r"^### \d+\.", text, re.M))


def collect_decisions(root):
    root = Path(root)
    adrs = _scan_decision_dir(root / ".claude" / "docs" / "adr")
    idrs = _scan_decision_dir(root / ".claude" / "docs" / "idr")

    def json_or_absent(path):
        if not path.is_file():
            return {"present": False, "path": str(path), "reason": "not present", "data": None}
        text = _read_text(path)
        try:
            return {"present": True, "path": str(path), "reason": None, "data": json.loads(text)}
        except (json.JSONDecodeError, TypeError):
            return {"present": False, "path": str(path), "reason": "present but unparseable",
                    "data": None}

    adr_queue = json_or_absent(root / ".claude" / "ops" / "adr-queue.json")
    revalidation_queue = json_or_absent(root / ".claude" / "ops" / "revalidation-queue.json")
    plan_path = root / ".claude" / "ops" / "plan.md"
    plan = {"present": plan_path.is_file(), "path": str(plan_path),
            "pending_count": _count_plan_pending(plan_path) if plan_path.is_file() else 0}
    return {"adrs": adrs, "idrs": idrs, "adr_queue": adr_queue,
            "revalidation_queue": revalidation_queue, "plan": plan}


def collect_issues(issues_path):
    if issues_path is None:
        return {"present": False, "path": None,
                "reason": "no --issues JSON supplied (session dumps `gh issue list` before "
                           "invoking this script — determinism, no network in a check)",
                "items": []}
    p = Path(issues_path)
    if not p.is_file():
        return {"present": False, "path": str(p), "reason": "issues.json not found", "items": []}
    text = _read_text(p)
    try:
        items = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {"present": False, "path": str(p), "reason": "issues.json present but unparseable",
                "items": []}
    if not isinstance(items, list):
        return {"present": False, "path": str(p), "reason": "issues.json is not a JSON array",
                "items": []}
    return {"present": True, "path": str(p), "reason": None, "items": items}


def _line_count(path):
    text = _read_text(path)
    return len(text.splitlines()) if text is not None else 0


SKIP_DIRS = {".git", "node_modules", "dist", ".refactor-attic", "worktrees", ".ruff_cache",
             "fixture-estate"}  # this skill's own assets/fixture-estate/CLAUDE.md is a fixture
                                # input, never a real entry file (gh#645 minor-4)


def collect_census(root, metrics):
    root = Path(root).resolve()
    entry_files = []
    for p in root.rglob("CLAUDE.md"):
        # Only the directory SEGMENTS BETWEEN root and the file are checked against SKIP_DIRS —
        # never root's own name — so a selftest that points `root` directly AT a fixture dir
        # (e.g. assets/fixture-estate/ itself) still sees its own positive-control CLAUDE.md;
        # only a NESTED fixture-estate/ (the real-workspace case, gh#645 minor-4) is skipped.
        rel_dirs = p.resolve().relative_to(root).parts[:-1]
        if any(part in SKIP_DIRS for part in rel_dirs):
            continue
        n = _line_count(p)
        entry_files.append({"path": str(p), "lines": n, "over_threshold": n > ENTRY_FILE_LINE_THRESHOLD})

    rules_files = []
    rules_dir = root / ".claude" / "rules"
    if rules_dir.is_dir():
        for p in sorted(rules_dir.glob("*.md")):
            rules_files.append({"path": str(p), "lines": _line_count(p)})

    plugin_chars = {}
    at = metrics.get("attention_trend", {})
    if at.get("present"):
        # latest row per plugin, by APPEND order (never date sort — attention-trend.csv's own
        # documented ordering, Resolution b).
        for row in at["rows"]:
            plugin = row.get("plugin")
            if not plugin:
                continue
            try:
                routable = int(row.get("routable_chars") or 0)
                agent = int(row.get("agent_chars") or 0)
            except ValueError:
                continue
            plugin_chars[plugin] = routable + agent  # last write wins == latest append

    return {
        "entry_files": entry_files,
        "rules_count": len(rules_files),
        "rules_total_lines": sum(r["lines"] for r in rules_files),
        "rules_files": rules_files,
        "plugin_chars": plugin_chars,
    }


def collect(root, memory_dir=None, issues_path=None, rent_path=None, window_days=90, now=None):
    root = Path(root).resolve()
    today = now or date.today().isoformat()
    memory = collect_memory(memory_dir)
    metrics = collect_metrics(root)
    decisions = collect_decisions(root)
    issues = collect_issues(issues_path)
    census = collect_census(root, metrics)

    rent = {"present": False, "path": rent_path,
            "reason": "authorkit not installed / no --rent given"}
    if rent_path and Path(rent_path).is_file():
        text = _read_text(Path(rent_path))
        try:
            rent = {"present": True, "path": rent_path, "reason": None, "data": json.loads(text)}
        except (json.JSONDecodeError, TypeError):
            rent = {"present": False, "path": rent_path, "reason": "rent.json unparseable"}

    inputs = {
        "memory": {"present": memory["present"], "reason": memory["reason"]},
        "attention_trend": {"present": metrics["attention_trend"]["present"],
                             "reason": metrics["attention_trend"]["reason"]},
        "recurrence_trend": {"present": metrics["recurrence_trend"]["present"],
                              "reason": metrics["recurrence_trend"]["reason"]},
        "cost_ledger": {"present": metrics["cost_ledger"]["present"],
                         "reason": metrics["cost_ledger"]["reason"]},
        "issues": {"present": issues["present"], "reason": issues["reason"]},
        "rent": {"present": rent["present"], "reason": rent.get("reason")},
        "adr_queue": {"present": decisions["adr_queue"]["present"],
                      "reason": decisions["adr_queue"]["reason"]},
        "revalidation_queue": {"present": decisions["revalidation_queue"]["present"],
                                "reason": decisions["revalidation_queue"]["reason"]},
        "plan": {"present": decisions["plan"]["present"],
                 "reason": None if decisions["plan"]["present"] else "plan.md not present"},
    }

    return {
        "run": {"date": today, "root": str(root), "window_days": window_days},
        "inputs": inputs,
        "memory": memory,
        "metrics": metrics,
        "decisions": decisions,
        "issues": issues,
        "census": census,
        "rent": rent,
    }


def selftest():
    fixture = Path(__file__).resolve().parents[1] / "assets" / "fixture-estate"
    assert fixture.is_dir(), f"fixture-estate missing: {fixture}"

    bundle = collect(
        fixture,
        memory_dir=fixture / "memory",
        issues_path=fixture / "issues.json",
        window_days=3,
        now="2026-08-25",
    )

    # positive control: every registered metric source present in the fixture is actually read
    assert bundle["metrics"]["attention_trend"]["present"], bundle["metrics"]["attention_trend"]
    assert len(bundle["metrics"]["attention_trend"]["rows"]) >= 3
    assert bundle["metrics"]["recurrence_trend"]["present"]
    # cost ledger is a registered-absent source from day one — never an exception
    assert bundle["metrics"]["cost_ledger"]["present"] is False
    assert bundle["metrics"]["cost_ledger"]["reason"]

    # memory: feedback entries parsed with type
    assert bundle["memory"]["present"]
    feedback = [e for e in bundle["memory"]["entries"] if e["type"] == "feedback"]
    assert len(feedback) >= 3, bundle["memory"]["entries"]

    # issues: fixture pair + control loaded
    assert bundle["issues"]["present"]
    assert len(bundle["issues"]["items"]) >= 3, bundle["issues"]["items"]

    # census: the fixture's over-threshold CLAUDE.md and two rules files are counted
    over = [e for e in bundle["census"]["entry_files"] if e["over_threshold"]]
    assert len(over) >= 1, bundle["census"]["entry_files"]
    assert bundle["census"]["rules_count"] == 2, bundle["census"]

    # gh#645 minor-4: scanning a root that CONTAINS assets/fixture-estate/ as a nested
    # subdirectory must exclude the fixture's own CLAUDE.md from the census — the skill must
    # never flag its own fixture as a D4 finding about itself. (The assertion just above proves
    # the OPPOSITE case still works: pointing `root` directly AT fixture-estate still sees its
    # own positive-control CLAUDE.md, since only NESTED occurrences are skipped.)
    skill_root = Path(__file__).resolve().parents[1]  # harness/skills/estate-maintenance/
    nested = collect(skill_root, memory_dir=None, issues_path=None, window_days=90,
                      now="2026-08-25")
    nested_paths = [e["path"] for e in nested["census"]["entry_files"]]
    assert not any("fixture-estate" in p for p in nested_paths), nested_paths

    # gh#645 MAJOR-1: key_columns/series_columns ride through into the bundle for every metric
    # source (present or absent) — detect.py's D3 grouping depends on this, never re-derived.
    assert bundle["metrics"]["attention_trend"]["key_columns"] == ["plugin"]
    assert bundle["metrics"]["attention_trend"]["series_columns"] == [
        "routable_chars", "agent_chars", "dead", "stolen", "leaked"]
    assert bundle["metrics"]["cost_ledger"]["key_columns"] == ["event-kind"]

    # decisions: absent adr-queue/revalidation-queue in the fixture -> present:false, never raises
    assert bundle["decisions"]["adr_queue"]["present"] is False

    # negative control: an empty root with no optional inputs -> every optional input UNMEASURED,
    # never an exception, and the bundle still has the expected top-level shape
    empty = Path(__file__).resolve().parent  # this scripts/ dir has no fixture inputs of its own
    clean = collect(empty, memory_dir=None, issues_path=None, window_days=90, now="2026-08-25")
    assert clean["memory"]["present"] is False
    assert clean["issues"]["present"] is False
    assert clean["metrics"]["attention_trend"]["present"] is False
    assert clean["metrics"]["cost_ledger"]["present"] is False
    assert clean["census"]["rules_count"] == 0

    # determinism
    assert collect(fixture, memory_dir=fixture / "memory", issues_path=fixture / "issues.json",
                    window_days=3, now="2026-08-25") == bundle

    print("collect.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("root", nargs="?")
    ap.add_argument("--memory")
    ap.add_argument("--issues")
    ap.add_argument("--rent")
    ap.add_argument("--window-days", type=int, default=90)
    ap.add_argument("--now")
    ap.add_argument("--out")
    ap.add_argument("-h", "--help", action="store_true")
    args = ap.parse_args()

    if args.help or args.root is None:
        print(__doc__)
        return 2
    if args.root == "selftest":
        return selftest()

    root = Path(args.root)
    if not root.is_dir():
        print(f"collect.py: root not found or not a directory: {root}", file=sys.stderr)
        return 2

    bundle = collect(root, memory_dir=args.memory, issues_path=args.issues,
                      rent_path=args.rent, window_days=args.window_days, now=args.now)
    text = json.dumps(bundle, indent=2, sort_keys=True)
    if args.out:
        try:
            Path(args.out).write_text(text + "\n", encoding="utf-8")
        except OSError as e:
            print(f"collect.py: could not write --out {args.out}: {e}", file=sys.stderr)
            return 1
    else:
        print(text)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"collect.py error: {e}", file=sys.stderr)
        sys.exit(2)
