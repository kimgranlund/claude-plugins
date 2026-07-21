#!/usr/bin/env python3
"""audit-diff.py — the ui-audit baseline differ (the audit ledger). Self-contained (stdlib only).

An audit run persists its evidence into a dated dir (audits/<date>/): cards, checker outputs,
inventory.json, and findings.jsonl — the NORMALIZED ledger Step 6 appends every gate finding to,
one JSON object per line:

  {"checker": "check-colors", "gate": "CONTRAST_FAIL_AA", "id": "dashboard",
   "screen": "dashboard", "detail": "4.2:1 body text"}

checker/gate/id are REQUIRED (they are the finding's identity); screen/detail are optional
context. Checker output formats vary (contrast-check --json emits a full pair table; the other
checkers print text), so the differ never re-runs or re-parses checkers — it consumes ONLY the
persisted ledger. No ledger, no diff: that is an error, not an empty result.

  python3 audit-diff.py <baseline-dir> <current-dir> [--json] [--first-run]
  python3 audit-diff.py --ledger <baseline> <current> [--json] [--first-run]
  python3 audit-diff.py selftest

--ledger mode diffs CAMPAIGN ledgers (the skills-audit deep-review shard format) instead of audit
runs: rows are {"skill", "dim", "tier", "finding"?, "fix"?, "status"?} — skill/dim/tier REQUIRED —
and are mapped onto the usual identity (checker <- dim, gate <- tier, id <- skill; finding <-
detail, fix/status passed through), then diffed exactly as usual: same buckets, same exit codes.
Rows sharing (dim, tier, skill) dedupe like any ledger (first occurrence wins — a ledger is a
set). In --ledger mode each path may be either a directory (containing findings.jsonl) or a
direct path to the .jsonl file itself (campaign shards are named <skill>.findings.jsonl).

Findings are keyed by (checker, gate, id) — duplicates within one ledger dedupe (a ledger is a
set, not a log) — and bucketed:

  NEW           — in current, not baseline  -> regressions; they lead the report and FAIL the run
  RESOLVED      — in baseline, not current
  STILL_FAILING — in both

Exit codes: 0 = no NEW findings (or --first-run) · 1 = NEW findings non-empty (the CI regression
gate) · 2 = unusable input (missing ledger, malformed line) — never silently swallowed.

First runs have no baseline: pass --first-run — the baseline is treated as empty (the baseline
dir need not even exist), everything lands in NEW, but the gate is OFF (exit 0): a first run
establishes the baseline, it cannot regress against nothing. Without --first-run a missing
baseline ledger is an exit-2 error, never an empty diff.

Inventory delta (informational, never gates): when BOTH dirs carry a readable inventory.json,
screens and modules added/removed (by id) are reported; when either side lacks one, the delta is
reported as not diffed with the reason — an omission is stated, never blank.

Python 3.8+.
"""
import io
import json
import os
import sys
import tempfile

REQUIRED_KEYS = ("checker", "gate", "id")
LEDGER_REQUIRED_KEYS = ("skill", "dim", "tier")  # campaign-ledger identity (--ledger mode)
USAGE = ("usage: audit-diff.py [--ledger] <baseline-dir> <current-dir> [--json] [--first-run] "
         "| selftest\n")


def _map_ledger_row(obj):
    """Campaign-ledger row -> normalized finding: checker <- dim, gate <- tier, id <- skill,
    detail <- finding; fix/status pass through as context."""
    mapped = {"checker": obj["dim"], "gate": obj["tier"], "id": obj["skill"]}
    if obj.get("finding"):
        mapped["detail"] = obj["finding"]
    for k in ("fix", "status"):
        if obj.get(k):
            mapped[k] = obj[k]
    return mapped


