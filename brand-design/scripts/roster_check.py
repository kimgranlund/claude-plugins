#!/usr/bin/env python3
"""roster-check — mechanical validator for a council's references/roster.md.

Proves the roster-file contract (council-rules' references/roster-file-contract.md):
handle<->persona-file bijection against the council's critics/ directory, every row's
sub-councils cell non-empty, `full` never used as a literal sub-council value, every
`## Groups` entry resolving to a seated active handle or the literal VACANT, role/status
values drawn from their fixed enums, the reserved `advisory` sub-council's exact pairing
with `role: advisor`, and the `## Role agents` mapping section (dangling agent handle,
a role with no mapped agent, a reserved-name key). A VACANT lead is a named WARNING,
never a failure; an ordinary sub-council with zero seated active critics (declared via
a `leads:` entry) is a named WARNING at the same severity; a zero-member `advisory`
sub-council is a named INFO line, narrower still — it is that reserved sub-council's
normal steady state until a user mints one via /make-critic.

Usage:
  roster_check.py <council-skill-dir>   # e.g. brand-design/skills/check-brand-council
  roster_check.py selftest

Exit codes: 0 = clean (warnings/infos allowed), 1 = a real violation found, 2 = usage
error (missing roster.md, missing critics/ dir, bad arguments). Stdlib only (Python 3.8+).
"""
import os
import re
import sys

ROLE_ENUM = {"lead", "member", "advisor"}
STATUS_ENUM = {"active", "retired"}
ADVISORY = "advisory"
CHAIR = "chair"


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
    """Return (groups, groups_kv). `groups`: {group_name: [tokens]} from the '## Groups'
    section's '- name: a=b, c=d' lines (values only, as before). `groups_kv`: {group_name:
    {key: value}} for entries actually written in 'key=value' shape — used to recover which
    ordinary sub-councils the 'leads' entry declares (its keys), since `groups` alone keeps
    only the values."""
    m = re.search(r"^##\s*Groups\s*$", text, re.M)
    if not m:
        return {}, {}
    body = text[m.end():]
    nxt = re.search(r"^##\s+", body, re.M)
    if nxt:
        body = body[:nxt.start()]
    groups = {}
    groups_kv = {}
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
        kv = {}
        for part in rest.split(","):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                if v:
                    tokens.append(v)
                    kv[k] = v
            elif part:
                tokens.append(part)
        groups[name] = tokens
        if kv:
            groups_kv[name] = kv
    return groups, groups_kv


def _parse_role_agents(text):
    """Return {role: agent_handle} from the '## Role agents' section's '- role: handle' lines,
    or None if the section is entirely absent (distinct from an empty section)."""
    m = re.search(r"^##\s*Role agents\s*$", text, re.M)
    if not m:
        return None
    body = text[m.end():]
    nxt = re.search(r"^##\s+", body, re.M)
    if nxt:
        body = body[:nxt.start()]
    mapping = {}
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue
        line = line.lstrip("-").strip()
        if ":" not in line:
            continue
        role, handle = line.split(":", 1)
        role, handle = role.strip(), handle.strip()
        if role and handle:
            mapping[role] = handle
    return mapping


