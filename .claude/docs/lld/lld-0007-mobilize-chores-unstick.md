---
doc-type: lld
id: lld-0007-mobilize-chores-unstick
status: draft
version: 0.1.0
date: 2026-08-17
owner: kim.granlund
ticket: nonoun-plugins#558
spec: none — acceptance rides in #558's own Acceptance section plus this LLD's checkable predicates (D2); the criteria were unambiguous from the ask, so a standalone SPEC would be manufactured process (doc-writing-rules' own routing test)
---
# LLD — mobilize-chores works the stuck set: dependency-first unsticking of `Blocked-by:` chains (#558)

**Verdict, head-first: unsticking gets exactly ONE verb — the dispatch verb the skill already
has.** A `Blocked-by:` blocker that is itself a fully mobilizable ticket is dispatched to
`build-lead` dependency-first, inside the same confirm round, under the same PR-opened ceiling.
Every other blocker shape stays report-only. Within-run chaining exists only as a bounded,
read-only re-check after dispatches return — never a wait, watch, or poll on a PR — so on the
default ceiling it degrades exactly to next-run sequencing, and only an ADR-0012 quick-build
merge can ever make a dependent dispatchable in the same run. No ceiling widens, no second
auto-merge path appears, no review is ever automated, and `blocked-by-convention.md`'s format is
untouched.

The three charter rulings (#558 Scope/Open), verdict-first:

1. **Auto-resolvable vs report-only (the shape taxonomy)** — a blocker is auto-resolvable IFF it
   is itself a ticket that passes step 2's FULL mobilizable predicate (Components C1, class
   MOBILIZABLE). Every blocker matching any of step 6's five human shapes, anything unresolvable,
   anything in flight, anything the sweep flagged human-decision, and every cycle member is
   report-only. The skill gains NO new authority: no `Blocked-by:`-line edits, no relabeling, no
   claim-reclaiming, no ratify comments. Rationale: constraint 1–2's ceilings are preserved by
   construction when the only unstick action is the already-ceilinged dispatch; any second verb
   would need its own authority analysis and its own audit trail (Rejected alternatives, RA1–RA3).
2. **Within-run chaining vs next-run-only** — a hybrid, bounded on the side of single-pass
   (Components C2, Interfaces I3): blockers dispatch this run in dependency order; dependents are
   confirmed *conditionally* in the same round and dispatch this run ONLY if a post-wave re-READ
   shows every named blocker CLOSED (possible in-run solely via ADR-0012's quick-build merge or
   an out-of-band human close that happened meanwhile). Otherwise they are sequenced-for-next-run.
   Max three waves; the loop never sleeps, watches `gh pr checks`, or re-polls. Rationale: "wait
   for B's PR to merge" means waiting on a human act of unbounded latency — incompatible with the
   single-pass model — while a one-shot re-read after returns costs one `gh issue view` per
   blocker and honestly captures the only case where chaining is even possible.
3. **Interaction with chore-planner / where the ordering algorithm lives** —
   `blocked-by-convention.md` stays the ONE format canon, unedited except its consumer-pointer
   list (Components C4). The mobilization-side ordering (classification, topo order, cycle
   detection, wave bounds) lands in a NEW reference file,
   `teamwork/skills/mobilize-chores/references/unstick-ordering.md` — exactly parallel to how
   chore-planner's ordering lives in harness's own `blocked-by-rules` skill, and required by the
   convention file's own charter line: "neither's own read/exclude/order logic is restated here."
   No shared format or cross-consumer contract changes → per docs' ADR-default-no, **no ADR is
   authored for this change** (non-decisions recorded in Risks R6).

## Components

### C1 — Blocker classification taxonomy (the auto-resolvable ruling, fail-closed)

For each candidate ticket A that step 2's existing `Blocked-by:` exclusion catches, resolve each
named blocker id B per `references/blocked-by-convention.md`'s realization table (cited, never
restated — format, per-backend read, `#NN`/`TKT-####` shapes all live there), then classify B
into exactly one class. Classes are evaluated top-down; first match wins:

