# Progress-comment contract (gh#994)

**F6 split** of dispatch-ticket's Phase 4/5 boundary bullet — the parent file's own line-cap left
no room to inline this detail; read it before this procedure's first live firing.

## The incident

Overdue build handbacks are undetectable from the record unless the record itself carries the
evidence. On 2026-08-29 in agent-ui, two `build-leader` dispatches (90- and 60-minute budgets) ran
5-6 hours with no chase — both were alive, blocked on long vitest runs, and emitted only
content-free idle notifications. The ticket showed nothing, and the marshal had no timer to
notice.

## The rule

Whatever wall-clock budget a dispatch carries, post one dated progress comment at budget/2, and
again before any single wait longer than 5 minutes — a long test run, a held gate, a wait on a
peer — each comment naming what it is waiting on, never a content-free ping. The 5-minute wait
threshold and the budget/2 checkpoint are the ticket's own seed numbers; tune only against
evidence from a second incident, never on a hunch.

**Applies at every kind branch that reaches a live dispatch** — Phase 2's task branch (an
`Agent`-tool dispatch straight out of Phase 3, which never walks through Phase 4's sizing at all)
owes the same comment discipline as Phase 4's feature/big path, even though its own procedural
walk skips Phase 4 entirely.

**Write-back verb follows the resolved backend**, the same split as every other write-back act in
this file (the claim comment, the release comment, the Findings entry): git-native — `gh issue
comment`; file backend — an interim note appended under the TICKET file's `## Findings` section;
an external adapter — its own `update` operation.

**Distinct from the Findings write-back.** This is a time-triggered progress ping, not the
result-triggered `## Findings` entry Phase 5 stage 4 already mandates (slice built, gate green, PR
opened) — the two triggers are independent and neither substitutes for the other.

## Where the rest of the contract lives

`agents/build-leader.md` carries a one-line citation back to this file rather than restating the
mechanics — a dispatched seat reads its own agent file for comms discipline, not this skill's
body, so the pointer has to exist there too. `agents/fleet-marshal.md` Priority 5's dispatch-time
budget timer (armed via `CronCreate` or a `Monitor` until-loop — the implementer's call) is what
turns a missed comment into a chase, then a re-dispatch on a second silence; `bind-team`'s
host-adopted mirror of Priority 5 carries the identical sequence for a `/bind-team` host session.
