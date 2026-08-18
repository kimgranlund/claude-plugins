#!/usr/bin/env python3
"""validate.py — schema owner + standalone re-validator for the spend ledger (idr-0010).

Owns the spend-ledger row schema for `authorkit:spend-audit`: `HEADER`, the closed
enums (`EVENT_KINDS`, `TOKENS_SOURCES`, `OUTCOMES`, `VERDICTS`), `DATE_RE`,
`validate_row(row: dict) -> list[str]` (single-row findings, empty = clean), and
`validate_file(path) -> dict` (per-line findings + summary, cross-row dedupe). This is
the ONE file that defines the schema — `trend.py` imports it as a sibling module
(`import validate`) and never redefines any of `HEADER`/the enums/`validate_row`, so a
schema change is one edit here and both scripts' selftests move together
(lld-0018-estate-economy-ledger.md, Resolution 2 / Interfaces).

The ledger row (`.claude/ops/spend-ledger.csv`) is one line per firing (a sweep or a
dispatched build): `date,event_kind,seat,ref,tokens,tokens_source,outcome,verdict,archetype`.
`tokens_source` is a categorical provenance flag on `tokens` (`measured` | `estimated` |
`absent`), never a derived number; `verdict` is the closing seat's ingested judgment for
that firing, never computed here (Resolution 5) — this validator checks SHAPE only,
never grades a row's worth. `archetype` (gh#673, lld-0021) attributes the firing to one of
the estate's eight orchestration archetypes (#666's taxonomy: A1 solo · A2 unnamed sync
fan-out · A3 named background/teammate seats · A4 fleet terminal seats · A5 forked intake ·
A6 scheduled routines + `/goal` loops · A7 Workflow scripts · A8 `/batch`) or the literal
`UNMEASURED` — REQUIRED (never empty) on every row, but `UNMEASURED` is reserved for
best-effort RETROACTIVE backfill of an ambiguous historical firing; a live/new firing's own
closing seat always knows its own shape and states it, never `UNMEASURED` by default
(policy, not a shape rule this validator enforces — it only checks the value is in the
closed set).

No blended column, ever (the family's Goodhart rule, `attention-audit`/`recurrence-audit`
`trend.py`'s own selftest-asserted law, extended here): the header carries no
`ratio`/`quotient`/`per_token` column, and `tokens_source`/`verdict` are a provenance tag
and a recorded judgment respectively, never a computation over `tokens` (Resolution 2's
"No-blended-column precedent").

Usage:
  validate.py <ledger.csv> [--json]
  validate.py selftest

Exit codes: 0 clean (also: no ledger file yet at the given path — the expected
first-run state, never a false failure, mirrors recurrence-audit's zero-seeded
honesty) / 1 findings present (FAIL and/or WARN) / 2 usage (no path given) or an
unreadable existing file (permission error, decode error — distinct from "file simply
does not exist yet", which is exit 0).
"""
import argparse
import csv
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

HEADER = ["date", "event_kind", "seat", "ref", "tokens", "tokens_source", "outcome", "verdict",
          "archetype"]

EVENT_KINDS = {"sweep", "build"}
TOKENS_SOURCES = {"measured", "estimated", "absent"}
OUTCOMES = {"pr-merged", "pr-opened", "acted", "no-op", "blocked", "failed"}
VERDICTS = {"worth-firing", "not-worth-firing", "undetermined"}

# gh#673 (lld-0021) — the estate's eight orchestration archetypes, #666's taxonomy comment,
# plus the retroactive-only escape hatch. Never add a ninth without also adding it to #666's
# own taxonomy first — this validator is a consumer of that taxonomy, not its source. NOTE:
# A8 (`/batch`) is itself still PROVISIONAL as of this ticket — #666's own taxonomy amendment
# comment (2026-08-18) words it as "gains it as an eighth entry (OR an A2×A7 hybrid)", not yet
# a settled distinct-vs-hybrid call; ticket #673's body still says "seven archetypes". Shipped
# here as its own closed-set member because gh#666's comment already commits to SOME eighth
# slot and this ledger needs one value to write, but a future #666 ruling that folds A8 into
# an A2×A7 hybrid is a taxonomy-side decision, not a code change here.
ARCHETYPE_NAMES = {
    "A1": "solo — host session + skills, no dispatch",
    "A2": "unnamed sync fan-out — an unnamed Agent-tool/fork dispatch, synchronous return",
    "A3": "named background/teammate seats — SendMessage-routed, mailbox delivery",
    "A4": "fleet terminal seats — joined via team-scaffolding/fleet-bootstrap, marshal-coordinated",
    "A5": "forked intake — a `context: fork` command (file-bug/file-feature/build-feature)",
    "A6": "scheduled routines + `/goal` loops — CronCreate-armed or loop-driven",
    "A7": "Workflow scripts — `harness/workflows/*.js`",
    "A8": "`/batch` — decompose + one subagent per unit + PR-per-unit",
}
ARCHETYPES = set(ARCHETYPE_NAMES) | {"UNMEASURED"}
# per-outcome-class normalization (gh#673's own definition — it existed nowhere before this
# ticket): kept simple and stated against the EXISTING closed `outcome` enum, no new column.
OUTCOME_CLASSES = {
    "pr-shipped": {"pr-merged"},
    "record-minted": {"acted"},
}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REF_ISSUE_RE = re.compile(r"^#\d+$")


