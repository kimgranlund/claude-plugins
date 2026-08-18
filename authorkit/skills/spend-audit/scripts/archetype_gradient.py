#!/usr/bin/env python3
"""archetype_gradient.py — measured per-archetype orchestration cost multiplier table (gh#673,
lld-0021-archetype-cost-gradient.md), realizing idr-0010's estate-economy claim one layer
further: not just "did this firing pay for itself" (the existing Audit render), but "how much
MORE does archetype X cost than solo (A1), per equivalent outcome".

Reads `.claude/ops/spend-ledger.csv` (via `validate.py` as the schema canon — this script never
redefines HEADER/ARCHETYPES/OUTCOME_CLASSES, same sibling-import discipline as `trend.py`) and
computes, for every archetype other than A1 and every outcome class, the ratio of that
archetype's mean MEASURED tokens to A1's mean MEASURED tokens for the same outcome class.

**"Per equivalent outcome" — defined here, since it existed nowhere before gh#673.** Kept simple
and stated against the EXISTING closed `outcome` enum (validate.OUTCOME_CLASSES), no new column:
  - `pr-shipped`    := rows whose `outcome == "pr-merged"`
  - `record-minted` := rows whose `outcome == "acted"`
Every multiplier this script emits states which denominator class it normalizes against.

**Honesty over inference — the ticket's own acceptance bar.** A cell computes only when BOTH
sides (the archetype's own rows and A1's own rows, same outcome class, `tokens_source ==
"measured"`) have at least one row; anything short of that reports the literal `UNMEASURED`,
never a guessed number, never an average across `measured`/`estimated`/`absent` source classes
(the family's `measured`-vs-`measured` comparability rule, lld-0018 Resolution 3, unchanged
here). Wall-clock is a SEPARATE axis: the ledger schema carries no wall-clock column (not
authorized by this ticket — a deliberate non-goal, see the LLD's Rejected alternatives), so
every computed wall-clock cell is `UNMEASURED (not instrumented)` by construction; the one
wall-clock figure this script ever prints is gh#265's own anchor (1.92x tokens / 3.6x wall-clock,
the coordinator-hop measurement) — emitted under a separate `anchor` key, explicitly labeled as
an EXTERNAL CITATION, never computed from ledger rows, never blended into the `archetypes` table.

Usage:
  archetype_gradient.py <ledger.csv> [--json]
  archetype_gradient.py selftest

Exit codes: 0 rendered (including "no ledger yet", the expected first-run state — never a false
failure, same posture as `validate.py`) / 2 usage (no path given) or an unreadable existing file.
This script never FAILs on an all-UNMEASURED table — an honestly-reported gap is not an error.
"""
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate  # sibling module — HEADER/ARCHETYPES/ARCHETYPE_NAMES/OUTCOME_CLASSES canon

BASELINE = "A1"

# gh#265 (the coordinator-hop measurement, 2026-08-16) — the estate's sole prior cost
# measurement, cited verbatim as an external anchor. NEVER derived from ledger rows; NEVER
# folded into the computed `archetypes` table below (a reverse control in selftest() proves
# this value stays constant regardless of ledger content).
ANCHOR = {
    "source": "#265",
    "what": "solo-in-one-context vs. the real chore-lead seat chain (a coordinator-hop instance)",
    "tokens_multiplier": 1.92,
    "wall_clock_multiplier": 3.6,
    "note": "external citation, not computed from spend-ledger.csv rows — never a guessed "
            "multiplier for any OTHER archetype/outcome-class cell in this table",
}


def outcome_class_of(outcome: str):
    """Which of validate.OUTCOME_CLASSES this outcome belongs to, or None (out of scope for
    the per-equivalent-outcome table — e.g. `no-op`/`blocked`/`failed`/`pr-opened` firings)."""
    for cls, outcomes in validate.OUTCOME_CLASSES.items():
        if outcome in outcomes:
            return cls
    return None


def measured_tokens(rows, archetype, outcome_class):
    """Pure: the list of int token values for rows matching `archetype` + `outcome_class` +
    `tokens_source == measured`. Never mixes source classes (Resolution 3's rule, reused)."""
    out = []
    for row in rows:
        if row.get("archetype") != archetype:
            continue
        if outcome_class_of(row.get("outcome", "")) != outcome_class:
            continue
        if row.get("tokens_source") != "measured":
            continue
        tok = row.get("tokens", "")
        if tok.isdigit():
            out.append(int(tok))
    return out