def load_findings(dirpath, role, allow_missing=False, ledger=False):
    """Parse <dir>/findings.jsonl -> {(checker, gate, id): finding dict}.

    Duplicate keys dedupe (first occurrence wins). Raises ValueError with the offending line
    number on malformed input. A missing ledger raises unless allow_missing (the --first-run
    baseline), in which case the baseline is honestly empty. With ledger=True (--ledger mode)
    the path may be a directory OR the .jsonl file itself; rows are campaign-ledger rows
    (skill/dim/tier required) mapped onto the usual identity before diffing."""
    if ledger and os.path.isfile(dirpath):
        path = dirpath
    else:
        path = os.path.join(dirpath, "findings.jsonl")
    if not os.path.isfile(path):
        if allow_missing:
            return {}
        hint = (" (first run? pass --first-run to diff against an empty baseline)"
                if role == "baseline" else "")
        what = ("ledger path %r has no findings.jsonl" if ledger
                else "dir %r has no findings.jsonl — not a persisted audit dir")
        raise ValueError(("%s " + what + "%s") % (role, dirpath, hint))
    required = LEDGER_REQUIRED_KEYS if ledger else REQUIRED_KEYS
    findings = {}
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError("%s line %d: not valid JSON (%s)" % (path, n, e))
            if not isinstance(obj, dict):
                raise ValueError("%s line %d: a finding must be a JSON object, got %s"
                                 % (path, n, type(obj).__name__))
            missing = [k for k in required if not obj.get(k)]
            if missing:
                raise ValueError("%s line %d: finding missing required key(s): %s"
                                 % (path, n, ", ".join(missing)))
            if ledger:
                obj = _map_ledger_row(obj)
            key = (str(obj["checker"]), str(obj["gate"]), str(obj["id"]))
            findings.setdefault(key, obj)
    return findings


def diff_findings(baseline, current):
    """Bucket keyed findings: NEW (current only) · RESOLVED (baseline only) · STILL_FAILING."""
    return {
        "new": [current[k] for k in sorted(set(current) - set(baseline))],
        "resolved": [baseline[k] for k in sorted(set(baseline) - set(current))],
        "still_failing": [current[k] for k in sorted(set(baseline) & set(current))],
    }


def load_inventory_ids(dirpath, role):
    """<dir>/inventory.json -> ({'screens': set, 'modules': set}, None), or (None, reason)."""
    path = os.path.join(dirpath, "inventory.json")
    if not os.path.isfile(path):
        return None, "%s has no inventory.json" % role
    try:
        with open(path, encoding="utf-8") as fh:
            inv = json.load(fh)
        return ({"screens": {s["id"] for s in inv.get("screens", []) if isinstance(s, dict)},
                 "modules": {m["id"] for m in inv.get("modules", []) if isinstance(m, dict)}},
                None)
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as e:
        return None, "%s inventory.json unreadable (%s)" % (role, e)


def diff_inventory(base_inv, cur_inv):
    """Screens/modules added/removed by id — informational, never gates."""
    return {
        "screens_added": sorted(cur_inv["screens"] - base_inv["screens"]),
        "screens_removed": sorted(base_inv["screens"] - cur_inv["screens"]),
        "modules_added": sorted(cur_inv["modules"] - base_inv["modules"]),
        "modules_removed": sorted(base_inv["modules"] - cur_inv["modules"]),
    }


def _fmt_finding(f):
    s = "%s/%s %s" % (f["checker"], f["gate"], f["id"])
    if f.get("screen") and f["screen"] != f["id"]:
        s += " [screen: %s]" % f["screen"]
    if f.get("detail"):
        s += " — %s" % f["detail"]
    return s


