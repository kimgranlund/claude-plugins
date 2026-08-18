#!/usr/bin/env python3
"""trend.py — append the recurrence-audit trend row(s) at a release boundary (IDR-0006).

Consumes scan.py's own --json output, plus two OPTIONAL judgment-layer inputs the SKILL body
computes live (never here — this script stays deterministic and network-blind):

  --recurrence <path>      {"<class-slug>": true|false, ...} — the live gh-issue conjunct-A
                            check's per-class verdict.
  --routing-report <path>  {"passed": N, "total": M} — a check-routing run transcribed to JSON.

Columns stay SEPARATE series, never a blended quotient (attention-audit's own Goodhart rule,
extended: no cross-series column either). A missing routing report records `absent`, never an
invented number — same degraded-mode contract as attention-audit/scripts/trend.py. Zero seeded
classes records `recurred_classes` as `0` (nothing to check); seeded classes present with no
--recurrence supplied records `absent` (the live check just wasn't run this pass) — the
zero-vs-absent distinction is deliberate, never collapsed.

Usage:
  python3 trend.py --scan <scan.json> [--recurrence <recurrence.json>]
                    [--routing-report <path>] --out <trend.csv> [--date YYYY-MM-DD]
  python3 trend.py selftest

Exit: 0 appended · 2 error.
"""
import argparse
import csv
import datetime
import json
import os
import sys

HEADER = ["date", "seeded_classes", "recurred_classes", "bare_citations", "files_scanned",
          "routing_passed", "routing_total", "routing_pass_rate"]


def compute_recurred(scan, recurrence):
    seeded = scan["totals"]["seeded_classes"]
    if seeded == 0:
        return "0"
    if recurrence is None:
        return "absent"
    return str(sum(1 for v in recurrence.values() if v))


def compute_routing(routing):
    if not routing:
        return "absent", "absent", "absent"
    passed = routing.get("passed")
    total = routing.get("total")
    if passed is None or total is None or total == 0:
        return "absent", "absent", "absent"
    rate = round(passed / total, 4)
    return str(passed), str(total), str(rate)


def append_row(scan, recurrence, routing, out_path, date):
    new = not os.path.isfile(out_path)
    recurred = compute_recurred(scan, recurrence)
    rpassed, rtotal, rrate = compute_routing(routing)
    row = [
        date,
        scan["totals"]["seeded_classes"],
        recurred,
        scan["totals"]["bare_citations"],
        scan["files_scanned"],
        rpassed, rtotal, rrate,
    ]
    with open(out_path, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(HEADER)
        w.writerow(row)
    return row


def selftest():
    import tempfile

    base_scan = {
        "target": "/x", "files_scanned": 10,
        "seeded_classes": [], "bare_citations": {"count": 5, "files": 3},
        "totals": {"seeded_classes": 0, "seeded_citations": 0, "bare_citations": 5},
    }

    # Fresh file gets the header row (positive), second append does not rewrite the first.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        r1 = append_row(base_scan, None, None, out, "2026-08-18")
        append_row(base_scan, None, None, out, "2026-08-19")
        rows = list(csv.reader(open(out)))
        assert rows[0] == HEADER
        assert len(rows) == 1 + 2, rows
        assert rows[1][0] == "2026-08-18" and rows[2][0] == "2026-08-19"
        assert r1[0] == "2026-08-18"

    # Zero seeded classes -> recurred_classes is the literal "0", never "absent".
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        row = append_row(base_scan, None, None, out, "2026-08-18")
        assert row[2] == "0", row

    # Seeded classes present, no --recurrence supplied -> "absent" (the live check wasn't
    # run this pass) — never collapsed with the zero-seeded case above.
    seeded_scan = dict(base_scan)
    seeded_scan["totals"] = dict(base_scan["totals"], seeded_classes=2)
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        row = append_row(seeded_scan, None, None, out, "2026-08-18")
        assert row[1] == 2 and row[2] == "absent", row

    # A supplied --recurrence with a true/false mix counts only the trues.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        recurrence = {"class-a": True, "class-b": False}
        row = append_row(seeded_scan, recurrence, None, out, "2026-08-18")
        assert row[2] == "1", row

    # Missing --routing-report -> all three routing columns read "absent".
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        row = append_row(base_scan, None, None, out, "2026-08-18")
        assert row[5:] == ["absent", "absent", "absent"], row

    # A present, parseable --routing-report -> real numbers + computed pass rate.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        row = append_row(base_scan, None, {"passed": 92, "total": 100}, out, "2026-08-18")
        assert row[5:] == ["92", "100", "0.92"], row

    # A malformed/zero-total routing report is treated as absent, never a divide-by-zero.
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        row = append_row(base_scan, None, {"passed": 0, "total": 0}, out, "2026-08-18")
        assert row[5:] == ["absent", "absent", "absent"], row

    # No blended/ratio column across the two series, ever (Goodhart rule, extended).
    assert not any(
        ("ratio" in c or "quotient" in c or "per_token" in c) for c in HEADER
    ), HEADER
    assert "routing_pass_rate" in HEADER and "recurred_classes" in HEADER
    assert not any(c == "combined_score" for c in HEADER)

    print("trend.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--scan")
    ap.add_argument("--recurrence")
    ap.add_argument("--routing-report")
    ap.add_argument("--out")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    if a.mode == "selftest":
        return selftest()
    if not a.scan or not a.out:
        print("trend.py: --scan and --out required (or `selftest`)", file=sys.stderr)
        return 2
    scan = json.load(open(a.scan))
    recurrence = json.load(open(a.recurrence)) if (
        a.recurrence and os.path.isfile(a.recurrence)) else None
    routing = json.load(open(a.routing_report)) if (
        a.routing_report and os.path.isfile(a.routing_report)) else None
    row = append_row(scan, recurrence, routing, a.out, a.date)
    print(f"appended row to {a.out}: {dict(zip(HEADER, row))}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"trend.py error: {e}", file=sys.stderr)
        sys.exit(2)
