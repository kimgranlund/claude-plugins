#!/usr/bin/env python3
"""write_routing_report.py — persist ONE plugin's check-routing matrix to a stable, shared path.

Closes issue #693's remaining open item: check-routing itself never persisted its Phase 5
routing matrix anywhere — its report was ephemeral session output only (the `harness-audit-*/`
family a few evals.json comments cite is `check-everything`'s own dated, gitignored audit
output, never check-routing's, and never committed). authorkit's `attention-audit` already
INGESTS a routing report at trend-capture time (`scripts/trend.py --routing-report <path>`,
shape `{"<plugin>": {"dead": n, "stolen": n, "leaked": n}}`) — it just had nothing durable to
point at. This script is the missing write side, nothing else: it does not change check-routing's
own matrix-computation procedure, only persists the three tunable counts once Phase 4 has them.

Path is STABLE (one file, never dated) rather than the `harness-audit-<date>/` convention:
one merged JSON at a fixed location, each run overwriting only its own plugin's entry — so a
reader (attention-audit) never has to glob for "the latest" dated directory; each plugin's own
entry already IS its latest. Default path: `<repo-root>/.claude/ops/routing-report.json`,
tracked in git alongside this workspace's other durable ops state (`fleet.json`, `plan.md`,
`held-items.md`) — never the gitignored `harness-audit-*/` family, which is local-only audit
scratch space, not a durable cross-session artifact.

Usage:
  write_routing_report.py <plugin> --dead N --stolen N --leaked N --out <path> [--date YYYY-MM-DD]
  write_routing_report.py selftest

Exit: 0 written · 2 error (bad args, unreadable existing file).
"""
import argparse
import datetime
import json
import os
import sys


def merge_entry(existing: dict, plugin: str, dead: int, stolen: int, leaked: int, date: str) -> dict:
    """Pure: returns a NEW dict — existing's other plugins untouched, this plugin's entry
    replaced wholesale (never merged field-by-field, so a stale key from an older report shape
    never survives under a plugin that stopped reporting it)."""
    out = dict(existing)
    out[plugin] = {"dead": dead, "stolen": stolen, "leaked": leaked, "as_of": date}
    return out


def load_existing(path: str) -> dict:
    """Absent file -> {} (first write). A present-but-unreadable file is a real error, not
    silently discarded — never overwrite another plugin's already-recorded numbers by accident."""
    if not os.path.isfile(path):
        return {}
    with open(path) as fh:
        return json.load(fh)


def write_report(path: str, data: dict) -> None:
    out_dir = os.path.dirname(path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(path, "w") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write("\n")


def selftest():
    import tempfile

    # merge_entry — pure, no I/O
    existing = {"authorkit": {"dead": 1, "stolen": 0, "leaked": 2, "as_of": "2026-08-10"}}
    merged = merge_entry(existing, "harness", 3, 1, 0, "2026-08-18")
    assert merged["authorkit"] == existing["authorkit"], "an untouched plugin's entry must survive"
    assert merged["harness"] == {"dead": 3, "stolen": 1, "leaked": 0, "as_of": "2026-08-18"}
    # re-running for the SAME plugin replaces wholesale, never accretes stale fields
    remerged = merge_entry(merged, "harness", 0, 0, 0, "2026-08-19")
    assert remerged["harness"] == {"dead": 0, "stolen": 0, "leaked": 0, "as_of": "2026-08-19"}
    assert remerged["authorkit"] == existing["authorkit"]

    with tempfile.TemporaryDirectory() as td:
        out = os.path.join(td, "nested", "routing-report.json")

        # absent file -> {} (first write), and the nested dir is created
        assert load_existing(out) == {}
        write_report(out, merge_entry({}, "authorkit", 2, 1, 0, "2026-08-18"))
        assert os.path.isfile(out)

        # second write for a DIFFERENT plugin preserves the first's entry (the reason this
        # is a merged single file rather than one file per run)
        data = load_existing(out)
        data = merge_entry(data, "docs", 0, 0, 1, "2026-08-19")
        write_report(out, data)
        reread = load_existing(out)
        assert reread["authorkit"] == {"dead": 2, "stolen": 1, "leaked": 0, "as_of": "2026-08-18"}
        assert reread["docs"] == {"dead": 0, "stolen": 0, "leaked": 1, "as_of": "2026-08-19"}

        # a present-but-corrupt file is a real error, never silently treated as empty
        bad = os.path.join(td, "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not json")
        try:
            load_existing(bad)
            raise AssertionError("expected json.JSONDecodeError on a corrupt existing report")
        except json.JSONDecodeError:
            pass

    print("write_routing_report.py selftest: PASS")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode_or_plugin", nargs="?", default="")
    ap.add_argument("--dead", type=int)
    ap.add_argument("--stolen", type=int)
    ap.add_argument("--leaked", type=int)
    ap.add_argument("--out", default=os.path.join(".claude", "ops", "routing-report.json"))
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    if a.mode_or_plugin == "selftest":
        return selftest()

    plugin = a.mode_or_plugin
    if not plugin or a.dead is None or a.stolen is None or a.leaked is None:
        print("write_routing_report.py: <plugin> --dead N --stolen N --leaked N required "
              "(or `selftest`)", file=sys.stderr)
        return 2

    existing = load_existing(a.out)
    data = merge_entry(existing, plugin, a.dead, a.stolen, a.leaked, a.date)
    write_report(a.out, data)
    print(f"wrote {plugin} (dead={a.dead} stolen={a.stolen} leaked={a.leaked}) to {a.out}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except json.JSONDecodeError as e:
        print(f"write_routing_report.py: unreadable existing report at the --out path: {e}",
              file=sys.stderr)
        sys.exit(2)
    except Exception as e:  # noqa: BLE001
        print(f"write_routing_report.py error: {e}", file=sys.stderr)
        sys.exit(2)