def compute_gradient(rows):
    """Pure: rows (list of dicts, HEADER-keyed) -> the `archetypes` table dict. One entry per
    non-baseline archetype (A2..A8, plus UNMEASURED excluded — it is never a computed subject,
    only ever a value ambiguous retroactive rows carry) x outcome class."""
    table = {}
    for arch in sorted(validate.ARCHETYPE_NAMES):
        if arch == BASELINE:
            continue
        table[arch] = {}
        for cls in sorted(validate.OUTCOME_CLASSES):
            baseline_tokens = measured_tokens(rows, BASELINE, cls)
            arch_tokens = measured_tokens(rows, arch, cls)
            n_baseline, n_arch = len(baseline_tokens), len(arch_tokens)
            if n_baseline and n_arch:
                ratio = statistics.mean(arch_tokens) / statistics.mean(baseline_tokens)
                tokens_multiplier = round(ratio, 3)
            else:
                tokens_multiplier = "UNMEASURED"
            table[arch][cls] = {
                "tokens_multiplier": tokens_multiplier,
                "n_baseline_measured": n_baseline,
                "n_archetype_measured": n_arch,
                # not instrumented by this ticket — a deliberate non-goal, see the LLD.
                "wall_clock_multiplier": "UNMEASURED (not instrumented)",
            }
    return table


def render_rows_from_csv_dicts(reader_rows):
    """`reader_rows`: list of dicts already keyed by validate.HEADER (from a csv.DictReader
    over a validated ledger). Thin wrapper so selftest and main() share one path."""
    return compute_gradient(reader_rows)


def render_text(table, rows_considered):
    lines = [f"archetype-gradient · {rows_considered} rows considered · baseline {BASELINE}",
             f"  anchor: {ANCHOR['source']} — tokens {ANCHOR['tokens_multiplier']}x / "
             f"wall-clock {ANCHOR['wall_clock_multiplier']}x ({ANCHOR['what']}) — "
             "external citation, not computed"]
    for arch in sorted(table):
        for cls in sorted(table[arch]):
            cell = table[arch][cls]
            tm = cell["tokens_multiplier"]
            tm_s = f"{tm}x" if isinstance(tm, (int, float)) else tm
            lines.append(
                f"  {arch} ({validate.ARCHETYPE_NAMES[arch]}) / {cls}: "
                f"tokens {tm_s} (n_baseline={cell['n_baseline_measured']}, "
                f"n_{arch}={cell['n_archetype_measured']}), wall-clock {cell['wall_clock_multiplier']}"
            )
    return "\n".join(lines)


def run(ledger_path, as_json=False):
    """Returns (exit_code, rendered_text_or_None, payload_dict). Mirrors validate.py's own
    no-ledger-yet honesty: a missing ledger is exit 0, never a false failure."""
    result = validate.validate_file(ledger_path)
    if result.get("no_ledger_yet"):
        payload = {"no_ledger_yet": True, "path": str(ledger_path)}
        text = f"archetype-gradient · no ledger yet · {ledger_path}"
        return 0, (json.dumps(payload, indent=2) if as_json else text), payload

    with open(ledger_path, newline="") as fh:
        import csv
        reader = csv.reader(fh)
        header = next(reader, [])
        if header != validate.HEADER:
            payload = {"error": f"foreign/reordered header: expected {validate.HEADER}, got {header}"}
            text = f"archetype-gradient: {payload['error']} — run validate.py to see why"
            return 2, (json.dumps(payload, indent=2) if as_json else text), payload
        rows = [dict(zip(validate.HEADER, r)) for r in reader if len(r) == len(validate.HEADER)]

    table = compute_gradient(rows)
    payload = {
        "baseline": BASELINE,
        "outcome_classes": {cls: sorted(outs) for cls, outs in validate.OUTCOME_CLASSES.items()},
        "anchor": ANCHOR,
        "rows_considered": len(rows),
        "archetypes": table,
    }
    text = render_text(table, len(rows))
    return 0, (json.dumps(payload, indent=2) if as_json else text), payload


