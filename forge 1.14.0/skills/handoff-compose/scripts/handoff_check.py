#!/usr/bin/env python3
"""Mechanical gate for a handoff block (rubric H1 + the Status enum).

Usage:
    python3 handoff_check.py <file-containing-block>
    ... | python3 handoff_check.py            (block on stdin)
    python3 handoff_check.py selftest         (fixture-locked proof of the gates)

Checks only what is mechanically checkable — field presence, order, `(none)`
markers for empties, and a valid Status enum. The judgment dimensions
(H2 verifiability, H3 honesty, H4 routing, H5 freshness) stay with the rubric.
Exit 0 = all checks pass; exit 1 = at least one failure.

Selftest: a complete block must pass every gate, and a negative control missing the
Evidence field and claiming `Status: ok` (not in the enum) must exit 1 with both the
field-presence and Status-enum gates firing.
"""

import re
import sys

FIELDS = [
    "Status",
    "Summary",
    "Files changed",
    "Tests/checks run",
    "Evidence",
    "Risks",
    "Open questions",
    "Recommended next action",
]

STATUS_RE = re.compile(r"^\s*(done|partial\b.*|blocked\s*\(.+\))\s*$", re.IGNORECASE)


def field_pattern(name: str) -> re.Pattern:
    # Match "- **Name** — ...", "**Name**: ...", "Name — ...", etc., at line start.
    return re.compile(
        rf"^[ \t]*[-*]?[ \t]*\**{re.escape(name)}\**[ \t]*[—:-]",
        re.MULTILINE | re.IGNORECASE,
    )


def check_text(text: str) -> int:
    ok = True

    def report(passed: bool, label: str) -> bool:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}")
        return passed

    # Presence + position of every field.
    positions = {}
    for name in FIELDS:
        m = field_pattern(name).search(text)
        if not report(m is not None, f"H1 field present: {name}"):
            ok = False
        if m:
            positions[name] = m.start()

    # Order (only among the fields that are present).
    present = [n for n in FIELDS if n in positions]
    in_order = all(
        positions[a] < positions[b] for a, b in zip(present, present[1:])
    )
    if not report(in_order, "H1 fields in canonical order"):
        ok = False

    # No field left empty: content (which `(none)` satisfies) must follow each label.
    for i, name in enumerate(present):
        start = positions[name]
        end = positions[present[i + 1]] if i + 1 < len(present) else len(text)
        segment = text[start:end]
        body = re.sub(field_pattern(name), "", segment, count=1).strip()
        if not report(bool(body), f"H1 field non-empty (use `(none)`): {name}"):
            ok = False

    # Status enum: done | partial ... | blocked(reason).
    if "Status" in positions:
        seg_end = positions[present[1]] if len(present) > 1 else len(text)
        status_body = re.sub(
            field_pattern("Status"), "", text[positions["Status"]:seg_end], count=1
        ).strip().strip("`")
        if not report(
            bool(STATUS_RE.match(status_body)),
            "Status is done | partial <what remains> | blocked(reason)",
        ):
            ok = False

    checks_run = len(FIELDS) + 1 + len(present) + (1 if "Status" in positions else 0)
    print(f"-- {'all' if ok else 'NOT all'} {checks_run} gate checks passed --")
    return 0 if ok else 1


# --- selftest -------------------------------------------------------------------------------------
# Fixture-locked proof of the gates: drives check_text() — the SAME function the CLI uses.

_FIX_PASS = """\
- **Status** — done
- **Summary** — Implemented the selftest and verified the gates fire.
- **Files changed** — scripts/handoff_check.py
- **Tests/checks run** — python3 handoff_check.py selftest
- **Evidence** — selftest exit 0; transcript above
- **Risks** — (none)
- **Open questions** — (none)
- **Recommended next action** — merge
"""

# Negative control: no Evidence field, and `Status: ok` is outside the done|partial|blocked
# enum — an unverifiable feel-good handback. Must exit 1.
_FIX_NO_EVIDENCE = """\
- **Status** — ok
- **Summary** — Did the work.
- **Files changed** — (none)
- **Tests/checks run** — (none)
- **Risks** — (none)
- **Open questions** — (none)
- **Recommended next action** — (none)
"""


def selftest() -> int:
    import contextlib
    import io

    errs = []

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = check_text(_FIX_PASS)
    if code != 0:
        errs.append("complete block fixture did not exit 0; output:\n" + buf.getvalue())

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = check_text(_FIX_NO_EVIDENCE)
    out = buf.getvalue()
    if code != 1:
        errs.append("no-Evidence negative control did not exit 1")
    if "[FAIL] H1 field present: Evidence" not in out:
        errs.append("negative control: missing Evidence field did not fire the presence gate")
    if "[FAIL] Status is done | partial <what remains> | blocked(reason)" not in out:
        errs.append("negative control: 'Status: ok' did not fire the Status-enum gate")

    if errs:
        print("handoff_check selftest: FAIL (%d)" % len(errs))
        for e in errs:
            print("  - %s" % e)
        return 1
    print("handoff_check selftest: OK — complete block passes; missing-Evidence + 'Status: ok' "
          "negative control exits 1 with both gates firing")
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        return selftest()
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    return check_text(text)


if __name__ == "__main__":
    sys.exit(main())
