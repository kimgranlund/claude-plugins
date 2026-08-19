# Write-gate dry-run fixture — payload-layer proof for Phase 5 stage 2a (gh#686, ADR-0023 (c))

**What this proves.** Two worked, fully-fictional dry-run traces against a fixture ticket
(`TKT-FIXTURE-001`), each a literal, greppable log of Phase 5 stage 2's own sequence — the
plan-approval write-gate's hold, its accept marker, the PR-open act it authorizes, and (Trace 2
only) how stage 2b's ADR-0012 predicate composes strictly on top without ever preceding the
accept. This is the payload-layer check gh#686's own Acceptance section asks for ("a dry-run of
`dispatch-ticket` Phase 5 against a fixture ticket shows the hold point, the accepting seat, and
the composition with checker/QB5 — checkable from the SKILL.md text and any bundled fixture, no
browser/human layer required") — every line below is a literal marker, machine-greppable, never a
narrative a reader has to interpret.

**What this is NOT.** Not a runnable script — `dispatch-ticket` has no bundled `scripts/`
directory today, and this fixture is checkable end to end by plain `grep` (below); inventing an
executable harness solely to run what a grep already proves would fail `script-writing-rules`'
own "is this mechanizable, and does mechanizing it buy anything a plain read-and-grep doesn't"
test. Not a substitute for the SKILL.md text itself — Phase 5 stage 2/2a/2b are the actual
contract; this fixture illustrates it, one-way (`lld-0022-fleet-native-write-gate.md`'s
Interfaces section).

**How to check it.** `grep -E '^(HOLD|ACCEPT-MARKER|PR-OPEN|QB5|2B-EVAL-ORDER):' <this file> |
wc -l` returns `8` (Trace 1's 3 + Trace 2's 5). A per-trace check (bounded by each `## Trace N`
heading) returns exactly 3 markers for Trace 1, in order (`HOLD`, `ACCEPT-MARKER`, `PR-OPEN`, no
`QB5`/`2B-EVAL-ORDER`), and exactly 5 for Trace 2, in order (the same three, then `QB5`, then
`2B-EVAL-ORDER`).

## Trace 1 — unconditional path, no ADR-0012 grant (3 markers)

The common case: no `auto-merge: authorized` line was in the sealed dispatch prompt, so stage 2b
never evaluates (Phase 5's own "absent → this stage does not exist" rule) — the write-gate still
fires, unconditionally, exactly as Resolution 3 rules.

```
HOLD: branch `tkt-fixture-001-demo-slice` pushed to origin, no PR open — 2a hold in effect
ACCEPT-MARKER: gh issue comment on TKT-FIXTURE-001, marshal @fixture-marshal, 2026-08-18T00:00:00Z,
  branch `tkt-fixture-001-demo-slice` @ a1b2c3d4 — accepted, PR-open may proceed
PR-OPEN: PR opens against main, body cites the accept-marker comment URL; in-flight label removed
```

## Trace 2 — ADR-0012-granted path, QB5 already green (5 markers)

The quick-build case: the sealed dispatch prompt carried the literal `auto-merge: authorized`
line, so once the PR opens, stage 2b's eight-conjunct evaluation runs. This trace demonstrates the
strict ordering Resolution 3 states: `QB5` (the fresh-context checker's own verdict, a DISTINCT
record from the accept marker) and `2B-EVAL-ORDER` (an explicit statement of when 2b's evaluation
began) both appear only AFTER `PR-OPEN`, which itself only appears after `ACCEPT-MARKER`.

```
HOLD: branch `tkt-fixture-001-demo-slice-b` pushed to origin, no PR open — 2a hold in effect
ACCEPT-MARKER: gh issue comment on TKT-FIXTURE-001, marshal @fixture-marshal, 2026-08-18T00:05:00Z,
  branch `tkt-fixture-001-demo-slice-b` @ b2c3d4e5 — accepted, PR-open may proceed
PR-OPEN: PR opens against main, body cites the accept-marker comment URL; in-flight label removed
QB5: fresh-context checker verdict recorded, zero blocker/major findings
2B-EVAL-ORDER: 2b's eight-conjunct evaluation begins AFTER PR-OPEN, never before ACCEPT-MARKER
```

## The negative case, stated (not traced — no PR/branch state to log)

A third scenario intentionally has no trace here, since nothing past the hold ever happens: no
live marshal entry in `fleet.json`'s `live_state.joined` at the moment the branch is pushed. The
dispatch reports `write-gate-blocked` (Phase 5's Failure branches) and stops — no `PR-OPEN` line
is ever written, because none is ever opened. A trace with only a `HOLD:` line and nothing after
it would be indistinguishable from "still running normally, not yet accepted"; the actual
distinguishing fact (no marshal was reachable) lives in the reported blocker text, not in a marker
this file could log without inventing a fourth, unneeded marker for a state that produces no
durable write of its own.