| # | Class | Predicate (git-native realization) | Disposition |
|---|---|---|---|
| B0 | CLOSED | `gh issue view <B> --json state` reads CLOSED | Not blocking — existing behavior, unchanged (all-closed → A proceeds through step 2 normally) |
| B1 | UNRESOLVABLE | The id fails to resolve (deleted, typo, cross-repo ref, `gh` error) | Treated OPEN, report-only — the existing fail-closed failure branch, unchanged. A → still-stuck |
| B2 | CYCLE / TOO-DEEP | B appears on the current resolution path already, or the chain depth from the original candidate exceeds 5 | Report-only; the whole cycle (every member id) or the too-deep chain is named. Nothing on a cycle is EVER dispatched. A → still-stuck |
| B3 | IN-FLIGHT | B has an open PR (the GraphQL `closedByPullRequestsReferences` check — the same form step 2 mandates, never the flattened one) OR a non-empty `assignees` array / `claimed-by` (#184) | Someone owns it — sequenced: A → sequenced-for-next-run, B reported as the awaited work. No dispatch, no check-in comment |
| B4 | HUMAN-SHAPE | B is unlabeled, ambiguously labeled (≠ exactly one of feature/bug/task), sweep-flagged as a human-decision item or blocker, an ops/hygiene item, or its content matches any of step 6's five blocker shapes | Report-only with step 6's existing classified-paragraph discipline. A → still-stuck |
| B5 | MOBILIZABLE | B passes step 2's FULL existing predicate — exactly one of feature/bug/task, no active claim, no open PR (GraphQL check), not sweep-excluded — AND B's own `Blocked-by:` line is either absent, all-closed, or resolvable within this same chain walk (depth ≤ 5, no cycle) | **Unstick candidate** — dispatch B (subject to the one confirm round), A → sequenced (conditionally dispatchable, I3) |

Two invariants worth stating because they close drift holes:

- **The mobilizable predicate is REUSED, never forked or relaxed.** B5 cites step 2's own
  checks; a blocker gets zero exemptions from the label, claim, PR, or sweep-judgment gates. In
  a full SWEEP-SCOPE run, a B5 blocker was usually already in step 2's candidate set on its own
  — the behavioral delta there is A's report class (blocked → sequenced) plus the wave re-check.
  The big delta is TICKET FILTER runs (#449): a filter naming only A now pulls B into
  consideration via the chain; B is reported as "pulled in by #A's chain," never silently
  dispatched off-scope (I4 amends the done-when scope sentence accordingly).
- **Only ONE verb.** The unstick action set is exactly {dispatch-to-build-lead}. Explicitly NOT
  granted (report-only forever under this design): editing or removing a `Blocked-by:` line
  (the convention's own non-goal — nothing infers or auto-writes these lines, and by symmetry
  nothing auto-removes them), relabeling a ticket into mobilizability, reclaiming a stale claim
  (repo-cleaner's finding, ADR-0005 D6), or posting a ratification/sign-off comment (step 6's
  protocol shape requires a real human utterance).

### C2 — Chain resolution and ordering (new reference file `references/unstick-ordering.md`)

A new, small reference file inside mobilize-chores carries the algorithm as buildable prose (not
code — this is a skill-prose change, per #558's own constraint):

- **Walk**: depth-first from each Blocked-by-excluded candidate, resolving each blocker per
  C1, carrying a path-visited set for cycle detection and a depth counter capped at 5. Memoize
  every resolved id in a per-run cache (Data D1) — an id is read once per run, never re-fetched
  (`blocked-by-rules`' own batching discipline, cited).
- **Order**: dependency-first — a B5 blocker dispatches before (or without) its dependents;
  among unrelated chains, ordering falls back to step 5's existing serial/parallel rules
  unchanged. This is topological order over the resolved chain fragments; cycles never enter the
  order (B2 removes them whole). The file cites `blocked-by-convention.md` for the format and
  names harness's `blocked-by-rules` as the sibling consumer's ordering doctrine (a cross-plugin
  MENTION, degrading gracefully — never a preload or `${CLAUDE_PLUGIN_ROOT}` path, per
  `.claude/rules/plugin-authoring.md`).
- **Waves** (the within-run chaining bound, I3): after all of a wave's dispatches RETURN, one
  read-only re-check pass over the sequenced dependents; all-blockers-CLOSED → dispatchable next
  wave. Max 3 waves total; a pass that unlocks nothing ends the loop. No sleeping, no PR
  watching, no re-polling an id already re-read this pass.
- **Outcome classes for step 6**: `unstuck-this-run` (a dependent actually dispatched in wave
  ≥ 2, or a blocker dispatched whose dependent then dispatched), `sequenced-for-next-run`
  (blocker dispatched or in flight; dependent waits for its close), `still-stuck-and-why` (B1,
  B2, B4 — with the classified paragraph).

### C3 — SKILL.md step edits (the behavior deltas, sized per step)

1. **Frontmatter `description`**: the clause "…and no open `Blocked-by:` dependency (#193)"
   gains "— a blocked ticket whose blocker is itself mobilizable gets the blocker dispatched
   dependency-first instead of a bare skip (#558)". mobilize-chores is
   `disable-model-invocation: true`, so no `evals.json` exists or is owed for this
   description edit (the plugin-authoring rule binds model-invocable descriptions);
   `/check-routing teamwork` still runs at build as the cheap boundary proof.
2. **Step 2** (the `Blocked-by:` reading paragraph, ~lines 132–139): the terminal "ANY named
   blocker still open excludes the candidate this run" amends to "…excludes the candidate from
   the PLAIN mobilizable set — it then enters chain resolution per
   `references/unstick-ordering.md`, which classifies each blocker (that file's B0–B5) and
   emits unstick candidates, sequenced dependents, and the still-stuck set." Fail-closed
   defaults (unresolvable → OPEN) unchanged and cited, not restated.
3. **Step 3** (empty-pass stop): stops only when the plain mobilizable set AND the unstick
   candidate set are both empty. A still-stuck-only run still reports (step 6) without a
   confirm round — report-only outcomes need no confirmation.
4. **Step 4** (the ONE confirm round): the same single `AskUserQuestion` gains a second listed
   section — each chain rendered as one entry: "unstick chain: #B (blocker, dispatches now) →
   #A (sequenced; dispatches this run only if #B closes in-run via the ADR-0012 quick-build
   carve-out, else next run)". Confirming the entry confirms the WHOLE chain — blocker dispatch
   plus the dependent's conditional dispatch — so no second round ever exists. Declining
   declines the chain whole. UNATTENDED: auto-confirmed exactly like the plain set, step 2's
   filtering (now including C1's classification) being the correctness gate, per the existing
   doctrine sentence — no new gate, no new prompt.
5. **Step 5** (dispatch): unstick blockers are ORDINARY confirmed dispatches — same
   `Agent(subagent_type: …)` call, same grant-line rules verbatim (UNATTENDED places
   `auto-merge: authorized`, INTERACTIVE never does), same serial/parallel target analysis, same
   independence. One added paragraph: the wave re-check (C2) — after all returns, re-read
   sequenced dependents' blockers once; all CLOSED → dispatch in the next wave (already
   confirmed conditionally in step 4); max 3 waves; never wait on a PR. Explicit line: a chain
   member's dispatch carries no extra authority — the quick-build predicate and grant line are
   evaluated by `dispatch-ticket` stage 2b exactly as for any other ticket, and unsticking never
   constitutes a second auto-merge path or any review act.
6. **Step 6** (report): the considered-tickets table gains the three-way outcome vocabulary —
   unstuck-this-run / sequenced-for-next-run / still-stuck-and-why — and the blocker-breakdown
   paragraphs now apply to the still-stuck set (B1/B2/B4) plus, as today, any
   `build-lead`-returned named blocker. A cycle gets ONE paragraph naming every member. A
   TICKET FILTER run that pulled in off-filter blockers names each as "pulled in by #A's
   chain." The five human shapes and the commands-only follow-up pass are unchanged.
7. **Done-when / NOT-done paragraph**: scope sentence extends — "a TICKET FILTER's scope is
   exactly its named ids plus any blocker ids its chains pulled in (each disclosed in step 6)";
   NOT-done gains: a cycle member or human-shape blocker dispatched, a dependent dispatched
   while any named blocker still reads OPEN, a second confirm round, any wait/watch/poll on a
   PR between waves, more than 3 waves, or any unstick action other than the build-lead
   dispatch (a `Blocked-by:` line edited, a label changed, a claim reclaimed, a ratify comment
   posted).

### C4 — blocked-by-convention.md: consumer-pointer update only

The "two named consumers" section's mobilize-chores line amends from "exclusion semantics: that
skill's own step 2" to "exclusion + unstick-ordering semantics: step 2 and
`references/unstick-ordering.md` (#558)". Nothing in the format, realization table, or non-goals
changes; the file's charter (consumer logic never restated here) is what forces C2's separate
file. chore-planner and harness's `blocked-by-rules` need no edit — their ordering semantics
are untouched, and the convention remains their unchanged citation target.

### C5 — Out-of-scope observation (named, not fixed)

SKILL.md's prose says `build-lead` / `subagent_type: "teamwork:build-lead"` in several places
while the registered agent in this estate is `build-leader` — pre-existing drift unrelated to
#558. This design's step-5 edit adds a paragraph NEAR but not ON those lines; the builder must
not fold the rename in. It stays a separate ticket's fix.

## Interfaces

### I1 — Confirm-round entry (step 4, INTERACTIVE)

One option per chain in the existing single `AskUserQuestion`:
`unstick #B → #A` with the description "dispatch blocker #B <title> now; #A <title> sequenced —
dispatches this run only if #B closes in-run (ADR-0012 quick-build), else next run". Multi-level
chains render the full ordered path (`#C → #B → #A`). Selection semantics: whole-chain
confirm/decline, no partial selection within a chain (a human wanting only #B re-runs with a
ticket filter naming #B).

### I2 — Dispatch (step 5) — unchanged contract

Identical `Agent` dispatch to the build-lead seat carrying one ticket id; grant-line placement
rules verbatim from today's step 5; `dispatch-ticket`'s Phase 3 isolation and stage 2b
quick-build evaluation apply unmodified. Unsticking introduces zero new fields into the sealed
prompt.

### I3 — The wave loop (bounded, read-only between dispatches)

```
wave = 1; confirmed = plain set + unstick blockers (topo order)
repeat:
  dispatch confirmed per step 5 (serial/parallel rules); collect ALL returns
  recheck: for each sequenced dependent, re-read each named blocker's state ONCE
  newly-unblocked (all CLOSED) → confirmed for wave+1
  stop when: nothing newly unblocked, or wave == 3
remaining sequenced dependents → sequenced-for-next-run (step 6)
```

Exit-honesty: on the default PR-opened ceiling nothing closes in-run, so the recheck finds
nothing and the loop ends after wave 1 — next-run-only behavior, by construction rather than by
a mode switch.

### I4 — Report vocabulary (step 6)

Three outcome classes replace the single "blocked by an open `Blocked-by:` dependency" row
class: `unstuck-this-run` / `sequenced-for-next-run` / `still-stuck-and-why` (C2). Rows cite the
classifying B-class (B1–B5) so a misclassification is observable in the artifact of record.

## Data

### D1 — Per-run blocker cache

In-session memo (no file, no persistence): id → {state, labels, assignees, open-PR?, parsed
Blocked-by list, B-class}. Written on first resolution, read thereafter; the ONLY permitted
re-read is I3's post-wave state re-check (state field only, once per wave). Bounds `gh` traffic
to ≤ ~4 calls per unique id plus one per sequenced blocker per wave.

### D2 — Build-slice manifest (the plan the builder executes from, in order)

| # | Slice | Files | Depends on |
|---|---|---|---|
| 1 | New reference file: C1 taxonomy table + C2 walk/order/waves/outcome-classes, citing blocked-by-convention.md and mentioning harness's blocked-by-rules | `teamwork/skills/mobilize-chores/references/unstick-ordering.md` (new) | this LLD approved |
| 2 | SKILL.md edits per C3 items 1–7 (description clause; steps 2, 3, 4, 5, 6; done-when/NOT-done) | `teamwork/skills/mobilize-chores/SKILL.md` | 1 |
| 3 | Consumer-pointer line per C4 | `teamwork/skills/mobilize-chores/references/blocked-by-convention.md` | 1 |
| 4 | Version bump 2.21.7 → 2.22.0 + ledger line | `teamwork/.claude-plugin/plugin.json`, `teamwork/README.md` | 2–3 |
| 5 | Gates: `python3 harness/scripts/release_gate.py teamwork` exit 0; `/check-routing teamwork`; fresh-context critic pass over slices 1–3 (semantic edits — the code-checker seat, per charter) | — | 2–4 |

Acceptance predicates, checkable before the PR is called done:
- `doc_lint.py` green on this LLD.
- `release_gate.py teamwork` exit 0; `/check-routing teamwork` reports no boundary regression.
- Grep proofs: `unstick-ordering.md` exists and contains `blocked-by-convention.md` (citation,
  not restatement — and contains NO second definition of the `Blocked-by:` line format);
  SKILL.md contains all three of `unstuck-this-run`, `sequenced-for-next-run`, `still-stuck`;
  SKILL.md's `AskUserQuestion` occurrence count in the procedure is unchanged (still the one
  step-4 round); SKILL.md contains no new `gh pr merge`, `--watch`, `sleep`, or approve/review
  verb introduced by this diff; `blocked-by-convention.md`'s diff touches only the consumers
  section; the `auto-merge: authorized` grant-line paragraph is byte-identical to before.
- Behavioral acceptance (from #558, restated as predicates over the SKILL prose): the step-2/4/5
  text yields — A blocked solely by mobilizable B → B dispatched, A sequenced (and dispatched
  in-run only on an all-CLOSED re-read); multi-level chains ordered dependency-first; cycles and
  B4 shapes never dispatched; step-6 three-way vocabulary present; UNATTENDED path adds no
  prompt and INTERACTIVE adds no second round.

## Risks

1. **Chain resolution inflates run cost on a big backend** (many blocked tickets × chain depth).
   Detection: step 6's considered-table growth; the D1 cache's unique-id count. Fallback: depth
   cap 5 + memoization bound the walk; a chain past the cap degrades to today's exact behavior
   (report blocked), losing nothing.
2. **A blocker slips the mobilizable predicate via stale reads** (claimed between resolution and
   dispatch). Mitigation: unchanged from today — `dispatch-ticket` Phase 3's claim operation is
   the arbiter at dispatch time; a double-claim surfaces as that dispatch's own failure branch.
   No new window is opened: C1 reuses the same checks at the same freshness step 2 already has.
3. **The wave re-check misreads an in-flight close** (issue closed by a human mid-run for an
   unrelated reason; dependent dispatches against a half-done blocker). Mitigation: CLOSED is
   the convention's own unblock condition — the same fact next run would act on; acting on it a
   few minutes earlier is not a new failure class. The dispatch still pays every downstream gate.
4. **Confirm-round overload** — chains make step 4's single round longer. Mitigation: one entry
   per chain (I1), not per member; a human wanting finer grain uses a ticket filter. Never a
   second round (constraint encoded in NOT-done).
5. **Builder drift into the adjacent naming defect** (C5's build-lead/build-leader drift sits in
   the same step 5 the diff touches). Mitigation: C5 names it out-of-scope explicitly; the
   grep predicate "grant-line paragraph byte-identical" plus the critic pass catch accidental
   folding.
6. **Non-decisions noted (no ADR here, per ADR-default-no):** (a) the depth cap of 5 and wave
   cap of 3 are bounds chosen for cost honesty, not ratified contracts — a one-line edit each if
   reality wants different numbers; (b) keeping the ordering file inside mobilize-chores rather
   than promoting a shared cross-plugin topo-sort home is the status quo the convention file
   already mandates (consumer logic stays with the consumer) — no fork was resolved, so nothing
   to ratify; (c) auto-writing a `Blocked-by:` line from a build-lead-returned blocker was
   REJECTED (RA3), which reaffirms #193's existing non-goal rather than deciding anything new.

## Rejected alternatives

- **RA1 — A wider auto-resolve verb set** (edit stale `Blocked-by:` lines, relabel
  near-mobilizable blockers, reclaim stale claims, post ratify comments). Rejected: each verb
  needs authority the skill doesn't have and the dispatch's ceiling constraints forbid growing;
  line-removal is redundant anyway (all-closed already unblocks without an edit), reclaiming is
  repo-cleaner's ruled territory (ADR-0005 D6), and ratification is definitionally a human
  utterance (step 6's own shape 2).
- **RA2 — True within-run chaining (watch B's PR, dispatch A on merge).** Rejected: merging is a
  human act on the default ceiling, so the watch is unbounded; even bounded, a `--watch` loop
  inside an unattended sweep is exactly the stall class lld-0002's I2 had to feature-detect
  wrappers for. The one-shot post-wave re-read captures every case chaining is actually possible
  in (quick-build merges) at the cost of one `gh issue view` per blocker per wave.
- **RA3 — Auto-writing a `Blocked-by:` line when build-lead returns a named blocker**, so next
  run's unstick logic sees it. Rejected: #193's convention rules auto-detection/inference out
  ("nothing infers this line…a human writes it"); step 6's breakdown may PROPOSE adding the line
  — the human's act, as today.
- **RA4 — Extending `blocked-by-convention.md` with the ordering algorithm** (one file for
  format + order). Rejected: the file's own charter says consumer read/exclude/order logic is
  never restated there, and chore-planner's ordering already lives consumer-side in
  `blocked-by-rules`; centralizing would fork the established shape, not unify it.
- **RA5 — A SPEC and/or ADR alongside this LLD.** Rejected: acceptance was unambiguous from
  #558's own Acceptance section (SPEC would be manufactured sign-off); no cross-consumer
  contract or hard-to-reverse fork was resolved (ADR-default-no — the closest candidates are
  Risks R6's named non-decisions).

## Agent verification

No new harness is required. Existing instruments cover the design: `release_gate.py teamwork`
(G-checks incl. skill lint over the edited SKILL.md and new reference file), `/check-routing
teamwork` (description-boundary proof after C3 item 1), `doc_lint.py` on this LLD, and D2's
grep predicates (runnable one-liners, no human judgment). The semantic quality of the prose
edits — the one thing no script proves — is covered by the dispatching charter's fresh-context
code-checker pass (the plugin-authoring semantic-edit invariant), which is an existing
instrument of this workspace, not a new one. mobilize-chores has no evals suite (dmi: true) and
this design deliberately does not create one — flagged here rather than silently: routing risk
is bounded because the skill is user-invocable only.