def valid_date(value):
    if not DATE_RE.match(value or ""):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def valid_ref(ref):
    """`#NNN` (issue/PR), a repo-relative path (no leading `/`), or the literal `none`."""
    if ref == "none":
        return True
    if REF_ISSUE_RE.match(ref or ""):
        return True
    if not ref or ref.startswith("/"):
        return False
    return True  # a repo-relative path — permissive by design (Resolution 2)


def valid_tokens(tokens):
    if tokens == "absent":
        return True
    return bool(tokens) and tokens.isdigit()  # non-negative integer, no sign, no decimal


def validate_row(row):
    """Single-row shape findings. `row` is a dict keyed by HEADER's columns (already
    column-count-checked by the caller). Returns a list of finding strings — empty
    means the row is clean. Never touches other rows (dedupe is a validate_file, i.e.
    cross-row, concern)."""
    findings = []

    date = row.get("date", "")
    if not valid_date(date):
        findings.append(f"date {date!r} is not a valid YYYY-MM-DD date")

    event_kind = row.get("event_kind", "")
    if event_kind not in EVENT_KINDS:
        findings.append(f"event_kind {event_kind!r} not in {sorted(EVENT_KINDS)}")

    seat = row.get("seat", "")
    if not seat.strip():
        findings.append("seat is empty")

    ref = row.get("ref", "")
    if not valid_ref(ref):
        findings.append(f"ref {ref!r} is not `#NNN`, a repo-relative path, or `none`")

    tokens = row.get("tokens", "")
    if not valid_tokens(tokens):
        findings.append(f"tokens {tokens!r} is not a non-negative integer or `absent`")

    tokens_source = row.get("tokens_source", "")
    if tokens_source not in TOKENS_SOURCES:
        findings.append(f"tokens_source {tokens_source!r} not in {sorted(TOKENS_SOURCES)}")

    # Cross-field rule (Resolution 2): tokens == absent <=> tokens_source == absent —
    # never a number paired with `absent`, never `absent` paired with a declared source.
    tokens_is_absent = tokens == "absent"
    source_is_absent = tokens_source == "absent"
    if tokens_is_absent and not source_is_absent:
        findings.append(
            f"tokens_source `{tokens_source}` requires an integer tokens value, got `absent`"
        )
    elif not tokens_is_absent and source_is_absent and valid_tokens(tokens):
        findings.append(
            f"tokens `{tokens}` is present but tokens_source is `absent`"
        )

    outcome = row.get("outcome", "")
    if outcome not in OUTCOMES:
        findings.append(f"outcome {outcome!r} not in {sorted(OUTCOMES)}")

    verdict = row.get("verdict", "")
    if verdict not in VERDICTS:
        findings.append(f"verdict {verdict!r} not in {sorted(VERDICTS)}")

    archetype = row.get("archetype", "")
    if archetype not in ARCHETYPES:
        findings.append(f"archetype {archetype!r} not in {sorted(ARCHETYPES)}")

    return findings


