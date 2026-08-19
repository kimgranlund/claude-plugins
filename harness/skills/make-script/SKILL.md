---
name: make-script
description: >-
  AUTHOR a bundled scripts/taskname.py|mjs end to end, right now — qualify, plan, confirm, then
  BUILD it (selftest green, negative control bites, wired to its caller and the gate). An
  authoring-workflow ask, not a rules lookup. Use for "turn this checklist into a script",
  "mechanize this check", "build/add a selftest to this script", or "script this verification".
  NOT the standard itself, nor a bare "what should a selftest look like" / "is this mechanizable"
  rules question with nothing to build yet (script-writing-rules), event-fired enforcement
  (make-hook), a whole new skill (make-skill), or a one-off/throwaway script (session-local —
  write it inline, ship nothing).
disable-model-invocation: false
user-invocable: true
argument-hint: "[the check or procedure to mechanize, or a script path to retrofit]"
---

# make-script

make-script turns a hand-run check into a bundled script that proves itself — the deterministic
tier's maker, pairing with `script-writing-rules` the way make-hook pairs with its
standard. Invoke `script-writing-rules` now; the anatomy, placement, and selftest contracts
below are its, not restated here. Seed: `$ARGUMENTS`.

## Phase 1 — Qualify

Three signals admit a candidate; the standard's mechanization test then rules on it:

1. **An eyeballed gate** — a verification step performed by reading and judging when the pass/fail
   function is writable (counts, schema conformance, pointer integrity, threshold math).
2. **A prose checklist re-followed by hand** — the same steps executed manually a second or third
   time; the second occurrence is a signal to watch, the third is a candidate (the frequency bar
   save-lessons uses, applied to procedures).
3. **A retrofit ask** — an existing script missing its selftest, negative control, or exit-code
   contract; the plan then covers only the gap, not a rewrite.

**Escape hatches — name the one that fires and stop:** the property is judgment the checker can
never see (state the boundary in the owning skill's prose instead); a checker already owns it
(compose, don't twin — the standard's disqualifier); the procedure is ephemeral, one-shot, or
session-local (a scratchpad script, not a shipped one — write it there and skip this workflow).

## Phase 2 — Plan

Work out, concretely, before asking: **taskname** · **language** (the standard's default rules) ·
**home** (its placement split) · **selftest shape** (which fixtures, which negative control
bites, whether its tri-state skip applies) · **caller wiring** (which SKILL.md line invokes it,
by portable path — an orphan script is a non-goal by construction). The slot values come from
`script-writing-rules`, filled for this candidate — never re-derived.

## Phase 3 — Confirm

One AskUserQuestion carrying the plan — the recommended option IS the concrete plan (name, home,
language, selftest shape), never a bare "should I script this?"; always a "skip — keep it manual"
option. A decline ends the candidate: record nothing, do not re-propose this session. Exception:
the user's ask WAS the explicit instruction ("mechanize this as a script", "/make-script <x>") —
the ask is the confirmation; proceed, and say so.

## Phase 4 — Author

Write the script to the standard's anatomy — every contract it names (invocation, exit codes,
verdict line, dependency honesty), plus the `selftest` mode with its controls (shapes:
`script-writing-rules` references/selftest-patterns.md). Wire the caller in the same
change: the owning SKILL.md gains (or already has) the line that invokes it — and if the prose it
mechanizes was a checklist, that prose shrinks to the pointer, per the standard's failure
catalog.

## Phase 5 — Validate

In order: run `taskname selftest` — green, with the negative control demonstrably biting (run it
against the inversion fixture and show the catch, not just the PASS line). Run the script against
one real target. Then the gate: the owning plugin's `release_gate.py` run picks the script up in
G4 — confirm the swept count moved. A validation failure lands its fix in the failed phase; the
same failure three times stops and hands to the user.

Report: script path · selftest verdict line · the negative-control catch (quoted) · caller line
(`file:line`) · G4 swept count before → after.

## Failure branches

- Qualify finds judgment-in-costume → decline with the boundary stated; no script.
- An existing checker covers it → point at the owner; extending IT may be the real task.
- User declines at Phase 3 → nothing written, no re-ask this session.
- Selftest green but the negative control does not bite → the check is dead; fix the check, not
  the control.
- The script works but no caller names it → wire the caller or delete the script; both exits are
  legal, orphanhood is not.

Done when the script exists at its planned home, its selftest is green with a biting negative
control, a caller invokes it by portable path, the mechanized prose shrank to a pointer, and G4's
swept count includes it. NOT done if the selftest only proves the happy path, or if the script
shipped without the confirmation gate (or the explicit ask that stands in for it).
