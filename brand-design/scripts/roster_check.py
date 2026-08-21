#!/usr/bin/env python3
"""roster-check — mechanical validator for a council's references/roster.md.

Proves the roster-file contract (council-rules' references/roster-file-contract.md):
handle<->persona-file bijection against the council's critics/ directory, every row's
sub-councils cell non-empty, `full` never used as a literal sub-council value, every
`## Groups` entry resolving to a seated active handle or the literal VACANT, and
role/status values drawn from their fixed enums. A VACANT lead is a named WARNING,
never a failure.

Usage:
  roster_check.py <council-skill-dir>   # e.g. brand-design/skills/check-brand-council
  roster_check.py selftest

Exit codes: 0 = clean (warnings allowed), 1 = a real violation found, 2 = usage error
(missing roster.md, missing critics/ dir, bad arguments). Stdlib only (Python 3.8+).
"""
import os
import re
import sys

ROLE_ENUM = {"lead", "member"}
STATUS_ENUM = {"active", "retired"}


class RosterError(Exception):
    """Usage-level problem (exit 2) — file/dir missing, table unparsable."""


def _parse_table(text):
    """Return list of row dicts from the first markdown table in text."""
    lines = text.splitlines()
    rows = []
    header = None
    in_table = False
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            in_table = True
            continue
        if all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue  # separator row
        if len(cells) != len(header):
            continue
        rows.append(dict(zip(header, cells)))
    if header is None:
        raise RosterError("no markdown table found in roster.md")
    required = {"handle", "sub-councils", "role", "status", "seated", "fixture"}
    missing = required - set(header)
    if missing:
        raise RosterError(f"roster.md table missing column(s): {sorted(missing)}")
    return rows


def _parse_groups(text):
    """Return {group_name: [tokens]} from the '## Groups' section's '- name: a=b, c=d' lines."""
    m = re.search(r"^##\s*Groups\s*$", text, re.M)
    if not m:
        return {}
    body = text[m.end():]
    nxt = re.search(r"^##\s+", body, re.M)
    if nxt:
        body = body[:nxt.start()]
    groups = {}
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        line = line.lstrip("-").strip()
        if ":" not in line:
            continue
        name, rest = line.split(":", 1)
        name = name.strip()
        # entries are "sub=handle, sub2=handle2" or a plain comma list of handles
        tokens = []
        for part in rest.split(","):
            part = part.strip()
            if "=" in part:
                part = part.split("=", 1)[1].strip()
            if part:
                tokens.append(part)
        groups[name] = tokens
    return groups


def check_roster(roster_dir):
    """roster_dir: a council skill's directory (e.g. .../check-brand-council).
    Returns (violations, warnings) — both lists of strings."""
    roster_path = os.path.join(roster_dir, "references", "roster.md")
    critics_dir = os.path.join(roster_dir, "references", "critics")
    if not os.path.isfile(roster_path):
        raise RosterError(f"no roster.md at {roster_path}")
    if not os.path.isdir(critics_dir):
        raise RosterError(f"no critics/ directory at {critics_dir}")

    text = open(roster_path, encoding="utf-8").read()
    rows = _parse_table(text)
    groups = _parse_groups(text)

    violations = []
    warnings = []

    roster_handles = {r["handle"] for r in rows if r.get("handle")}
    file_handles = set()
    for fn in os.listdir(critics_dir):
        m = re.fullmatch(r"critic-(.+)\.md", fn)
        if m:
            file_handles.add(m.group(1))

    # bijection
    for h in sorted(roster_handles - file_handles):
        violations.append(f"roster row '{h}' has no matching critic-{h}.md file")
    for h in sorted(file_handles - roster_handles):
        violations.append(f"critic-{h}.md exists on disk but has no roster.md row")

    active_handles = {r["handle"] for r in rows if r.get("status") == "active"}

    for r in rows:
        handle = r.get("handle", "<blank>")
        subs = [s.strip() for s in r.get("sub-councils", "").split(",") if s.strip()]
        if not subs:
            violations.append(f"'{handle}' has an empty sub-councils cell")
        if "full" in subs:
            violations.append(f"'{handle}' lists reserved name 'full' as a sub-council")
        role = r.get("role", "")
        if role not in ROLE_ENUM:
            violations.append(f"'{handle}' has unknown role '{role}' (expected lead|member)")
        status = r.get("status", "")
        if status not in STATUS_ENUM:
            violations.append(f"'{handle}' has unknown status '{status}' (expected active|retired)")
        if not r.get("seated", "").strip():
            violations.append(f"'{handle}' has an empty seated cell")
        if not r.get("fixture", "").strip():
            violations.append(f"'{handle}' has an empty fixture cell")

    # at most one lead per sub-council
    lead_subs = {}
    for r in rows:
        if r.get("role") == "lead":
            for s in [x.strip() for x in r.get("sub-councils", "").split(",") if x.strip()]:
                lead_subs.setdefault(s, []).append(r.get("handle"))
    for sub, handles in lead_subs.items():
        if len(handles) > 1:
            violations.append(f"sub-council '{sub}' has more than one lead row: {handles}")

    # groups: every token resolves to VACANT or a seated active handle
    for gname, tokens in groups.items():
        for tok in tokens:
            if tok == "VACANT":
                warnings.append(f"group '{gname}' has a VACANT slot")
                continue
            if tok not in active_handles:
                violations.append(
                    f"group '{gname}' references '{tok}', which is not a seated active handle"
                )

    return violations, warnings


