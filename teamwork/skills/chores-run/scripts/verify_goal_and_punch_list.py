#!/usr/bin/env python3
"""verify_goal_and_punch_list — agent-verifiability proof for chores-run (issue #637).

Two independent, mechanical checks, run without a live multi-turn `/goal` session:

  1. `check_goal_shape(text)` — the exact two dimensions `teamwork:loop-rules`' own
     `harness_checks.py goal` checks (C1 measurable end-state, C3 bounded cap; the third
     dimension it scores, "no vague success terms", is folded into C1 here). Replicated locally
     rather than imported: a skill's own `scripts/` is never referenced from OUTSIDE that skill
     (spec-naming-convention.md REQ-005 §6.1 point 3 — the skill-folder encapsulation invariant),
     so this file cannot shell out to loop-rules/scripts/harness_checks.py even though both live
     in the teamwork plugin. Small, deliberate duplication of ~10 lines of regex, not a shared
     library extraction — one consumer each, per doc-writing-rules' own extraction rule.
  2. `check_punch_list_columns(header_row)` — a punch-list header row carries exactly the five
     columns the ticket's own acceptance criterion names: id, seat, worktree/branch, PR, state.

`extract_goal_block`/`extract_punch_list_header` pull the LIVE text straight out of this skill's
own SKILL.md rather than a hand-duplicated copy — `selftest` proves the two checks above against
whatever SKILL.md actually ships, so this proof cannot silently drift from the shipped text (the
#619-class "narrated but not proven" failure this workspace has hit before).

Usage:
  verify_goal_and_punch_list.py goal <path-or-literal-text>
  verify_goal_and_punch_list.py punch-list <path-or-literal-text>
  verify_goal_and_punch_list.py selftest

Exit 0 clean, 1 on a finding, 2 on a usage error. Network: none — pure text checks only.
"""
import re
import sys
from pathlib import Path

VAGUE = ("clean", "elegant", "good", "nice", "properly", "robust", "well")

REQUIRED_PUNCH_LIST_COLUMNS = ("id", "seat", "worktree/branch", "pr", "state")

SKILL_MD_PATH = Path(__file__).resolve().parent.parent / "SKILL.md"


def _read(arg: str) -> str:
    """A CLI arg that names an existing file reads its contents; otherwise the arg IS the text
    (mirrors harness_checks.py's own `read()` convention in this same plugin's loop-rules)."""
    p = Path(arg)
    return p.read_text(encoding="utf-8") if p.exists() else arg


def extract_goal_block(skill_md_text: str):
    """Pure. Returns the content of the first fenced code block whose first non-blank line
    starts with '/goal:' — None if no such block exists. Language-tag-agnostic (plain ``` or
    ```text etc.)."""
    for m in re.finditer(r"```[a-zA-Z]*\n(.*?)```", skill_md_text, re.DOTALL):
        block = m.group(1)
        if block.lstrip().startswith("/goal:"):
            return block
    return None


def extract_punch_list_header(skill_md_text: str):
    """Pure. Returns the markdown table header row (a line starting with '| id |', case-
    insensitive) found anywhere in the text — None if absent."""
    for line in skill_md_text.splitlines():
        stripped = line.strip()
        if re.match(r"^\|\s*id\s*\|", stripped, re.I):
            return stripped
    return None


def check_goal_shape(text: str):
    """Pure. Returns (ok, findings) — findings is [(code, ok, msg), ...], mirroring the house
    _report shape other bundled scripts in this workspace use (e.g. version_claim_check.py)."""
    findings = []
    ok_all = True

    bounded = bool(re.search(r"stop after|\b\d+\s*(turn|minute|hour|wave)", text, re.I))
    findings.append(("C3", bounded, "bounded (a 'stop after' or a numeric turn/wave cap)"))
    ok_all = ok_all and bounded

    measurable = bool(
        re.search(r"exits?\s*0|passes|== |\bzero\b|\btest", text, re.I) or re.search(r"\d", text)
    )
    findings.append(("C1", measurable, "measurable end-state token present"))
    ok_all = ok_all and measurable

    vague_hits = [w for w in VAGUE if re.search(rf"\b{w}\b", text, re.I)]
    findings.append(("C1", not vague_hits, f"no vague success terms (hit: {', '.join(vague_hits)})"
                      if vague_hits else "no vague success terms"))
    ok_all = ok_all and not vague_hits

    return ok_all, findings