def validate_file(path):
    """Validate an on-disk ledger CSV. Returns a dict (the --json shape): path, rows,
    header_ok, findings ([{line, level, message}]), duplicate_keys, summary
    ({fail, warn}), last_date, keys — plus no_ledger_yet: True when the file does not
    exist yet (never a false failure; the expected first-run state)."""
    p = Path(path)
    if not p.is_file():
        return {
            "path": str(path), "rows": 0, "header_ok": None, "findings": [],
            "duplicate_keys": [], "summary": {"fail": 0, "warn": 0},
            "last_date": None, "keys": [], "no_ledger_yet": True,
        }

    with open(p, newline="") as fh:
        reader = list(csv.reader(fh))

    findings = []
    data_rows = []
    if not reader:
        header_ok = False
        findings.append({"line": 1, "level": "FAIL", "message": "ledger file is empty (no header row)"})
    else:
        header = reader[0]
        header_ok = header == HEADER
        if not header_ok:
            findings.append({
                "line": 1, "level": "FAIL",
                "message": f"foreign/reordered header: expected {HEADER}, got {header}",
            })
            # Column semantics are unknown under a foreign header — never coerced,
            # never guessed; nothing else is checked (Components: "a foreign/reordered
            # header is a FAIL, never coerced").
        else:
            data_rows = reader[1:]

    keys_seen = {}
    keys_all = []
    duplicate_keys = []
    last_date = None

    for i, raw in enumerate(data_rows, start=2):  # line 2 is the first data row
        if len(raw) != len(HEADER):
            findings.append({
                "line": i, "level": "FAIL",
                "message": f"wrong column count: got {len(raw)}, expected {len(HEADER)}",
            })
            continue
        row = dict(zip(HEADER, raw))
        for msg in validate_row(row):
            findings.append({"line": i, "level": "FAIL", "message": msg})

        key = (row["date"], row["event_kind"], row["seat"], row["ref"])
        keys_all.append(list(key))
        if row["date"] and (last_date is None or row["date"] > last_date):
            last_date = row["date"]

        # Duplicate key = (date, event_kind, seat, ref) with ref != "none" — WARN, not
        # FAIL (a legitimate re-fire is possible; the backfill must not double-add).
        # ref == "none" is deliberately exempt (Resolution 2/Components' reverse control).
        if row["ref"] != "none":
            if key in keys_seen:
                findings.append({
                    "line": i, "level": "WARN",
                    "message": f"duplicate key {list(key)} (also at line {keys_seen[key]})",
                })
                duplicate_keys.append({"key": list(key), "lines": [keys_seen[key], i]})
            else:
                keys_seen[key] = i

    fail = sum(1 for f in findings if f["level"] == "FAIL")
    warn = sum(1 for f in findings if f["level"] == "WARN")

    return {
        "path": str(path), "rows": len(data_rows), "header_ok": header_ok,
        "findings": findings, "duplicate_keys": duplicate_keys,
        "summary": {"fail": fail, "warn": warn},
        "last_date": last_date, "keys": keys_all,
    }


def render_verdict_line(rows, summary):
    """The NORMATIVE verdict line — pinned exactly, selftest-asserted."""
    fail, warn = summary["fail"], summary["warn"]
    tier = "clean" if (fail == 0 and warn == 0) else f"{fail} fail / {warn} warn"
    return f"spend-ledger validate · {tier} · {rows} rows"


