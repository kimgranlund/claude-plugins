---
doc-type: lld
id: lld-0022-fleet-native-write-gate
status: draft
version: 0.2.0  # 0.1.0 -> 0.2.0, 2026-08-19: the "## Resolution 5" section below (gh#713). LLD
  # is a versioned-contract class (doc-writing-rules' mutability table) — changed via versioned
  # release, never silently; Resolutions 1-4 are unchanged from 0.1.0 except Resolution 3's
  # dated gh#713 supersession note (append-only, original text preserved below it).
date: 2026-08-19
owner: kim.granlund
ticket: nonoun-plugins#686  # gh#713 additionally resolved by Resolution 5 (version 0.2.0) — the
  # pre-accept grant line Resolution 3's own text named as a standing revisit.
adr: adr-0023 (accepted — .claude/docs/adr/0023-fleet-canon-vs-native-agent-teams.md,
  decision (c); cited, never edited — this LLD is the follow-up build under it, not a
  supersession); adr-0012 (accepted — .claude/docs/adr/0012-quick-build-auto-merge.md) —
  Resolution 5's grant-line mechanics precedent, cited not amended
spec: none — gh#686's own Acceptance section carries the checkable criteria, and ADR-0023
  decision (c) already carries the ruled claim ("pursue a fleet-native equivalent... not
  designed in this ADR... the follow-up names them"); a standalone SPEC would restate what the
  ticket and the accepted ADR already state (the same routing test lld-0017/lld-0021 both
  already applied).
scope: component
audience: builder, reviewer
---
# LLD — Fleet-native plan-approval write-gate in `dispatch-ticket` Phase 5 (gh#686, ADR-0023 (c))

**Verdict, head-first.** `dispatch-ticket`'s Phase 5 stage 2 gains one new sub-stage, **2a — the
plan-approval write-gate** — inserted between the branch push and the PR-open act, unconditional
on every build dispatch reaching that point (feature or task, small or big), never inferred from
or gated by ADR-0012's quick-build grant. The hold IS the pushed-but-unopened branch; the release
IS a durable accept-marker comment, posted by the marshal (`fleet-rules` §7's routing seat),
naming the pushed branch's HEAD SHA; no live marshal → the hold stands and the dispatch reports
`write-gate-blocked` rather than opening a PR or guessing acceptance. ADR-0012's stage 2b composes
strictly ON TOP — its own QB5 critic-green conjunct is unchanged and still required, but 2b's own
merge sequence never begins until 2a's accept marker has already landed and the PR it authorizes
is already open. The `in-flight` label's existing removal trigger moves with the PR-open act
(now accept-triggered) rather than gaining a second state. A worked dry-run fixture ships
alongside the SKILL.md edit so the mechanism is checkable at the payload layer — grep-able
markers on a fixture trace — with no browser or live-human layer required to prove the four
Acceptance criteria gh#686 names.

This build's own irony, disclosed rather than worked around: this dispatch (`build-leader` on
gh#686) itself runs under the OLD contract — the gate it is building does not yet exist to gate
its own PR. Applying it retroactively to this build's own PR would be incoherent (the gate cannot
hold a branch to protect a rule the branch itself is introducing); this is named in the PR body
and the Findings write-back, never silently glossed over.

## Non-goals

- **Not an edit to `fleet-rules` itself.** The marshal's role as accepting seat is this LLD's
  CONSUMPTION of §7's already-ratified routing-seat definition, not a new responsibility minted
  here — `teamwork/skills/fleet-rules/SKILL.md` is not touched by this build (Interfaces, below).
- **Not a new bundled `scripts/` directory for `dispatch-ticket`.** The payload-layer Acceptance
  criterion is satisfied by grep against a plain-text fixture; this build does not invent an
  executable harness `dispatch-ticket` has never had (Rejected alternatives).
- **Not a `check-state --fleet` extension surfacing a stalled write-gate.** R-2 names this as a
  real, live operational gap (an unattended run stuck on `write-gate-blocked` with no dashboard
  surfacing it) but explicitly defers building that surface to a future ticket — this build ships
  the gate's mechanics, not its monitoring.
- **Not the `#666` A4 rubric write-gate criterion.** gh#686's own Acceptance section names that
  criterion as "tracked there, not here" once this ships; this LLD's Acceptance section carries no
  predicate for it, and none is owed here.

## Resolution 1 — Hold mechanics: pushed-branch-without-a-PR, PR-open IS the accept act

**Fork:** does the hold sit at (a) push-without-PR, (b) an open draft PR, or (c) somewhere inside
the worker's own isolated worktree before any push at all?

**Decision: (a).** The marshal's lean is adopted as-is, with the reasoning made explicit rather
than assumed: ADR-0023's own Decision (c) frames the gap this closes as "before [writes] can
affect anything outside the worker's own isolation" — a push to a feature branch on `origin` is
already outside the worktree (any peer with repo read access can see and pull it), so (c) doesn't
actually name a real gap Phase 3's isolation doesn't already close, and gating BEFORE push would
block legitimate isolated-worktree-external visibility the fleet already depends on (a successor
session inventorying `git worktree list` against branch names, `fleet-rules` §5, needs the branch
to actually be pushed to reason about it at all). (b) is rejected because a draft PR is already
"visible/mergeable outside" in ADR-0023 Decision (c)'s own sense — GitHub surfaces a draft PR in
every list view, a reviewer can already comment on it, and `gh pr merge` on a draft only needs one
extra `--ready` step; treating a draft as still "held" would be a distinction Decision (c) doesn't
draw and this LLD declines to invent. So the hold is exactly the gap between "branch
pushed" and "PR opened" (draft or ready) — nothing more, nothing less. **PR-open, draft or ready,
IS the accept act** — the write-gate has nothing left to hold once either exists.

## Resolution 2 — Acceptance protocol: a durable SHA-naming comment, marshal accepts, no-marshal FAILS CLOSED

**Fork:** what durable shape does "accept" take, who plays the accepting seat for an unattended
dispatch, and what happens with no live accepting seat at all?

**Decision:** the marshal's lean is adopted as-is on all three sub-questions, reasoned from
existing canon rather than freshly invented:

- **Shape — a durable comment naming the branch SHA.** Mirrors ADR-0005's own claim-comment
  convention exactly (identity + a durable, timestamped, re-readable write beats an ephemeral
  nudge, `fleet-rules` §3's "durable records carry truth" default) — reusing an already-ratified
  pattern rather than minting a second one. Naming the SHA (not just the branch name) closes a
  real gap the branch name alone leaves open: a branch can be force-pushed or amended after an
  accept lands, and a SHA-naming comment makes staleness detectable (a later SHA on the same
  branch with no fresh marker is an un-accepted state, not a silently-still-accepted one).
- **Accepting seat — the marshal.** ADR-0023 (c) names this seat directly ("the marshal, per
  `fleet-rules` Section 7's routing seat, is the natural candidate — never inferred to be the
  human by default"); `fleet-rules` §7 already casts the marshal as the standing
  route-anything-incoming seat for exactly this class of decision (a decision belonging to no
  live human routes through the marshal, never absorbed or skipped). Never the dispatching
  worker itself: a worker accepting its own hold is the same generator-grades-its-own-artifact
  gap the fresh-context checker pass already exists to close one layer up (`plugin-authoring.md`'s
  semantic-edit invariant) — extending that same discipline to the write-gate rather than
  re-deriving a separate rule for it.
- **No-marshal fallback — FAIL-CLOSED.** Adopted over the alternative (auto-accept after a
  timeout, or fall back to the human) because ADR-0023's whole rationale for pursuing (c) at all
  is that the estate's current posture has "no equivalent in-loop write-hold" — a fallback that
  silently reverts to no-hold-at-all on marshal absence would reintroduce the exact gap the gate
  exists to close, on precisely the runs (marshal down, unattended) where the hold matters most.
  `write-gate-blocked` is a reported, terminal-for-this-turn outcome (Phase 6's own
  unattended-failure-branch discipline, `dispatch-ticket`'s existing `stale-premise`/SKIPPED/named-
  blocker family) — never a build failure, and never grounds to release the Phase 3 claim (an
  ordinary in-progress build's claim stays held through a routine wait; a wait for acceptance is
  not different in kind).

**Rejected: an auto-accept timeout.** Considered (e.g., "accept after 30 minutes of marshal
silence") — rejected because a timeout duration is an arbitrary number this LLD has no evidence
to set, and because ADR-0023's own stated rationale for pursuing the gate is structural strength
("structurally stronger than... the deny-hook reviewer wall", gh#686's own grounding, `#404`/
`#427`) — a hook wall that time-boxes itself into a no-op under exactly the condition (no reviewer
present) it exists to cover was never the standard being matched.

## Resolution 3 — Unconditional at first; ADR-0012 composes on top, never bypasses

> **Superseded in part, 2026-08-19 (gh#713) — append-only note, original resolution preserved
> below unedited.** "Unconditional" here meant *not gated by ADR-0012's own auto-merge grant*
> (the Rejected-alternatives entry directly below still holds exactly as written: 2a never fires
> ONLY alongside an auto-merge grant). It never meant un-revisitable — this Resolution's own
> closing clause ("revisit later if disproportionate for size:small") is the standing invitation
> gh#713 acts on. Resolution 5 (below) adds a SEPARATE, narrower grant —
> `accept-grant: authorized` — that composes ON TOP of this Resolution's unconditional default
> rather than replacing it: absent the new grant, 2a still fires on every dispatch exactly as
> decided here. Everything else in this Resolution stands unchanged. See Resolution 5 for the
> full mechanism.

**Fork:** does the gate fire on every dispatch unconditionally, or only when some condition (a
size floor, an explicit second grant) is also present?

**Decision:** the marshal's lean is adopted — unconditional at first, revisit later if
disproportionate for `size:small`. Reasoning: gh#686's own Acceptance criterion (c) asks how the
gate composes with ADR-0012's QB5 conjunct "reusing both, duplicating neither" — a
conditional-on-`size:small`-only gate would need its own new predicate logic duplicating QB1's
existing size read, buying nothing ADR-0012 doesn't already check for its OWN purposes. Making the
gate unconditional and composing ADR-0012 strictly on top keeps exactly one size-aware predicate
in the file (QB1, inside 2b) rather than two. **Composition, stated explicitly (closes gh#686's
own (c) criterion):** 2a's accept marker and QB5's critic-green conjunct answer two different
questions — QB5 asks "is this change GOOD" (a fresh-context checker graded it), 2a asks "is this
change ACCEPTED to land" (the marshal signed off) — and both are required on any dispatch that
reaches 2b eligible: 2a's accept marker must already exist (2b cannot begin evaluating its eight
conjuncts, let alone run its merge sequence, until 2a's hold has already released and the PR it
authorizes is already open — 2b operates on an ALREADY-OPEN PR by construction, so ordering is
strict: 2a's accept → PR-open → 2b's conjunct evaluation). Neither conjunct duplicates the other:
QB5 stays exactly as specified (a fresh-context checker verdict recorded on the change), and 2a's
accept marker is a distinct, separately-checkable durable comment naming the SHA. Nothing in 2b's
existing eight conjuncts is removed, renumbered, or restated — 2a is a strictly earlier gate that
2b's whole evaluation now presupposes already passed.

**Rejected: grant-only (2a fires only alongside an ADR-0012 `auto-merge: authorized` grant).**
Rejected — this would leave every non-quick-build dispatch (the overwhelming majority: any
`size:big` build, and any `size:small` build with no explicit grant) with NO in-loop write-hold at
all, which is exactly the gap ADR-0023's Context names as unclosed today. Scoping the gate to only
the rare auto-merge-eligible path would defeat its own stated purpose.

## Resolution 4 — `in-flight` label: same removal point, later in time, no new label state

**Fork:** does the `in-flight` label drop at push (today's rewritten trigger point would be
BEFORE PR-open under the new hold), at accept, or does it need a distinct third label state for
"held, awaiting accept"?

**Decision:** the marshal's lean is adopted — the label stays ON through the hold and drops at
the accept-triggered PR-open; the existing removal point (today: "the moment the PR opens") moves
later in wall-clock time (PR-open now happens only after 2a's accept) but is not a NEW removal
point in the SKILL.md's own state machine — the same line, describing the same event ("PR opens"),
now gated by one more precondition. Reasoning: minting a third label state ("held, awaiting
accept") would need a new label, a new removal rule for THAT label, and a new cross-reference for
every reader of `in-flight-label-semantics.md` and `mobilize-chores`' own pre-filter — real cost
for a distinction `fleet-rules` §2's guard layers don't currently need (an `in-flight` ticket
that's held-for-accept is exactly as "someone is actively working this, don't double-dispatch" as
one that's mid-build with no PR yet; the guard's own semantics don't change). **Rejected: a
distinct `awaiting-accept` label.** Rejected for the cost-with-no-behavioral-payoff reason above —
the existing `in-flight` semantics already cover the held state correctly.

## Resolution 5 — Pre-accept grant line: a narrow, explicit skip of 2a's hold alone (gh#713)

**Fork:** does every small, single-plugin, checker-and-gate-green build still owe a live marshal
accept round, or does a pre-placed grant let it skip 2a's hold specifically, without touching any
other discipline?

**Decision:** a literal grant line, `accept-grant: authorized`, placed in the sealed dispatch
prompt by the dispatching coordinator/seat AT DISPATCH TIME — same mechanics as ADR-0012's
`auto-merge: authorized` (explicit, never inferred from `size:small`, "unattended", or tone;
absent → the paragraph below does not exist), deliberately spelled distinct from that token so
the two grants are never conflated in a transcript or a grep. Chosen over reusing
`auto-merge: authorized` itself because the two authorize different acts on different clocks (one
skips a HOLD before PR-open; the other skips a MERGE after PR-open) and a dispatch may legally
carry one, both, or neither.

**The four-part predicate, evaluated by the dispatched seat, never the placer** (mirrors ADR-0012
Decision 2's own placer-vs-evaluator split exactly):

- **AG1 — `size:small`.** The same size read QB1 already makes off the ticket's own label —
  not a second detector.
- **AG2 — single-plugin.** QB2's own read.
- **AG3 — checker-green.** Phase 4's own fresh-context checker verdict, when Phase 4's
  semantic-edit trigger applied to this dispatch — or Phase 4's own "pure code/config, no
  checker owed" determination, when it didn't. Never a second checker pass invented for this
  gate; AG3 reads whichever of the two Phase 4 already produced.
- **AG4 — gate-green.** The SAME local aggregate gate run (`references/gate-run-time-budget.md`'s
  single-run-never-ground rule) stage 2 already performs before PR-open — pulled EARLIER in wall
  clock for a granted dispatch only (see Components, below): the gate run and Phase 4's checker
  both already exist by the time AG1–AG4 are evaluated; nothing runs twice.

All four green → **skip 2a's hold alone.** No accept marker is required or produced; the dispatch
proceeds directly to the version-collision re-checks and PR-open (Resolution 1's existing
mechanics, unaltered). Any conjunct absent, failing, or indeterminate → the hold stands exactly as
Resolution 2 specifies, full accept round owed — the grant is not a retry lever and is never
re-evaluated into eligibility on a later pass.

**Explicit scope — this skips ONLY stage 2a's hold.** Stage 2b's own ADR-0012 predicate
(QB0–QB7), the fresh-context checker pass, and the local+CI gate run are UNCHANGED and still
mandatory on every path, granted or not — a build that clears AG1–AG4 and skips the accept round
still needs its own separate `auto-merge: authorized` grant and all-green QB0–QB7 to also skip the
human merge. The two grants compose independently; neither implies the other.

**Composes with Resolution 3, doesn't disturb it.** Resolution 3's unconditional-by-default
posture is unchanged for every dispatch carrying no `accept-grant` line — the overwhelming
majority. Resolution 3's own "exactly one size-aware predicate... rather than two" concern is
preserved in kind, not in count: AG1/AG2 are READS of the same QB1/QB2 facts stage 2b already
computes, consulted a second TIME (pre-2a) for a second QUESTION (may the hold be skipped) —
never a second size/plugin-count DETECTOR. This is the same "two different questions, one shared
fact" shape Resolution 3 already used to reconcile 2a's accept marker against QB5's critic
verdict; Resolution 5 extends it one predicate further, not a new kind of coupling.

**Rejected: reusing `auto-merge: authorized` for both skips.** One token authorizing two
independently-revocable acts on two different clocks would make revoking one silently revoke the
other — the same "explicit, revocable" property ADR-0012 Decision 4 names as load-bearing breaks
under overload. Two literal, greppable tokens cost one more line and buy independent revocation.

## Components

### `teamwork/skills/dispatch-ticket/SKILL.md` (edit — Phase 5 stage 2, stage 4, sealed-contract
paragraph, Failure branches)

Phase 5 stage 2 is split at its own existing "push the claimed branch" clause: everything up to
and including the push stays; a new **2a** sub-stage (the write-gate: hold, accepting seat,
accept-marker shape, no-marshal fail-closed, and the explicit composition-ordering statement with
2b) is inserted; the existing version-collision re-checks / PR-open / gate-run-budget paragraph
is re-anchored to fire "once 2a's accept marker lands" rather than unconditionally, and the PR
body's required-fields list gains the accept marker's own comment URL. The `in-flight`
label-removal sentence is reworded to name the accept-triggered PR-open (Resolution 4) with no new
state. **2b**'s own opening sentence gains one clause stating it composes on top of, never
bypasses, 2a (Resolution 3), with the strict 2a→PR-open→2b ordering spelled out once. Stage 4's
typed-handoff bullet gains the accept-marker comment URL as a required field alongside the PR URL
and Findings-comment URL. The sealed-contract paragraph (the one enumerating what's true of every
dispatch: ticket path + enumerated inputs + budget + typed return + `--remove-label in-flight` +
`version_claim_check.py` re-run + the VALUE-race re-read) gains 2a's accept-marker requirement to
the same enumerated list. Failure branches gains one new bullet: `write-gate-blocked` (Resolution
2's fail-closed outcome), stated in the same reported-not-a-failure register as `stale-premise`
and the SKIPPED task branch already use. **Canon note:** once this build ships, the shipped
SKILL.md text and its fixture are the canonical, live description of the mechanism — this LLD is
frozen at its own `version:` as the build record, never re-synced if the SKILL.md text is later
worded differently (`CLAUDE.md`'s "sources flow outward" invariant, applied one layer down: a
build LLD documents the design decision, the shipped artifact is the standing source of truth
going forward).

### `teamwork/skills/dispatch-ticket/references/write-gate-dry-run.md` (new — the payload-layer
fixture, gh#686's own Acceptance criterion)

TWO worked, fully-fictional dry-run traces against a fixture ticket (`TKT-FIXTURE-001`), each a
different composition path so the fixture proves both Resolution 2 (the hold/accept mechanics
alone) and Resolution 3 (the 2a→PR-open→2b ordering) without conflating them:

- **Trace 1 — unconditional path, no ADR-0012 grant** — exactly THREE markers, in order: branch
  pushed (`HOLD:`), the marshal's accept-marker comment (`ACCEPT-MARKER:`, naming a fixture SHA),
  the PR-open act (`PR-OPEN:`, citing that comment's URL). No `QB5:`/`2B-EVAL-ORDER:` lines appear
  in this trace — there is no grant, so stage 2b never evaluates (Phase 5's own "absent → this
  stage does not exist" rule).
- **Trace 2 — ADR-0012-granted path, QB5 already green** — exactly FIVE markers, in order: the
  same `HOLD:`/`ACCEPT-MARKER:`/`PR-OPEN:` triple, THEN `QB5:` (the fresh-context checker verdict,
  recorded distinct from the accept marker per Resolution 3), THEN `2B-EVAL-ORDER:` (an explicit
  line stating 2b's eight-conjunct evaluation began strictly after `PR-OPEN:`, never before
  `ACCEPT-MARKER:`).

Every marker is a literal, greppable line-prefix. The exact, disambiguated payload-layer check:
`grep -E '^(HOLD|ACCEPT-MARKER|PR-OPEN|QB5|2B-EVAL-ORDER):' references/write-gate-dry-run.md |
wc -l` returns `8` (3 + 5), and a per-trace grep (`sed`-delimited on each trace's own `## Trace N`
heading) returns exactly 3 lines for Trace 1 and exactly 5 for Trace 2, each in the stated
order — satisfying gh#686's own "checkable from the SKILL.md text and any bundled fixture, no
browser/human layer required" criterion at the pure-payload layer (`docs:agent-harness-rules`'
assert-layer ladder, rung 1). A short header states what the fixture proves and what it does NOT
(it is not a runnable script — `dispatch-ticket` has no bundled `scripts/` directory today, and
inventing one solely to execute a fixture already checkable by grep would be
script-writing-rules' own "is this mechanizable, and does mechanizing it buy anything a plain
read-and-grep doesn't" question answered no).

### `teamwork/skills/dispatch-ticket/references/plan-approval-write-gate.md`, `gate-run-time-budget.md`, `quick-build-auto-merge-predicate.md` (new — F6 splits, build-time addition)

Not part of the original plan; added during the build once the fresh-context `harness:skill-checker`
pass and this skill's own `skill_lint.py` F6 check both confirmed the SKILL.md body exceeded its
line budget with 2a inserted inline in full. Rather than under-specify 2a in-place, the fuller
mechanics (accept-marker shape, SHA-staleness rule, the fail-closed rationale) moved to
`plan-approval-write-gate.md`; the pre-existing gate-run-time-budget paragraph and the pre-existing
QB0–QB7/merge-sequence block (stage 2b) — both unrelated to this ticket's own scope but the two
largest self-contained blocks available to cut — moved to their own reference files so the budget
closed without under-specifying 2a itself. Each SKILL.md citation point is a short pointer, same
convention as this skill's other F6 splits (`isolation-ladder.md`, `spec-lock-gate.md`, etc.).

### gh#713 Components (version 0.2.0 addendum — Resolution 5's own build)

`teamwork/skills/dispatch-ticket/SKILL.md` gains the Resolution-5 pre-accept-grant paragraph
inserted immediately after 2a's existing FAIL-CLOSED bullet and before the "Immediately before
opening the PR" paragraph (whose opening clause now names the granted branch too), plus one
clause each on stage 4's typed-handoff bullet and the in-flight-label sentence covering the
grant-triggered PR-open. `teamwork/skills/dispatch-ticket/references/plan-approval-write-gate.md`
gains the full AG1–AG4 conjunct definitions the SKILL.md body only summarizes (same F6-split
convention the file already uses). Two further, INDEPENDENT gh#713 levers ship in the same
campaign but touch neither this LLD's own mechanism nor its Components list above — named here
only for the record, never re-derived: a new `teamwork/scripts/merge_queue_watch.py` (batched
merge-queue check-runs watcher, its own selftest) and terse one-line close-out wording across
`docs/skills/file-bug|file-feature|file-task/SKILL.md`. Per this file's own "Canon note" above,
the SKILL.md text shipped by this build is the standing source of truth for Resolution 5's exact
wording going forward; this addendum records the design decision, not a live mirror.

## Interfaces

- **2a → 2b:** strict ordering, one-way — 2b's eight-conjunct evaluation reads the PR as an
  already-open precondition (its own QB2/QB3 diff-inspection conjuncts already assume a PR
  exists to diff against `origin/main...HEAD`); 2a's accept marker is what made that PR possible
  to open in the first place. No new data interface between them — 2a produces a durable comment
  URL, 2b's stage-4 handoff already had a slot for "the Findings write-back's own comment URL" the
  accept-marker URL sits beside, not inside.
- **2a ↔ ADR-0005's claim protocol:** the accept-marker's shape (durable comment naming an
  identity + a re-checkable fact) is the SAME shape Phase 3's claim comment already uses,
  reasoned in Resolution 2 — a citation, not a new pattern.
- **2a ↔ `fleet-rules` §7:** the marshal's role as accepting seat is this LLD's consumption of an
  already-ratified routing-seat definition; `fleet-rules` itself is not edited by this build (no
  new marshal responsibility is being defined here beyond what §7 already grants it — accepting a
  write-gate hold is one more instance of "a decision belonging to no live human routes through
  the marshal," not a new kind of decision).
- **`write-gate-dry-run.md` ↔ Phase 5 text:** citation-only, one-way (the fixture illustrates the
  prose; the prose is not generated from the fixture) — same relationship every other
  `references/*.md` file in this skill already has to its own SKILL.md citation point.

## Data

The accept-marker comment's own minimal shape (git-native backend; a file-backend/adapter
equivalent restates the same three facts in its own write path):

```
Accept: <marshal-seat-identity>, <UTC timestamp>, branch `<decided-branch-name>` @ <head-sha> —
plan-approval write-gate accepted (ADR-0023 (c)); PR-open may proceed.
```

`write-gate-dry-run.md`'s two fixture trace shapes (abbreviated; the real file gives each its own
`## Trace 1` / `## Trace 2` heading so a per-trace grep can isolate them):

```
## Trace 1 — unconditional path, no ADR-0012 grant (3 markers)
HOLD: branch `tkt-fixture-001-demo-slice` pushed to origin, no PR open — 2a hold in effect
ACCEPT-MARKER: gh issue comment on TKT-FIXTURE-001, marshal @fixture-marshal, 2026-08-18T00:00:00Z,
  branch `tkt-fixture-001-demo-slice` @ a1b2c3d4 — accepted, PR-open may proceed
PR-OPEN: PR opens against main, body cites the accept-marker comment URL; in-flight label removed

## Trace 2 — ADR-0012-granted path, QB5 already green (5 markers)
HOLD: branch `tkt-fixture-001-demo-slice-b` pushed to origin, no PR open — 2a hold in effect
ACCEPT-MARKER: gh issue comment on TKT-FIXTURE-001, marshal @fixture-marshal, 2026-08-18T00:05:00Z,
  branch `tkt-fixture-001-demo-slice-b` @ b2c3d4e5 — accepted, PR-open may proceed
PR-OPEN: PR opens against main, body cites the accept-marker comment URL; in-flight label removed
QB5: fresh-context checker verdict recorded, zero blocker/major findings
2B-EVAL-ORDER: 2b's eight-conjunct evaluation begins AFTER PR-OPEN, never before ACCEPT-MARKER
```

## Build sequence

| # | Step | Path | Done when |
|---|---|---|---|
| 1 | Draft this LLD, resolve the four forks | `.claude/docs/lld/lld-0022-fleet-native-write-gate.md` | fresh-context `docs:doc-checker` pass recorded, findings fixed |
| 2 | Edit Phase 5 stage 2: insert 2a, re-anchor the PR-open paragraph, reword the `in-flight` sentence | `teamwork/skills/dispatch-ticket/SKILL.md` | the four Resolutions are each realized as literal prose, greppable |
| 3 | Edit Phase 5 stage 2b's opening sentence: composition + ordering clause | same file | 2b's text states it never begins before 2a's accept |
| 4 | Edit Phase 5 stage 4 + the sealed-contract paragraph: accept-marker URL as a required field | same file | both paragraphs name the accept-marker URL explicitly |
| 5 | Edit Failure branches: `write-gate-blocked` bullet | same file | bullet present, reported-not-failure register matched |
| 6 | Write the dry-run fixture | `teamwork/skills/dispatch-ticket/references/write-gate-dry-run.md` | both worked traces present; Trace 1 greps 3 markers in order, Trace 2 greps 5, total 8 |
| 7 | Fresh-context `harness:skill-checker` pass on the edited SKILL.md; record verdict, fix findings | — | verdict recorded, zero unresolved blocker/major |
| 8 | README ledger + version bump (re-read `origin/main` first, per Phase 3/5's own VALUE-race discipline) | `teamwork/README.md`, `teamwork/.claude-plugin/plugin.json` | `release_gate.py teamwork --package` fully green |
| 9 | Dated Findings write-back on gh#686 | gh#686 | comment posted |

## Acceptance (checkable predicates)

1. `grep -n "2a\." teamwork/skills/dispatch-ticket/SKILL.md` shows the write-gate sub-stage
   present inside Phase 5 stage 2, between the push clause and the PR-open paragraph.
2. `grep -n "FAIL-CLOSED\|write-gate-blocked" teamwork/skills/dispatch-ticket/SKILL.md` shows both
   the fallback rule and its Failure-branches outcome.
3. `grep -n "Accepting seat:" teamwork/skills/dispatch-ticket/SKILL.md` returns exactly one line,
   inside the new 2a text, naming the marshal (a literal anchor unique to 2a's own bullet — never
   satisfied by an unrelated existing citation of the word "marshal" elsewhere in the file).
4. `grep -n "composes\|never bypass" teamwork/skills/dispatch-ticket/SKILL.md` shows 2a/2b's
   composition and non-bypass relationship stated in 2b's own opening text.
5. `grep -E '^(HOLD|ACCEPT-MARKER|PR-OPEN|QB5|2B-EVAL-ORDER):' teamwork/skills/dispatch-ticket/references/write-gate-dry-run.md | wc -l`
   returns `8` (Trace 1's 3 + Trace 2's 5); a per-trace grep bounded by each `## Trace N` heading
   returns exactly 3 lines for Trace 1 (`HOLD`, `ACCEPT-MARKER`, `PR-OPEN`, in that order, no
   `QB5`/`2B-EVAL-ORDER`) and exactly 5 for Trace 2 (the same three, then `QB5`, then
   `2B-EVAL-ORDER`, in that order).
6. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0022-fleet-native-write-gate.md` → exit 0.
7. `python3 harness/scripts/skill_lint.py teamwork/skills/dispatch-ticket/SKILL.md` → exit 0
   (description untouched, so no routing-surface re-check owed; body-only edit still lints clean).
8. `python3 harness/scripts/release_gate.py teamwork --package` → green.
9. Fresh-context `harness:skill-checker` verdict on the edited SKILL.md recorded in this build's
   Findings write-back, zero unresolved blocker/major findings.

**gh#713 (Resolution 5, version 0.2.0) — continuing the numbering above:**

10. `grep -n "accept-grant: authorized" teamwork/skills/dispatch-ticket/SKILL.md` shows the
    literal grant token.
11. `grep -n "AG1\|AG2\|AG3\|AG4" teamwork/skills/dispatch-ticket/SKILL.md` shows all four
    conjuncts named.
12. `grep -n "skip only this hold\|skips 2a alone" teamwork/skills/dispatch-ticket/SKILL.md`
    shows the explicit scope-limiting statement (2b/checker/gate unchanged).
13. `python3 docs/scripts/doc_lint.py .claude/docs/lld/lld-0022-fleet-native-write-gate.md` →
    exit 0 (version-bump + append-only-note pass the mutability lint).
14. `python3 harness/scripts/skill_lint.py teamwork/skills/dispatch-ticket/SKILL.md` → exit 0.
15. Fresh-context `harness:skill-checker` verdict recorded on the edited SKILL.md (semantic edit
    to a prompt-carrying artifact, `.claude/rules/plugin-authoring.md`'s critic invariant).

## Risks

- **R-1 — a marshal that silently stops posting a fresh accept-marker after an amended branch
  reads as still-accepted if a reader trusts the branch name alone.** Mitigated by Resolution 2's
  own SHA-naming requirement — a later HEAD SHA with no matching marker is detectably un-accepted,
  not silently still-good. Detection: the accept-marker's SHA vs. the branch's current
  `HEAD` at PR-open time; a mismatch is this LLD's own PR-open precondition failing, named as
  `write-gate-blocked` again rather than opened anyway. Locus: spec (the SKILL.md text states the
  SHA-match precondition explicitly).
- **R-2 — an unattended run with the marshal down could stall indefinitely with no one to notice.**
  Named as a real cost of the fail-closed choice (Resolution 2's own rejected-alternative
  discussion) rather than hidden: `fleet-rules` §5's session-death resilience already inventories
  from durable state on any successor session, so a `write-gate-blocked` report sitting on a
  ticket is exactly the kind of durable, re-discoverable state that resilience model is built to
  surface — not a silent hang. Locus: plan (an operational monitoring gap, not a design defect;
  `check-state --fleet` is the natural place a stalled write-gate would surface, a future
  extension this LLD doesn't build).
- **R-3 — this build's own PR ships under the OLD contract, which could read as inconsistent to a
  reviewer expecting the new rule to apply to itself.** Disclosed explicitly (Verdict's own closing
  paragraph, and again in the PR body) rather than worked around with a manufactured self-exception
  — the gate genuinely cannot hold a branch to protect a rule that same branch is introducing.
  Locus: spec (a stated, permanent exception for the introducing PR only, never a precedent for
  any LATER PR skipping the gate on the same reasoning).

## Rejected alternatives

- **Gating before push (inside the worker's own isolated worktree).** Rejected — Resolution 1; no
  real gap Phase 3's isolation doesn't already close, and it would block the fleet's own
  push-then-inventory resilience model.
- **Treating an open draft PR as still "held."** Rejected — Resolution 1; ADR-0023's own
  visible/mergeable-outside test is already satisfied by a draft.
- **An auto-accept timeout on marshal silence.** Rejected — Resolution 2; reintroduces the exact
  gap the gate exists to close on precisely the runs where it matters most.
- **Grant-only gating (2a fires only alongside ADR-0012's grant).** Rejected — Resolution 3; would
  leave the overwhelming majority of dispatches with no hold at all.
- **A distinct `awaiting-accept` label state.** Rejected — Resolution 4; real cost, no behavioral
  payoff over the existing `in-flight` semantics.
- **A new bundled `scripts/` fixture-runner for `dispatch-ticket`.** Rejected — the payload-layer
  criterion is already satisfiable by grep against a plain-text fixture; inventing a script solely
  to execute what a grep already proves fails `script-writing-rules`' own mechanization test.
- **A standalone SPEC document.** Rejected — gh#686's Acceptance section plus the accepted
  ADR-0023 already carry the checkable claim; a SPEC would restate both.
- **Reusing `auto-merge: authorized` for the pre-accept grant too (gh#713).** Rejected —
  Resolution 5; one token authorizing two independently-revocable acts on two different clocks
  would make revoking one silently revoke the other.

## Agent verification

Per `docs:agent-harness-rules`, the assert layer is the cheapest one that catches this criterion's
failure — pure text/payload, rung 1 of the ladder, no browser or live-human layer needed:
**Mechanical layer:** `doc_lint.py` on this LLD; `skill_lint.py` on the edited SKILL.md;
`release_gate.py teamwork --package`. **Payload layer (gh#686's own Acceptance criterion,
satisfied directly):** the grep predicates above (eight as of version 0.2.0: predicates 1–5 for
gh#686, 10–12 added for gh#713's Resolution 5), run against the SKILL.md's own Phase 5 text
and the new fixture file — no bundled script needed, `references/write-gate-dry-run.md`'s
plain-text markers ARE the checkable payload. **Fresh-context checkers:** `docs:doc-checker` on
this LLD before the build proceeds; `harness:skill-checker` on the edited SKILL.md before merge
(semantic edit to a prompt-carrying artifact, `.claude/rules/plugin-authoring.md`). **Human/
judgment layer, stated exception:** whether the marshal-as-accepting-seat choice (Resolution 2)
still holds once `agent-teams` itself is re-evaluated (ADR-0023 (b)'s own trigger) is a future
re-check this LLD doesn't attempt to pre-empt — named here so it isn't silently assumed
permanent.
