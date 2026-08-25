---
doc-type: lld
id: lld-0026-gate-first-mode
status: draft
version: 0.1.0
date: 2026-08-25
owner: kim.granlund
ticket: claude-plugins#939
spec: none — #939's own body is the ratified design surface (Kim-ruled LLD-first, size:big);
  its Acceptance section already enumerates the five provisional predicates and names this LLD
  as the document that finalizes them. A standalone SPEC would restate the ticket (the same
  routing test lld-0022/lld-0023/lld-0024 each applied).
scope: feature
audience: builder, reviewer
---
# LLD — Gate-first mode: validator-authored executable acceptance gates before build (gh#939)

**Verdict, head-first.** `dispatch-ticket` Phase 4 gains an OPT-IN gate-first branch, armed only
by the literal sealed-prompt line `gate-first: authorized` (the `auto-merge: authorized` /
`accept-grant: authorized` idiom — explicit, never inferred). When armed and the ticket
qualifies (Resolution 2), a validator-class seat (unnamed, synchronous, `general-purpose` with
`model: sonnet` pinned per #313/#919 — no new named agent) reads the ticket's Acceptance section
and the build's scratch clone READ-ONLY and writes one gate script,
`gate_<id>.py`, per `harness:script-writing-rules` (tri-state exit, one PASS/FAIL line per
check, each FAIL naming expected-vs-actual + exact path + exactly what to do, selftest where
sensible). The gate lives OUTSIDE the build tree (Resolution 1) — a sibling directory of the
scratch clone that the builder's sealed prompt never enumerates — and a new helper,
`teamwork/scripts/gate_guard.py`, hashes the gate before every run so tamper is detected
mechanically. The build loop becomes gate → feed FAIL lines back verbatim as the builder's
next-round instructions → rebuild → re-run, capped at 3 rounds (Resolution 4), with the SAME
check failing twice consecutively firing `loop-rules`' existing triage-diagnostician +
gate-repair mechanism (Resolution 3/5a — cited, never duplicated). Gate green is a new
precondition on Phase 5 stage 2a's hold; the existing fresh-context checker pass stays exactly
where it is, unchanged, as the semantic layer on top. The default path — no grant line — is
byte-for-byte today's behavior: the branch does not exist.

## Non-goals

- **Not replacing the semantic-edit critic invariant.** `.claude/rules/plugin-authoring.md`'s
  fresh-context checker pass on any prompt-carrying-artifact edit is untouched and still owed on
  every qualifying build, gate-first or not. The gate proves the LETTER of the request
  mechanically (files, exit codes, behavior); the checker judges QUALITY and semantics. **A green
  gate never discharges the critic pass** — a future reader who conflates the two has misread
  this section, which exists to be cited against exactly that conflation. (The ticket's own
  Scope/Open flags this; stated here as the design's standing rule.)
- **Not a new named agent.** The validator is a checker-CLASS dispatch, not a checker seat:
  `general-purpose` + `model: sonnet` explicit + tools narrowed to read-only against the clone
  plus Write scoped to the gate directory alone. Minting a `validator` agent fails the
  anti-matrix bar (one caller, one moment in one skill's lifecycle).
- **Not touching the task-kind or bug-kind branches in this pass.** Gate-first ships on the
  feature path only (Phase 4/5); Resolution 2 states why task stays out for now.
- **Not editing `loop-rules`.** Its triage-diagnostician section (PR #941) is already written
  generically ("the SAME check's second consecutive failure"); gate-first cites it and supplies
  the gate that section presupposes. A reciprocal pointer there is optional polish, not owed.
- **Not a delegation plan.** See Resolution 5b — one validator plus one builder is a linear
  pipeline, not a multi-task graph; no `delegation-plan-schema` artifact is produced or owed.
- **Not shipping the gate script in the PR.** The gate is run-scoped scaffolding, not product
  code; Resolution 1 gives it a durable home on the ticket instead of the tree.

## Resolution 1 — Where the gate lives: outside the clone, durable copy on the ticket

**Fork:** inside the build's scratch clone, vs. "the ticket's artifacts" (which the git-native
backend does not have as a real store), vs. a dispatcher-owned path outside the tree.

**Decision: a dispatcher-owned sibling directory outside the build tree, with the ticket comment
as the durable copy.** The executable gate lands at `<scratch-parent>/gate-<id>/gate_<id>.py` —
a sibling of the scratch clone (isolation-ladder Rung 2's own parent directory), never inside
it. Structural, not conventional: the builder's sealed dispatch enumerates ONLY the clone path
(Phase 5's sealed-contract discipline — enumerated inputs are the write surface), so the gate
sits outside everything the builder was handed; and `gate_guard.py` (Build sequence step 2)
SHA-256-hashes the gate file before every run and refuses a changed hash with a loud
`gate-tampered` failure. Stated honestly, as `loop-rules` does for the same fusion-harness
pattern: this is directory-scoping plus hash-detection, not OS-level enforcement — the stack has
no stronger primitive today, and claiming one would be false.

Because scratch clones are torn down (Phase 3's teardown bullet), the run posts the gate script
verbatim as a `gh issue comment` on the ticket the moment the validator finishes — the same
write-back verb the Findings contract already uses, giving git-native the "ticket artifact"
the ticket's open question was reaching for. In-tree commit was rejected: it hands the builder
write access to the gate via the very tree it owns, and ships one-shot scaffolding as product.

The one legitimate write to the gate after authoring is `loop-rules`' gate-repair privilege
(#938/#941): the diagnostician's widened grant is scoped to this one file, the byte-diff +
audit-copy + immediate-drop mechanics apply as written there, and the repaired gate is re-posted
to the ticket as a second comment naming the repair.

## Resolution 2 — Which tickets qualify: feature-path records with mechanizable Acceptance

**Decision: `kind: feature` (and Phase 2's default arm) only, and only when the Acceptance
section passes `script-writing-rules`' own mechanization test** — every explicit requirement
maps to a pass/fail function over repo state, command exit codes, or observable behavior. The
validator applies that test as its first act: a record whose acceptance is judgment wearing a
costume (wording quality, "reads well", consolidating/administrative/knowledge-shaped records —
the ticket's own exclusion) gets a typed `gate-infeasible` return naming the unmappable
requirement, and the dispatch proceeds on the DEFAULT path with that return recorded in
Findings — never a weakened gate, never an existence check standing in for content/behavior
(the ticket's no-proxy rule), never checks the request didn't ask for (its no-scope-creep rule).

Task-kind stays out this pass: a task is ONE sealed dispatch with no try-cap wrapper (Phase 2's
own words), so it has no round structure for FAIL-feedback to thread through; extending
gate-first there means first giving task a loop, which is a separate design. Bug-kind is
`file-bug`'s lifecycle, categorically out.

## Resolution 3 — How FAIL feedback threads through the existing round structure

**Decision: gate rounds ARE the existing `/goal` try-cap's tries — no second loop.** Phase 5
already wraps the feature path in a `/goal` with capped tries and an escalate-on-same-failure
clause. Gate-first does not add a parallel loop; it makes the existing loop's stopping predicate
mechanical. Concretely, per round:

1. Builder builds in the clone (small: inline in the dispatching seat's own tree per the
   no-nested-wait rule; big: the `builder` seat, re-dispatched sealed).
2. The seat running this procedure (the leader) runs `gate_guard.py run <gate> <clone>` —
   hash-check, bounded execution, exit + per-check lines captured.
3. Exit 0 → gate green; proceed to the untouched checker pass and Phase 5 stage 2a. The
   gate-green line and round count join stage 4's typed handoff.
4. Exit 1 → the FAIL lines — verbatim, unedited, unsummarized (fusion-harness's core move; a
   leader paraphrase is a second hallucination surface) — become the entire work instruction of
   the next round's sealed prompt, alongside the unchanged ticket reference. Loop to 1.

The gate runs BEFORE stage 2a's hold: a build that cannot pass its own ticket's letter never
reaches the accept marker. On a big build the coordinator owns steps 2–4; on a small build the
`build-leader`/host seat does — either way the BUILDER never runs or reads the gate file
directly, only its output lines.

## Resolution 4 — Round cap: 3, with triage inside it, not beside it

**Decision: default cap of 3 gate rounds, and the FAIL loop feeds the SAME
triage-diagnostician mechanism — it is not a separate budget.** Three matches this workspace's
established gate-as-goal convention (`loop-rules`' gates table: `release_gate.py`,
`skill_lint.py` et al. all run "3 tries, then stop and report"). Composition with #941's canon,
exactly as that section is written: the same CHECK (a named PASS/FAIL line, not the gate as a
whole) failing twice consecutively fires the triage diagnostician mid-loop — one bounded
Diagnosis/Do-exactly-this/Do-NOT brief handed to the builder, gate-repair privilege available
exactly once if and only if the gate itself is defective, and a repaired-gate re-run charging no
try. A second identical failure AFTER diagnosis, or the cap exhausting, ends the run through the
EXISTING "unresolved gate failure" failure branch (claim released per Phase 3, failure recorded
in Findings, ticket stays `doing`) plus a new sibling line naming `gate-rounds-exhausted` with
the final FAIL lines quoted. Two budgets would double-count the same failures and contradict
#941's "not a second triage pass" rule; one budget with triage as its interior escalation is the
composition that skill already specifies.

## Resolution 5 — Composition with the 2026-08-25 canon (PRs #941, #940, #942)

- **(a) #941 triage-diagnostician: same mechanism, earlier stage supplied.** Gate-first is the
  loop that PRODUCES the deterministic check #941's escalation clause presupposes; the
  diagnostician, its read-only start, its gate-repair privilege, and its never-weaken rule are
  cited from `loop-rules` and applied to `gate_<id>.py` as the gate file — zero mechanics
  restated here or in the skill edit (Resolution 4 names the one seam: which failures charge a
  try).
- **(b) #940 delegation-plan schema: out of scope.** The schema formalizes multi-seat fan-out —
  `depends_on[]` graphs, wave parallelism, read/write serialization. Gate-first is a strictly
  linear two-seat pipeline (validator, then builder rounds) with one implicit edge; a one-edge
  graph artifact is ceremony, and the schema's own propose→merge flow (N proposers, one
  coordinator) has no analogue here. If a future gate-first build itself fans out into a
  delegation plan, the plan governs the BUILD tasks and the gate stays the plan-level stopping
  predicate — composition deferred to that future design.
- **(c) #942 push-verification: not on this path, by design.** The convention governs
  direct-to-main commits (`ops-write-sandbox-rules`' `ls-remote` re-read). The gate script never
  touches main: its executable copy lives outside any checkout (Resolution 1) and its durable
  copy is an issue comment, whose confirmation is the `gh` API response itself — no push, no
  re-read owed. The design deliberately avoids the direct-to-main path rather than adding a
  fourth documented case to that skill; a builder tempted to commit the gate in-tree should
  re-read Resolution 1's rejection instead.

## Components

- **`teamwork/skills/dispatch-ticket/references/gate-first-mode.md`** (new, F6-split pattern) —
  the full mechanics: grant-line detection, Resolution 2's qualifying test and the validator's
  sealed prompt contract (read-only tools + Write scoped to the gate dir; the no-proxy /
  no-scope-creep / fails-against-current-state rules from the ticket, stated as the authored
  gate's own acceptance), Resolution 1's paths and ticket-comment write-back, Resolution 3's
  round loop, Resolution 4's cap + triage citation, the `gate-infeasible` and
  `gate-rounds-exhausted` outcomes, and the Non-goals' critic-pass non-conflation rule verbatim.
- **`teamwork/scripts/gate_guard.py`** (new) — mechanizable slice only: `run <gate> <clone>`
  hash-checks the gate against its recorded post-author (or post-repair) hash, executes it
  bounded, tri-states (0 green / 1 FAIL lines on stdout / 2 usage-or-tamper), and carries a
  `selftest` with negative controls (tampered-hash fixture, failing-gate fixture) per
  `.claude/rules/scripts.md`.
- **`teamwork/skills/dispatch-ticket/SKILL.md`** — Phase 4 gains one short gate-first paragraph
  (grant line → reference file, never inline mechanics); Phase 5 stage 2a gains the gate-green
  precondition clause; Failure branches gain the two typed outcomes.
- **`teamwork/agents/build-leader.md`** — one relay sentence: the `gate-first: authorized` line
  travels in the sealed prompt like the other two grants, and the gate-round fields in
  `dispatch-ticket`'s handoff relay verbatim like everything else (its existing one-rule frame
  already covers this; the sentence names the new fields so a missing one is nameable).

## Interfaces

- Grant line: `gate-first: authorized` — sealed dispatch prompt, literal, same non-inheritance
  and injection-immunity posture as ADR-0012's grant (cited from
  `references/quick-build-auto-merge-predicate.md`, not restated).
- Validator return (typed): `gate-authored: <path> · checks: <n> · ticket-comment: <url>` or
  `gate-infeasible: <requirement that fails the mechanization test>`.
- Handoff additions (Phase 5 stage 4, only when the mode armed): `gate-rounds: <k>/3 ·
  gate-final: green|gate-rounds-exhausted|gate-infeasible|gate-tampered · gate-comment: <url>`.

## Data

- Gate file: `<scratch-parent>/gate-<id>/gate_<id>.py`, plus `gate_<id>.sha256` (recorded at
  authoring and after any triage repair) and `gate_<id>.pre-repair.py` (the audit copy #941's
  gate-repair mechanics require, written only if a repair fired).
- Durable record: the gate script verbatim in a `gh issue comment` on the ticket (and a second
  comment on repair), same backend verb as the Findings write-back — no new store, no in-tree
  artifact, nothing survives teardown that isn't on the record.
- No schema, config key, or persistent state file is introduced; the grant line and handoff
  fields (Interfaces) are the only new wire data.

## Risks

- **A gamed gate the validator itself under-writes** (existence where behavior was asked). The
  reference's authored-gate acceptance rules are prose; the fresh-context checker pass on the
  eventual PR is the semantic backstop, and a recurring miss becomes a lint fixture per the
  incident→infrastructure invariant. No ADR here: no hard-to-reverse fork was resolved — every
  decision above is a skill-body contract, revisable by the same process that wrote it.
- **Hash-guard is detection, not prevention** — stated in Resolution 1; accepted, matching
  fusion-harness's own honesty about the same gap.
- **Round-cap interaction with the outer `/goal` cap of 5**: gate rounds consume tries, so a
  build spending 3 on the gate has 2 left for post-gate failures (checker, version races). Judged
  acceptable — a build that needed 3 gate rounds AND 3+ post-gate retries is exactly what the
  escalation exists to stop.

## Agent verification

Command/exit-code assert layer, confirming the ticket's provisional note: `gate_guard.py
selftest` exits 0 (including its negative controls); `release_gate.py teamwork` green;
`grep -c "gate-first: authorized" teamwork/skills/dispatch-ticket/SKILL.md` ≥ 1 and the
reference file exists; `skill_lint.py` green on both edited prompt artifacts. The authored
gate's own exit status is the per-run assert, as the ticket anticipated.

## Build sequence

1. **`teamwork/skills/dispatch-ticket/references/gate-first-mode.md`** — author the full
   mechanics per Components above (grant, qualifying test, validator contract, paths, loop, cap,
   triage citation, typed outcomes, critic non-conflation rule).
2. **`teamwork/scripts/gate_guard.py`** — hash-record/hash-check/bounded-run/tri-state +
   `selftest` with tampered and failing fixtures.
3. **`dispatch-ticket/SKILL.md` Phase 4** — the gate-first paragraph: grant detection,
   Resolution 2's kind guard, validator dispatch (unnamed, synchronous, sonnet pinned), pointer
   to the reference.
4. **`dispatch-ticket/SKILL.md` Phase 5 + Failure branches** — gate-green precondition ahead of
   stage 2a; stage-4 handoff fields; `gate-infeasible` (proceed-default, recorded) and
   `gate-rounds-exhausted` (existing unresolved-gate-failure branch, extended) lines.
5. **`teamwork/agents/build-leader.md`** — the one relay sentence naming the grant line and the
   new handoff fields.
6. **Eval/fence sweep** — `dispatch-ticket`'s description is unchanged (no routing edit), so no
   eval delta expected; verify with `eval_check.py`, and run the fresh-context checker pass owed
   on steps 3–5's semantic edits (plugin-authoring invariant — the very rule the Non-goals
   protect).
7. **Ship** — teamwork version bump + README ledger line, `release_gate.py teamwork`, PR citing
   #939 with this LLD in Links; ticket Acceptance restated from this Build sequence per the
   ticket's own instruction.

## Acceptance (checkable predicates)

- Steps 1–5's files exist/changed as named; `gate_guard.py selftest` exits 0.
- With no `gate-first: authorized` line, Phase 4's text path is unchanged (diff shows the branch
  gated entirely behind the literal-line test).
- `release_gate.py teamwork` exits 0; `skill_lint.py` green on every edited SKILL/agent file.
- The reference file contains the critic non-conflation statement and cites (not restates)
  `loop-rules`' triage section.

## Links

- Ticket: kimgranlund/claude-plugins#939 (this design). Companions from the same
  fusion-harness ingest: #937 (delegation-plan schema → PR #940), #938 (triage-diagnostician +
  gate-repair → PR #941), #936 (writer-lease / push-verification → PR #942).
- Canon cited: `teamwork/skills/loop-rules/SKILL.md` §Escalation;
  `teamwork/skills/fleet-rules/references/delegation-plan-schema.md`;
  `harness/skills/ops-write-sandbox-rules/SKILL.md` §push-verification;
  `harness/skills/script-writing-rules/SKILL.md`;
  `teamwork/skills/dispatch-ticket/references/isolation-ladder.md`;
  `.claude/rules/plugin-authoring.md` (semantic-edit critic invariant).
- Source pattern: disler/fusion-harness — `SYSTEM_PROMPT_VALIDATOR.md`,
  `USER_PROMPT_BUILDER.md`, `USER_PROMPT_CORRECTION.md`.