def check_roster(roster_dir):
    """roster_dir: a council skill's directory (e.g. .../check-brand-council).
    Returns (violations, warnings, infos) — three lists of strings."""
    roster_path = os.path.join(roster_dir, "references", "roster.md")
    critics_dir = os.path.join(roster_dir, "references", "critics")
    if not os.path.isfile(roster_path):
        raise RosterError(f"no roster.md at {roster_path}")
    if not os.path.isdir(critics_dir):
        raise RosterError(f"no critics/ directory at {critics_dir}")

    text = open(roster_path, encoding="utf-8").read()
    rows = _parse_table(text)
    groups, groups_kv = _parse_groups(text)
    role_agents = _parse_role_agents(text)

    violations = []
    warnings = []
    infos = []

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
            violations.append(
                f"'{handle}' has unknown role '{role}' (expected lead|member|advisor)"
            )
        # advisory <-> advisor pairing is exact and bidirectional
        if ADVISORY in subs and role != "advisor":
            violations.append(
                f"'{handle}' lists '{ADVISORY}' in sub-councils but role is '{role}', "
                f"not 'advisor'"
            )
        if role == "advisor" and subs != [ADVISORY]:
            violations.append(
                f"'{handle}' has role 'advisor' but sub-councils is {subs!r}, "
                f"not exactly ['{ADVISORY}']"
            )
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

    # advisory: zero active advisors is legal-by-design (user-minted, never shipped seated) —
    # reported as a named INFO line, never a warning or failure
    advisor_count = sum(
        1 for r in rows
        if r.get("status") == "active" and ADVISORY in
        [s.strip() for s in r.get("sub-councils", "").split(",") if s.strip()]
    )
    if advisor_count == 0:
        infos.append(
            f"'{ADVISORY}' sub-council has no seated critics — expected until a user mints "
            f"one via /make-critic"
        )

    # ordinary sub-councils are enumerated from the required 'leads' group's own keys
    # (roster-file-contract.md: "one entry per sub-council, naming that sub-council's lead
    # handle, or VACANT") — 'full' (the computed union) and 'advisory' (no lead concept) are
    # never leads-group keys, so this list is exactly the ordinary sub-councils.
    ordinary_subcouncils = list(groups_kv.get("leads", {}).keys())
    for sub in ordinary_subcouncils:
        seated = sum(
            1 for r in rows
            if r.get("status") == "active"
            and sub in [s.strip() for s in r.get("sub-councils", "").split(",") if s.strip()]
        )
        if seated == 0:
            warnings.append(
                f"sub-council '{sub}' has no seated active critics — an ordinary sub-council "
                f"may legitimately start empty (e.g. newly declared), same severity as a "
                f"VACANT lead"
            )

    # '## Role agents' mapping: dangling handle -> FAIL, unmapped role -> WARNING, a key that
    # is neither 'chair' nor a declared ordinary sub-council (incl. the reserved 'advisory') ->
    # FAIL. Section entirely absent is treated as an empty mapping (every role unmapped).
    agents_dir = os.path.normpath(os.path.join(roster_dir, os.pardir, os.pardir, "agents"))
    known_roles = {CHAIR} | set(ordinary_subcouncils)
    mapping = role_agents or {}
    for role, handle in mapping.items():
        if role not in known_roles:
            reason = (
                f"'{role}' is the reserved 'advisory' sub-council, which has no role agent"
                if role == ADVISORY
                else f"'{role}' is neither 'chair' nor a 'leads:'-declared ordinary sub-council"
            )
            violations.append(f"'## Role agents' names '{role}' as a key, but {reason}")
            continue
        agent_path = os.path.join(agents_dir, f"{handle}.md")
        if not os.path.isfile(agent_path):
            violations.append(
                f"'## Role agents' entry '{role}' -> '{handle}' has no matching "
                f"agents/{handle}.md file"
            )
    for role in sorted(known_roles - set(mapping.keys())):
        warnings.append(
            f"role '{role}' has no '## Role agents' entry — an addressable seat not yet mapped"
        )

    return violations, warnings, infos


def main(argv):
    if argv and argv[0] == "selftest":
        return selftest()
    if len(argv) != 1:
        sys.stderr.write("usage: roster_check.py <council-skill-dir>|selftest\n")
        return 2
    try:
        violations, warnings, infos = check_roster(argv[0])
    except RosterError as e:
        sys.stderr.write(f"roster-check: {e}\n")
        return 2
    for i in infos:
        print(f"INFO: {i}")
    for w in warnings:
        print(f"WARN: {w}")
    if violations:
        for v in violations:
            print(f"FAIL: {v}")
        return 1
    print(f"roster-check: OK ({len(warnings)} warning(s), {len(infos)} info line(s))")
    return 0