def run(argv, out, err):
    """The CLI body: parse args, diff, print, return the exit code (0/1/2)."""
    baseline_dir = current_dir = None
    as_json = first_run = ledger = False
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--json":
            as_json = True
        elif a == "--first-run":
            first_run = True
        elif a == "--ledger":
            ledger = True
        elif baseline_dir is None:
            baseline_dir = a
        elif current_dir is None:
            current_dir = a
        else:
            err.write("audit-diff: unexpected argument %r\n" % a)
            return 2
    if not baseline_dir or not current_dir:
        err.write(USAGE)
        return 2

    try:
        baseline = load_findings(baseline_dir, "baseline", allow_missing=first_run, ledger=ledger)
        current = load_findings(current_dir, "current", ledger=ledger)
    except ValueError as e:
        err.write("audit-diff: %s\n" % e)
        return 2

    buckets = diff_findings(baseline, current)
    counts = {k: len(v) for k, v in buckets.items()}
    gate_exit = 1 if counts["new"] and not first_run else 0

    base_inv, base_note = load_inventory_ids(baseline_dir, "baseline")
    cur_inv, cur_note = load_inventory_ids(current_dir, "current")
    inv_delta, inv_note = None, None
    if base_inv is not None and cur_inv is not None:
        inv_delta = diff_inventory(base_inv, cur_inv)
    else:
        inv_note = "; ".join(n for n in (base_note, cur_note) if n)

    if as_json:
        json.dump({"baseline": baseline_dir, "current": current_dir, "first_run": first_run,
                   "ledger": ledger,
                   "new": buckets["new"], "resolved": buckets["resolved"],
                   "still_failing": buckets["still_failing"], "counts": counts,
                   "inventory_delta": inv_delta, "inventory_note": inv_note,
                   "regression_gate": "FAIL" if gate_exit else "PASS"}, out, indent=2)
        out.write("\n")
        return gate_exit

    out.write("audit-diff: baseline %s (%d finding(s)) vs current %s (%d finding(s))%s\n"
              % (baseline_dir, len(baseline), current_dir, len(current),
                 "   [--first-run: gate off]" if first_run else ""))
    for label, key in (("NEW (regressions)", "new"), ("RESOLVED", "resolved"),
                       ("STILL_FAILING", "still_failing")):
        out.write("%s: %d\n" % (label, counts[key]))
        for f in buckets[key]:
            out.write("  - %s\n" % _fmt_finding(f))
    if inv_delta is not None:
        out.write("Inventory delta (informational): screens +%d%s / -%d%s · modules +%d%s / -%d%s\n"
                  % (len(inv_delta["screens_added"]),
                     " (%s)" % ", ".join(inv_delta["screens_added"]) if inv_delta["screens_added"] else "",
                     len(inv_delta["screens_removed"]),
                     " (%s)" % ", ".join(inv_delta["screens_removed"]) if inv_delta["screens_removed"] else "",
                     len(inv_delta["modules_added"]),
                     " (%s)" % ", ".join(inv_delta["modules_added"]) if inv_delta["modules_added"] else "",
                     len(inv_delta["modules_removed"]),
                     " (%s)" % ", ".join(inv_delta["modules_removed"]) if inv_delta["modules_removed"] else ""))
    else:
        out.write("Inventory delta: not diffed (%s)\n" % inv_note)
    if first_run:
        out.write("Delta vs baseline: first run — baseline established (%d finding(s))\n"
                  % len(current))
    else:
        out.write("Delta vs baseline: %d new · %d resolved · %d still-failing\n"
                  % (counts["new"], counts["resolved"], counts["still_failing"]))
    return gate_exit


# --- selftest fixtures ---------------------------------------------------------------------------
# Baseline: 3 findings. Current: 2 of them persist, 1 (NO_VISIBLE_FOCUS) is resolved, 1 is new —
# so the diff must report NEW=1, RESOLVED=1, STILL_FAILING=2 and exit 1 (regression gate).
FIX_BASE = [
    {"checker": "check-colors", "gate": "CONTRAST_FAIL_AA", "id": "dashboard",
     "screen": "dashboard", "detail": "4.2:1 body text"},
    {"checker": "focus-verify", "gate": "NO_VISIBLE_FOCUS", "id": "settings#save"},
    {"checker": "flow-check", "gate": "DEAD_END", "id": "checkout:pay"},
]
FIX_CUR = [
    {"checker": "check-colors", "gate": "CONTRAST_FAIL_AA", "id": "dashboard",
     "screen": "dashboard", "detail": "4.2:1 body text"},
    {"checker": "flow-check", "gate": "DEAD_END", "id": "checkout:pay"},
    {"checker": "focus-verify", "gate": "POSITIVE_TABINDEX", "id": "reports#filter",
     "detail": "tabindex=3"},
]
FIX_BASE_INV = {"screens": [{"id": "home"}, {"id": "settings"}], "flows": [],
                "modules": [{"id": "x-chip", "kind": "element"}]}
