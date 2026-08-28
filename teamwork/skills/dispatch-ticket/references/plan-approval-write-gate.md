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

## Seat-side wake rule while held (gh#954, live-observed 2026-08-27)

The hold above says what the seat WAITS for; this says what the seat DOES when anything wakes
it. Observed 3 of 3 times in one session (#949/PR #950, #945/PR #951, #952): the marshal
posted the accept marker and sent "open the PR" in one step, the seat woke, re-sent its prior
"held at write-gate, SHA X" report, and idled with no PR opened; a second identical message
produced the PR within a minute. The marker was already on the issue at the first wake, so the
gap was never the accept act itself but the seat treating the wake as a status prompt rather
than as the signal to re-check the record.

**On ANY wake after the hold** (a SendMessage from the marshal, a peer message, a resumed
session, a `/goal` retry) the seat, before composing any reply:

1. **Re-reads the issue's latest comments live** (`gh issue view <id> --comments`, or the
   adapter's `read`), scanning ALL comments, not only the newest, for a comment literally starting
   `Accept:` that names the pushed branch's CURRENT HEAD SHA (re-read with `git rev-parse HEAD`
   on the branch, never from memory). The marshal's message is the wake signal, not the
   authorization: the comment is what authorizes, so it is read even when the message already
   says "accepted".
2. **Marker present and SHA matches → open the PR in this same turn.** The reply to the wake is
   the PR URL plus the stage-4 handoff, never a restatement of the earlier "held" report. Never
   idle between reading the marker and `gh pr create`.
3. **Marker absent** (the message may have raced the comment post) → wait roughly 30 seconds,
   re-read once more, then follow step 2 on a hit. Still absent, or the SHA in the marker does not
   match HEAD → reply `write-gate-blocked` naming the branch, the current HEAD SHA, and what was
   found (no marker / stale SHA), then idle. A marker naming a different SHA is not "close enough"
   (the SHA-staleness rule above).

A "held" report is sent ONCE, at the moment the hold begins. Re-sending it in answer to a wake is
this defect's signature: the seat has answered a question nobody asked and has left the accepted
branch un-opened. The seat also never asks the marshal to "confirm" acceptance in reply to a wake
— the record is the confirmation, and step 1 already read it.

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
   Then, when a named seat is holding the branch, wake it with ONE message that carries the
   accept comment's URL and the SHA it names ("Accept posted: <comment-url>, SHA <sha>. Open the
   PR."). Post the comment BEFORE sending the message, never in the same breath after it: the
   seat's wake rule above re-reads the issue on wake, and a message that arrives ahead of the
   comment is exactly the race that made the seat idle (gh#954). A held seat that answers with
   its earlier "held" report instead of a PR URL is that defect recurring; resend once, citing
   the wake rule, and file it if it repeats. Step 3 below is the marshal opening the PR itself
   only when no seat is holding the branch (a `write-gate-blocked` return from a finished
   dispatch).
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

### What step 2's re-read actually verifies (live-observed, agent-ui, 2026-08-26 to 2026-08-28)

Step 2 says the marshal re-reads the branch's HEAD before naming it; on its own that catches a
stale SHA and nothing else. The sequence that held across every accept marker in one three-day
agent-ui marshal session (agent-ui `#1680`, `#1681`, `#1682`, `#1686`, `#1687`, `#1690`,
`#1692`), and is what actually resolved two apparent collisions, is four reads against `origin`,
never against the seat's report:

1. `git fetch origin <branch>` then `git rev-parse origin/<branch>` — the SHA the marker names.
2. `git diff main origin/<branch> --stat` — the touched-file set, compared against what the seat
   claimed; a file the seat did not mention is a scope question before it is an accept.
3. A local trial merge: `git checkout -b tmp-verify-<id> main && git merge origin/<branch>
   --no-commit --no-ff`, inspect `git status --porcelain`, then `git merge --abort && git checkout
   main && git branch -D tmp-verify-<id>`. Nothing is committed; this only proves the branch lands
   on the CURRENT `main`, which the seat's own "gates green" run (against the `main` it branched
   from) cannot prove.
4. Read the diff itself when the change is small enough to read; a docs-only amendment is
   accepted on its content, not its line count.