def selftest():
    import tempfile
    fails = []

    def expect(cond, msg):
        if not cond:
            fails.append(msg)

    DEMO_AGENTS = ("demo-chair-agent", "demo-strategy-agent", "demo-design-agent")

    def make_council(tmp, roster_text, handles, agent_files=DEMO_AGENTS):
        # Mirrors the real layout: <plugin>/skills/<council>/... and <plugin>/agents/*.md,
        # siblings — roster_check.py's agents_dir resolves two levels up from the skill dir.
        plugin_dir = os.path.join(tmp, "plugin")
        d = os.path.join(plugin_dir, "skills", "council")
        os.makedirs(os.path.join(d, "references", "critics"), exist_ok=True)
        with open(os.path.join(d, "references", "roster.md"), "w", encoding="utf-8") as f:
            f.write(roster_text)
        for h in handles:
            open(os.path.join(d, "references", "critics", f"critic-{h}.md"), "w").write("# x\n")
        if agent_files:
            agents_dir = os.path.join(plugin_dir, "agents")
            os.makedirs(agents_dir, exist_ok=True)
            for name in agent_files:
                open(os.path.join(agents_dir, f"{name}.md"), "w").write("# agent\n")
        return d

    valid_roster = """\
| handle | sub-councils | role | status | seated | fixture |
|---|---|---|---|---|---|
| a-b | strategy | lead | active | 2026-08-01 | inline |
| c-d | strategy | member | active | 2026-08-01 | inline |
| e-f | design | member | active | 2026-08-01 | inline |

## Groups

- leads: strategy=a-b, design=VACANT

## Role agents

- chair: demo-chair-agent
- strategy: demo-strategy-agent
- design: demo-design-agent
"""

    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d", "e-f"])
        violations, warnings, infos = check_roster(d)
        expect(violations == [], f"valid roster wrongly flagged: {violations}")
        expect(len(warnings) == 1 and "VACANT" in warnings[0],
               f"expected exactly one VACANT warning (role-agent mapping is complete), got {warnings}")
        expect(len(infos) == 1 and ADVISORY in infos[0],
               f"expected exactly one advisory-empty INFO (no advisory rows in this fixture), "
               f"got {infos}")
        rc = main([d])
        expect(rc == 0, f"main() should exit 0 on a valid roster with only a VACANT warning, got {rc}")

    # negative: orphan persona file (no roster row)
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d", "e-f", "g-h"])
        violations, _, _ = check_roster(d)
        expect(any("g-h" in v and "no roster.md row" in v for v in violations),
               f"orphan persona file not caught: {violations}")

    # negative: roster row with no matching file
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d"])  # missing e-f
        violations, _, _ = check_roster(d)
        expect(any("e-f" in v and "no matching critic" in v for v in violations),
               f"dangling roster row not caught: {violations}")

    # negative: empty sub-councils cell
    empty_subs = valid_roster.replace("| e-f | design | member", "| e-f |  | member")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, empty_subs, ["a-b", "c-d", "e-f"])
        violations, _, _ = check_roster(d)
        expect(any("empty sub-councils" in v for v in violations),
               f"empty sub-councils cell not caught: {violations}")

    # negative: 'full' used as a literal sub-council value
    full_literal = valid_roster.replace("| e-f | design |", "| e-f | full |")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, full_literal, ["a-b", "c-d", "e-f"])
        violations, _, _ = check_roster(d)
        expect(any("reserved name 'full'" in v for v in violations),
               f"literal 'full' sub-council value not caught: {violations}")

    # negative: dangling group handle
    dangling_group = valid_roster.replace("design=VACANT", "design=nobody")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, dangling_group, ["a-b", "c-d", "e-f"])
        violations, _, _ = check_roster(d)
        expect(any("nobody" in v for v in violations),
               f"dangling group handle not caught: {violations}")

    # negative: unknown role/status
    bad_role = valid_roster.replace("| c-d | strategy | member |", "| c-d | strategy | chair |")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, bad_role, ["a-b", "c-d", "e-f"])
        violations, _, _ = check_roster(d)
        expect(any("unknown role" in v for v in violations),
               f"unknown role value not caught: {violations}")

    # negative: two leads in the same sub-council
    two_leads = valid_roster.replace("| c-d | strategy | member |", "| c-d | strategy | lead |")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, two_leads, ["a-b", "c-d", "e-f"])
        violations, _, _ = check_roster(d)
        expect(any("more than one lead" in v for v in violations),
               f"double-lead sub-council not caught: {violations}")

    # positive: a correctly-seated advisor row -> clean, and the empty-advisory INFO disappears
    with_advisor = valid_roster.replace(
        "|---|---|---|---|---|---|\n",
        "|---|---|---|---|---|---|\n"
        "| g-h | advisory | advisor | active | 2026-08-21 | unpromoted, inline |\n",
    )
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, with_advisor, ["a-b", "c-d", "e-f", "g-h"])
        violations, _, infos = check_roster(d)
        expect(violations == [], f"a correctly-seated advisor row was wrongly flagged: {violations}")
        expect(infos == [], f"a seated advisor should clear the empty-advisory INFO, got {infos}")

    # negative: 'advisory' in sub-councils but role isn't 'advisor'
    advisory_wrong_role = with_advisor.replace(
        "| g-h | advisory | advisor |", "| g-h | advisory | member |"
    )
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, advisory_wrong_role, ["a-b", "c-d", "e-f", "g-h"])
        violations, _, _ = check_roster(d)
        expect(any("g-h" in v and "not 'advisor'" in v for v in violations),
               f"advisory row with non-advisor role not caught: {violations}")

    # negative: role 'advisor' but sub-councils isn't exactly ['advisory']
    advisor_wrong_subs = with_advisor.replace(
        "| g-h | advisory | advisor |", "| g-h | strategy | advisor |"
    )
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, advisor_wrong_subs, ["a-b", "c-d", "e-f", "g-h"])
        violations, _, _ = check_roster(d)
        expect(any("g-h" in v and "not exactly" in v for v in violations),
               f"advisor role with wrong sub-councils not caught: {violations}")

    # negative: an ordinary sub-council declared (via 'leads') with zero seated active
    # critics -> a named WARNING, same severity as a VACANT lead, distinct from advisory's INFO
    empty_ordinary = valid_roster.replace(
        "- leads: strategy=a-b, design=VACANT",
        "- leads: strategy=a-b, design=VACANT, creative=VACANT",
    ).replace(
        "- design: demo-design-agent",
        "- design: demo-design-agent\n- creative: demo-creative-agent",
    )
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(
            tmp, empty_ordinary, ["a-b", "c-d", "e-f"],
            agent_files=DEMO_AGENTS + ("demo-creative-agent",),
        )
        violations, warnings, _ = check_roster(d)
        expect(violations == [], f"a newly-declared empty ordinary sub-council wrongly failed: {violations}")
        expect(any("creative" in w and "no seated active critics" in w for w in warnings),
               f"empty ordinary sub-council ('creative') not caught as a WARNING: {warnings}")

    # positive: role-agent mapping complete and every handle resolves -> no mapping violations
    # or warnings (already proven by the baseline valid_roster case above; restated here as its
    # own explicit case so a future edit to the baseline can't silently stop covering this)
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, valid_roster, ["a-b", "c-d", "e-f"])
        violations, warnings, _ = check_roster(d)
        expect(not any("Role agents" in v for v in violations),
               f"a complete, resolvable role-agent mapping was wrongly flagged: {violations}")
        expect(not any("Role agents" in w for w in warnings),
               f"a complete role-agent mapping wrongly warned about an unmapped role: {warnings}")

    # negative: dangling role-agent handle (mapped name has no agents/<handle>.md file) -> FAIL
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(
            tmp, valid_roster, ["a-b", "c-d", "e-f"],
            agent_files=("demo-chair-agent", "demo-design-agent"),  # demo-strategy-agent missing
        )
        violations, _, _ = check_roster(d)
        expect(any("demo-strategy-agent" in v and "no matching" in v for v in violations),
               f"dangling role-agent handle not caught: {violations}")

    # negative: a role with no '## Role agents' entry at all -> WARNING, never a FAIL
    missing_role_entry = valid_roster.replace("- design: demo-design-agent\n", "")
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, missing_role_entry, ["a-b", "c-d", "e-f"])
        violations, warnings, _ = check_roster(d)
        expect(not any("design" in v and "Role agents" in v for v in violations),
               f"an unmapped role was wrongly FAILed instead of warned: {violations}")
        expect(any("design" in w and "no '## Role agents' entry" in w for w in warnings),
               f"unmapped role 'design' not caught as a WARNING: {warnings}")

    # negative: '## Role agents' section entirely absent -> treated as every role unmapped
    # (warnings only, never a FAIL)
    no_role_agents_section = valid_roster.split("\n## Role agents")[0] + "\n"
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(tmp, no_role_agents_section, ["a-b", "c-d", "e-f"])
        violations, warnings, _ = check_roster(d)
        expect(not any("Role agents" in v for v in violations),
               f"an absent '## Role agents' section wrongly failed: {violations}")
        expect(sum(1 for w in warnings if "no '## Role agents' entry" in w) == 3,
               f"expected one unmapped-role warning each for 'chair', 'strategy', and 'design' "
               f"(chair + this fixture's two leads keys), got {warnings}")

    # negative: '## Role agents' names the reserved 'advisory' sub-council -> FAIL
    role_agents_advisory = valid_roster.replace(
        "- design: demo-design-agent",
        "- design: demo-design-agent\n- advisory: demo-advisory-agent",
    )
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(
            tmp, role_agents_advisory, ["a-b", "c-d", "e-f"],
            agent_files=DEMO_AGENTS + ("demo-advisory-agent",),
        )
        violations, _, _ = check_roster(d)
        expect(any("advisory" in v and "reserved" in v for v in violations),
               f"'## Role agents' naming the reserved 'advisory' sub-council not caught: {violations}")

    # negative: '## Role agents' names a key that is neither 'chair' nor a declared sub-council
    role_agents_unknown_key = valid_roster.replace(
        "- design: demo-design-agent",
        "- design: demo-design-agent\n- marketing: demo-marketing-agent",
    )
    with tempfile.TemporaryDirectory() as tmp:
        d = make_council(
            tmp, role_agents_unknown_key, ["a-b", "c-d", "e-f"],
            agent_files=DEMO_AGENTS + ("demo-marketing-agent",),
        )
        violations, _, _ = check_roster(d)
        expect(any("marketing" in v and "neither 'chair' nor" in v for v in violations),
               f"'## Role agents' naming an undeclared role not caught: {violations}")

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
          "not-failure, zero-advisor-is-info-not-failure, advisory<->advisor exact pairing both "
          "directions, empty-ordinary-sub-council-is-warning, '## Role agents' mapping "
          "(dangling handle FAIL, unmapped role WARNING incl. section-absent, reserved-name and "
          "undeclared-key FAIL), and both usage-error paths all correctly caught)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