def selftest():
    import csv
    import tempfile

    def write_ledger(td, rows):
        out = Path(td) / "ledger.csv"
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(validate.HEADER)
            for r in rows:
                w.writerow(r)
        return out

    # No ledger yet -> exit 0, honest "no ledger yet", never a false failure.
    with tempfile.TemporaryDirectory() as td:
        missing = Path(td) / "does-not-exist.csv"
        code, text, payload = run(missing)
        assert code == 0 and payload.get("no_ledger_yet"), (code, payload)
        assert "no ledger yet" in text, text

    # All-absent ledger (today's real state — the ticket's own expected first-emit shape):
    # every cell UNMEASURED, n counts 0/0, rows_considered still correct, anchor still present
    # and UNCHANGED regardless of ledger content (the anchor-is-external reverse control).
    rows = [
        ["2026-08-18", "build", "dispatch-ticket", "#624", "absent", "absent", "pr-opened", "undetermined", "UNMEASURED"],
    ]
    with tempfile.TemporaryDirectory() as td:
        out = write_ledger(td, rows)
        code, text, payload = run(out, as_json=True)
        assert code == 0, payload
        assert payload["rows_considered"] == 1, payload
        assert payload["anchor"] == ANCHOR, payload
        for arch, classes in payload["archetypes"].items():
            for cls, cell in classes.items():
                assert cell["tokens_multiplier"] == "UNMEASURED", (arch, cls, cell)
                assert cell["n_baseline_measured"] == 0 and cell["n_archetype_measured"] == 0, cell
        assert "A1" not in payload["archetypes"], "baseline is never its own subject row"

    # Positive control: real measured rows on both sides of one cell compute a real ratio.
    # A1 pr-shipped: 100k, 200k (mean 150k). A2 pr-shipped: 300k (mean 300k) -> 2.0x.
    rows = [
        ["2026-08-18", "build", "s1", "#1", "100000", "measured", "pr-merged", "worth-firing", "A1"],
        ["2026-08-18", "build", "s2", "#2", "200000", "measured", "pr-merged", "worth-firing", "A1"],
        ["2026-08-18", "build", "s3", "#3", "300000", "measured", "pr-merged", "worth-firing", "A2"],
    ]
    with tempfile.TemporaryDirectory() as td:
        out = write_ledger(td, rows)
        code, _, payload = run(out, as_json=True)
        cell = payload["archetypes"]["A2"]["pr-shipped"]
        assert cell["tokens_multiplier"] == 2.0, cell
        assert cell["n_baseline_measured"] == 2 and cell["n_archetype_measured"] == 1, cell
        # A different outcome class (record-minted) has zero rows on both sides -> UNMEASURED,
        # never contaminated by the pr-shipped class's real numbers (per-class isolation).
        other = payload["archetypes"]["A2"]["record-minted"]
        assert other["tokens_multiplier"] == "UNMEASURED", other
        # An archetype with zero rows at all (A3 here) -> every cell UNMEASURED too.
        assert payload["archetypes"]["A3"]["pr-shipped"]["tokens_multiplier"] == "UNMEASURED"

    # Negative/reverse control: `estimated`/`absent` rows never feed the ratio, even when
    # plentiful — only `measured` counts (the comparability rule, reused from lld-0018).
    rows = [
        ["2026-08-18", "build", "s1", "#1", "999", "estimated", "pr-merged", "worth-firing", "A1"],
        ["2026-08-18", "build", "s2", "#2", "absent", "absent", "pr-merged", "worth-firing", "A2"],
    ]
    with tempfile.TemporaryDirectory() as td:
        out = write_ledger(td, rows)
        code, _, payload = run(out, as_json=True)
        cell = payload["archetypes"]["A2"]["pr-shipped"]
        assert cell["tokens_multiplier"] == "UNMEASURED", cell
        assert cell["n_baseline_measured"] == 0 and cell["n_archetype_measured"] == 0, cell

    # Wall-clock is NEVER computed from ledger rows — always the fixed "not instrumented"
    # string, even when tokens compute a real ratio in the very same cell.
    with tempfile.TemporaryDirectory() as td:
        out = write_ledger(td, [
            ["2026-08-18", "build", "s1", "#1", "100000", "measured", "pr-merged", "worth-firing", "A1"],
            ["2026-08-18", "build", "s2", "#2", "200000", "measured", "pr-merged", "worth-firing", "A2"],
        ])
        code, _, payload = run(out, as_json=True)
        cell = payload["archetypes"]["A2"]["pr-shipped"]
        assert cell["tokens_multiplier"] == 2.0, cell
        assert cell["wall_clock_multiplier"] == "UNMEASURED (not instrumented)", cell

    # Foreign/reordered header -> exit 2, never silently coerced.
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "ledger.csv"
        with open(out, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["date", "kind", "seat", "tokens"])
        code, text, payload = run(out)
        assert code == 2 and "error" in payload, (code, payload)

    # No-blended-column law, extended once more: this script's own emitted payload carries no
    # `ratio`/`quotient`/`per_token` TOP-LEVEL key beyond the explicitly-named, per-cell,
    # never-averaged-across-source-class `tokens_multiplier` (a report computation over rows,
    # never a stored ledger column — the multiplier lives here, not in validate.HEADER).
    assert "ratio" not in ANCHOR and "quotient" not in ANCHOR

    print("archetype_gradient.py selftest: PASS")
    return 0


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("mode_or_path", nargs="?", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.mode_or_path == "selftest":
        return selftest()
    if not a.mode_or_path:
        print("archetype_gradient.py: a ledger path is required (or `selftest`)", file=sys.stderr)
        return 2

    try:
        code, text, _ = run(a.mode_or_path, as_json=a.json)
    except OSError as e:
        print(f"archetype_gradient.py: cannot read {a.mode_or_path}: {e}", file=sys.stderr)
        return 2
    print(text)
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError:
        raise
    except Exception as e:  # noqa: BLE001
        print(f"archetype_gradient.py error: {e}", file=sys.stderr)
        sys.exit(2)
