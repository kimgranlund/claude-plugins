#!/usr/bin/env python3
"""trend.py — append exactly one validated row to the spend ledger (idr-0010).

One row per firing (a sweep or a dispatched build), append-only, per
`lld-0018-estate-economy-ledger.md`'s close-out convention (Resolution 4): the seat that
owns a firing's close-out on a real checkout appends the row as its last step; a sealed
dispatched seat's dispatcher appends on its behalf. Imports `validate.py` as a sibling
module (`import validate` — `sys.path[0]` is this script's own dir when run by path) so
the row schema exists in exactly ONE file; this script never redefines `HEADER` or any
enum.

Behaviour that differs from its `attention-audit`/`recurrence-audit` siblings, and is the
point: it validates BEFORE it writes. A malformed row is refused outright — nothing is
written, not even the header on a fresh file. An existing file whose header is not the
canonical `HEADER` is refused too (never append under a foreign schema — run
`validate.py` on it to see why).

Usage:
  trend.py --out <ledger.csv> --event-kind <sweep|build> --seat <slug>
           --ref <#NNN|path|none> [--tokens <N|absent>] [--tokens-source <measured|estimated|absent>]
           --outcome <enum> --verdict <enum> --archetype <A1..A8|UNMEASURED> [--date YYYY-MM-DD]
           [--dry-run]
  trend.py selftest

Exit codes: 0 appended (or, with --dry-run, printed without writing) / 1 row invalid
(a validate_row finding — nothing written) / 2 usage error or schema mismatch (an
existing file's header is not HEADER).

`--archetype` (gh#673, lld-0021) is REQUIRED like `--event-kind`/`--seat`/`--ref`/`--outcome`/
`--verdict` — an omitted flag is a usage error (exit 2), same tier as the other required
fields; an out-of-enum VALUE (an invalid-but-supplied archetype) still routes through
validate_row for the exit-1 write-refusal path, same reasoning as every other enum column
(see main()'s own comment on why none of these carry argparse `choices=`).
"""
import argparse
import csv
import datetime
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # sibling module — the schema canon (HEADER + enums + validate_row)


def build_row(args):
    """Build the row dict from argv-shaped args. Returns (row_dict, error) — error is a
    usage-error string (never None alongside a usable row) when exactly one of
    tokens/tokens-source was supplied without its pair."""
    tokens_given = args.tokens is not None
    source_given = args.tokens_source is not None
    if tokens_given != source_given:
        return None, (
            "--tokens and --tokens-source must be supplied together (or neither, "
            "defaulting to `absent`,`absent`) — never a number paired with `absent`"
        )
    tokens = args.tokens if tokens_given else "absent"
    tokens_source = args.tokens_source if source_given else "absent"
    row = {
        "date": args.date,
        "event_kind": args.event_kind or "",
        "seat": args.seat or "",
        "ref": args.ref or "",
        "tokens": tokens,
        "tokens_source": tokens_source,
        "outcome": args.outcome or "",
        "verdict": args.verdict or "",
        "archetype": args.archetype or "",
    }
    return row, None


