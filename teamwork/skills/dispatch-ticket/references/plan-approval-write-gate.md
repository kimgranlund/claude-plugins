# Plan-approval write-gate — Phase 5 stage 2a's full mechanics (ADR-0023 decision (c), gh#686)

Cited from `SKILL.md`'s Phase 5 stage 2a rather than restated inline (the same F6 split-to-
references pattern as `isolation-ladder.md`, `spec-lock-gate.md`, and this skill's other
reference files). Design record and the four resolved forks: `.claude/docs/lld/
lld-0022-fleet-native-write-gate.md`. Worked, greppable dry-run traces: `references/
write-gate-dry-run.md`.

## Why this stage exists

ADR-0023 (accepted) rules the fleet stays canon over native `agent-teams` (decision (a)), but
names one concept `agent-teams` gets right that the fleet's own pre-merge posture didn't have an
equivalent for: a **plan-approval write-gate** — holding a dispatched worker's writes un-landed
until an explicit acceptance step, before they can affect anything outside the worker's own
isolation. Decision (c) rules pursuing a fleet-native equivalent, expressed natively in
`dispatch-ticket`'s own Phase 5 lifecycle rather than depending on `agent-teams` or its
experimental flag. This stage is that equivalent.

## The hold point (LLD Resolution 1)

The hold is exactly the gap between "branch pushed" and "PR opened" (draft or ready) — nothing
before it (gating inside the worker's own isolated worktree would block the fleet's own
push-then-inventory resilience model, `fleet-rules` §5) and nothing after it (a draft PR is
already "visible/mergeable outside" in ADR-0023's own sense — GitHub surfaces it in every list
view, a reviewer can already comment on it). **PR-open, draft or ready, IS the accept act** — the
gate has nothing left to hold once either exists.

## Accepting seat and accept-marker shape (LLD Resolution 2)