def main(argv):
    if argv and argv[0] == "selftest":
        return selftest()
    if len(argv) != 1:
        sys.stderr.write("usage: roster_check.py <council-skill-dir>|selftest\n")
        return 2
    try:
        violations, warnings = check_roster(argv[0])
    except RosterError as e:
        sys.stderr.write(f"roster-check: {e}\n")
        return 2
    for w in warnings:
        print(f"WARN: {w}")
    if violations:
        for v in violations:
            print(f"FAIL: {v}")
        return 1
    print(f"roster-check: OK ({len(warnings)} warning(s))")
    return 0


def selftest():
    import tempfile
    fails = []

    def expect(cond, msg):
        if not cond:
            fails.append(msg)

    def make_council(tmp, roster_text, handles):
        d = os.path.join(tmp, "council")
        os.makedirs(os.path.join(d, "references", "critics"), exist_ok=True)
        with open(os.path.join(d, "references", "roster.md"), "w", encoding="utf-8") as f:
            f.write(roster_text)
        for h in handles:
            open(os.path.join(d, "references", "critics", f"critic-{h}.md"), "w").write("# x\n")
        return d

    valid_roster = """\
| handle | sub-councils | role | status | seated | fixture |
|---|---|---|---|---|---|
| a-b | strategy | lead | active | 2026-08-01 | inline |
| c-d | strategy | member | active | 2026-08-01 | inline |
| e-f | design | member | active | 2026-08-01 | inline |

## Groups

- leads: strategy=a-b, design=VACANT
"""

    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d", "e-f"])
        violations, warnings = check_roster(d)
        expect(violations == [], f"valid roster wrongly flagged: {violations}")
        expect(len(warnings) == 1 and "VACANT" in warnings[0],
               f"expected exactly one VACANT warning, got {warnings}")
        rc = main([d])
        expect(rc == 0, f"main() should exit 0 on a valid roster with only a VACANT warning, got {rc}")

    # negative: orphan persona file (no roster row)
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d", "e-f", "g-h"])
        violations, _ = check_roster(d)
        expect(any("g-h" in v and "no roster.md row" in v for v in violations),
               f"orphan persona file not caught: {violations}")

    # negative: roster row with no matching file
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d"])  # missing e-f
        violations, _ = check_roster(d)
        expect(any("e-f" in v and "no matching critic" in v for v in violations),
               f"dangling roster row not caught: {violations}")

    # negative: empty sub-councils cell
    empty_subs = valid_roster.replace("| e-f | design | member", "| e-f |  | member")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, empty_subs, ["a-b", "c-d", "e-f"])
        violations, _ = check_roster(d)
        expect(any("empty sub-councils" in v for v in violations),
               f"empty sub-councils cell not caught: {violations}")

    # negative: 'full' used as a literal sub-council value
    full_literal = valid_roster.replace("| e-f | design |", "| e-f | full |")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, full_literal, ["a-b", "c-d", "e-f"])
        violations, _ = check_roster(d)
        expect(any("reserved name 'full'" in v for v in violations),
               f"literal 'full' sub-council value not caught: {violations}")

    # negative: dangling group handle
    dangling_group = valid_roster.replace("design=VACANT", "design=nobody")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, dangling_group, ["a-b", "c-d", "e-f"])
        violations, _ = check_roster(d)
        expect(any("nobody" in v for v in violations),
               f"dangling group handle not caught: {violations}")

    # negative: unknown role/status
    bad_role = valid_roster.replace("| c-d | strategy | member |", "| c-d | strategy | chair |")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, bad_role, ["a-b", "c-d", "e-f"])
        violations, _ = check_roster(d)
        expect(any("unknown role" in v for v in violations),
               f"unknown role value not caught: {violations}")

    # negative: two leads in the same sub-council
    two_leads = valid_roster.replace("| c-d | strategy | member |", "| c-d | strategy | lead |")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, two_leads, ["a-b", "c-d", "e-f"])
        violations, _ = check_roster(d)
        expect(any("more than one lead" in v for v in violations),
               f"double-lead sub-council not caught: {violations}")

    # usage-error path: missing roster.md / missing critics dir -> exit 2
    with tempfile.TemporaryDirectory() as tmp:
        empty_dir = os.path.join(tmp, "nope")
        os.makedirs(empty_dir)
        rc = main([empty_dir])
        expect(rc == 2, f"missing roster.md should exit 2 (usage error), got {rc}")

    # usage-error path: wrong arg count
    rc_argc = main([])
    expect(rc_argc == 2, f"no args should exit 2, got {rc_argc}")

    if fails:
        sys.stderr.write("roster_check selftest: FAIL\n")
        for m in fails:
            sys.stderr.write(f"  - {m}\n")
        return 1
    print("roster_check selftest: OK (bijection both directions, empty sub-councils, reserved "
          "'full', dangling group handle, unknown role/status, double-lead, VACANT-is-warning-"
          "not-failure, and both usage-error paths all correctly caught)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