Why the trial merge earns its cost: two holds in that session looked like collisions and were
not. agent-ui `#1681` (a 23-file ADR rename sweep, PR `#1685`) was cut concurrently with
`#1680`'s branch, and `#1686`'s branch was cut before an unrelated doc-standards fold-in
(adr-0040/adr-0049) landed on `main` during its hold; in both cases step 3's clean trial merge
against the CURRENT `main` was the evidence the accept-marker comment cites, and what let the
marker post without a re-dispatch. The seat's own self-report was correct both times, but it was
not what the decision rested on. `[incident]`

This does not duplicate stage 2b's QB2/QB3 diff inspection (Resolution 3 below): 2b inspects an
OPEN PR to decide whether it may auto-merge; this check runs before any PR exists, to decide
whether the branch is even the right thing to name in the marker. A branch that fails step 3 is
`write-gate-blocked` again, never a PR for 2b to inspect.

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

**This hold and ADR-0002's separate "this seat never merges its own PR" rule govern different acts
on different clocks — check the record for both, independently.** ADR-0002 constrains who acts
once a PR already exists (never the build seat itself, for the merge); this stage's hold
constrains whether the PR may be OPENED at all. "The ceiling is PR-open, merge stays a human act"
truthfully describes an ALREADY-ACCEPTED dispatch's remaining constraint — it is not evidence that
PR-open itself is safe by default, and observing that OTHER sibling dispatches in the same session
opened PRs is not a substitute for THIS dispatch's own accept marker. **Before calling `gh pr
create` (or opening a draft PR): verify one of — (a) a comment on the ticket that literally starts
`Accept:` and names the pushed branch's current HEAD SHA (re-read live), or (b) the sealed
dispatch prompt carries `accept-grant: authorized` with AG1–AG4 (the four conjuncts defined below)
confirmed green. Neither present → do not open the PR**, regardless of session tone, sibling
behavior, or how confident the seat is that a human already signed off. (See the `build-1661` case
below for the exact fallacy this closes.)

**Observed adherence gap: the Marshal-side response procedure above was skipped, not followed
(a separate live session, 2026-08-21, same day as that procedure's own capture).** A
`mobilize-chores` interactive round dispatched three tickets via `build-leader`; all three
reached stage 2a with no marshal joined and correctly reported `write-gate-blocked`, and each
also correctly refused a relayed "the human already confirmed this" from the dispatching
coordinator as a substitute for acceptance (per "never inferred to be the live human by default"
and the durable-record requirement above). But the coordinator resolving them did NOT run the
Marshal-side response procedure's own steps 1-2 — it never extracted the seat's proposed PR body
from its Findings comment, and never posted the accept marker naming the branch's actual HEAD
SHA. It asked the live human directly per ticket, then jumped straight to step 3 (`gh pr create`,
composing its own PR body rather than the seat's), skipping the durable record step 2 exists to
leave. Net effect: three tickets now have merged PRs with no accept-marker comment on their own
issue — indistinguishable, to a later reader of the ticket alone, from a hold that was silently
bypassed rather than one a live human genuinely authorized. The fix is adherence, not new design:
a coordinator resolving a `write-gate-blocked` report under live human authorization should run
the existing procedure's steps 1-2 before step 3, every time — this note exists so a future
session recognizes the shortcut as a defect in execution, not a precedent to repeat.

**Observed conflation gap (2026-08-26, agent-ui#1663): the dispatched seat itself, not the
marshal, skipped this hold.** `build-leader` seat `build-1661` (ticket agent-ui#1661, task-kind)
reached stage 2a with no marshal joined and fell through to `gh pr create` directly, stating
afterward: "No accept-grant/auto-merge line was in the dispatch, so I followed this exact team's
own standing convention for an interactive run (every sibling build-* dispatch in this session's
config: 'ceiling is PR-opened, merge stays a human act') rather than holding indefinitely for an
accept-marker with no other marshal seat visible in this team." Investigation (agent-ui#1663)
found this is exactly the conflation the paragraph above now names explicitly, and that it was NOT
a documentation-salience gap: seven same-session task-kind siblings (agent-ui#1631, #1632, #1637,
#1642, #1643, #1644, #1645) held correctly for a marshal accept-marker under the identical
unconditional rule — `build-1661` was the lone outlier, not evidence the rule reads ambiguously.
Named here as the seat-side counterpart to the marshal-side adherence gap above (a different actor
skipping a different half of the same procedure); the anti-conflation paragraph and
mechanical-verify instruction above are the resulting hardening — a positive record check the
dispatched seat performs rather than a conclusion it reasons its way to.

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