FIX_CUR_INV = {"screens": [{"id": "home"}, {"id": "admin"}], "flows": [], "modules": []}
# Campaign-ledger fixtures (--ledger mode): rows keyed (dim, tier, skill) after mapping.
# Baseline: 3 rows. Current: 2 persist, ui-audit/S2 resolves, agents-audit/A4 is the PLANTED
# regression -> NEW=1, RESOLVED=1, STILL_FAILING=2, exit 1.
LEDGER_BASE = [
    {"skill": "ui-audit", "dim": "S2", "tier": "review",
     "finding": "description missing genre anchor", "fix": "anchor added", "status": "fixed"},
    {"skill": "ui-audit", "dim": "A3", "tier": "review",
     "finding": "probe docstring stale", "status": "open"},
    {"skill": "agents-audit", "dim": "M2", "tier": "gate",
     "finding": "fence not parseable", "status": "open"},
]
LEDGER_CUR = [
    {"skill": "ui-audit", "dim": "A3", "tier": "review",
     "finding": "probe docstring stale", "status": "open"},
    {"skill": "agents-audit", "dim": "M2", "tier": "gate",
     "finding": "fence not parseable", "status": "open"},
    {"skill": "agents-audit", "dim": "A4", "tier": "review",
     "finding": "index has no selftest", "status": "open"},
]


def _write_dir(root, findings=None, inventory=None, raw_ledger=None):
    os.makedirs(root, exist_ok=True)
    if raw_ledger is not None:
        with open(os.path.join(root, "findings.jsonl"), "w", encoding="utf-8") as fh:
            fh.write(raw_ledger)
    elif findings is not None:
        with open(os.path.join(root, "findings.jsonl"), "w", encoding="utf-8") as fh:
            for f in findings:
                fh.write(json.dumps(f) + "\n")
    if inventory is not None:
        with open(os.path.join(root, "inventory.json"), "w", encoding="utf-8") as fh:
            json.dump(inventory, fh)


def _run(argv):
    out, err = io.StringIO(), io.StringIO()
    code = run(argv, out, err)
    return code, out.getvalue(), err.getvalue()


def _keys(items):
    return [(f["checker"], f["gate"], f["id"]) for f in items]