def check_punch_list_columns(header_row: str):
    """Pure. The header row (a markdown table header line, e.g.
    '| id | seat | worktree/branch | PR | state |') must carry every required column, in any
    case, order-insensitive (the ticket names the five columns, not a fixed left-to-right order)."""
    cells = [c.strip().lower() for c in header_row.strip().strip("|").split("|")]
    missing = [col for col in REQUIRED_PUNCH_LIST_COLUMNS if col not in cells]
    ok = not missing
    findings = [("PL1", ok, "all 5 required columns present"
                 if ok else f"missing columns: {', '.join(missing)}")]
    return ok, findings


def _report(ok, findings):
    print(f"verify_goal_and_punch_list · {'clean' if ok else 'FAIL'}")
    for code, item_ok, msg in findings:
        print(f"  {'ok  ' if item_ok else 'FAIL'} {code}  {msg}")


def selftest():
    skill_md = SKILL_MD_PATH.read_text(encoding="utf-8")

    # extract_goal_block / extract_punch_list_header — must actually find the shipped fixtures.
    goal_text = extract_goal_block(skill_md)
    assert goal_text, "SKILL.md must carry a fenced block starting with '/goal:'"
    header = extract_punch_list_header(skill_md)
    assert header, "SKILL.md must carry a punch-list table header row starting with '| id |'"

    # check_goal_shape — the LIVE, shipped goal text (extracted, never a hand copy) must pass.
    ok, findings = check_goal_shape(goal_text)
    assert ok, f"the skill's own shipped /goal text must pass C1+C3 clean: {findings}"

    # check_goal_shape — negative control: no cap at all must fail C3.
    ok, findings = check_goal_shape("/goal: no unclaimed ticket remains open.")
    assert not ok, "a goal with no cap and no digit must fail (C3 uncapped, C1 unmeasurable)"
    assert any(code == "C3" and not f_ok for code, f_ok, _ in findings)

    # check_goal_shape — negative control: a vague success term must fail C1 even with a cap.
    vague_goal = "/goal: the queue is clean and robust. Stop after 5 turns."
    ok, findings = check_goal_shape(vague_goal)
    assert not ok, "a vague success term ('clean', 'robust') must fail C1 even with a real cap"
    assert any(code == "C1" and not f_ok and "vague" in msg for code, f_ok, msg in findings)

    # check_goal_shape — reverse control: a capped, measurable, non-vague goal passes.
    ok, findings = check_goal_shape("/goal: 0 open tickets remain. Stop after 3 tries.")
    assert ok, "a capped, digit-bearing, non-vague goal must pass clean"

    # check_punch_list_columns — the LIVE, shipped header (extracted) must carry all 5 columns.
    ok, findings = check_punch_list_columns(header)
    assert ok, f"the skill's own shipped punch-list header must carry all 5 columns: {findings}"

    # check_punch_list_columns — negative control: a header missing a column must FAIL, never be
    # silently accepted (the #619-class "narrated but not actually proven" failure mode).
    ok, findings = check_punch_list_columns("| id | seat | PR | state |")
    assert not ok, "a header missing 'worktree/branch' must fail, not pass"
    assert any(code == "PL1" and not f_ok and "worktree/branch" in msg for code, f_ok, msg in findings)

    # check_punch_list_columns — order-insensitive reverse control.
    ok, findings = check_punch_list_columns("| state | PR | id | worktree/branch | seat |")
    assert ok, "column order must not matter, only presence"

    # extract_goal_block — negative control: text with no '/goal:' fence returns None.
    assert extract_goal_block("no fenced block here at all") is None
    assert extract_goal_block("```\nplain code, no goal marker\n```") is None

    print("verify_goal_and_punch_list selftest · PASS · the LIVE goal text and punch-list header "
          "extracted straight from SKILL.md both pass their own gates; uncapped, vague, missing-"
          "column, and no-fence negative controls all correctly FAIL")
    return 0


def main():
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "selftest":
        return selftest()
    if argv[0] not in ("goal", "punch-list") or len(argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    text = _read(argv[1])
    if argv[0] == "goal":
        ok, findings = check_goal_shape(text)
    else:
        ok, findings = check_punch_list_columns(text)
    _report(ok, findings)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