**Accepting seat:** the marshal (`fleet-rules` §7's route-anything-incoming seat) — never
inferred to be the live human by default, and never the dispatching worker itself (that would be
the worker grading its own plan to land, the same generator≠critic gap the fresh-context checker
pass already exists to close one layer up).

**Accept marker, the durable record:** a comment posted by the accepting seat on the ticket's own
record —

```
Accept: <marshal-seat-identity>, <UTC timestamp>, branch `<decided-branch-name>` @ <head-sha> —
plan-approval write-gate accepted (ADR-0023 (c)); PR-open may proceed.
```

git-native: `gh issue comment` on the closing issue; file backend: the TICKET file's own
`## Findings`; an adapter: its `update` operation. This mirrors ADR-0005's own claim-comment
convention exactly (identity + a durable, timestamped, re-readable write beats an ephemeral
nudge, `fleet-rules` §3's "durable records carry truth" default) — reusing an already-ratified
pattern rather than minting a second one.

**Naming the SHA is load-bearing, not decorative.** A comment that doesn't name the pushed
branch's HEAD SHA isn't an accept marker. A branch amended or force-pushed to a different SHA
after a marker lands needs a FRESH marker naming the new SHA — the old marker never authorizes an
unnamed later SHA. At PR-open time, the accept marker's cited SHA is checked against the branch's
actual current HEAD; a mismatch is this stage's own precondition failing, reported as
`write-gate-blocked` again rather than opened anyway (LLD Risk R-1).

## Marshal-side response procedure (live-observed, 2026-08-21)

The sections above specify the gate; this specifies what the accepting marshal actually DOES on
receiving a `write-gate-blocked` report, end to end — a gap the LLD's own Resolutions leave
implicit. Observed across 11 real dispatches in one session (`gh#824`–`gh#829`, `gh#842`,
`gh#852`, `gh#853`, `gh#855`, `gh#856`; every one lacked a `size:small` label, so the AG1–AG4
pre-accept grant never fired and the full round below ran every time), under a live human's
standing session-scoped merge authorization (a "proceed"/"merge on green" instruction covering
the whole run) — this procedure assumes that authorization exists; a marshal with none stops at
PR-open (step 3) and hands off, same as an ungranted stage-2b dispatch.

1. **Extract the seat's own proposed PR body**, already posted as its final Findings comment —
   the seat states it in a fenced ` ```markdown ` block starting with `Closes #<id>` (this
   convention is the seat's own contract; a caller dispatching a build should seal that
   requirement into the prompt, since a free-form Findings comment makes step 3 below brittle to
   parse). Multiple Findings comments may exist on one ticket — the fenced block is not always
   the LAST comment (an earlier progress comment can post first); search all comments for the
   fence, not just the newest.
2. **Post the accept marker** per the format above. Re-read the branch's actual current HEAD
   first — that reading, not the seat's own report, is the load-bearing referent (Resolution 2);
   name THAT SHA in the marker. A mismatch between the two is this stage's own precondition
   failing, reported `write-gate-blocked` again, never papered over with the seat's stale value.
3. **Open the PR** from the pushed branch using the extracted body verbatim (title from the
   seat's proposal, or a short one the marshal composes if the seat didn't propose one). **A
   marshal with no live human's standing merge authorization for this run stops here** and hands
   the opened PR to a human — steps 4–5 below require that authorization exactly as stage 2b
   requires its own `auto-merge: authorized` grant; PR-open is never itself the authorization.
4. **Watch CI to green**, then merge — `gh pr checks --watch --fail-fast && gh pr merge --squash
   --delete-branch`, backgroundable so the marshal isn't blocked mid-turn on a slow suite.
5. **Verify the merge landed clean**: the host repo's own `campaign_close.py <pr-number> --repo
   <owner/repo> --gate <plugin-root>` (or equivalent) — never trust the merge command's own exit
   code alone; re-verify MERGED state, branch deletion, and the touched plugin's gate.
6. **Pull the primary checkout forward** before dispatching the next ticket sharing a version
   slot — a stale local `main` produces a wrong `dispatch_envelope.py` read (a plugin version one
   behind, or a stray branch checkout from an earlier step never returned to `main`) for the very
   next dispatch. Run `sync_main.py` (or a plain `git checkout main && git pull --ff-only`)
   unconditionally before that next same-slot dispatch, regardless of what state the marshal
   believes the checkout is already in.

Two dispatches sharing one plugin's version slot run this whole loop SERIALLY — a second dispatch
minted before the first's version bump lands collides at `version_claim_check.py`. Two dispatches
on disjoint plugins may run steps 1–5 concurrently.

## No-marshal fallback: FAIL-CLOSED (LLD Resolution 2)

No live marshal entry (`fleet.json`'s `live_state.joined` carries no orchestrator role, or the
seat is unreachable) → the hold STANDS. Never auto-accept, never infer acceptance from silence,
never fall through to PR-open on a timeout — an auto-accept timeout was considered and rejected
(the LLD's own Resolution 2 rejected-alternatives: a timeout duration has no evidence backing it,
and ADR-0023's whole rationale for pursuing (c) is structural strength, "stronger than the deny-
hook reviewer wall," gh#686's own grounding — a gate that silently no-ops under exactly the
condition, no reviewer present, it exists to cover was never the standard being matched). Report
`write-gate-blocked` (`SKILL.md`'s Failure branches) and stop: the pushed branch stays exactly as
pushed, the Phase 3 claim stays held (an ordinary in-progress build's claim stays held through a
routine wait; a wait for acceptance is not different in kind), and a later run — the marshal
coming back live, or a human posting the accept marker directly — resumes from the same pushed
branch rather than restarting.

## Unconditional scope, and composition with ADR-0012 (LLD Resolution 3)

This stage fires on EVERY build dispatch reaching Phase 5 stage 2 — feature or task, small or
big — unconditionally, regardless of whether ADR-0012's quick-build `auto-merge: authorized`
grant is present. Making it unconditional (rather than gated on `size:small` or the grant itself)
keeps exactly one size-aware predicate in the file (QB1, inside stage 2b) rather than duplicating
a second one, and avoids leaving the overwhelming majority of dispatches (any `size:big` build,
any ungranted `size:small` build) with no in-loop write-hold at all — exactly the gap ADR-0023's
Context names as unclosed today.

**Composition, stated precisely:** 2a's accept marker and stage 2b's QB5 critic-green conjunct
answer two different questions. QB5 asks "is this change GOOD" (a fresh-context checker graded
it). 2a asks "is this change ACCEPTED to land" (the marshal signed off). Neither substitutes for
the other, and both are required on any dispatch that reaches 2b eligible. Ordering is strict and
one-way: **2a's accept → PR-open → 2b's eight-conjunct evaluation** — 2b's own QB2/QB3
diff-inspection conjuncts already assume an open PR to diff against `origin/main...HEAD`, so this
ordering is not a new constraint on 2b, only a stated one.

## `in-flight` label: same removal point, later in time (LLD Resolution 4)

The label stays ON through the hold and drops at the accept-triggered PR-open — the SAME removal
point the pre-gate contract already used ("the moment the PR opens"), now gated by one more
precondition, not a new label state. A distinct `awaiting-accept` label was considered and
rejected: real cost (a new label, a new removal rule, a new cross-reference for
`in-flight-label-semantics.md` and `mobilize-chores`' pre-filter), no behavioral payoff (an
`in-flight` ticket held-for-accept is exactly as "someone is actively working this, don't
double-dispatch" as one mid-build with no PR yet — the guard's own semantics don't change).

## Failure outcome: `write-gate-blocked`

Reported, terminal-for-this-turn, never a build failure — the same register as `stale-premise`
and the SKIPPED task branch. No PR URL and no accept-marker URL ride in the handoff when this
fires (`SKILL.md` stage 4); name the missing accepting seat and the branch/SHA awaiting
acceptance instead. See `SKILL.md`'s Failure branches for the canonical statement.

## Pre-accept grant — a narrow skip of the hold alone (gh#713, lld-0022 Resolution 5)

A literal grant line, `accept-grant: authorized`, placed in the sealed dispatch prompt by the
dispatching coordinator/seat AT DISPATCH TIME — same explicit-never-inferred mechanics as
ADR-0012's own `auto-merge: authorized` line, deliberately a DIFFERENT token so the two grants
are never conflated in a transcript or a grep. The two authorize different acts on different
clocks (one skips a HOLD before PR-open; the other skips a MERGE after PR-open), so a dispatch
may legally carry one, both, or neither.

**The four conjuncts, evaluated by the dispatched seat, never the placer** (mirrors ADR-0012's
own placer-vs-evaluator split):

- **AG1 — `size:small`.** The same size read stage 2b's own QB1 already makes off the ticket's
  own label — not a second detector.
- **AG2 — single-plugin.** QB2's own read.
- **AG3 — checker-green.** Phase 4's own fresh-context checker verdict, when Phase 4's
  semantic-edit trigger applied — or Phase 4's own "pure code/config, no checker owed"
  determination, when it didn't. Never a second checker pass invented for this gate.
- **AG4 — gate-green.** The SAME local aggregate gate run (`gate-run-time-budget.md`'s
  single-run-never-ground rule) stage 2 already performs before PR-open — pulled earlier in wall
  clock for a granted dispatch only; nothing runs twice.

All four green → skip 2a's hold alone: no accept marker is required or produced, and the
dispatch proceeds directly to the version-collision re-checks and PR-open. Any conjunct absent,
failing, or indeterminate → the hold stands exactly as the Acceptance protocol above specifies,
full accept round owed — the grant is not a retry lever and is never re-evaluated into
eligibility on a later pass.

**Scope — this skips ONLY stage 2a's hold.** Stage 2b's own ADR-0012 predicate (QB0–QB7), the
fresh-context checker pass, and the local+CI gate run are UNCHANGED and still mandatory on every
path, granted or not — a build that clears AG1–AG4 and skips the accept round still needs its
own separate `auto-merge: authorized` grant and all-green QB0–QB7 to also skip the human merge.
The two grants compose independently; neither implies the other.

**Rejected: reusing `auto-merge: authorized` for both skips.** One token authorizing two
independently-revocable acts on two different clocks would make revoking one silently revoke the
other — the same "explicit, revocable" property ADR-0012 names as load-bearing breaks under
overload. Two literal, greppable tokens cost one more line and buy independent revocation.

Full resolution + rejected-alternatives text: `.claude/docs/lld/lld-0022-fleet-native-write-gate.md`
Resolution 5 (version 0.2.0).