def selftest():
    errs = []

    # --- 1. the three buckets + regression gate (exit 1) + inventory delta ---------------------
    with tempfile.TemporaryDirectory() as td:
        base, cur = os.path.join(td, "2026-07-01"), os.path.join(td, "2026-07-02")
        _write_dir(base, findings=FIX_BASE, inventory=FIX_BASE_INV)
        _write_dir(cur, findings=FIX_CUR, inventory=FIX_CUR_INV)
        code, out, _ = _run([base, cur, "--json"])
        if code != 1:
            errs.append("regression run must exit 1 (NEW non-empty), got %d" % code)
        data = json.loads(out)
        if _keys(data["new"]) != [("focus-verify", "POSITIVE_TABINDEX", "reports#filter")]:
            errs.append("NEW bucket wrong: %r" % _keys(data["new"]))
        if _keys(data["resolved"]) != [("focus-verify", "NO_VISIBLE_FOCUS", "settings#save")]:
            errs.append("RESOLVED bucket wrong: %r" % _keys(data["resolved"]))
        if sorted(_keys(data["still_failing"])) != [
                ("check-colors", "CONTRAST_FAIL_AA", "dashboard"),
                ("flow-check", "DEAD_END", "checkout:pay")]:
            errs.append("STILL_FAILING bucket wrong: %r" % _keys(data["still_failing"]))
        if data["counts"] != {"new": 1, "resolved": 1, "still_failing": 2}:
            errs.append("counts wrong: %r" % data["counts"])
        if data["regression_gate"] != "FAIL":
            errs.append("regression_gate must be FAIL: %r" % data["regression_gate"])
        inv = data["inventory_delta"]
        if not inv or inv["screens_added"] != ["admin"] or inv["screens_removed"] != ["settings"] \
                or inv["modules_added"] != [] or inv["modules_removed"] != ["x-chip"]:
            errs.append("inventory delta wrong: %r" % (inv,))
        code2, out2, _ = _run([base, cur])
        if code2 != 1 or "Delta vs baseline: 1 new · 1 resolved · 2 still-failing" not in out2:
            errs.append("text output delta line wrong (exit %d): %r" % (code2, out2))

    # --- 2. no NEW findings -> exit 0 (fixes only, gate passes) --------------------------------
    with tempfile.TemporaryDirectory() as td:
        base, cur = os.path.join(td, "b"), os.path.join(td, "c")
        _write_dir(base, findings=FIX_BASE)
        _write_dir(cur, findings=FIX_BASE[:2])  # one resolved, two still, nothing new
        code, out, _ = _run([base, cur, "--json"])
        data = json.loads(out)
        if code != 0 or data["counts"] != {"new": 0, "resolved": 1, "still_failing": 2}:
            errs.append("no-NEW run must exit 0 with 0/1/2 counts, got %d %r"
                        % (code, data["counts"]))

    # --- 3. first run: empty/absent baseline + --first-run -> everything NEW but exit 0 --------
    with tempfile.TemporaryDirectory() as td:
        ghost, cur = os.path.join(td, "never-ran"), os.path.join(td, "c")
        _write_dir(cur, findings=FIX_CUR)
        code, out, _ = _run([ghost, cur, "--first-run", "--json"])
        data = json.loads(out)
        if code != 0 or data["counts"]["new"] != 3 or data["regression_gate"] != "PASS":
            errs.append("first run must report all 3 NEW yet exit 0/PASS, got %d %r"
                        % (code, data["counts"]))
        codet, outt, _ = _run([ghost, cur, "--first-run"])
        if codet != 0 or "first run — baseline established (3 finding(s))" not in outt:
            errs.append("first-run text output wrong (exit %d): %r" % (codet, outt))
        # the same missing baseline WITHOUT --first-run is an error, never an empty diff
        code2, _, err2 = _run([ghost, cur])
        if code2 != 2 or "--first-run" not in err2:
            errs.append("missing baseline without --first-run must exit 2 with guidance, "
                        "got %d: %r" % (code2, err2))

    # --- 4. malformed ledger lines error cleanly (exit 2, line number named) -------------------
    with tempfile.TemporaryDirectory() as td:
        base, cur = os.path.join(td, "b"), os.path.join(td, "c")
        _write_dir(base, findings=FIX_BASE)
        _write_dir(cur, raw_ledger='{"checker": "a", "gate": "G", "id": "x"}\n{not json\n')
        code, _, err = _run([base, cur])
        if code != 2 or "line 2" not in err:
            errs.append("broken JSON line must exit 2 naming line 2, got %d: %r" % (code, err))
        _write_dir(cur, raw_ledger='{"checker": "a", "id": "x"}\n')  # gate missing
        code, _, err = _run([base, cur])
        if code != 2 or "gate" not in err:
            errs.append("missing required key must exit 2 naming it, got %d: %r" % (code, err))

    # --- 5b. --ledger mode: campaign rows map (dim->checker, tier->gate, skill->id), then diff --
    with tempfile.TemporaryDirectory() as td:
        base_f = os.path.join(td, "batch-3.findings.jsonl")   # direct FILE paths, not dirs
        cur_f = os.path.join(td, "batch-4.findings.jsonl")
        with open(base_f, "w", encoding="utf-8") as fh:
            for row in LEDGER_BASE:
                fh.write(json.dumps(row) + "\n")
        with open(cur_f, "w", encoding="utf-8") as fh:
            for row in LEDGER_CUR:
                fh.write(json.dumps(row) + "\n")
        code, out, _ = _run(["--ledger", base_f, cur_f, "--json"])
        data = json.loads(out)
        if code != 1 or data["regression_gate"] != "FAIL":
            errs.append("ledger planted regression must bite (exit 1/FAIL), got %d %r"
                        % (code, data.get("regression_gate")))
        if _keys(data["new"]) != [("A4", "review", "agents-audit")]:
            errs.append("ledger NEW bucket wrong (mapping dim->checker, tier->gate, skill->id): %r"
                        % _keys(data["new"]))
        if _keys(data["resolved"]) != [("S2", "review", "ui-audit")]:
            errs.append("ledger RESOLVED bucket wrong: %r" % _keys(data["resolved"]))
        if data["counts"] != {"new": 1, "resolved": 1, "still_failing": 2}:
            errs.append("ledger counts wrong: %r" % data["counts"])
        newf = data["new"][0]
        if newf.get("detail") != "index has no selftest" or newf.get("status") != "open":
            errs.append("ledger row context (finding->detail, status) not carried: %r" % (newf,))
        # clean pass: current is a subset of baseline (nothing NEW) -> exit 0
        clean_f = os.path.join(td, "batch-4-clean.findings.jsonl")
        with open(clean_f, "w", encoding="utf-8") as fh:
            for row in LEDGER_BASE[1:]:
                fh.write(json.dumps(row) + "\n")
        code, out, _ = _run(["--ledger", base_f, clean_f, "--json"])
        data = json.loads(out)
        if code != 0 or data["counts"]["new"] != 0:
            errs.append("clean ledger pass must exit 0 with no NEW, got %d %r"
                        % (code, data["counts"]))
        # a row missing a required ledger key errors cleanly (exit 2, key named)
        bad_f = os.path.join(td, "bad.findings.jsonl")
        with open(bad_f, "w", encoding="utf-8") as fh:
            fh.write('{"skill": "ui-audit", "dim": "S1", "finding": "no tier"}\n')
        code, _, err = _run(["--ledger", base_f, bad_f])
        if code != 2 or "tier" not in err:
            errs.append("ledger row missing tier must exit 2 naming it, got %d: %r" % (code, err))

    # --- 5. dedupe within a ledger + honest inventory omission ---------------------------------
    with tempfile.TemporaryDirectory() as td:
        base, cur = os.path.join(td, "b"), os.path.join(td, "c")
        dup = json.dumps(FIX_CUR[0])
        _write_dir(base, findings=[])
        _write_dir(cur, raw_ledger=dup + "\n" + dup + "\n")
        code, out, _ = _run([base, cur, "--json"])
        data = json.loads(out)
        if data["counts"]["new"] != 1:
            errs.append("duplicate ledger lines must dedupe to 1 finding: %r" % data["counts"])
        if data["inventory_delta"] is not None or "inventory.json" not in (data["inventory_note"] or ""):
            errs.append("absent inventories must be a stated omission: %r / %r"
                        % (data["inventory_delta"], data["inventory_note"]))

    return errs


def main(argv):
    if not argv or argv[0] == "selftest":
        errs = selftest()
        if errs:
            sys.stderr.write("audit-diff: FAIL (%d)\n" % len(errs))
            for e in errs:
                sys.stderr.write("  - %s\n" % e)
            return 1
        print("audit-diff: OK — NEW/RESOLVED/STILL_FAILING buckets, regression-gate exit codes, "
              "first-run baseline, malformed-ledger errors, dedupe + inventory delta, and "
              "--ledger campaign-row mapping (dim->checker, tier->gate, skill->id; planted "
              "regression bites, clean pass exits 0) verified over embedded fixtures")
        return 0
    return run(argv, sys.stdout, sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