def append_row(row, out_path):
    """Append `row` (already validated) to `out_path`. Writes the header first on a
    fresh OR empty (0-byte) file — a pre-created-but-empty file is treated as fresh,
    never as a foreign/missing header (the file existing at all must not skip the
    header write). Returns the row as a HEADER-ordered list."""
    new = (not os.path.isfile(out_path)) or os.path.getsize(out_path) == 0
    ordered = [row[c] for c in validate.HEADER]
    with open(out_path, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(validate.HEADER)
        w.writerow(ordered)
    return ordered


def run(row, out_path, dry_run=False):
    """Validate `row`; on success either append (default) or just render it
    (--dry-run). Returns (exit_code, message, row_or_none).

    - row invalid -> (1, findings, None), nothing written.
    - existing file's header foreign -> (2, message, None), nothing written.
    - dry-run -> (0, rendered row, ordered_row), file untouched.
    - else -> (0, appended message, ordered_row).
    """
    findings = validate.validate_row(row)
    if findings:
        return 1, "; ".join(findings), None

    if os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
        with open(out_path, newline="") as fh:
            existing_header = next(csv.reader(fh), None)
        if existing_header is not None and existing_header != validate.HEADER:
            return 2, (
                f"schema mismatch: {out_path} has header {existing_header}, expected "
                f"{validate.HEADER} — never append under a foreign schema; run "
                f"validate.py to see why"
            ), None

    if dry_run:
        ordered = [row[c] for c in validate.HEADER]
        return 0, f"would append to {out_path}: {dict(zip(validate.HEADER, ordered))}", ordered

    ordered = append_row(row, out_path)
    return 0, f"appended row to {out_path}: {dict(zip(validate.HEADER, ordered))}", ordered


def selftest():
    import tempfile

    good = {
        "date": "2026-08-18", "event_kind": "build", "seat": "dispatch-ticket",
        "ref": "#624", "tokens": "absent", "tokens_source": "absent",
        "outcome": "pr-opened", "verdict": "undetermined", "archetype": "A3",
    }

    # Fresh file -> header + one row (positive); second append does not rewrite the first.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        code1, _, row1 = run(good, out)
        code2, _, row2 = run(dict(good, date="2026-08-19"), out)
        assert code1 == 0 and code2 == 0, (code1, code2)
        rows = list(csv.reader(open(out)))
        assert rows[0] == validate.HEADER, rows
        assert len(rows) == 1 + 2, rows
        assert rows[1][0] == "2026-08-18" and rows[2][0] == "2026-08-19"
        assert row1 == rows[1] and row2 == rows[2]

    # A malformed row (bad outcome) -> exit-1 path AND the file is byte-identical
    # before/after — the write is refused, not partially applied (negative control).
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        run(good, out)
        before = Path(out).read_bytes()
        bad = dict(good, outcome="bogus")
        code, msg, row = run(bad, out)
        after = Path(out).read_bytes()
        assert code == 1 and row is None, (code, msg, row)
        assert before == after, "write must be refused, not partially applied"

    # A fresh path + a malformed row -> no file created at all.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        bad = dict(good, outcome="bogus")
        code, msg, row = run(bad, out)
        assert code == 1 and not os.path.isfile(out), (code, msg)

    # A foreign-header file -> the schema-mismatch path (exit 2), no append.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date", "kind", "seat", "tokens"])
            w.writerow(["2026-08-18", "build", "t", "1"])
        before = Path(out).read_bytes()
        code, msg, row = run(good, out)
        after = Path(out).read_bytes()
        assert code == 2 and row is None, (code, msg)
        assert before == after, "a foreign-header file must never be appended to"

    # A pre-created but EMPTY (0-byte) file is treated as fresh -> header IS written,
    # never silently skipped (the file-existence check alone must not suppress it).
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        Path(out).touch()
        assert os.path.getsize(out) == 0
        code, _, row = run(good, out)
        assert code == 0, (code, row)
        rows = list(csv.reader(open(out)))
        assert rows[0] == validate.HEADER, rows
        assert len(rows) == 2, rows

    # Both tokens flags omitted -> row carries absent,absent (build_row's own contract).
    def make_ns(tokens, tokens_source):
        return argparse.Namespace(
            date=good["date"], event_kind=good["event_kind"], seat=good["seat"],
            ref=good["ref"], outcome=good["outcome"], verdict=good["verdict"],
            archetype=good["archetype"], tokens=tokens, tokens_source=tokens_source,
        )

    ns = make_ns(None, None)
    row, err = build_row(ns)
    assert err is None and row["tokens"] == "absent" and row["tokens_source"] == "absent", (row, err)

    # Only one of tokens/tokens-source supplied -> usage error, never silently paired.
    ns.tokens = "1200"
    ns.tokens_source = None
    row, err = build_row(ns)
    assert row is None and err, (row, err)
    ns.tokens = None
    ns.tokens_source = "measured"
    row, err = build_row(ns)
    assert row is None and err, (row, err)

    # --dry-run leaves the file untouched and prints the row (via run()'s dry_run=True).
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        code, msg, row = run(good, out, dry_run=True)
        assert code == 0 and row == [good[c] for c in validate.HEADER], (code, row)
        assert not os.path.isfile(out), "--dry-run must never touch the file"
        assert "would append" in msg, msg

    # No blended/ratio column, ever (the family's Goodhart rule, extended to this schema
    # too — validate.HEADER is the one canon both scripts assert against).
    assert not any(("ratio" in c or "quotient" in c or "per_token" in c) for c in validate.HEADER)

    # gh#673: an invalid archetype value -> exit-1 write-refusal path (same tier as a bad
    # outcome/verdict), never a usage error.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        code, msg, row = run(dict(good, archetype="A9"), out)
        assert code == 1 and row is None, (code, msg, row)

    # `UNMEASURED` is a valid archetype value end-to-end (the retroactive-backfill escape
    # hatch) — a positive control, not just a validate.py-level enum membership check.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        code, _, row = run(dict(good, archetype="UNMEASURED"), out)
        assert code == 0, row
        readback = list(csv.reader(open(out)))[1]
        assert readback[validate.HEADER.index("archetype")] == "UNMEASURED", readback

    # A live CLI call with no `--archetype` at all is a usage error (exit 2) — required like
    # `--outcome`/`--verdict`, not silently defaulted.
    proc = subprocess.run(
        [sys.executable, __file__, "--out", "/dev/null", "--event-kind", "build",
         "--seat", "t", "--ref", "none", "--outcome", "acted", "--verdict", "undetermined"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 2 and "--archetype" in proc.stderr, (proc.returncode, proc.stderr)

    # verdict is passed through verbatim — the script never rewrites it from tokens.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "ledger.csv")
        extreme = dict(good, tokens="999999", tokens_source="measured", verdict="worth-firing")
        code, _, row = run(extreme, out)
        assert code == 0, row
        readback = list(csv.reader(open(out)))[1]
        assert readback[validate.HEADER.index("verdict")] == "worth-firing", readback
        assert readback[validate.HEADER.index("tokens")] == "999999", readback

    print("trend.py selftest: PASS")
    return 0


def main():
    # Deliberately NO `choices=` on event-kind/tokens-source/outcome/verdict: an invalid
    # enum value must reach validate_row and take the exit-1 write-refusal path (LLD
    # Acceptance 4, checked live) — argparse's own `choices=` would intercept it first
    # and exit 2 (a usage error), which is the wrong exit code for a semantically
    # invalid-but-well-formed row.
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--out")
    ap.add_argument("--event-kind")
    ap.add_argument("--seat")
    ap.add_argument("--ref")
    ap.add_argument("--tokens", default=None)
    ap.add_argument("--tokens-source", dest="tokens_source", default=None)
    ap.add_argument("--outcome")
    ap.add_argument("--verdict")
    ap.add_argument("--archetype")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.mode == "selftest":
        return selftest()

    missing = [f"--{name}" for name, val in (
        ("out", a.out), ("event-kind", a.event_kind), ("seat", a.seat),
        ("ref", a.ref), ("outcome", a.outcome), ("verdict", a.verdict),
        ("archetype", a.archetype),
    ) if not val]
    if missing:
        print(f"trend.py: required flags missing: {', '.join(missing)} (or `selftest`)",
              file=sys.stderr)
        return 2

    row, err = build_row(a)
    if err:
        print(f"trend.py: {err}", file=sys.stderr)
        return 2

    code, msg, _ = run(row, a.out, dry_run=a.dry_run)
    print(msg, file=(sys.stderr if code else sys.stdout))
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"trend.py error: {e}", file=sys.stderr)
        sys.exit(2)
