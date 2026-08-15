#!/usr/bin/env python3
"""trend.py — append the per-plugin attention trend row(s) at a release boundary.

Consumes rent.py --json output plus (optionally) a routing report JSON of the shape
{"<plugin>": {"dead": n, "stolen": n, "leaked": n}}. Columns stay SEPARATE series —
always-on chars and the three routing counts — never a combined quotient (Goodhart rule,
2026-08-15: a single quotient rewards deleting fences that protect rare-but-expensive
misroutes; the header is selftest-asserted to carry no ratio column). A missing routing
report records `absent`, never an invented number.

Usage:
  python3 trend.py --rent <rent.json> [--routing-report <path>] --out <trend.csv> [--date YYYY-MM-DD]
  python3 trend.py selftest

Exit: 0 appended · 2 error.
"""
import argparse
import csv
import datetime
import json
import os
import sys

HEADER = ["date", "plugin", "routable_skills", "routable_chars",
          "zero_rent_skills", "zero_rent_chars", "agents", "agent_chars",
          "dead", "stolen", "leaked"]


def append_rows(rent, routing, out_path, date):
    new = not os.path.isfile(out_path)
    with open(out_path, "a", newline="") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(HEADER)
        for row in rent["plugins"]:
            r = (routing or {}).get(row["plugin"], {})
            w.writerow([date, row["plugin"],
                        row["routable_skills"], row["routable_chars"],
                        row["zero_rent_skills"], row["zero_rent_chars"],
                        row["agents"], row["agent_chars"],
                        r.get("dead", "absent"), r.get("stolen", "absent"),
                        r.get("leaked", "absent")])
    return len(rent["plugins"])


def selftest():
    import tempfile
    rent = {"plugins": [
        {"plugin": "p1", "routable_skills": 2, "routable_chars": 100,
         "zero_rent_skills": 1, "zero_rent_chars": 20, "agents": 1, "agent_chars": 30},
        {"plugin": "p2", "routable_skills": 1, "routable_chars": 50,
         "zero_rent_skills": 0, "zero_rent_chars": 0, "agents": 0, "agent_chars": 0}]}
    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "trend.csv")
        n1 = append_rows(rent, {"p1": {"dead": 2, "stolen": 1, "leaked": 0}}, out, "2026-08-15")
        n2 = append_rows(rent, None, out, "2026-08-16")  # second boundary, no routing report
        rows = list(csv.reader(open(out)))
        assert n1 == 2 and n2 == 2 and len(rows) == 1 + 4, rows
        assert rows[0] == HEADER
        # separate-series law: no blended column, ever
        assert not any(("ratio" in c or "quotient" in c or "per_token" in c) for c in rows[0])
        # routing report present → real numbers; absent → the literal string, never invented
        assert rows[1][8:] == ["2", "1", "0"], rows[1]
        assert rows[3][8:] == ["absent", "absent", "absent"], rows[3]
        # append semantics: run 2 did not rewrite run 1
        assert rows[1][0] == "2026-08-15" and rows[3][0] == "2026-08-16"
    print("trend.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="")
    ap.add_argument("--rent")
    ap.add_argument("--routing-report")
    ap.add_argument("--out")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    if a.mode == "selftest":
        return selftest()
    if not a.rent or not a.out:
        print("trend.py: --rent and --out required (or `selftest`)", file=sys.stderr)
        return 2
    rent = json.load(open(a.rent))
    routing = json.load(open(a.routing_report)) if (
        a.routing_report and os.path.isfile(a.routing_report)) else None
    n = append_rows(rent, routing, a.out, a.date)
    print(f"appended {n} row(s) to {a.out}"
          + ("" if routing else " (routing columns: absent)"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"trend.py error: {e}", file=sys.stderr)
        sys.exit(2)