def selftest():
    import tempfile

    def write(td, lines):
        out = Path(td) / "ledger.csv"
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            for row in lines:
                w.writerow(row)
        return out

    clean_rows = [
        HEADER,
        ["2026-08-18", "build", "dispatch-ticket", "#624", "absent", "absent", "pr-opened", "undetermined", "UNMEASURED"],
        ["2026-08-17", "sweep", "issue-sorter", ".claude/ops/reports/2026-08-17T00-00-00Z.md",
         "absent", "absent", "acted", "undetermined", "A2"],
        ["2026-08-16", "build", "build-leader", "#626", "117950", "measured", "pr-merged", "worth-firing", "A1"],
    ]

    # Clean 3-row fixture -> 0 findings (reverse control); verdict line pinned exactly.
    with tempfile.TemporaryDirectory() as td:
        out = write(td, clean_rows)
        result = validate_file(out)
        assert result["rows"] == 3, result
        assert result["header_ok"] is True, result
        assert result["findings"] == [], result["findings"]
        assert result["summary"] == {"fail": 0, "warn": 0}, result
        assert render_verdict_line(result["rows"], result["summary"]) == \
            "spend-ledger validate · clean · 3 rows"

    # Foreign/reordered header -> FAIL, nothing else checked.
    with tempfile.TemporaryDirectory() as td:
        foreign = ["date", "kind", "seat", "tokens"]
        out = write(td, [foreign, ["2026-08-18", "build", "t", "1"]])
        result = validate_file(out)
        assert result["header_ok"] is False, result
        assert any(f["level"] == "FAIL" and "foreign/reordered header" in f["message"]
                   for f in result["findings"]), result["findings"]

    def one_bad_row(bad_row, expect_substr):
        with tempfile.TemporaryDirectory() as td:
            out = write(td, [HEADER, bad_row])
            result = validate_file(out)
            fails = [f for f in result["findings"] if f["level"] == "FAIL"]
            assert fails, f"expected a FAIL for {bad_row}"
            assert any(expect_substr in f["message"] for f in fails), (bad_row, fails)
            return result

    base = ["2026-08-18", "build", "dispatch-ticket", "#624", "absent", "absent", "pr-opened", "undetermined", "A3"]

    def with_field(field, value):
        row = list(base)
        row[HEADER.index(field)] = value
        return row

    # Bad date, unknown event_kind, unknown outcome, unknown verdict -> each one FAIL.
    one_bad_row(with_field("date", "2026-13-99"), "not a valid YYYY-MM-DD date")
    one_bad_row(with_field("event_kind", "audit"), "event_kind")
    one_bad_row(with_field("outcome", "meh"), "outcome")
    one_bad_row(with_field("verdict", "great"), "verdict")

    # gh#673: unknown archetype -> FAIL; every one of the eight archetypes plus the
    # `UNMEASURED` escape hatch stays clean (positive + reverse control, every closed value).
    one_bad_row(with_field("archetype", "A9"), "archetype")
    one_bad_row(with_field("archetype", ""), "archetype")
    for good_archetype in sorted(ARCHETYPES):
        with tempfile.TemporaryDirectory() as td:
            out = write(td, [HEADER, with_field("archetype", good_archetype)])
            result = validate_file(out)
            assert result["findings"] == [], (good_archetype, result["findings"])

    # tokens/tokens_source cross-field FAIL, both directions.
    row = with_field("tokens", "absent")
    row[HEADER.index("tokens_source")] = "measured"
    one_bad_row(row, "requires an integer tokens value")

    row = with_field("tokens", "1200")
    row[HEADER.index("tokens_source")] = "absent"
    one_bad_row(row, "tokens_source is `absent`")

    # Negative / non-integer tokens -> FAIL (each paired with a matching non-absent
    # tokens_source so only the tokens-shape finding fires, not the cross-field one too).
    for bad in ("-5", "12.5", "abc"):
        row = with_field("tokens", bad)
        row[HEADER.index("tokens_source")] = "estimated"
        one_bad_row(row, "not a non-negative integer")

    # Bad ref -> FAIL; the three legal ref shapes stay clean (positive + reverse control).
    one_bad_row(with_field("ref", "/abs"), "is not `#NNN`")
    for good_ref in ("#12", "none", ".claude/ops/reports/x.md"):
        with tempfile.TemporaryDirectory() as td:
            out = write(td, [HEADER, with_field("ref", good_ref)])
            result = validate_file(out)
            assert result["findings"] == [], (good_ref, result["findings"])

    # Exact duplicate key (ref != none) -> WARN.
    dup_row = list(base)
    with tempfile.TemporaryDirectory() as td:
        out = write(td, [HEADER, dup_row, dup_row])
        result = validate_file(out)
        warns = [f for f in result["findings"] if f["level"] == "WARN"]
        assert warns and "duplicate key" in warns[0]["message"], result["findings"]
        assert result["duplicate_keys"], result
        assert result["summary"]["warn"] == 1, result

    # Reverse control: the same repeated key with ref `none` -> NOT a warn.
    none_row = with_field("ref", "none")
    with tempfile.TemporaryDirectory() as td:
        out = write(td, [HEADER, none_row, none_row])
        result = validate_file(out)
        assert not any(f["level"] == "WARN" for f in result["findings"]), result["findings"]
        assert result["duplicate_keys"] == [], result

    # No-blended-column law, extended to this schema (Resolution 2's own precedent check).
    assert not any(("ratio" in c or "quotient" in c or "per_token" in c) for c in HEADER), HEADER

    # Missing-file path -> exit-0 "no ledger yet", never a false failure.
    with tempfile.TemporaryDirectory() as td:
        missing = Path(td) / "does-not-exist.csv"
        result = validate_file(missing)
        assert result["no_ledger_yet"] is True, result
        assert result["rows"] == 0, result

    # Same missing-file path, but at the main()-level CLI surface: a live subprocess
    # run must exit 0 and print the pinned "no ledger yet" line — not just the
    # validate_file() dict checked above.
    with tempfile.TemporaryDirectory() as td:
        missing = Path(td) / "does-not-exist.csv"
        proc = subprocess.run(
            [sys.executable, __file__, str(missing)],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, (proc.returncode, proc.stdout, proc.stderr)
        assert f"spend-ledger validate · no ledger yet · {missing}" in proc.stdout, proc.stdout

    print("validate.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode_or_path", nargs="?", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.mode_or_path == "selftest":
        return selftest()
    if not a.mode_or_path:
        print("validate.py: a ledger path is required (or `selftest`)", file=sys.stderr)
        return 2

    try:
        result = validate_file(a.mode_or_path)
    except OSError as e:
        print(f"validate.py: cannot read {a.mode_or_path}: {e}", file=sys.stderr)
        return 2

    if result.get("no_ledger_yet"):
        if a.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"spend-ledger validate · no ledger yet · {a.mode_or_path}")
        return 0

    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(render_verdict_line(result["rows"], result["summary"]))
        for f in result["findings"]:
            print(f"{result['path']}:{f['line']}: {f['level']} {f['message']}")
    return 0 if (result["summary"]["fail"] == 0 and result["summary"]["warn"] == 0) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"validate.py error: {e}", file=sys.stderr)
        sys.exit(2)
