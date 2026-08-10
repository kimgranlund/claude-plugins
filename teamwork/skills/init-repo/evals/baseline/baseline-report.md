# Baseline: ad hoc session-arming ask (no skill), 2026-08-10

Fresh-context dry-run. Ask: Kim's sit-down habit verbatim — "Set this session up as my main
working session for this repo — make sure the repo has its CLAUDE.md, and I want an intake
helper for filing bugs/ideas and build support for driving tickets. Coordinate everything
through here." Read-only grounding real (git status, CLAUDE.md present, enabledPlugins).

## What the ad hoc session did — the strongest baseline of the family

Credit where due, disclosed honestly: it checked CLAUDE.md before touching anything, refused
to scaffold duplicate tooling (citing this workspace's own anti-duplication norm), refused to
spawn subagents (citing solo-first), routed the ask onto the existing routing table, and
offered — rather than fired — a check-state snapshot. Nothing it did was wrong.

## What it did NOT produce — the arrangement

1. **No standing INTAKE seat.** "I want an intake helper" collapsed into "type /file-bug in
   this session yourself" — the main session does everything inline. Kim's pattern wants the
   seat: a standing sibling holding the intake procedures, receiving relayed seeds, keeping
   the main session's context clean. The baseline reasoned its way to solo-first correctly IN
   GENERAL and thereby declined the exact arrangement the user was describing.
2. **No adopted contract.** The session self-described as "I'll route through the table" —
   nothing binds it; no team-lead adoption, no write-scoping discipline, no roll-up shape.
   Three turns later that self-description is prose in the scrollback.
3. **No armed report, no lifecycle.** No statement of what stands, how to feed it, or that
   any of it dies with the session.

## Probe limitation, disclosed

This repo carries a rich CLAUDE.md whose routing table answers the ask — the strongest
possible "do nothing" case, and the /init leg's only reachable outcome here is
skipped-present. A fresh repo (no CLAUDE.md, no table — the command's other home turf) would
have stripped the baseline of every crutch it leaned on; that leg is exercised in the
with-skill check by simulation instead.

## The deltas the skill must produce (checked in Phase 5)

1. Conditional /init with the outcome NAMED either way (assertion 1).
2. Team-lead adoption acknowledged with the session-charter deviation — a binding contract,
   not a self-description (assertion 2).
3. The asymmetric seats actually wired: INTAKE spawned standing per its own contract; build
   per-ticket (assertion 3).
4. The armed report with every outcome and the per-session lifetime (assertion 4).
