---
name: init-repo
description: >-
  Arms this session as a repo's working session, in one command: runs the built-in /init when
  no CLAUDE.md exists, makes this session adopt the team-lead contract, spawns the standing
  INTAKE sibling (docs' intake-lead), and wires per-ticket build capacity (build-lead
  dispatches) — then reports the armed arrangement. Per-session: spawned siblings die with the
  session; re-run each work session. Run /init-repo [optional repo root]. NOT the parts alone
  (/init, /lead-team, /lead-intake, /lead-build, /lead-review); NOT batch ticket mobilization
  (/mobilize-chores).
disable-model-invocation: true
user-invocable: true
argument-hint: "[optional target repo root — defaults to the current working directory]"
---

# init-repo — one command arms the work session

The /lead-* family's composer: everything it does is a shipped part reached by reference — the
name rides the built-in `/init` it wraps (term-of-art; the ruling is in this skill's
intent record). It arms ONE work session: Agent-tool siblings die with the session that spawned
them, so this is the sit-down command, not durable infrastructure — the same per-session
re-arm shape as the estate's session-scoped ops crons. Seed: `$ARGUMENTS` (a target repo root;
blank = the current working directory).

## The arming sequence

Each step's outcome is named in the closing report — run, skipped-present, failed-plainly, or
seat-absent-degraded. A failed step never silently vanishes, and a later step never pretends an
earlier one succeeded.

1. **Bind the repo.** Resolve the root (`$ARGUMENTS`, else cwd); state it back in one line.
2. **CLAUDE.md, conditionally.** The repo root already carries a CLAUDE.md → report
   skipped-present and move on, never re-run or rewrite it. Absent → invoke the built-in
   `init` skill (Skill tool — legal here: `init` is model-invocable, the reachable side of the
   #134 dichotomy step 3 states the blocked side of) and let it complete before arming
   continues — an armed session over an unmapped repo coordinates blind.
3. **Adopt team-lead — this session becomes the apex, no spawn.** `/lead-team` itself is
   `disable-model-invocation: true` and cannot be Skill-invoked from inside this command (the
   #134/#135 class), so this step carries the adoption directly, per that command's own
   Phase 2: read `${CLAUDE_PLUGIN_ROOT}/agents/team-lead.md` in full and adopt its priorities
   as this session's standing rules; invoke `team-or-solo-rules` and `loop-rules` (the same
   preloads the agent carries). ONE named deviation from /lead-team: the charter. /lead-team
   binds one bounded charter; here the charter IS the session — "this session's incoming work
   on <repo>" — closing at session end or an explicit stand-down. /lead-team's own host
   deltas (roll-up audience, review-seat degradation, the write-scoping discipline) apply as
   written. **Acknowledge the adoption in one standing block** — the contract file read, the
   charter deviation, the duration — before any spawn fires.
4. **Spawn the standing INTAKE sibling.** Dispatch `docs:intake-lead` (Agent tool, named
   `INTAKE`, background) with its canonical dispatch fields: Repo root: <the bound root> ·
   Markers: none · no Seed — and expect back, by design, its missing-seed branch's exact
   return ("0 records minted, 1 blocked · seed field absent") — that return IS the liveness
   ack: it proves the seat is alive with its contract intact, at zero contract-bending
   (empirically proven shape, its own A4 record). The seat then idles; every raw
   report/idea/chore arriving in THIS session relays to it via `SendMessage` (a send resumes
   a named teammate), seeds VERBATIM — the fork-blind rule applies: INTAKE sees no history,
   so a pointer like "the bug above" travels as the full report, never the pointer.
5. **Wire build capacity — per-ticket, not a standing spawn.** `build-lead`'s own contract is
   one confirmed ticket per dispatch, so there is no idle BUILD sibling to spawn — build
   capacity IS this session dispatching `Agent(teamwork:build-lead)` per confirmed ticket as
   work arrives, serially (mobilize-chores' mutating-dispatches rule), each relayed
   verdict-first with its Findings evidence. The asymmetry is the seats' own contracts, not
   an omission.
6. **The armed report.** One closing block: each step's outcome; how to feed each seat (raw
   intake → relayed to INTAKE; a confirmed ticket → a build-lead dispatch; a review target →
   its owning checker, or `/lead-review` in a dedicated session); the per-session lifetime
   line. From here the session runs under the adopted team-lead contract until it ends.

## Failure branches

- **The `init` invocation fails** (step 2) → report it plainly and STOP the arming — every
  later step coordinates against the repo map; arming blind compounds the failure.
- **The INTAKE spawn fails (tool error, docs installed)** → seat-absent-degraded: the arming
  continues, intake asks route to the file-* commands by name (`/file-bug`, `/file-feature`,
  `/file-task` — present, since docs is), and the failure is in the armed report — never a
  fabricated "INTAKE ready".
- **docs not installed at all** → a different degradation, named as such: the file-* commands
  are docs' own and absent with it, so no intake procedure exists here — raw seeds get a plain
  host-recorded work item (the backend the repo actually has: a `gh issue`, or a dated note in
  the repo's own convention), each with the gap named, and the armed report says intake runs
  degraded until docs is installed.
- **A CLAUDE.md exists but is plainly stale or empty** → not this command's repair: report the
  observation in the armed report and continue; `/check-entry-file` (harness) owns that fix.
- **`/init-repo` invoked again while the session is already armed** → rebind the root,
  re-verify the INTAKE sibling still lives (a dead one is re-spawned, reported), re-acknowledge
  in one line — never stack a second adoption or a duplicate INTAKE.

## When this ends

The armed state holds until the session ends or the human stands it down ("stand down" /
"back to normal work") — acknowledged in one line; the INTAKE sibling is told to stand down
too (SendMessage), not abandoned. A new session re-runs `/init-repo`.

Done when the armed report was delivered with every step's outcome named, the adoption
acknowledged before any spawn, INTAKE live (or its degradation named), and build capacity
wired per-ticket. NOT done while a step's failure is silent, a second adoption stacked, an
idle build seat sits spawned against its own contract, or the session coordinates a repo it
never mapped.
